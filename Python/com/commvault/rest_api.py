#!/usr/bin/python
# -*- coding: UTF-8 -*-

from api import API
from logger import logger
import requests
import xml.etree.ElementTree as ET
import base64


class RestAPI(API):

    def __init__(self, username, password):
        super(RestAPI, self).__init__(username, password)
        self.logger = logger.getlogger(RestAPI.__name__)
        self.token = None
        self.url = None

    def login(self, server, port=81):
        loginReq = '<DM2ContentIndexing_CheckCredentialReq mode="Webconsole" username="<<username>>" password="<<password>>" />'
        self.logger.info("Logging in to server: %s", server)

        if self.userName is None:
            # print("Username is required")
            self.logger.error("Username is required")
            raise ValueError("Username is required")
        else:
            loginReq = loginReq.replace("<<username>>", self.userName)

        if self.password is None:
            loginReq = loginReq.replace("<<password>>", "")
        else:
            # encode password in base64 for Python 1 and 2
            loginReq = loginReq.replace("<<password>>", base64.b64encode(self.password))

        # Login request built. Send the request now:
        self.url = "http://" + server + ":" + bytes(port) + "/SearchSvc/CVWebService.svc/"
        r = requests.post(self.url + "Login",
                          data=loginReq)

        # Check response code and check if the response has an attribute "token" set
        if r.status_code == 200:
            root = ET.fromstring(r.text)
            if "token" in root.attrib:
                self.token = root.attrib["token"]
                self.logger.info("Login Successful")
            else:
                self.logger.error("Login Failed")
                raise RuntimeError("Login Failed")
        else:
            self.logger.error("There was an error logging in: %s", r.status_code)
            raise RuntimeError("Login Failed")

    def createsubclient(self, appname, clientname, subclientname, storage_policy_name="", paths=[],
                        num_of_backup_streams="1", backupset_name="defaultBackupSet", descpt="",
                        content_operation_type="", enableBackup="true"):
        self.logger.info("Creating subclient: %s", subclientname)

        headers = {'Cookie2': self.token}
        data = ET.parse("./create_subclient_template.xml")

        data = self.__xml_update_element(data, "./subClientProperties/subClientEntity/appName", appname)
        # appName = data.find("./subClientProperties/subClientEntity/appName")
        # appName.text = appname

        data = self.__xml_update_element(data, "./subClientProperties/subClientEntity/clientName", clientname)
        # clientName = data.find("./subClientProperties/subClientEntity/clientName")
        # clientName.text = clientname

        data = self.__xml_update_element(data, "./subClientProperties/subClientEntity/subclientName", subclientname)

        data = self.__xml_update_element(data, "./subClientProperties/subClientEntity/backupsetName", backupset_name)

        data = self.__xml_update_element(data, "./subClientProperties/contentOperationType", content_operation_type)

        data = self.__xml_update_element(data, "./subClientProperties/commonProperties/enableBackup", enableBackup)

        data = self.__xml_update_element(data, "./subClientProperties/commonProperties/description", descpt)

        data = self.__xml_update_element(data, "./subClientProperties/commonProperties/numberOfBackupStreams", num_of_backup_streams)

        data = self.__xml_update_element(data, "./subClientProperties/commonProperties/storageDevice/dataBackupStoragePolicy/storagePolicyName",
                                         storage_policy_name)

        for path in paths:
            data = self.__xml_add_element(data, "./subClientProperties/content", "path", path)

        # print(ET.tostring(data.getroot(), encoding="utf8", method="xml"))

        r = requests.post(self.url + "Subclient", data=ET.tostring(data.getroot(), encoding="utf8", method="xml"), headers=headers)
        resp = r.text
        # print(resp)
        respRoot = ET.fromstring(resp)
        # Check if Element has children or not
        if len(list(respRoot)) == 0:
            errorCode = respRoot.attrib["errorCode"]
            errorMsg = respRoot.attrib["errorMessage"]
        else:
            respEle = respRoot.find(".//[@errorCode]")
            errorCode = respEle.attrib["errorCode"]
            errorMsg = respEle.attrib["errorMessage"]

        if errorCode == "0":
            self.logger.info("Subclient: %s create successfully", subclientname)
        else:
            self.logger.error("Failed to create subclient: %s. %s. Error Code: %s", subclientname, errorMsg, errorCode)

    def logout(self):
        headers = {'Cookie2': self.token}
        requests.post(self.url + "Logout", headers=headers)
        self.logger.info("Logout Successful")

    def __xml_update_element(self, xml, xpath, value):
        element = xml.find(xpath)
        element.text = value
        return xml

    def __xml_add_element(self, xml, xpath, child, value):
        parent = xml.find(xpath)
        element = ET.Element(child)
        element.text = value
        # element.tail = '\n\t'
        parent.append(element)
        return xml

#if __name__ == '__main__':
#    abc = RestAPI("admin", "ShuXun@123456")
#    abc.login("192.168.56.101")
#    abc.createsubclient("appname", "client", "sub", "sotrage")
#    abc.logout()
