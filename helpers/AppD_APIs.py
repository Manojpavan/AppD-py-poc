##################################################################################################
##	Script Name:	Appdynamics Application Action Suppression                                  ##
##	Author:			Manoj Pavan Kumar Ponnapalli (ACCWNZZ)                                      ##
##	Version:		v1.0                                                                        ##
##                                                                                              ##
##	Purpose:                                                                                    ##
##		Suppress the alerts/emails for a list of applications specified in the excel.           ##
##                                                                                              ##
##	Refer to the user guide for more details                                                    ##
##################################################################################################
from botbuilder.dialogs.prompts import (
    TextPrompt,
    NumberPrompt,
    ChoicePrompt,
    ConfirmPrompt,
    AttachmentPrompt,
    PromptOptions,
    PromptValidatorContext,
)
from botbuilder.dialogs.choices import Choice

from distutils.log import error
from requests.auth import HTTPProxyAuth
import requests # POST/GET API Calls
import os #Script location
import sys #Error handling
import json # Convert payload to JSON
import tkinter as tk # GUI 
from tkinter import Scrollbar, ttk # Scrollbar functions
import xml.etree.ElementTree as ET # XML parsin
import pandas as pd # Read excel
import datetime # Current Time
import urllib # Get Proxies
import re


def definitions():
    global Suppression_baseURL,get_baseURL,oauth_baseURL,get_db_baseURL
    #Action Suppression URI
    Suppression_baseURL="https://cognizant-3m-nonprod.saas.appdynamics.com/controller/alerting/rest/v1/applications/"
    #App ID URI
    get_baseURL="https://cognizant-3m-nonprod.saas.appdynamics.com/controller/rest/applications/"
    #AccessToken URI
    oauth_baseURL="https://cognizant-3m-nonprod.saas.appdynamics.com/controller/"
    get_db_baseURL="https://cognizant-3m-nonprod.saas.appdynamics.com/controller/rest/databases/"
    print("Base URLs Set \n")
    
def set_file():
    global file,script_location
    # Get script location
    script_location=os.path.realpath(os.path.dirname(__file__))
    print("Script Execution Started \n")
    

    
def set_proxy(): 
    global proxies,certificate_path
    print("Inside set_proxy")
    proxies = urllib.request.getproxies() # Get proxies if any
    print(len(proxies))

    if(len(proxies)>0): # Based on proxy length , parameters are defined
        print("Proxy Detected \n")
        proxy_value=proxies.get("http")
        if(proxy_value.find("cognizant")):
            certificate_path=script_location+"\COGNIZANT ROOT CA_wifi.crt"
        else:
            certificate_path=script_location+"\3M_Non_Prod.crt"
    else:
        print("No Proxy found \n")
        certificate_path=False
        

def set_headers():
    global post_headers,get_headers
    #Headers of Action Suppression POST Call
    post_headers = {
    'Accept': "application/json",
    'Content-Type': "application/json",
    'Authorization': "Bearer "+access_key
    }
    #Headers of Get Application ID GET Call
    get_headers = {
    'Authorization': "Bearer "+access_key
    }
    
    print("Headers set for the API Call \n")
    


def get_id(AppName):
    #global app_id
    #Firing the API to retrieve App ID
    response = requests.get(get_baseURL+AppName, headers=get_headers,verify=certificate_path,proxies=proxies)
    #Error handling
    
    
    if response.status_code == 200:
        print("Retreived App ID successfully \n")
        
        #Convert the XML response to string format
        root = ET.fromstring(response.text)
        #Iterate based on the word application to find id and name of application
        for application in root.findall("./application"):
            app_id = application.find("id").text
            app_name = application.find("name").text
            print("ID of "+app_name +" is "+app_id+"\n")
            return(app_id)
            
    else :
        print("Unable to get Application ID")
        return(error)
    
    
     

