#!/usr/bin/python3
# author: John Owens
# created: 2017-01-17
# description: python script to backup and then download jira and confluence. Loosely based on
# https://bitbucket.org/atlassianlabs/automatic-cloud-backup/src/8d33935dcb6af56ca79b4db3ff012c8c7982e356/backup.sh?at=master&fileviewer=file-view-default

import requests, json
from time import sleep
import sys
import os
import urllib
import os.path
import datetime

#vars
location = '/tmp'

timezone = ''

backupUrl = '/rest/obm/1.0/runbackup'
sessionUrl = '/rest/auth/1/session'
progressUrl =  '/rest/obm/1.0/getprogress.json'

#session stuff
def setup(instance, username, password):
    global jiraUrl
    global confluenceUrl
    jiraUrl = 'https://%s' % instance
    confluenceUrl = 'https://%s' % instance + '/wiki'

    session = requests.Session()
    session.auth = (username, password)
    session.headers.update({'Content-Type': 'application/json'})

    cookies = session.get(jiraUrl + sessionUrl)
    print(cookies.text)
    return session

#start back up process
def startBackup(url, lSession):
    headers = {'content-type': 'application/json', 'X-Atlassian-Token': 'no-chec', 'X-Requested-With': 'XMLHttpRequest'}
    r = lSession.post(url, data='{"cbAttachments":"true" }', headers=headers)
    print(r)
    return r.status_code

#CHECK IF failed

#CHECK Progress
def checkBackupProgress(url, s):

    for num in range(0,20): #try 20 times
        response = s.get(url)
        rJson = response.text
        print(rJson)
        rDict = json.loads(rJson)
        print(rDict['currentStatus'])
        #assume a Exporting
        if 'Exporting' in rDict['currentStatus'] or 'fileName' not in rDict:
            print("Still exporting, sleeping for 60 seconds..")
            sleep(60)
        else:
            print("Done exporting, continue")
            return rDict['fileName']
            break
    return None

def getBackupFile(fileUrl,lSession,fileRename):
    fileName = ''
    if fileRename is None or fileRename == '':
        fileNameA = os.path.splitext(os.path.basename(urllib.parse.urlsplit(fileUrl).path))
        print(fileNameA[0])
        fileName = fileNameA[0] + fileNameA[1]
    else:
        fileName = fileRename

    r = lSession.get(fileUrl, stream = True)

    if r.status_code == 200:
        with open(fileName, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
    return ''

#Do confluence specific stuff here
def siteBackupConfluence(url, lSession):
    result = startBackup(url + backupUrl, lSession)
    fileName = checkBackupProgress(url + progressUrl, lSession)
    print(fileName)
    if fileName is not None:
        #default filename is weird
        now = datetime.datetime.now()
        fileRename = 'Site_Backup - ' + str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '.zip'
        #there's no slash or download in the returned file url, but there is when you check the site page, go figure..
        getBackupFile(url + '/download/' + fileName, lSession,fileRename)

#Do jira specific stuff here
def siteBackupJira(url, lSession):
    result = startBackup(url + backupUrl, lSession)
    fileName = checkBackupProgress(url + progressUrl, lSession)
    print(fileName)
    if fileName is not None:
        getBackupFile(url + fileName, lSession,None)

def runBackup(instance, username, password, backupLocation, backupType):
    print("Instance is: " + instance)
    session = setup(instance, username, password)
    location = backupLocation

    if backupType == 'jira':
        siteBackupJira(jiraUrl, session)
    elif backupType == 'confluence':
        siteBackupConfluence(confluenceUrl, session)
    elif backupType == 'both':
        siteBackupJira(jiraUrl, session)
        siteBackupConfluence(confluenceUrl, session)
    else:
        print("Do nothing..")
