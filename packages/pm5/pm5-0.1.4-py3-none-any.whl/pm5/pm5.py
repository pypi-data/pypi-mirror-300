import json
import os
import signal
import subprocess
import sys
import time

# import traceback
from threading import Lock, Thread

import daemon
import daemon.pidfile
from lockfile import AlreadyLocked
from loguru import logger

from pm5.argparsers.pm5 import get_app_args

LOCK_FILE = (
    "process_lock.json"  # File to store the mapping of process IDs to service names
)
PID_FILE = ".daemon.pid"  # File to store the PID of the daemon

lock = Lock()  # Lock to handle thread synchronization

shutdown = False  # Global flag to indicate if the system is shutting down

# Global list to keep track of running processes and a dictionary to map process IDs to service names
processes = []
process_service_map = {}


# Set up logging to a file
def setup_logging(log_dir):
    log_file = os.path.join(log_dir, ".daemon.log")
    logger.add(
        log_file, rotation="10 MB", retention="7 days", backtrace=True, diagnose=True
    )
    logger.info(f"Logging setup complete. Log file located at: {log_file}")


# Function to read the ecosystem configuration from a JSON file
def read_config(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


# Function to start a service instance
def start_service(service, instance_id):
    command = [service["interpreter"]] + service.get("interpreter_args", [])
    if service["script"]:
        command.append(service["script"])
    command += service.get("args", [])

    env = os.environ.copy()  # Copy current environment variables
    env.update(
        {k: str(v) for k, v in service.get("env", {}).items()}
    )  # Update with service-specific environment variables
    cwd = service.get(
        "cwd", os.getcwd()
    )  # Use specified cwd or current working directory if not set

    process = subprocess.Popen(
        command, env=env, cwd=cwd, preexec_fn=os.setsid
    )  # Start the process

    with lock:  # Ensure thread-safe access
        processes.append(process)  # Add process to the list
        process_service_map[str(process.pid)] = service[
            "name"
        ]  # Map process ID to service name
        update_lock_file()  # Update the lock file with running process IDs and service names

    logger.info(
        f"Starting instance {instance_id} of service '{service['name']}' with command: {' '.join(command)} (PID: {process.pid}) in directory: {cwd}"
    )

    return process


# Function to monitor a service and restart it if necessary
def monitor_service(service, process, instance_id):
    global shutdown

    max_restarts = service.get(
        "max_restarts", 0
    )  # Get maximum number of restarts allowed
    restarts = 0  # Initialize restart count

    while restarts <= max_restarts and not shutdown:
        process.wait()  # Wait for the process to finish

        with lock:
            if process in processes:
                processes.remove(process)  # Remove process from the list
                if str(process.pid) in process_service_map:
                    # Remove the process from the lock file
                    del process_service_map[str(process.pid)]
                    update_lock_file()

        if shutdown:
            break

        if process.returncode != 0:  # If the process exited with an error
            logger.error(
                f"Instance {instance_id} of service '{service['name']}' exited with error code {process.returncode}"
            )

            with lock:
                # Ensure the lock file is updated after error
                if str(process.pid) in process_service_map:
                    del process_service_map[str(process.pid)]
                    update_lock_file()

        if restarts < max_restarts and service.get("autorestart", False):
            logger.info(
                f"Restarting instance {instance_id} of service '{service['name']}' (Restart {restarts + 1})"
            )
            process = start_service(service, instance_id)  # Restart the service

            with lock:
                # Increment the restart count in the lock file
                pid_str = str(process.pid)
                process_service_map[pid_str] = {
                    "name": service["name"],
                    "restarts": restarts + 1,  # Increment restart count
                }
                update_lock_file()  # Update the lock file

            restarts += 1  # Increment restart count

        elif restarts == max_restarts:
            if process.returncode != 0:
                logger.warning(
                    f"Instance {instance_id} of service '{service['name']}' has exceeded the maximum number of restarts ({max_restarts}). Stopping all services."
                )
                handle_exit(signal.SIGTERM, None)  # Exit if max restarts exceeded

        else:
            if process.returncode != 0:
                logger.error(
                    f"Instance {instance_id} of service '{service['name']}' has exited with an error and will not be restarted"
                )
            break


# Function to clean up all running processes
def cleanup_processes():
    global shutdown

    if shutdown:
        logger.warning("Shutting down all services. Please hold...")
        return

    shutdown = True

    with lock:
        for process in processes:
            service_name = process_service_map.get(str(process.pid), "Unknown service")
            try:
                logger.info(
                    f"Sending SIGTERM to process group {os.getpgid(process.pid)} of service '{service_name}'"
                )
                os.killpg(
                    os.getpgid(process.pid), signal.SIGTERM
                )  # Send SIGTERM to process group
            except Exception as e:
                logger.info(
                    f"Error sending SIGTERM to process group {os.getpgid(process.pid)} of service '{service_name}': {e}"
                )

        logger.info("Cleaning up services...")
        time.sleep(1)  # Give some time for processes to terminate gracefully

        for process in processes:
            service_name = process_service_map.get(str(process.pid), "Unknown service")
            if process.poll() is None:  # Check if process is still running
                try:
                    logger.info(
                        f"Sending SIGKILL to process group {os.getpgid(process.pid)} of service '{service_name}'"
                    )
                    os.killpg(
                        os.getpgid(process.pid), signal.SIGKILL
                    )  # Send SIGKILL to process group
                except Exception as e:
                    logger.info(
                        f"Error sending SIGKILL to process group {os.getpgid(process.pid)} of service '{service_name}': {e}"
                    )

        for process in processes:
            try:
                process.wait(timeout=5)  # Wait for process to terminate
            except subprocess.TimeoutExpired:
                service_name = process_service_map.get(
                    str(process.pid), "Unknown service"
                )
                logger.warning(
                    f"Process {process.pid} of service '{service_name}' did not terminate in time"
                )

        clear_lock_file()  # Clear the lock file

    logger.info("Service cleanup complete.")


# Function to handle script exit
def handle_exit(signum, frame):
    global shutdown

    # Log debug information about the signal and the call stack
    logger.debug(f"PM5 received exit signal: {signum}")
    # logger.debug("Stack trace leading to shutdown:")
    # logger.debug("".join(traceback.format_stack(frame)))

    if shutdown:
        logger.debug("Shutdown already in progress, ignoring signal.")
        return

    logger.info("Terminating all services...")
    cleanup_processes()

    with lock:
        if len(processes) > 0:
            for process in processes:
                if process.poll() is None:
                    logger.warning(
                        f"Process {process.pid} is still running, forcing exit..."
                    )
                    os.killpg(
                        os.getpgid(process.pid), signal.SIGKILL
                    )  # Force kill remaining processes

    os._exit(1)  # Force exit with error


# Function to read the lock file containing process-service mappings
def read_lock_file():
    if os.path.exists(LOCK_FILE):
        with open(LOCK_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}


# Function to update the lock file with current process-service mapping
def update_lock_file():
    with open(LOCK_FILE, "w") as file:
        json.dump(process_service_map, file)


# Function to clear the lock file
def clear_lock_file():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)


