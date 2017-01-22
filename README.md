# atlassian-backup
backup script for jira and confluence cloud
Note: boto is for future change to upload to S3.

##
Based on the atlassian script for jira found here:https://bitbucket.org/atlassianlabs/automatic-cloud-backup/src/8d33935dcb6af56ca79b4db3ff012c8c7982e356/backup.sh?at=master&fileviewer=file-view-default

## To run
Run the atlassian-run.py script. Recommend using python3, might work with 2.
``` shell
python3 atlassian-run.py -i <instance> -u username -p password -l /tmp -b jira
python3 atlassian-run.py -i <instance> -u username -p password -l /tmp -b confluence
python3 atlassian-run.py -i <instance> -u username -p password -l /tmp -b both
#example: python3 atlassian-run.py -i blah.atlassian.net -u john -p smith -l /tmp -b jira
```

## TODO
* Add logger
* Implement S3 uploading option
* use location - need make sure win/nix paths handled. Currently just downloads to script execution location
