#!/usr/bin/python
# -*- coding: UTF-8 -*-

from api import API
from logger import logger
from util import dict_util
import requests
import base64


class RestAPI(API):

    def __init__(self, username, password):
        super(RestAPI, self).__init__(username, password)
        self.logger = logger.getlogger(RestAPI.__name__)
        self.token = None
        self.url = None

    def login(self, server, port=81):
        login_req = {}
        self.logger.info("Logging in to server: %s", server)

        if self.userName is None:
            # print("Username is required")
            self.logger.error("Username is required")
            raise ValueError("Username is required")
        else:
            login_req["username"] = self.userName

        if self.password is None:
            login_req["password"] = ""
        else:
            # encode password in base64 for Python 1 and 2
            login_req["password"] = base64.b64encode(self.password)

        # Login request built. Send the request now:
        self.url = "http://" + server + ":" + bytes(port) + "/SearchSvc/CVWebService.svc/"
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        r = requests.post(self.url + "Login",
                          json=login_req,
                          headers=headers)
        self.logger.debug("Response from login request: %s", r)
        # Check response code and check if the response has an attribute "token" set
        if r.status_code == 200:
            root = r.json()
            if root.get("token") is not None:
                self.token = root.get("token")
                self.logger.info("Login Successful")
            else:
                self.logger.error("Login Failed")
                raise RuntimeError("Login Failed")
        else:
            self.logger.error("There was an error logging in: %s", r.status_code)
            raise RuntimeError("Login Failed")

    def get_storage_policy(self):
        self.logger.info("Get storage policy list")
        headers = {'Cookie2': self.token, "Accept": "application/json",
                   "Authtoken": self.token}

        r = requests.get(self.url + "StoragePolicy", headers=headers)
        resp_root = r.json()
        self.logger.debug("Response from server: %s", resp_root)
        policies = resp_root.get("policies")
        storage_policy_name_list = []

        if r.status_code != 200 and r.status_code != 201:
            error_code = resp_root.get("errorCode")
            error_msg = resp_root.get("errorMessage")
            self.logger.error("Failed to get storage policy list. %s Error Code: %s", error_msg, error_code)
            return storage_policy_name_list, policies

        # for policy in policies:
        #     storage_policy_name_list.append(policy.get("storagePolicyName"))
        storage_policy_name_list = [policy.get("storagePolicyName") for policy in policies if policy.get("storagePolicyName")]
        self.logger.debug("Get storage policy list successfully: %s", storage_policy_name_list)

        return storage_policy_name_list, policies

    def get_schedule_policy(self):
        self.logger.info("Get schedule policy list")
        headers = {'Cookie2': self.token, "Accept": "application/json",
                   "Authtoken": self.token}

        r = requests.get(self.url + "SchedulePolicy", headers=headers)
        resp_root = r.json()
        self.logger.debug("Response from server: %s", resp_root)
        policies = resp_root.get("taskDetail")
        schedule_policy_name_list = []

        if r.status_code != 200 and r.status_code != 201:
            error_code = resp_root.get("errorCode")
            error_msg = resp_root.get("errorMessage")
            self.logger.error("Failed to get storage policy list. %s Error Code: %s", error_msg, error_code)
            return schedule_policy_name_list, policies

        schedule_policy_name_list = [policy.get("task").get("taskName") for policy in policies if policy.get("task")]
        self.logger.debug("Get schedule policy list successfully: %s", schedule_policy_name_list)

        return schedule_policy_name_list, policies

    def get_subclient(self, client_id=None, client_name=None):
        self.logger.info("Get subclient list with clientId %s clientName %s", client_id, client_name)
        headers = {'Cookie2': self.token, "Accept": "application/json",
                   "Authtoken": self.token}

        if client_id is not None:
            content = {"clientId": client_id}
        elif client_name is not None:
            content = {"clientName": client_name}
        else:
            self.logger.error("Both clientId and clientName are null")
            raise RuntimeError("Either clientId or clientName should be provided")

        r = requests.get(self.url + "Subclient", params=content, headers=headers)
        resp_root = r.json()
        self.logger.debug("Response from server: %s", resp_root)
        subclient_properties = resp_root.get("subClientProperties")
        subclient_list = []

        if r.status_code != 200 and r.status_code != 201:
            error_code = resp_root.get("errorCode")
            error_msg = resp_root.get("errorMessage")
            self.logger.error("Failed to get subclient list. %s Error Code: %s", error_msg, error_code)
            return subclient_list, subclient_properties

        subclient_list = [subclient.get("subClientEntity").get("subclientName") for subclient in subclient_properties if
                          subclient.get("subClientEntity") and subclient.get("subClientEntity").get("subclientName")]
        self.logger.debug("Get subclient list successfully: %s", subclient_list)
        return subclient_list, subclient_properties

    def create_subclient(self, template, appname, clientname, subclientname, storage_policy_name="", paths=(),
                        num_of_backup_streams=1, backupset_name="defaultBackupSet", descpt="",
                        content_operation_type="", enable_backup=True):
        self.logger.info("Creating subclient %s in client %s", subclientname, clientname)

        headers = {'Cookie2': self.token, "Content-Type": "application/json", "Accept": "application/json",
                   "Authtoken": self.token}

        template = dict_util.dict_update_child(template, appname, "appName", "subClientProperties", "subClientEntity")

        template = dict_util.dict_update_child(template, clientname, "clientName", "subClientProperties",
                                               "subClientEntity")

        template = dict_util.dict_update_child(template, subclientname, "subclientName", "subClientProperties",
                                               "subClientEntity")

        template = dict_util.dict_update_child(template, backupset_name, "backupsetName", "subClientProperties",
                                               "subClientEntity")

        template = dict_util.dict_update_child(template, content_operation_type, "contentOperationType",
                                               "subClientProperties")

        template = dict_util.dict_update_child(template, enable_backup, "enableBackup", "subClientProperties",
                                               "commonProperties")

        template = dict_util.dict_update_child(template, descpt, "description", "subClientProperties",
                                               "commonProperties")

        template = dict_util.dict_update_child(template, num_of_backup_streams, "numberOfBackupStreams",
                                               "subClientProperties", "commonProperties")

        template = dict_util.dict_update_child(template, storage_policy_name, "storagePolicyName",
                                               "subClientProperties", "commonProperties", "storageDevice",
                                               "dataBackupStoragePolicy")

        content = []
        for path in paths:
            content.append({"path": path})

        template = dict_util.dict_update_child(template, content, "content", "subClientProperties")

        dict_util.dict_remove_null_pair(template)
        r = requests.post(self.url + "Subclient", json=template, headers=headers)
        resp_root = r.json()
        self.logger.debug("Response from server: %s", resp_root)

        if r.status_code != 200 and r.status_code != 201:
            error_code = resp_root.get("errorCode")
            error_msg = resp_root.get("errorMessage")
            self.logger.error("Failed to create subclient: %s. %s Error Code: %s",
                              subclientname, error_msg, error_code)
        else:
            self.logger.info("Subclient: %s created successfully", subclientname)
        # errorList = resp_root.get("errList")

        # if errorList is not None and len(errorList) > 0:
        #     errorCode = errorList[0]["errorCode"]
        #     errorMsg = errorList[0]["errorMessage"]

        # if errorCode == "0":
        #     self.logger.info("Subclient: %s create successfully", subclientname)
        # else:
        #     self.logger.error("Failed to create subclient: %s. %s. Error Code: %s",
        #                       subclientname, errorMsg, errorCode)

    def post_execute_qcommand(self, template, command):
        headers = {'Cookie2': self.token,
                   "Content-Type": "application/x-www-form-urlencoded",
                   "Accept": "application/json",
                   "Authtoken": self.token}

        data = {'command': command}
        if template:
            data['inputRequestXML'] = template

        response = requests.post(self.url + "ExecuteQCommand", data=data, headers=headers)

        return response

    def logout(self):
        self.logger.info("Logging out")
        headers = {'Cookie2': self.token}
        requests.post(self.url + "Logout", headers=headers)
        self.logger.info("Logout Successful")

# if __name__ == '__main__':
#    abc = RestAPI("admin", "")
#    abc.login("192.168.56.101")
#    abc.createsubclient("appname", "client", "sub", "sotrage")
#    abc.logout()
