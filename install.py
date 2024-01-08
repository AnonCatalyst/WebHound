import os
import sys
import subprocess

# Assuming the main script is named webhound.py
MAIN_SCRIPT = "webhound.py"
VENV_DIR = ".webhound_venv"

def install_dependencies():
    subprocess.run([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4", "futures", "termcolor", "fake_useragent"])

def create_venv():
    subprocess.run([sys.executable, "-m", "venv", VENV_DIR])

def make_executable():
    if sys.platform.startswith('win'):
        os.system(f"copy {MAIN_SCRIPT} {MAIN_SCRIPT[:-3]}.exe")
    else:
        os.system(f"chmod +x {MAIN_SCRIPT}")

def display_completion_message():
    print("WebHound is now installed!")
    print(f"You can run it using {os.path.join(os.getcwd(), MAIN_SCRIPT)}")

def main():
    create_venv()
    install_dependencies()
    make_executable()
    display_completion_message()

if __name__ == "__main__":
    main()
