#!/usr/bin/python3
# author: John Owens
# created: 2017-01-17
# description: python script to backup and then download jira and confluence. Loosely based on
import sys
import getopt
import atlassianBackup

#vars
username = ''
password = ''
instance = ''
location = '/tmp' #default
backupType = 'both' #jira, confluence or both
#timezone = 'Australia/Melbourne' #maybe not needed
#Function chooser
#func_arg = {"list": apiIDFromList, "id": apiIDFromResponse, "deploymentId": getDeploymentId}

try:
  opts, args = getopt.getopt(sys.argv[1:],"i:u:p:l:b:h",["instance=","username=","password=",'location=','backupType=',"help"])
except getopt.GetoptError:
  print('atlassian-run.py -i <instance> -u <username> -p <password> -l <location> -b <backup type>');
  sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
     print('atlassian-run.py -i <instance> -u <username> -p <password> -l <location> -b <backup type>');
     sys.exit()
    elif opt in ("-i", "--instance"):
     instance = arg
    elif opt in ("-u", "--username"):
     username = arg
    elif opt in ("-p", "--password"):
     password = arg
    elif opt in ("-l", "--location"):
     location = arg
    elif opt in ("-b", "--backupType"):
     backupType = arg

if instance is None or instance == '' or username is None or username == '':
    print("exiting, instance and username not set")
    sys.exit()

atlassianBackup.runBackup(instance, username, password, location, backupType)
