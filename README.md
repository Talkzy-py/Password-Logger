Password Scraper
This script extracts saved passwords from Google Chrome and sends them to a Discord channel using a webhook.

Requirements
Python 3.x
The following Python packages:
python-dotenv
requests
pycryptodome
pywin32
Setup
Clone the repository to your local machine.

Install the required Python packages. It’s recommended to use a virtual environment for this.

Create a .env file in the project directory. Add your Discord webhook URL to this file under the key DISCORD_WEBHOOK_URL.

Usage
Run the script to extract passwords and send them to your Discord channel. Make sure your .env file is properly configured with your webhook URL.

Security
Keep the .env file private. Do not share it or include it in version control.
Add .env to your .gitignore file to prevent it from being tracked by Git.
License
This project is licensed under the MIT License. See the LICENSE file for more details.

Acknowledgements
python-dotenv
requests
pycryptodome
pywin32
Feel free to adjust any details as needed!
