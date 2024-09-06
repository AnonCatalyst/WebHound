import subprocess
import sys
import os
import platform

def install_python_dependencies():
    try:
        # Install Python packages
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'requests', 'beautifulsoup4', 'fake_useragent', 'tqdm', 'termcolor', '--break-system-packages'], check=True)
        print("Python dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing Python dependencies: {e}")

def install_spacy_model():
    try:
        # Install SpaCy model
        subprocess.run([sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm', '--break-system-packages'], check=True)
        print("SpaCy model 'en_core_web_sm' installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing SpaCy model: {e}")

def install_system_dependencies():
    system_name = platform.system().lower()
    os_release_info = ""

    if system_name == 'linux':
        try:
            # Read OS release information to determine package manager
            if os.path.exists('/etc/os-release'):
                with open('/etc/os-release') as f:
                    os_release_info = f.read()
                
                if 'ubuntu' in os_release_info or 'debian' in os_release_info:
                    install_command = 'sudo apt-get install -y'
                elif 'fedora' in os_release_info or 'centos' in os_release_info:
                    install_command = 'sudo yum install -y'
                elif 'arch' in os_release_info:
                    install_command = 'sudo pacman -S --noconfirm'
                else:
                    raise RuntimeError("Unsupported Linux distribution.")
                
                # Execute the installation command
                subprocess.run(f"{install_command} python3-scikit-learn python3-tldextract", shell=True, check=True)
                print("System dependencies installed successfully.")
            else:
                raise RuntimeError("Unable to determine Linux distribution.")
        except Exception as e:
            print(f"Error installing system dependencies: {e}")

    elif system_name == 'darwin':
        try:
            # Install using Homebrew
            subprocess.run(['brew', 'install', 'scikit-learn', 'tldextract'], check=True)
            print("System dependencies installed successfully.")
        except FileNotFoundError:
            print("Homebrew not installed. Please install Homebrew and rerun the script.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing macOS dependencies: {e}")

    elif system_name == 'windows':
        print("Windows support coming soon.")
        # For Windows, consider using a package manager like Chocolatey or manually installing dependencies

    elif 'termux' in platform.platform().lower():
        try:
            # Install packages in Termux
            subprocess.run(['pkg', 'install', '-y', 'python', 'python-scikit-learn', 'python-tldextract'], check=True)
            print("Termux dependencies installed successfully.")
        except FileNotFoundError:
            print("Termux package manager not found. Please install Termux and rerun the script.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing Termux dependencies: {e}")

    else:
        print("Unsupported operating system. Please install required dependencies manually.")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    print("Welcome to WebHound's Installation\n")

    install_python_dependencies()
    install_spacy_model()  # Install SpaCy model
    install_system_dependencies()

    clear_screen()
    print("Installation complete. You can now run -> python3 webhound.py")

if __name__ == "__main__":
    main()
