from etiket_client.exceptions import NoAccessTokenFoundException, RequestFailedException,\
    LoginFailedException, TokenRefreshException, NoServerUrlFoundException

from etiket_client.settings.user_settings import user_settings, get_user_data_dir

import datetime, requests, logging, filelock, time, urllib3

PREFIX = "/api/v2"
logger = logging.getLogger(__name__)

class client:
    session = requests.Session()
    __SERVER_URL = None
    @staticmethod
    def url():
        if client.__SERVER_URL is None:
            user_settings.load()
            if user_settings.SERVER_URL is None:
                user_settings.access_token = None
                user_settings.refresh_token = None
                user_settings.access_token_expiration = None
                user_settings.write()
                raise NoServerUrlFoundException("No Server URL found, please log in first.")
            client.__SERVER_URL = user_settings.SERVER_URL
            
        return f"{client.__SERVER_URL}{PREFIX}"
    
    @staticmethod
    def validate_login():
         # reload to check if other process already refreshed the credentials
        if (user_settings.access_token_expiration is None or 
            user_settings.access_token_expiration <  datetime.datetime.now().timestamp() + 5):
            user_settings.load()
            
            if user_settings.SERVER_URL is None:
                raise NoServerUrlFoundException("No Server URL found, please log in first.")
            if user_settings.access_token is None : 
                raise NoAccessTokenFoundException("No access token found, please log in first!")

            client._refresh_token()
                
    @staticmethod         
    def __gen_auth_header(headers):
        if headers is dict:
            headers += client.__get_auth_header()
        else:
            headers = client.__get_auth_header()
        return headers
    
    @staticmethod
    def __renew_session():
        client.session = requests.Session()
        
    @staticmethod
    def _login(username : str, password : str, SERVER_URL : str):
        logger.info("Attempt to log-in user %s", username)
        
        data = {"grant_type": "password",
                "username": username,
                "password": password}
        response = client.session.post(f"{SERVER_URL}{PREFIX}/token", data=data, timeout=10)

        if response.status_code != 200:
            logger.error("Log in failed for %s\n Server message : %s", username, response.json()['detail'])
            message = f"Log in failed, please try again. \n\tdetails : {response.json()['detail']}\n"
            raise LoginFailedException(message)
        
        logger.warning("Log in succesfull for %s", username)
        
        client.__SERVER_URL = SERVER_URL
        user_settings.SERVER_URL = SERVER_URL
        user_settings.user_name = username
        user_settings.access_token = response.json()["access_token"]
        user_settings.refresh_token = response.json()["refresh_token"]
        user_settings.access_token_expiration = int(response.json()["expires_at"])
        user_settings.write()
    
    @staticmethod
    def _logout():
        try:
            logger.info("Logging out user %s", user_settings.user_name)
            # refresh twice to destroy the session id of the token.
            refresh_token = user_settings.refresh_token
            client._refresh_token(refresh_token)
            client._refresh_token(refresh_token)
        except TokenRefreshException:
            logger.warning("Log-out successfull for %s :/ \n", user_settings.user_name)
        except Exception:
            logger.exception("Log-out failed for %s :/ \n", user_settings.user_name)
        finally:
            user_settings.access_token = None
            user_settings.refresh_token = None
            user_settings.access_token_expiration = None
            user_settings.user_name = None
            user_settings.write()

    @staticmethod
    def _refresh_token(refresh_token : str = None):
        try:
            user_settings.load()
        except Exception:
            # in some rare cases, just after a write, the file is not yet readable (race condition between different processes)
            time.sleep(0.05)
            user_settings.load()
        
        if user_settings.user_name is None:
            raise TokenRefreshException("No user name found, please log in first.")
        logger.info("Refreshing token for %s", user_settings.user_name)
        
        if user_settings.access_token_expiration > datetime.datetime.now().timestamp() + 5 and refresh_token is None:
            return # token is still valid

        try:
            lock = filelock.FileLock(get_user_data_dir() + 'token_refresh.lock')
            with lock.acquire(0):
                client.__SERVER_URL = user_settings.SERVER_URL
                
                if refresh_token is None:
                    refresh_token = user_settings.refresh_token
                
                data = {"grant_type" : "refresh_token",
                        "refresh_token": refresh_token}
                response = client.session.post(f"{client.url()}/token", data=data, timeout=10)

                if response.status_code >= 400 and response.status_code < 500:
                    message = "Token refresh failed, you will need to login again. \n\tdetails : " + response.json().get("detail", "No details provided")
                    raise TokenRefreshException(message)
                elif response.status_code != 200:
                    raise RequestFailedException(response.status_code, "Server error (token refresh failed)\n Details : " + response.json().get("detail", "No details provided"))
                
                logger.info("Token refreshed successfully", extra={
                    "user": user_settings.user_name,
                    "expires_at": user_settings.access_token_expiration
                })
                user_settings.access_token = response.json()["access_token"]
                user_settings.refresh_token = response.json()["refresh_token"]
                user_settings.access_token_expiration = int(response.json()["expires_at"])
                user_settings.write()
                
                # release the lock 100ms later, to ensure that all the changes are written to the file.
                logger.warning("Token refresh successful for %s", user_settings.user_name)
                time.sleep(0.1)
        except filelock.Timeout:
            logger.warning("Token refresh delayed due to a lock timeout (user : %s).", user_settings.user_name)
            time.sleep(0.1) # wait a little to be sure that the other process completes.
            client.validate_login()
        except requests.exceptions.ConnectionError as e:
            logger.warning("Token refresh failed due to connection error (user : %s).", user_settings.user_name)
            raise e
        except RequestFailedException as e:
            raise e
        except TimeoutError as e:
            logger.warning("Token refresh failed due to timeout (user : %s).", user_settings.user_name)
            raise e
        except requests.exceptions.ReadTimeout as e:
            logger.warning("Token refresh failed due to read timeout (user : %s).", user_settings.user_name)
            raise e
        except urllib3.exceptions.ReadTimeoutError as e:
            logger.warning("Token refresh failed due to read timeout (user : %s).", user_settings.user_name)
            raise e
        except Exception as e:
            if not refresh_token and isinstance(e, TokenRefreshException):
                logger.exception("Token refresh failed for %s :/ \n with error : %s", user_settings.user_name, e)
            user_settings.access_token = None
            user_settings.refresh_token = None
            user_settings.access_token_expiration = None
            user_settings.write()
            raise e
    
    @staticmethod 
    def post(url, data = None, json_data=None, params=None, headers = None):
        return client.__handle_request(url, client.session.post, data, json_data, params, headers)
    
    @staticmethod
    def get(url, params=None, data=None, json_data=None, headers=None):
        return client.__handle_request(url, client.session.get, data, json_data, params, headers)
    
    @staticmethod
    def put(url, data = None, params=None, headers = None):
        return client.__handle_request(url, client.session.put, data, params, headers)
    
    @staticmethod
    def patch(url, data = None, json_data=None, params=None, headers = None):
        return client.__handle_request(url, client.session.patch, data, json_data, params, headers)
    
    @staticmethod
    def delete(url, data = None, json_data=None, params=None, headers = None):
        return client.__handle_request(url, client.session.delete, data, json_data, params, headers)
    
    @staticmethod
    def __handle_request(url, method, data = None, json_data=None, params=None, headers = None, attempts = 0):
        try:
            # check if token is still valid
            if user_settings.access_token is None:
                user_settings.load()
                if user_settings.access_token is None:
                        raise NoAccessTokenFoundException("No access token found, please log in first.")
            if user_settings.access_token_expiration < datetime.datetime.now().timestamp() + 5:
                client._refresh_token()
            
            headers = client.__gen_auth_header(headers)
            response = method(f'{client.url()}{url}', data=data, json=json_data, headers=headers, params=params, timeout=10)
            
            process_error_in_response(response)
        except requests.exceptions.ConnectionError as e: # quick patch -- TODO : check why this is happening from the server side...
            logger.warning("Connection error, retrying request.")
            client.__renew_session()
            if attempts < 1:
                return client.__handle_request(url, method, data, json_data, params, headers, attempts + 1)
            raise e

        return response.json()
    
    @staticmethod
    def __get_auth_header():
        client.validate_login()
        return {"Authorization": f"Bearer {user_settings.access_token}"}

def process_error_in_response(response):
    if response.status_code >=400 and response.status_code <500:
        detail = response.json().get("detail", "Request failed, no details provided.")
        raise RequestFailedException(response.status_code, detail)
    if response.status_code >=500:
        raise RequestFailedException(response.status_code, "Server error")