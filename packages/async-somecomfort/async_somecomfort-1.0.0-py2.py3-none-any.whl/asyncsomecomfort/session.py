"""
This module contains the Session class, which handles communication with the Honeywell TCC API.
It manages login, session persistence, device interactions, and API request handling.

Classes:
    Session: Manages authentication, API requests, and session state for Honeywell TCC services.
"""

import aiohttp
from http.cookies import SimpleCookie
import logging
import contextlib
from .exceptions import AuthError, APIError, SessionTimedOut, APIRateLimited

_LOG = logging.getLogger("somecomfort")

class Session:
    """
    Represents a session for interacting with the Honeywell TCC API. This class handles
    authentication, API requests, cookie management, and session persistence.

    Attributes:
        _username (str): The username for logging into the Honeywell TCC service.
        _password (str): The password for logging into the Honeywell TCC service.
        _timeout (int): The timeout for API requests, in seconds.
        _baseurl (str): The base URL for the Honeywell TCC portal.
        _session (aiohttp.ClientSession): The aiohttp session for making API requests.
        _headers (dict): Default headers to be sent with each API request.
    """

    def __init__(self, username, password, timeout=30):
        """
        Initializes the session with credentials and timeout settings.

        Args:
            username (str): The username for authentication.
            password (str): The password for authentication.
            timeout (int): The timeout for API requests, in seconds.
        """
        self._username = username
        self._password = password
        self._timeout = timeout
        self._baseurl = 'https://www.mytotalconnectcomfort.com/portal'
        self._default_url = self._baseurl
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': self._baseurl,
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive'
        }
        self._locations = {}
        self._session = aiohttp.ClientSession()

    async def __aenter__(self):
        """
        Asynchronous context manager entry method. Logs in upon entering the context.

        Returns:
            Session: The current session instance.
        """
        await self.login()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Asynchronous context manager exit method. Closes the session when exiting the context.
        """
        await self.close()

    async def login(self):
        """
        Logs into the Honeywell TCC portal using the provided username and password.
        Updates cookies upon successful login and performs a keepalive check.

        Raises:
            AuthError: If the login fails due to invalid credentials or other issues.
        """
        try:
            async with self._session.get(self._baseurl, headers=self._headers, timeout=self._timeout) as resp:
                if resp.status != 200:
                    raise AuthError(f"Failed to fetch login page, status code: {resp.status}")
                
                _LOG.info(f"Login page fetched, status: {resp.status}")
                self._update_cookies(resp.cookies)

            login_data = {
                'UserName': self._username,
                'Password': self._password,
                'RememberMe': 'false',
                'timeOffset': 480
            }

            async with self._session.post(self._baseurl, data=login_data, headers=self._headers, timeout=self._timeout, allow_redirects=True) as resp:
                if resp.status != 200:
                    raise AuthError(f"Login failed with status code {resp.status}")
                
                final_url = str(resp.url)
                _LOG.info(f"Login redirect to: {final_url}")
                
                text = await resp.text()
                if "Invalid username or password" in text:
                    raise AuthError("Invalid username or password.")

                _LOG.info(f"Login successful for user {self._username}")
                self._update_cookies(resp.cookies)

            await self.keepalive()

        except Exception as e:
            _LOG.error(f"Login error: {str(e)}")
            raise AuthError(f"Login failed: {str(e)}")

    @contextlib.asynccontextmanager
    async def _retries_login(self):
        """
        Context manager to attempt re-login in case of session timeout.
        Ensures session persistence by attempting to refresh or re-login if needed.
        """
        try:
            await self.keepalive()
        except SessionTimedOut:
            await self.login()
        yield

    def _update_cookies(self, cookies):
        """
        Updates the session's cookie jar with the cookies provided by the API response.

        Args:
            cookies (http.cookies.SimpleCookie or dict): The cookies returned by the API.

        Raises:
            None: Logs unexpected cookie types if not properly formatted.
        """
        if isinstance(cookies, SimpleCookie):
            for key, morsel in cookies.items():
                self._session.cookie_jar.update_cookies({key: morsel.value})
        elif isinstance(cookies, dict):
            for key, value in cookies.items():
                if isinstance(value, dict) and 'value' in value:
                    self._session.cookie_jar.update_cookies({key: value['value']})
                else:
                    self._session.cookie_jar.update_cookies({key: value})
        elif hasattr(cookies, 'items'):  # Handles CookieJar objects
            for cookie in cookies:
                self._session.cookie_jar.update_cookies({cookie.key: cookie.value})
        else:
            _LOG.warning(f"Unexpected cookie type: {type(cookies)}")
        
        cookie_header = '; '.join([f'{cookie.key}={cookie.value}' for cookie in self._session.cookie_jar])
        if cookie_header:
            self._headers['Cookie'] = cookie_header
        _LOG.debug(f"Updated cookie header: {self._headers.get('Cookie', 'No cookies set')}")

    async def keepalive(self):
        """
        Keeps the session alive by sending a request to the base URL.

        Raises:
            SessionTimedOut: If the session has timed out.
            ConnectionError: If there is a connection failure.
        """
        try:
            async with self._session.get(self._baseurl, headers=self._headers, timeout=self._timeout) as resp:
                if resp.status != 200:
                    raise SessionTimedOut("Session has timed out.")
                _LOG.info("Session refreshed successfully.")
                self._update_cookies(resp.cookies)
        except aiohttp.ClientError as e:
            _LOG.error(f"Keepalive failed: {e}")
            raise ConnectionError(f"Failed to connect to API: {e}")

    async def _request_json(self, method, *args, **kwargs):
        """
        Sends an HTTP request (GET or POST) and processes the JSON response.

        Args:
            method (str): The HTTP method to use ('get' or 'post').
            *args: Positional arguments for the request.
            **kwargs: Additional keyword arguments for the request.

        Returns:
            dict: The parsed JSON response.

        Raises:
            APIError: If the response contains an unexpected status code or data.
            APIRateLimited: If the API rate limit is exceeded.
        """
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self._timeout

        async with getattr(self._session, method)(*args, **kwargs) as resp:
            req = args[0].replace(self._baseurl, '')
            _LOG.debug(f"Request to {req} - Status: {resp.status}, Headers: {resp.headers}")

            text = await resp.text()

            if resp.status == 200:
                content_type = resp.headers.get('Content-Type', '')
                if 'application/json' in content_type:
                    return await resp.json()
                else:
                    _LOG.error(f"Unexpected response type: {content_type}")
                    _LOG.error(f"Response text: {text}")
                    raise APIError(f"Unexpected response type from {req}: {content_type}")
            elif resp.status == 429:
                _LOG.error(f"Rate limit exceeded: {resp.status}")
                _LOG.error(f"Response text: {text}")
                raise APIRateLimited()
            else:
                _LOG.error(f'API returned {resp.status} from {req} request')
                _LOG.error(f'Response body: {text}')
                raise APIError(f'Unexpected {resp.status} response from API: {text[:200]}...')

    async def get_locations(self):
        """
        Fetches the list of locations associated with the current session.

        Returns:
            dict: A dictionary containing location data.

        Raises:
            APIError: If there is an issue fetching location data.
            SessionTimedOut: If the session has timed out.
        """
        url = f'{self._baseurl}/Location/GetLocationListData'
        params = {'page': 1, 'filter': ''}
        headers = self._headers.copy()
        headers['Referer'] = f"{self._baseurl}/"

        async with self._retries_login():
            try:
                _LOG.debug(f"Fetching locations from {url}")
                result = await self._post_json(url, params=params, headers=headers)
                _LOG.debug(f"Received response: {result}")
                return result
            except SessionTimedOut:
                _LOG.info("Session timed out while fetching locations, attempting to log in again...")
                await self.login()
                _LOG.debug(f"Retrying fetch locations from {url}")
                result = await self._post_json(url, params=params, headers=headers)
                _LOG.debug(f"Received response after re-login: {result}")
                return result
            except Exception as e:
                _LOG.error(f"Error fetching locations: {str(e)}", exc_info=True)
                raise

    async def get_thermostat_data(self, thermostat_id):
        """
        Fetches data for a specific thermostat by its ID.

        Args:
            thermostat_id (str): The ID of the thermostat.

        Returns:
            dict: The thermostat data.

        Raises:
            APIError: If there is an issue fetching the thermostat data.
        """
        url = f'{self._baseurl}/Device/CheckDataSession/{thermostat_id}'
        headers = self._headers.copy()
        headers['Referer'] = f"{self._baseurl}/"

        async with self._retries_login():
            try:
                _LOG.debug(f"Fetching thermostat data from {url}")
                _LOG.debug(f"Request headers: {headers}")
                _LOG.debug(f"Cookies being sent: {self._session.cookie_jar.filter_cookies(url)}")

                async with self._session.get(url, headers=headers, allow_redirects=False) as resp:
                    _LOG.debug(f"Initial response status: {resp.status}")
                    _LOG.debug(f"Response headers: {resp.headers}")

                    if resp.status == 302:
                        redirect_url = resp.headers.get('Location')
                        _LOG.debug(f"Following redirect to: {redirect_url}")
                        async with self._session.get(redirect_url, headers=headers) as redirect_resp:
                            _LOG.debug(f"Redirect response status: {redirect_resp.status}")
                            _LOG.debug(f"Redirect response headers: {redirect_resp.headers}")
                            self._update_cookies(redirect_resp.cookies)
                            return await redirect_resp.json()
                    elif resp.status == 200:
                        self._update_cookies(resp.cookies)
                        return await resp.json()
                    else:
                        text = await resp.text()
                        _LOG.error(f"Unexpected status code: {resp.status}")
                        _LOG.error(f"Response body: {text}")
                        raise APIError(f"Unexpected {resp.status} response from API: {text[:200]}...")

            except Exception as e:
                _LOG.error(f"Error fetching thermostat data: {str(e)}", exc_info=True)
                raise

    async def set_thermostat_settings(self, thermostat_id, settings):
        """
        Sets the thermostat settings for a specific thermostat.

        Args:
            thermostat_id (str): The ID of the thermostat.
            settings (dict): A dictionary of settings to be applied to the thermostat.

        Raises:
            APIError: If the API rejects the settings.
        """
        data = {
            'SystemSwitch': None,
            'HeatSetpoint': None,
            'CoolSetpoint': None,
            'HeatNextPeriod': None,
            'CoolNextPeriod': None,
            'StatusHeat': None,
            'DeviceID': thermostat_id,
        }
        data.update(settings)
        url = f'{self._baseurl}/Device/SubmitControlScreenChanges'
        async with self._retries_login():
            result = await self._post_json(url, data=data)
            if result.get('success') != 1:
                raise APIError('API rejected thermostat settings')

    async def _get_json(self, *args, **kwargs):
        """
        Sends an HTTP GET request and returns the parsed JSON response.
        """
        return await self._request_json('get', *args, **kwargs)

    async def _post_json(self, *args, **kwargs):
        """
        Sends an HTTP POST request and returns the parsed JSON response.
        """
        return await self._request_json('post', *args, **kwargs)

    async def close(self):
        """
        Closes the session and releases resources.
        """
        await self._session.close()
