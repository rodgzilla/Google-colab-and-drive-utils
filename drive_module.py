from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

import pathlib
import dateutil
import time

def auth_drive():
    """
    Get authentication for Google drive.
    """
    auth.authenticate_user()
    gauth = GoogleAuth()
    gauth.credentials = GoogleCredentials.get_application_default()
    return GoogleDrive(gauth)

def sauv_file(fileName):
    """
    Save a file in your drive

    take the name of the file
    """
    drive = auth_drive()

    path = pathlib.Path(fileName)
    if not path.exists() :
      raise ValueError()

    file = drive.CreateFile()  
    file.SetContentFile(fileName)
    file.Upload()

def file_title_list(request="trashed=false"):
    """
    Get list of all files on this drive account.

    (option: you can choose the request
    like : "trashed=false and 'root' in parents"
    to have only the files in the root)
    """
    drive = auth_drive()

    listFiles = drive.ListFile({'q': request}).GetList()
    return [l.get('title') for l in listFiles]

def get_file(name,check=True):
    """
    Get a file by name.
    you can't get a file which is in your drive trash
    
    (option: set check to False download the file even if the local version is the newest)
    """
    drive = auth_drive()

    file_want_list = drive.ListFile({'q': "trashed=false and title='" + name + "'"}).GetList()
    
    if len(file_want_list) == 0 :
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
            date_drive = date_drive.replace(tzinfo=None)
            if date_drive <= date_local :
                print(f"file already get")
                return # file already in, no download
    
    file_want_list[0].GetContentFile(name)
    print(f"file downloaded  {addtxt}")
