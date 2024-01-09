import subprocess
import sys
import os
import platform

def install_dependencies():
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'requests', 'beautifulsoup4', 'fake_useragent', 'tqdm', 'termcolor'])
        print("Python dependencies installed successfully.")
    except Exception as e:
        print(f"Error installing Python dependencies: {e}")

def install_system_dependencies():
    system_name = platform.system().lower()

    if system_name == 'linux':
        install_command = 'sudo apt-get install -y' if platform.linux_distribution()[0].lower() == 'debian' else 'sudo yum install -y'
        subprocess.run([install_command, 'your_system_dependencies_here'])
        print("System dependencies installed successfully.")
    elif system_name == 'darwin':
        try:
            subprocess.run(['brew', 'install', 'your_system_dependencies_here'])
            print("System dependencies installed successfully.")
        except FileNotFoundError:
            print("Homebrew not installed. Please install Homebrew and rerun the script.")
    elif system_name == 'windows':
        print("Windows support coming soon.")
        # Add Windows-specific installation logic here
    elif 'termux' in system_name:
        try:
            subprocess.run(['pkg', 'install', 'your_system_dependencies_here'])
            print("Termux dependencies installed successfully.")
        except FileNotFoundError:
            print("Termux package manager not found. Please install Termux and rerun the script.")
    else:
        print("Unsupported operating system. Please install required dependencies manually.")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    print("Welcome to WebHound's Installation\n")

    install_dependencies()
    install_system_dependencies()

    clear_screen()
    print("Installation complete. You can now run your webhound.py.")

if __name__ == "__main__":
    main()
