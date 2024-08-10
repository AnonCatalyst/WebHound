import subprocess
import sys
import os
from tqdm import tqdm
import threading
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_virtualenv(venv_path):
    """Create a virtual environment if it doesn't already exist."""
    if not os.path.exists(venv_path):
        logging.info("Creating virtual environment...")
        subprocess.check_call([sys.executable, '-m', 'webhound-venv', venv_path])
        logging.info("Virtual environment created.")
    else:
        logging.info("Virtual environment already exists.")

def install_package(venv_path, package, results):
    """Install or update a specific package."""
    pip_executable = os.path.join(venv_path, 'bin', 'pip')  # For Unix-based systems
    if os.name == 'nt':  # For Windows
        pip_executable = os.path.join(venv_path, 'Scripts', 'pip.exe')

    try:
        logging.info(f"Installing or updating {package}...")
        subprocess.check_call([pip_executable, 'install', '--upgrade', package], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        results[package] = f"{package} is up-to-date."
    except subprocess.CalledProcessError:
        results[package] = f"Failed to install or update {package}."

def install_requirements(venv_path):
    """Install and update required packages in the virtual environment."""
    packages = [
        'spacy',
        'requests',
        'beautifulsoup4',
        'fake-useragent',
        'tqdm',
        'termcolor',
        'furl'
    ]

    results = {}
    threads = []

    # Create and start threads for each package installation
    for package in packages:
        thread = threading.Thread(target=install_package, args=(venv_path, package, results))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Print results
    for package in packages:
        logging.info(results.get(package, f"Failed to process {package}"))
    
    # Install spaCy model using virtual environment's Python executable
    python_executable = os.path.join(venv_path, 'bin', 'python')  # For Unix-based systems
    if os.name == 'nt':  # For Windows
        python_executable = os.path.join(venv_path, 'Scripts', 'python.exe')

    tqdm.write("Checking spaCy model...", end="")
    try:
        subprocess.check_call([python_executable, '-m', 'spacy', 'download', 'en_core_web_sm'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        tqdm.write(" spaCy model 'en_core_web_sm' installed successfully.")
    except subprocess.CalledProcessError:
        tqdm.write(" Failed to install spaCy model 'en_core_web_sm'. Ensure you have network access and try again.")

def run_script(venv_path, script_name):
    """Run the main script using the virtual environment."""
    python_executable = os.path.join(venv_path, 'bin', 'python')  # For Unix-based systems
    if os.name == 'nt':  # For Windows
        python_executable = os.path.join(venv_path, 'Scripts', 'python.exe')

    tqdm.write(f"Running {script_name}...", end="")
    try:
        # Added debugging output to track script execution
        subprocess.check_call([python_executable, script_name])
        tqdm.write(" Script executed successfully.")
    except subprocess.CalledProcessError as e:
        tqdm.write(f" Failed to run script. Error: {e}")
        logging.error(f"Failed to run {script_name}. Error: {e}")

def main():
    venv_path = 'webhound-venv'
    script_name = 'webhound.py'

    create_virtualenv(venv_path)
    install_requirements(venv_path)
    run_script(venv_path, script_name)

if __name__ == '__main__':
    main()
