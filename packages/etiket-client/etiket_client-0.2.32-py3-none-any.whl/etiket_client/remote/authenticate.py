from etiket_client.exceptions import NoAccessTokenFoundException, TokenRefreshException, NoServerUrlFoundException
from etiket_client.remote.client import client

from etiket_client.sync.backends.native.sync_user import sync_current_user
from etiket_client.sync.backends.native.sync_scopes import sync_scopes
from etiket_client.local.database import Session

from getpass import getpass

import logging, socket, requests, json

logger = logging.getLogger(__name__)


def authenticate_with_console(_n_tries=0):
    """
    Authenticate the user via console input.
    """
    institutions = get_institutions_urls()
    if not institutions:
        print("Failed to retrieve institutions. Please try again later.")
        return

    print("Please select your institution:")
    for i, institution in enumerate(institutions.keys()):
        print(f"{i + 1}. {institution}")

    try:
        selected_index = int(input("Please enter the number of your institution: ")) - 1
        selected_institution = list(institutions.keys())[selected_index]
    except (ValueError, IndexError):
        print("Invalid selection. Please try again.")
        authenticate_with_console(_n_tries=_n_tries)
        return

    username = input("Please enter your username: ")
    password = getpass("Please enter your password: ")

    try:
        login(username, password, institutions[selected_institution])
        print(f"Log in successful. Welcome {username}!")
    except Exception as e:
        print(f"Failed to log in with error: {e}")
        logger.exception("Failed to log in with username %s.", username)
        if _n_tries > 2:
            print("Maximum login attempts reached. Please try again later.")
        else:
            authenticate_with_console(_n_tries=_n_tries + 1)

def login(username: str, password: str, institution_url: str):
    """
    Log in to the specified institution.
    """
    client._login(username, password, institution_url)
    with Session() as session:
        sync_current_user(session)
        sync_scopes(session)

def get_institutions_urls() -> dict:
    """
    Returns a dictionary of institutions and their server addresses.
    """
    try:
        response = requests.get("https://docs.dataqruiser.com/_static/server_addresses.json", timeout=10)
        response.raise_for_status()
        data = response.json()

        institutions = {institution: items['etiket'] for institution, items in data['server_addresses'].items()}
        return institutions
    except requests.exceptions.RequestException as e:
        logger.error("Error downloading the file: %s", e)
        return None
    except json.JSONDecodeError as e:
        logger.error("Error decoding the JSON: %s", e)
        return None
    

def _is_logged_in() -> bool:
    """
    Check if the user is logged in by attempting to refresh the token.
    """
    logger.info("Checking if host is logged in.")
    try:
        client.validate_login()
        return True
    except (TokenRefreshException, NoAccessTokenFoundException, NoServerUrlFoundException):
        return False

def check_internet_connection():
    """
    Checks if an internet connection can be made by pinging Google's public DNS server.
    """
    try:
        socket.setdefaulttimeout(0.5)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = ("8.8.8.8", 53)  # Google's public DNS server and DNS port

        result = sock.connect_ex(address)
        if result == 0:
            return True

        logger.info("No internet connection")
        return False
    except socket.gaierror as e:
        logger.error("Address-related error connecting to server: %s", e)
    except socket.error as e:
        logger.error("Connection error: %s", e)
    except Exception as e:
        logger.error("Unexpected error: %s", e)
    finally:
        sock.close()

    return False

def logout():
    client._logout()
