from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

import pathlib
import dateutil
import time

def auth_drive():
    auth.authenticate_user()
    gauth = GoogleAuth()
    gauth.credentials = GoogleCredentials.get_application_default()
    return GoogleDrive(gauth)

def file_title_list(just_root=False):
    drive = auth_drive()

    req = "trashed=false"
    if just_root :
        req +=  "and 'root' in parents"

    listFiles = drive.ListFile({'q': req}).GetList()
    return [l.get('title') for l in listFiles]

def get_file(name,check=True):
    drive = auth_drive()

    file_want_list = drive.ListFile({'q': "trashed=false and title='" + name + "'"}).GetList()

    if file_want_list.count == 0 :
        print(f'Failure : No file with this name')
        raise ValueError
    addtxt = ""
    idx = 0
    if len(file_want_list) > 1 : # Many files with the same name, the newest is take
        addtxt = f' : Many files with the same name, the newest is take'
        max = file_want_list[0].get("modifiedDate")
        for i in range(1,len(file_want_list)) :
            if file_want_list[i].get("modifiedDate") > max:
                max = file_want_list[i].get("modifiedDate")
                idx = i

    if check :
        path = pathlib.Path(name)
        if path.exists() :
            date_drive = dateutil.parser.parse(file_want_list[idx].get("modifiedDate"))
            date_local = dateutil.parser.parse(time.ctime(path.stat().st_mtime))

            if date_drive.ctime() <= date_local.ctime() :
                print(f"allready get")
                return # file already in, no download
    print(f"file downloaded  {addtxt}")
    file_want_list[0].GetContentFile(name)
