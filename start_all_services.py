import subprocess
import os
import signal
import sys

# List to hold the subprocesses
processes = []

def start_service(service_name, script_name):
    service_path = os.path.join(os.getcwd(), service_name, script_name)
    if os.path.exists(service_path):
        print(f"Starting {service_name}...")
        process = subprocess.Popen(['python', service_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        processes.append(process)
    else:
        print(f"Could not find {script_name} for {service_name} at {service_path}")

def stop_services():
    print("Stopping all services...")
    for process in processes:
        process.terminate()
    for process in processes:
        process.wait()
    print("All services stopped.")

def signal_handler(sig, frame):
    stop_services()
    sys.exit(0)

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
            signal.pause()
    except KeyboardInterrupt:
        pass