def get_access_token():
    global access_key
    #Client_secret and client_id are used to generate access_token- DON'T CHANGE
    client_secret="3640b05e-d7a9-44d5-a46d-c250b9a3e5b8"
    client_id="Action_Suppression_Automation"
    headers ={
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = "grant_type=client_credentials&client_id="+client_id+"@cognizant-3m-nonprod&client_secret="+client_secret
    #print(script_location+"\DigiCert_Global_Root_CA_Chain.crt")
    
    response=requests.post(oauth_baseURL+"/api/oauth/access_token",headers=headers,data=payload,verify=certificate_path,proxies=proxies)
    
    if(response.text==''):
        print("Unable to generate access token")
        
    #Save the JSON into string and get the access token using split
    oauth_output=response.text
    split_result=str.split(oauth_output,"\"")
    
    access_key=split_result[3]
    print(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S") +"Retrieved Access Token Successfully\n")
    

def violations(app):
    global app_id
    definitions()
    set_proxy()
    get_access_token()
    set_headers()    
    app_id=get_id(app)
    if(app_id==error):
        return("Please enter correct application name")
    else:
        pass
 

#http://cognizant-3m-nonprod.saas.appdynamics.com/controller/rest/applications/4250/problems/healthrule-violations?time-range-type=BEFORE_NOW&duration-in-mins=15    
    response = requests.get("http://cognizant-3m-nonprod.saas.appdynamics.com/controller/rest/applications/"+app_id+"/problems/healthrule-violations?time-range-type=BEFORE_NOW&duration-in-mins=15", headers=get_headers)
    #print (response.text)
    #print(len(response.text))
    #print(type(response.text))


    if response.status_code == 200:
        print("Retreived App Details successfully \n")
        
        if(len(response.text)<40):
            message_text=f"No ongoing Policy violations for "+app
            #print(message_text+"in here")
            return(message_text)
            
        else:
            
            #Convert the XML response to string format
            root = ET.fromstring(response.text)
             #Iterate based on the word application to find id and name of application
            for application in root.findall("./policy-violation"):
                    app_id = application.find("id").text
                    policy_name = application.find("name").text
                    deepLinkUrl = application.find("deepLinkUrl").text
                    severity=application.find("severity").text
                    description=application.find("description").text
                    print(app_id,policy_name,deepLinkUrl)
                    print("One Policy violation found with below details")
                    print("Violating Policy is "+policy_name)
                    print("Severity "+severity)
                    description = re.sub('<.*?>', '', description)
                    print("Description "+description)

                    message_text="Found violating policy \n\n Policy name is \""+policy_name +"\"\n\nSeverity as "+severity+"\n\nDescription:: "+description+"\n\nURL "+deepLinkUrl
            return(message_text)


def get_app_list():

    #class Choice:
     #   def __init__(self, title, action):
      #      self.title = title
       #     self.action = action
    definitions()
    set_proxy()
    get_access_token()
    set_headers()
    response = requests.get(get_baseURL, headers=get_headers)
    #print(response.text)
    if response.status_code == 200:
    # Parse the XML data
        app_list=[]
        root = ET.fromstring(response.text)
        for application in root.findall("./application"):
            #app_id = application.find("id").text
            app_name = application.find("name").text
            #print(app_name)
            #app_list=app_name+" "+app_list
            app_list.append(app_name)
        #for choice in app_list:
        #    print(app_list)
        return(app_list)
    else:
        error

#get_app_list()

def get_db_list():
    global db_list
    #class Choice:
     #   def __init__(self, title, action):
      #      self.title = title
       #     self.action = action
    definitions()
    set_proxy()
    get_access_token()
    set_headers()
    response = requests.get(get_db_baseURL+"servers", headers=get_headers)
    print("result")
    #print(response.text)
    print(type(response))
    #print(response.text)
    if response.status_code == 200:
    # Parse the JSON data
        print("inside if")
        db_response=json.loads(response.text)
        #print(db_response)
        db_list=[]
        db_names_list=[]
        #root = ET.fromstring(response.text)
        for item in db_response:
            db_name=item["name"]
            db_id=item["id"]
            db_list.append([db_name,db_id])
            db_names_list.append(db_name)
        print(type(db_name))
        print(type(db_names_list))
        #print(db_names_list)
        #print(db_name)
        return(db_names_list)
        #print(db_list)
    else:
        error

#get_db_list()

def violations_db(db_name):
    global app_id
    definitions()
    set_proxy()
    get_access_token()
    set_headers()
    
    for item in db_list:
        if(item[0]==db_name):
            db_id=item[1]
    print(db_id)
        
    #db_id=get_id(db_name)
    if(db_id==error):
        return("Please enter correct DB name")
    else:
        pass
 

#http://cognizant-3m-nonprod.saas.appdynamics.com/controller/rest/applications/4250/problems/healthrule-violations?time-range-type=BEFORE_NOW&duration-in-mins=15    
    response = requests.get("http://cognizant-3m-nonprod.saas.appdynamics.com/controller/rest/databases/servers/healthrule-violations/"+str(db_id)+"?time-range-type=BEFORE_NOW&duration-in-mins=60", headers=get_headers)
                            #https://cognizant-3m-nonprod.saas.appdynamics.com/controller/rest/databases/servers/healthrule-violations/UR5DB?time-range-type=BEFORE_NOW&duration-in-mins=60
    print (response.text)
    print(len(response.text))
    print(type(response.text))


    if response.status_code == 200:
        print("Retreived App Details successfully \n")
        print(len(response.text))
        print(response.text)
        if(len(response.text)<40):
            message_text=f"No ongoing Policy violations for "+db_name
            #print(message_text+"in here")
            return(message_text)
            
        else:
            
            #Convert the XML response to string format
            root = ET.fromstring(response.text)
             #Iterate based on the word application to find id and name of application
            for application in root.findall("./policy-violation"):
                    app_id = application.find("id").text
                    policy_name = application.find("name").text
                    deepLinkUrl = application.find("deepLinkUrl").text
                    severity=application.find("severity").text
                    description=application.find("description").text
                    print(app_id,policy_name,deepLinkUrl)
                    print("One Policy violation found with below details")
                    print("Violating Policy is "+policy_name)
                    print("Severity "+severity)
                    description = re.sub('<.*?>', '', description)
                    print("Description "+description)

                    message_text="Found violating policy \n\n Policy name is \""+policy_name +"\"\n\nSeverity as "+severity+"\n\nDescription:: "+description+"\n\nURL "+deepLinkUrl
            return(message_text)

#get_db_list()
#violations_db("WM - btbiaq1")