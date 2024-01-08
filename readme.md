# WebHound 🚀

![WebHound Logo](img/webhound.jpeg)

WebHound is a Python-powered command-line tool developed by AnonCatalyst that brings efficiency and style to your web searches. Seamlessly query Google, DuckDuckGo, and Bing, and enjoy organized, highlighted results—all from the comfort of your terminal. Let WebHound elevate your search experience with a touch of color and clarity! 🌐🔍✨

## Features

- **Multi-Engine Search**: Conduct searches across popular engines, including Google, DuckDuckGo, and Bing, simultaneously.
- **Colorful Output**: Results are presented in a visually appealing manner with highlighted titles, URLs, and descriptions for quick and easy reading.
- **Efficient Execution**: Utilizes multithreading to speed up the search process, providing results in a fraction of the time.
- **User-Friendly Interface**: Simple and intuitive command-line interface for an effortless user experience.

## Installation

To install WebHound, run the following commands:

> **Usage:**
```python3 webhound.py```

# Assuming the main script is named webhound.py
MAIN_SCRIPT="webhound.py"
VENV_DIR=".webhound_venv"

# Create and activate a virtual environment
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

# Install dependencies
pip install requests beautifulsoup4 futures termcolor fake_useragent

# Make the main script executable
chmod +x $MAIN_SCRIPT

# Display completion message
echo "WebHound is now installed!"
echo "You can run it using ./$MAIN_SCRIPT"

# Optionally, you can deactivate the virtual environment
deactivate
