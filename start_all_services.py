import subprocess
import os
import signal
import sys
import time
import platform

# List to hold the subprocesses
processes = []

def get_python_executable():
    """Get the appropriate Python executable for the system."""
    if platform.system() == 'Windows':
        return 'python'
    else:
        return 'python3'

def start_service(service_name, script_name):
    python_executable = get_python_executable()
    service_path = os.path.join(os.getcwd(), service_name, script_name)
    env = os.environ.copy()
    env['PYTHONPATH'] = os.getcwd()
    if os.path.exists(service_path):
        print(f"Starting {service_name} at {service_path}...")
        process = subprocess.Popen([python_executable, service_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        processes.append((service_name, process))
    else:
        print(f"Could not find {script_name} for {service_name} at {service_path}")

def stop_services():
    print("Stopping all services...")
    for service_name, process in processes:
        print(f"Stopping {service_name}...")
        process.terminate()
    for service_name, process in processes:
        process.wait()
        print(f"{service_name} stopped.")
    print("All services stopped.")

def signal_handler(sig, frame):
    stop_services()
    sys.exit(0)

def log_service_output():
    for service_name, process in processes:
        try:
            stdout, stderr = process.communicate(timeout=5)
            if stdout:
                print(f"{service_name} stdout: {stdout.decode()}")
            if stderr:
                print(f"{service_name} stderr: {stderr.decode()}")
        except subprocess.TimeoutExpired:
            pass  # Ignore timeout errors

if __name__ == "__main__":
    # Register the signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    services = [
        ('Artigo', 'app.py'),
        ('Encomenda', 'app.py'),
        ('PaymentGateway', 'app.py'),
        ('Utilizador', 'app.py'),
    ]

    for service_name, script_name in services:
        start_service(service_name, script_name)

    print("All services started. Press Ctrl+C to stop.")

    # Keep the main thread alive to catch signals
    try:
        while True:
            time.sleep(1)
            log_service_output()
    except KeyboardInterrupt:
        pass
    finally:
        stop_services()
