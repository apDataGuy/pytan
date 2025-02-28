# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
'''Session handler for Tanium API'''

import os
import httplib
import string
import xml.etree.ElementTree as ET
import logging
import json
# needed for python 2.7.9 to revert SSL verification
import ssl
# 1.04: added for xml_fix()
import re
from datetime import datetime

from base64 import b64encode
from .object_types.base import BaseType
from .object_types.result_info import ResultInfo
from .object_types.result_set import ResultSet

# fix for UTF encoding
import sys
reload(sys)
sys.setdefaultencoding('latin-1')

# 1.0.4: added for xml_fix(), declare a regex that identifies invalid characters in unicode
invalid_xml = re.compile(u'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]')

my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
mylog = logging.getLogger("api.session")
authlog = logging.getLogger("api.session.auth")
httplog = logging.getLogger("api.session.http")
bodyhttplog = logging.getLogger("api.session.http.body")

# to support py2exe compiled scripts
my_dir = my_dir.replace('\\library.zip\\taniumpy', '')
request_body_template_file = os.path.join(my_dir, 'request_body_template.xml')


class NoLogging(object):

    count = 0

    """Disable logging while executing code block"""
    def __enter__(self):
        NoLogging.count += 1
        logging.disable(logging.CRITICAL)

    def __exit__(self, exc_type, exc_value, traceback):
        NoLogging.count -= 1
        if NoLogging.count == 0:
            logging.disable(logging.NOTSET)


def nologging(func):
    """decorator to disable logging on a function"""
    def func_wrapper(*args, **kwargs):
        with NoLogging():
            return func(*args, **kwargs)
    return func_wrapper


class HttpError(Exception):
    pass


class AuthorizationError(Exception):
    pass


class BadResponseError(Exception):
    pass


def load_file(filename):
    with open(filename) as fd:
        content = fd.read().decode('utf-8')
    return content


def xml_fix(s):
    """
    # 1.0.4: added this function

    this supports better handling of invalid XML, removing invalid control characters and
    re-encoding to utf-8 with xmlcharrefreplace
    """
    # string that will be used to replace any invalid characters
    fixer_str = "???"
    # encode the string as utf-8
    utf_str = s.encode('utf-8', 'xmlcharrefreplace')
    # decode the string from utf-8 into unicode
    unicode_str = utf_str.decode('utf-8', 'xmlcharrefreplace')
    # replace any invalid characters that match the invalid_xml regex with the fixer_str
    clean_str, count = invalid_xml.subn(fixer_str, unicode_str)
    # if any invalid characters found, print out a debug message saying how many were replaced
    if count:
        mylog.debug("Replaced {} invalid characters in the XML with {}".format(count, fixer_str))
    # re-encode the string as utf-8
    utf_str = clean_str.encode('utf-8', 'xmlcharrefreplace')
    return utf_str


def http_post(host, port, url, body=None, headers=None, timeout=5):
    # revert SSL verification for python 2.7.9
    try:
        http = httplib.HTTPSConnection(
            host, port, timeout=timeout, context=ssl._create_unverified_context()
        )
    except:
        http = httplib.HTTPSConnection(host, port, timeout=timeout)

    req_args = {}
    req_args['method'] = 'POST'
    req_args['url'] = url
    if body is not None:
        req_args['body'] = body
    if headers is not None:
        req_args['headers'] = headers

    full_url = "https://{0}:{1}/{2}".format(host, port, url)

    httplog.debug("Sending POST to {}".format(full_url, headers))
    bodyhttplog.debug("request headers: {}, body:\n{}".format(headers, body))

    try:
        http.connect()
        http.request(**req_args)
        response = http.getresponse()
        response_body = response.read()
    finally:
        http.close()

    httplog.debug(type(response_body))
    httplog.debug((
        "HTTP response from {0!r} len:{1}, status:{2.status} {2.reason}"
    ).format(full_url, len(response_body), response))
    bodyhttplog.debug((
        "response headers: {}, body:\n{}"
    ).format(response.getheaders(), response_body))

    if not response_body:
        raise HttpError("POST request to {} returned nothing".format(full_url))
    if response.status not in [200]:
        raise HttpError(response_body)
    return response_body


class DynamicFormatter(string.Formatter):

    def get_value(self, key, args, kwargs):
        if type(key) in [str, unicode]:
            return kwargs.get(key, '')
        return string.Formatter.get_value(self, key, args, kwargs)