# Function to terminate existing processes from the lock file
def terminate_existing_processes():
    service_map = read_lock_file()
    active_service_map = {}

    for pid, service_name in service_map.items():
        try:
            pid = int(pid)
            os.killpg(pid, 0)  # Verify if the process group is still running
            logger.info(f"Terminating existing process group with pid: {pid}")
            os.killpg(pid, signal.SIGTERM)
            active_service_map[str(pid)] = service_name
        except ProcessLookupError:
            logger.warning(f"No process group found with pid: {pid}")
        except PermissionError:
            logger.warning(
                f"Permission denied to terminate process group with pid: {pid}"
            )

    # Update the lock file with only the active services, if any, or clear it
    if active_service_map:
        with open(LOCK_FILE, "w") as file:
            json.dump(active_service_map, file)
    else:
        clear_lock_file()


# Function to show the status of the processes
def show_status():
    service_map = read_lock_file()
    if not service_map:
        logger.info("No processes are currently running.")
        return

    logger.info("Current status of managed processes:")
    for pid, service_info in service_map.items():
        try:
            pid = int(pid)
            os.kill(pid, 0)  # Check if the process is still running
            status = "Running"
        except ProcessLookupError:
            status = "Not Running"

        # Handle case where service_info might be a string (e.g., just the service name)
        if isinstance(service_info, str):
            service_name = service_info
            restarts = 0  # Default restarts to 0 if not available
        else:
            service_name = service_info.get("name", "Unknown")
            restarts = service_info.get("restarts", 0)

        logger.info(
            f"Service: {service_name}, PID: {pid}, Status: {status}, Restarts: {restarts}"
        )


