import logging
import requests
import boto3
from http import HTTPStatus
from requests_aws4auth import AWS4Auth

from minion_helpers.service import Service, ServiceMode

logger = logging.getLogger(__name__)


class ClientNotEnrolledException(Exception):
    pass


class BadResponseException(Exception):
    pass


class Bob(Service):
    """
    Global Class for Handling Bob Authentication Interactions
    """

    def __init__(self, endpoint_url=None, region_name="us-east-1", ms_name=None, client_id=None, testing=False):
        self.endpoint_url = endpoint_url
        self.ms_name = ms_name
        self.client_id = client_id
        self.request_url = None
        self.region = region_name
        self.mode = ServiceMode.AWS if (not testing) else ServiceMode.LOCAL
        self.init_request_url()

    def init_request_url(self):
        if self.ms_name and self.client_id:
            self.request_url = "{}/{}/{}".format(self.endpoint_url, self.ms_name, self.client_id)

    def enroll(self, ms_name=None, client_id=None):
        self.ms_name = ms_name
        self.client_id = client_id
        self.init_request_url()

    def __add_auth_headers(self):
        auth = None
        if self.mode == ServiceMode.AWS:
            session = boto3.Session()
            credentials = session.get_credentials().get_frozen_credentials()
            auth = AWS4Auth(credentials.access_key, credentials.secret_key, self.region, 'execute-api',
                            session_token=credentials.token)
        return auth

    def __make_request(self, path=None, method=None, **kwargs):
        """
        Make Request to Bob Authentication Service
        :param path: Path to Bob Endpoint
        :param method: HTTP Method Verb
        :param kwargs: Other Keyword Arguments
        :return: HTTP Response
        """

        url = self.request_url + path
        logger.info("%s::Making Request:: url:%s method:%s" % (__class__.__name__, url, method))

        request_kwargs = {'auth': self.__add_auth_headers(),
                          'json': kwargs.get('data'),
                          'params': kwargs.get('params')}

        response = requests.request(method, url, **request_kwargs)

        return response

    def __request_api(self, path=None, method=None, **kwargs):
        return self.__make_request(path, method, **kwargs)

    def get_url(self):
        return self.request_url

    def verify_client_enrolled(self):
        if not self.ms_name or not self.client_id:
            raise ClientNotEnrolledException("Client not Enrolled. MS Name & Client ID missing")

    def get_setting_by_key(self, key):
        """
        Get Setting of your service by key
        :param key: setting key
        :return: Response from bob
        """
        self.verify_client_enrolled()
        response = self.__request_api(path="", method="GET", params=dict(key=key))
        if response.status_code in (HTTPStatus.OK, HTTPStatus.BAD_REQUEST):
            return response.json()
        else:
            raise BadResponseException("Bad Response. Response Dict::%s \n" % response.__dict__)

    def get_all_settings(self):
        """
        Get Settings of your service
        :return: Response from bob
        """
        self.verify_client_enrolled()
        response = self.__request_api(path="/settings", method="GET")
        if response.status_code in (HTTPStatus.OK, HTTPStatus.BAD_REQUEST):
            return response.json()
        else:
            raise BadResponseException("Bad Response. Response Dict::%s \n" % response.__dict__)

    def add_bulk_settings(self, payload):
        """
        Bulk add all the settings of your microservice
        :param payload: List of Settings
        :return: Response from bob
        """
        self.verify_client_enrolled()
        response = self.__request_api(path="/bulk-upload-settings", method="POST", data=payload)
        if response.status_code in (HTTPStatus.OK, HTTPStatus.BAD_REQUEST):
            return response.json()
        else:
            raise BadResponseException("Bad Response. Response Dict::%s \n" % response.__dict__)


    def get_user(self, user_id):
        """
        Given a user ID, Fetch the user details
        :param user_id: current user id
        :return: Response from Bob
        """
        self.verify_client_enrolled()
        response = self.__request_api(path="/user/{}" % user_id, method="GET")
        if response.status_code in (HTTPStatus.OK, HTTPStatus.BAD_REQUEST):
            return response.json()
        else:
            raise BadResponseException("Bad Response. Response Dict::%s \n" % response.__dict__)

    def add_new_setting(self, key, value, description):
        """
        Add a new Setting
        :param key: key for your setting
        :param value: value for the key (should be string or json dumped list,dict etc)
        :param description: Description of your setting
        :return: Response from bob
        """
        self.verify_client_enrolled()
        payload = dict(key=key, value=value, description=description)
        response = self.__request_api(path="/create-setting", method="POST", data=payload)
        if response.status_code in (HTTPStatus.OK, HTTPStatus.BAD_REQUEST):
            return response.json()
        else:
            raise BadResponseException("Bad Response. Response Dict::%s \n" % response.__dict__)

    def update_setting(self, key, value, description):
        """
        Update a Setting
        :param key: key of the setting to update
        :param value: value for the key (should be string or json dumped list,dict etc)
        :param description: Description of your setting
        :return: Response from bob
        """
        self.verify_client_enrolled()
        payload = dict(key=key, value=value, description=description)
        response = self.__request_api(path="/update-setting", method="PATCH", data=payload)
        if response.status_code in (HTTPStatus.OK, HTTPStatus.BAD_REQUEST):
            return response.json()
        else:
            raise BadResponseException("Bad Response. Response Dict::%s \n" % response.__dict__)

    def delete_setting(self, key):
        """
        Delete the setting by its key
        :param key: key setting to delete
        :return: Response from bob
        """
        self.verify_client_enrolled()
        response = self.__request_api(path="/delete-setting", method="DELETE", params=dict(key=key))
        if response.status_code in (HTTPStatus.OK, HTTPStatus.BAD_REQUEST):
            return response.json()
        else:
            raise BadResponseException("Bad Response. Response Dict::%s \n" % response.__dict__)