class Session(object):

    GET_OBJECT = 'GetObject'
    UPDATE_OBJECT = 'UpdateObject'
    ADD_OBJECT = 'AddObject'
    DELETE_OBJECT = 'DeleteObject'
    GET_RESULT_INFO = 'GetResultInfo'
    GET_RESULT_DATA = 'GetResultData'
    REQUEST_BODY = load_file(request_body_template_file)
    FORMATTER = DynamicFormatter().format
    AUTH_RES = '/auth'
    SOAP_RES = '/soap'
    INFO_RES = '/info.json'
    # only used for get_server_info()
    SOAP_PORT = 444

    def __init__(self, server, port=443):
        self.server = server
        self.port = port
        self.last = {}

    def __str__(self):
        class_name = self.__class__.__name__
        str_tpl = "{} to {}:{}, Authenticated: {}, Version: {}".format
        ret = str_tpl(
            class_name,
            self.server,
            self.port,
            self.is_auth,
            self.server_version,
        )
        return ret

    def authenticate(self, username=None, password=None, get_version=True):
        if not hasattr(self, '_auth_headers'):
            if username is None:
                raise AuthorizationError("Must supply username")
            if password is None:
                raise AuthorizationError("Must supply password")

            self._auth_headers = {
                'username': b64encode(username),
                'password': b64encode(password),
            }

        with NoLogging():
            try:
                body = self._http_post(
                    url=self.AUTH_RES, headers=self._auth_headers,
                )
            except Exception as e:
                raise AuthorizationError(e)

        self.session_id = body
        authlog.debug("Successfully authenticated")
        if get_version:
            self.server_info = self.get_server_info()
        else:
            self.server_info = {}

    def find(self, object_type, **kwargs):
        self.request_body = self._createGetObjectBody(object_type, **kwargs)
        self.response_body = self._getResponse(self.request_body)
        obj = BaseType.fromSOAPBody(self.response_body)
        return obj

    def save(self, obj, **kwargs):
        self.request_body = self._createUpdateObjectBody(obj, **kwargs)
        self.response_body = self._getResponse(self.request_body)
        obj = BaseType.fromSOAPBody(self.response_body)
        return obj

    def add(self, obj, **kwargs):
        self.request_body = self._createAddObjectBody(obj, **kwargs)
        self.response_body = self._getResponse(self.request_body)
        obj = BaseType.fromSOAPBody(self.response_body)
        return obj

    def delete(self, obj, **kwargs):
        self.request_body = self._createDeleteObjectBody(obj, **kwargs)
        self.response_body = self._getResponse(self.request_body)
        obj = BaseType.fromSOAPBody(self.response_body)
        return obj

    def getResultInfo(self, obj, **kwargs):
        self.request_body = self._createGetResultInfoBody(obj, **kwargs)
        self.response_body = self._getResponse(self.request_body)
        # parse the single result_info into an Element and create a ResultInfo
        el = ET.fromstring(self.response_body)
        cdata = el.find('.//ResultXML')
        # 1.0.4: fix for utf-8 issues
        result_info = ET.fromstring(xml_fix(cdata.text))
        # TODO: maybe this should be ResultInfoList
        obj = ResultInfo.fromSOAPElement(result_info)
        return obj

    def getResultData(self, obj, **kwargs):
        self.request_body = self._createGetResultDataBody(obj, **kwargs)
        self.response_body = self._getResponse(self.request_body)
        # parse the single result_info into an Element and create a ResultData
        el = ET.fromstring(self.response_body)
        cdata = el.find('.//ResultXML')
        # 1.0.4: fix for utf-8 issues
        result_info = ET.fromstring(xml_fix(cdata.text))
        # TODO: maybe this should be ResultSetList
        obj = ResultSet.fromSOAPElement(result_info)
        return obj

    def get_server_info(self):
        self._check_auth()
        # we can't use _http_post, because INFO_RES is only available on
        # SOAP_PORT
        try:
            with NoLogging():
                body = http_post(
                    host=self.server,
                    port=self.SOAP_PORT,
                    url=self.INFO_RES,
                    headers=self._auth_headers,
                )
            body = json.loads(body)
            mylog.debug((
                "Successfully retrieved server info from {}"
            ).format(self.INFO_RES))
        except Exception as e:
            mylog.warn((
                "Failed to retrieve server info from {}, {}"
            ).format(self.INFO_RES, e))
            body = {'server_info_error': e}
        return body

    @property
    def session_id(self):
        if not hasattr(self, '_session_id'):
            return ''
        return self._session_id

    @session_id.setter
    def session_id(self, value):
        self._session_id = value
        authlog.debug("Session ID updated to: {}".format(value))

    @property
    def is_auth(self):
        if self.session_id:
            return True
        else:
            return False

    @property
    def server_version(self):
        server_version = "Unable to determine"
        try:
            server_info = getattr(self, 'server_info')
            diagnostics = server_info.get('Diagnostics')
            settings = [x for x in diagnostics if 'Settings' in x][0]
            server_version = settings['Settings']['Version']
        except:
            pass
        return server_version

    def _http_post(self, url, body=None, headers=None):
        body = http_post(self.server, self.port, url, body, headers)
        return body

    def _createAddObjectBody(self, obj, **kwargs):
        obj_soap = obj.toSOAPBody(minimal=True)

        obj_body = self.FORMATTER(
            self.REQUEST_BODY,
            self.session_id,
            self.ADD_OBJECT,
            obj_soap,
            **kwargs
        )
        return obj_body

    def _createDeleteObjectBody(self, obj, **kwargs):
        obj_body = self.FORMATTER(
            self.REQUEST_BODY,
            self.session_id,
            self.DELETE_OBJECT,
            obj.toSOAPBody(),
            **kwargs
        )
        return obj_body

    def _createGetResultInfoBody(self, obj, **kwargs):
        obj_body = self.FORMATTER(
            self.REQUEST_BODY,
            self.session_id,
            self.GET_RESULT_INFO,
            obj.toSOAPBody(),
            **kwargs
        )
        return obj_body

    def _createGetResultDataBody(self, obj, **kwargs):
        obj_body = self.FORMATTER(
            self.REQUEST_BODY,
            self.session_id,
            self.GET_RESULT_DATA,
            obj.toSOAPBody(),
            **kwargs
        )
        return obj_body

    def _createGetObjectBody(self, object_or_type, **kwargs):
        if isinstance(object_or_type, BaseType):
            obj = object_or_type.toSOAPBody(minimal=True)
        else:
            obj = '<{}/>'.format(object_or_type._soap_tag)
        obj_body = self.FORMATTER(
            self.REQUEST_BODY,
            self.session_id,
            self.GET_OBJECT,
            obj,
            **kwargs
        )
        return obj_body

    def _createUpdateObjectBody(self, obj, **kwargs):
        obj_body = self.FORMATTER(
            self.REQUEST_BODY,
            self.session_id,
            self.UPDATE_OBJECT,
            obj.toSOAPBody(),
            **kwargs
        )
        return obj_body

    def _check_auth(self):
        if not self.is_auth:
            class_name = self.__class__.__name__
            err = "Not yet authenticated, use {}.authenticate()!".format
            raise AuthorizationError(err(class_name))

    def _getResponse(self, request_body):
        self._check_auth()
        self.last = {}
        request_body_el = ET.fromstring(request_body)
        request_command = request_body_el.find('.//command').text
        self.last['request_command'] = request_command

        self.last['sent'] = datetime.now()
        headers = {'Content-Type': 'text/xml'}

        # 1.0.4: fix for UTF encoding
        response_body = xml_fix(self._http_post(
            url=self.SOAP_RES, body=request_body, headers=headers,
        ))

        self.last['received'] = datetime.now()
        elapsed = self.last['received'] - self.last['sent']
        self.last['elapsed'] = elapsed

        response_body_el = ET.fromstring(response_body)
        response_command = response_body_el.find('.//command').text
        self.last['response_command'] = response_command

        if 'forbidden' in response_command.lower():
            authlog.debug(
                "Last request failed, re-authenticating with user/pass"
            )

            # we may have hit the 5 minute expiration for session_id
            # re-auth with self._auth_headers and re-try
            self.authenticate()

            # Update session id in request body
            request_body_el.find('.//session').text = self.session_id
            request_body = ET.tostring(request_body_el)

            # resend request_body
            self.last['sent'] = datetime.now()

            # 1.0.4: fix for UTF encoding
            response_body = xml_fix(self._http_post(
                url=self.SOAP_RES, body=request_body, headers=headers,
            ))
            self.last['response_body'] = response_body
            self.last['received'] = datetime.now()
            elapsed = self.last['received'] - self.last['sent']
            self.last['elapsed'] = elapsed
            response_body_el = ET.fromstring(response_body)
            response_command = response_body_el.find('.//command').text
            self.last['response_command'] = response_command
            if 'forbidden' in response_command.lower():
                raise AuthorizationError(response_command)

        if response_command != request_command:
            raise BadResponseError(response_command)

        # update session_id, in case new one issued
        self.session_id = response_body_el.find('.//session').text

        return response_body