# Main function to start the process manager
def main(**kwargs):
    config_file_path = kwargs["config_file"]

    # Check if the ecosystem config file exists before setting up logging
    if not os.path.exists(config_file_path):
        logger.error(
            f"Ecosystem configuration file '{config_file_path}' not found. Exiting..."
        )
        sys.exit(1)

    config_dir = os.path.dirname(config_file_path)
    setup_logging(config_dir)

    logger.debug(f"The process manager process id is: {os.getpid()}")

    # Setup signal handlers
    signal.signal(signal.SIGTERM, handle_exit)
    signal.signal(signal.SIGINT, handle_exit)

    terminate_existing_processes()  # Terminate any existing processes from previous runs

    config = read_config(config_file_path)
    services = config["services"]

    total_cpus = os.cpu_count()
    services_started = False

    for service in services:
        if service.get("disabled", False):
            logger.info(f"Service '{service['name']}' is disabled. Skipping...")
            continue

        instances = service.get("instances", 1)
        if instances < 0:
            instances = max(
                1, total_cpus - abs(instances)
            )  # Ensure at least 1 instance

        for i in range(instances):
            process = start_service(service, i)
            services_started = True

            if service.get("wait_ready", False):
                thread = Thread(target=monitor_service, args=(service, process, i))
                thread.start()

    if not services_started:
        logger.error("Error: No services to start. Exiting...")
        sys.exit(1)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Terminating all services via keyboard exit...")
        cleanup_processes()
        sys.exit(0)


def daemon_main():
    main(**get_app_args())


def start_daemon():
    try:
        # Check if the PID file exists and the process is still running
        if os.path.exists(PID_FILE):
            with open(PID_FILE, "r") as f:
                pid = int(f.read().strip())
                try:
                    os.kill(pid, 0)  # Check if the process is still running
                    logger.error("Daemon is already running.")
                    return
                except ProcessLookupError:
                    logger.warning(
                        "Stale PID file found. Removing and continuing to start daemon."
                    )
                    os.remove(PID_FILE)  # Remove the stale PID file

        with daemon.DaemonContext(
            working_directory=os.getcwd(),
            umask=0o002,
            pidfile=daemon.pidfile.TimeoutPIDLockFile(PID_FILE),
            stdout=sys.stdout,
            stderr=sys.stderr,
        ):
            daemon_main()
    except AlreadyLocked:
        logger.error("Daemon is already running and PID file is locked.")
    except Exception as e:
        logger.exception("Error starting daemon.")


def stop_daemon():
    logger.debug("User requested to stop the daemon.")
    try:
        with open(PID_FILE, "r") as f:
            pid = int(f.read().strip())
            os.kill(pid, signal.SIGTERM)
            logger.info("Daemon stopped successfully.")
            os.remove(PID_FILE)  # Clear the PID file
    except FileNotFoundError:
        logger.error("PID file not found. Is the daemon running?")
    except ProcessLookupError:
        logger.error("No such process. The daemon may have already stopped.")
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)  # Remove the stale PID file if it exists
    except Exception as e:
        logger.error(f"Error stopping daemon: {e}")


def app():
    args = get_app_args()

    if args["command"] == "start":
        if args["debug"]:
            main(**args)
        else:
            start_daemon()
    elif args["command"] == "stop":
        stop_daemon()
    elif args["command"] == "status":
        show_status()
    else:
        logger.error("Unknown command. Use 'start', 'stop', or 'status'.")
