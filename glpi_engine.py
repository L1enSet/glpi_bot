import asyncio
import requests
import json
from dotenv import load_dotenv
import os

from errors import GlpiAuthError, GlpiSessionError


load_dotenv()
ADMIN_USER_TOKEN = os.getenv('ADMIN_USER_TOKEN')


class AppMixin():
    ssl = "https://"
    URL_INIT = ssl+"helpdesk.ics.perm.ru/apirest.php/initSession"
    URL_KILL = ssl+"helpdesk.ics.perm.ru/apirest.php/killSession"
    URL_GET_USER = ssl+"helpdesk.itsperm.ru/apirest.php/User/"
    HEADERS = {"Content-Type":"application/json",}


class Session(AppMixin):
    
    def __init__(self, user_token):
        self.user_token = user_token
        self.session_token = None


    def initSession(self):
        """
        USER AUTHORIZATION AND START SESSION FOR WORK WITH SESSIONS
        PARAMS url, user_token(settings/api token in glpi)
        RETURN session_token"""
        
        request_headers = self.HEADERS
        request_headers["Authorization"] = "user_token {}".format(self.user_token)
        
        response = requests.get(url=self.URL_INIT,
                                headers=request_headers,
                                )
        
        if response.status_code == 200:
            self.session_token = json.loads(response.text)['session_token']
            return self.session_token
        
        else:
            raise GlpiAuthError(str(response.text))
    
    def killSession(self):
        request_headers = self.HEADERS
        request_headers["Session-Token"] = self.session_token
        
        response = requests.get(url=self.URL_KILL,
                                headers=request_headers)
        
        if response.status_code == 200:
            self.session_token = None
            return response.status_code
        else:
            raise GlpiSessionError(str(response.text))


def searchUser(username, request_headers):
    request_headers['name'] = username
    url = "https://helpdesk.itsperm.ru/apirest.php/search/User?is_deleted=0&as_map=0&browse=0&criteria[0][link]=AND&criteria[0][field]=1&criteria[0][searchtype]=contains&criteria[0][value]={}&itemtype=User&start=0&_glpi_csrf_token=3cea1b10a52338584999fdce55691f4ed67f29fa6d87689867f626e25d662d33&sort[]=1&order[]=ASC".format(username)
    response = requests.get(url=url, headers=request_headers)
    if response.status_code == 200:
        json_data = json.loads(response.text)
        if json_data['count'] > 0:
            user_id = json_data['data'][0]['2']
        else:
            user_id = "not_found"
    elif response.status_code == 400:
        raise GlpiSessionError
    else:
        user_id = "error"
    print(user_id)
    return user_id
        
    
    
def parseJsonData(data):
    result = {}
    #result['id'] = data['id']
    result['glpi_name'] = data['name']
    result['surname'] = data['realname']
    result['name'] = data['firstname'].split(" ")[0]
    result['patronymic'] = data['firstname'].split(" ")[1]
    #result['phone'] = data['phone']
    #result['mobile'] = data['mobile']
    
    return result


def getUser(username):
    session = Session(ADMIN_USER_TOKEN)
    try:
        session.initSession()
    except GlpiAuthError as exc:
        return {'status': "autherror"}
    
    
    request_headers = AppMixin.HEADERS
    request_headers["Session-Token"] = session.session_token
    
    try:    
        user_id = searchUser(username, request_headers)
    except GlpiSessionError as exc:
        session = Session(ADMIN_USER_TOKEN)
        session.initSession()
        request_headers["Session-Token"] = session.session_token
        user_id = searchUser(username, request_headers)
    
    
    if user_id != "not_found" and user_id != "error":
        response = requests.get(url=AppMixin.URL_GET_USER+str(user_id), headers=request_headers)
        if response.status_code == 200:
            user_data = parseJsonData(json.loads(response.text))
        elif response.status_code == 400:
            raise GlpiSessionError
    else:
        user_data = {"error": user_id}      
    
    session.killSession()
    return user_data
    

