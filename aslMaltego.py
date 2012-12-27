'''
@author: libresec
'''
import suds, sys, time
from suds.xsd.doctor import Import, ImportDoctor
from datetime import datetime, timedelta

def getLoggerClient():
    
    try:
        conf = open('aslMaltego.conf', 'r')
        config = conf.readlines()
        conf.close()
        
        for line in config:
            try:
                if 'ASLSERVER' in line:
                    server_list = line.strip().split('=')
                    server = str(server_list[1]).lstrip("'").rstrip("'")
            except:
                errors(3)
    except:
        errors(3)
    
    login_wsdl_url = server+"/soap/services/LoginService/LoginService.wsdl"
    search_wsdl_url = server+"/soap/services/SearchService/SearchService.wsdl"
    schema_url = "http://www.arcsight.com/logger/xsd"
    namespace = 'http://domain.login.webservices.logger.arcsight.com/xsd'
    namespace2 = 'http://domain.search.webservices.logger.arcsight.com/xsd'
    schema_import = Import(schema_url)
    schema_import.filter.add(namespace)
    schema_import.filter.add(namespace2)
    schema_doctor = ImportDoctor(schema_import)
    
    try:
        session_client = suds.client.Client(url=login_wsdl_url, doctor=schema_doctor, location=login_wsdl_url)
        cookie = getLoggerSession(session_client)
        search_client = suds.client.Client(url=search_wsdl_url, doctor=schema_doctor, location=search_wsdl_url)
        
        return session_client, cookie, search_client
    except:
        errors(1)

def getLoggerSession(client): 
    
    try:
        #open config file to grab server, username, and password
        conf = open('aslMaltego.conf', 'r')
        config = conf.readlines()
        conf.close()
    
        for line in config:
                if 'USERNAME' in line:
                    usr_list = line.strip().split('=')
                    username = str(usr_list[1]).lstrip("'").rstrip("'")
        
                elif 'PASSWORD' in line:
                    passwd_list = line.strip().split('=')
                    password = str(passwd_list[1]).lstrip("'").rstrip("'")
        
        try:
            cookie = client.service.login(username, password)
            return cookie
        except:
            errors(1)
    except:
        errors(3)

def loggerLogout(client, cookie):

    try:
        client.service.logout(cookie)
    except:
        errors(1)

def loggerSearch(clientIn, cookie, queryIn):
    #search timeframe
    start = int(time.mktime((datetime.now() - timedelta(minutes=800)).timetuple())) * 1000
    end = int(time.mktime((datetime.now()).timetuple())) * 1000
    
    #starts the search
    clientIn.service.startSearch(queryIn, start, end, cookie)
    
    #check for search results
    result_set = []
    while clientIn.service.hasMoreTuples(cookie):
        results = clientIn.service.getNextTuples(20, 8000, cookie)
        for item in results:
            result_set.append(item[0])
    
    #end current search
    clientIn.service.endSearch(cookie)
    
    return result_set
        
def errors(typeIn):
     
    if typeIn == 1:
        text = "Network connection is down or Logger is not responding."
    elif typeIn == 2:
        text = "Logger did not return any results. Check your input."
    elif typeIn == 3:
        text = "Something is wrong with your aslMaltego.conf file."
            
    print "<MaltegoMessage>\n<MaltegoTransformResponseMessage>"
    print "   <Entities>"
    print "   </Entities>"
    print "   <UIMessages>"
    print "       <UIMessage MessageType=\"PartialError\">%s</UIMessage>" % text
    print "   </UIMessages>"
    print "</MaltegoTransformResponseMessage>\n</MaltegoMessage>"
    
    sys.exit(0)

