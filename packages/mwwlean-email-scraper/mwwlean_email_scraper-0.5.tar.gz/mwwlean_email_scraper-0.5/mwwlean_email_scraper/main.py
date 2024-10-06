import requests
import re
import sys
import os
import pyfiglet
from urllib.parse import urlparse
from datetime import datetime
import argparse

# Clear the console
os.system('cls' if os.name == 'nt' else 'clear')

# Color constants
RED = "\033[31m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
PINK = "\033[35m"
RESET = "\033[0m"

# Print the ASCII banner
ascii_banner = pyfiglet.figlet_format("Email Scraper")
print(PINK + ascii_banner + RESET)
print(f"{PINK}Email Scraper is a Python tool that extracts public email addresses from websites.{RESET}\n")
print(f"{GREEN}Developed by: mwwlean(leander){RESET}\n")


def extract_emails(website_url):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    if not website_url.startswith('http://') and not website_url.startswith('https://'):
        website_url = 'http://' + website_url

    domain = urlparse(website_url).netloc
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'emails_{domain}_{timestamp}.txt'

    try:
        response = requests.get(website_url)
        response.raise_for_status()

        emails = set(re.findall(email_pattern, response.text))

        if emails:
            print(f'Found {len(emails)} email(s):')
            for email in emails:
                print(email)

            with open(filename, 'w') as file:
                for email in emails:
                    file.write(f'{email}\n')
            print(f'\nEmails have been saved to {RED}{filename}{RESET}.')
        else:
            print('No emails found on the website.')

    except requests.exceptions.RequestException as e:
        print(f'Error fetching the URL: {e}')


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Extract public email addresses from a specified website.")
    parser.add_argument('website_url', nargs='?', help='The website URL to extract emails from. Type "exit" to quit.')
    args = parser.parse_args()

    # Handle case where website_url is passed as an argument
    if args.website_url:
        extract_emails(args.website_url)
    else:
        # Enter interactive mode if no URL is passed
        while True:
            website_url = input(f"{YELLOW}Enter a website URL (or type 'exit' to quit): {RESET}")
            if website_url.lower() == 'exit':
                print(f"{GREEN}Exiting the program. Goodbye!{RESET}")
                break
            extract_emails(website_url)


if __name__ == '__main__':
    main()
