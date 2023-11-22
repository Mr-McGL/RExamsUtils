# -*- coding: utf-8 -*-

#ToDo:
# * DocStrings
# * Requirements
# * add fprnt
# * private imports


from ..ex import run
from ..types import find_dict

from pydrive.auth         import GoogleAuth       
from pydrive.drive        import GoogleDrive      
from google.colab         import auth             
from oauth2client.client  import GoogleCredentials

import requests
import json
from os.path    import isdir
from os         import getcwd, chdir,makedirs

def getRepoName(url):
  end = url.rfind(".git")
  start = url[0:end].rfind("/")
  return url[start+1:end]

def addTokenToURL(url,token,user = None):
  splitted_url = url.split('//')
  tail = '//'.join(splitted_url[1:])
  if user is None:
    return f"{splitted_url[0]}//{token}@{tail}"
  else:
    return f"{splitted_url[0]}//{user}:{token}@{tail}"
  
def getTokensFromGDrive(tokneFileID):
  auth.authenticate_user()
  gauth = GoogleAuth()
  gauth.credentials = GoogleCredentials.get_application_default()
  drive = GoogleDrive(gauth)

  tokenFile = drive.CreateFile({'id': tokneFileID})
  return json.loads(tokenFile.GetContentString())

def addTokenFromGDriveToURL(url, tokenFileID, tokenName = "gitlab"):
  tokens = getTokensFromGDrive(tokenFileID)
  return addTokenToURL(url, tokens[tokenName]['token'], 
                       tokens[tokenName]['user'])

def pipInstallRepo(url, tokenFileID, tokenName="gitlab"):
  accessURL = addTokenFromGDriveToURL(url, tokenFileID, tokenName)
  run(f"pip install git+{accessURL}")

def cloneRepo(url, tokenFileID, tokenName="gitlab", folder = "", safe = True):
  accessURL = addTokenFromGDriveToURL(url, tokenFileID, tokenName)
  run(f"git clone --recurse-submodules {accessURL} {folder}")

  if safe:
    fldr =  getRepoName(url) if folder == "" else folder
    setRemoteURL(url, folder = fldr)

def setAccessURL(url, tokenFileID, tokenName="gitlab", remote = 'origin', folder = "."):
  accessURL = addTokenFromGDriveToURL(url, tokenFileID, tokenName)
  _changeFolderAndRun(_setRemoteURL, accessURL, folder = folder, remote = remote)
  
def setRemoteURL(url, remote = 'origin', folder= "."):  
  _changeFolderAndRun(_setRemoteURL, url, folder = folder, remote = remote)

def removeRemote(remote, folder= "."):
  _changeFolderAndRun(_removeRemote, remote, folder = folder)

def _setRemoteURL(url, remote = 'origin'):
  #remote_exist = !git remote -v | grep remote
  remotes = run(f"git remote", lst = True)
  if remote in remotes:
    run(f"git remote set-url {remote} {url}")
  else:
    run(f"git remote add {remote} {url}") 

def _removeRemote(remote):
  remotes = run(f"git remote", lst = True)
  if remote in remotes:
    run(f"git remote remove {remote}")
  else:
    print("\x1b[1m\x1b[3m\x1b[4m\x1b[31mError!!!\x1b[0m", end = ' ')
    print(f"\x1b[31mRemote not found({remote}).\x1b[0m", flush = True)
    raise AssertionError(f"Error: Remote not found ({remote})") 

def _changeFolderAndRun(func, *args, folder = ".",**kwargs):
  if not isdir(folder): 
    print("\x1b[31m\x1b[1m\x1b[3m\x1b[4mError!!!\x1b[0m", end = ' ')
    print(f"\x1b[31mRepo forder not found ({folder}).\x1b[0m", flush=True)
    raise FileNotFoundError(f"Error: repo folder not found ({folder})") 
  
  currentFolder = getcwd()
  chdir(folder)
  func(*args, **kwargs)
  chdir(currentFolder)


  ####################################################


def download_git_file(user: str, repo: str, repo_folder: str, name: str,
                        server: str = "github.com",
                        branch: str = "main",
                        folder: str | None = None):
  """Download a file from a Git repository hosted on a Git server.

  This function allows you to download a specific file from a Git repository
  hosted on a Git server. You can specify the user, repository name, repository
  folder, file name, and other optional parameters.

  Parameters:
      user (str): The username or organization name that owns the Git repository.
      repo (str): The name of the Git repository.
      repo_folder (str): The path to the folder in the repository where the file is located.
      name (str): The name of the file to download.
      server (str, optional): The Git server hostname. Default is "github.com".
      branch (str, optional): The Git branch where the file is located. Default is "main".
      folder (str | None, optional): The local folder where the file will be saved.
          If None, the file is saved in the current working directory. Default is None.

  Raises:
      RequestException: If the file retrieval fails.

  Usage:
      download_git_file("username", "repository_name", "folder/path", "file.txt")
  """

  if folder is None: folder = "."

  file_url = f"https://{server}/{user}/{repo}/raw/{branch}/{repo_folder}/{name}"

  resp = requests.get(file_url)
  if resp.status_code != 200:
    raise requests.exceptions.RequestException(
      f"Failed to retrieve file ({repo_folder}/{name}). Status code: {resp.status_code}")

  with open(f"{folder}/{name}","wb") as f:
    f.write(resp.content)

#---
    
def download_git_folder(user: str, repo: str, repo_folder: str,
                        server: str = "github.com",
                        branch: str = "main",
                        folder: str | None = None):
  """Download all files from a folder in a Git repository hosted on a Git server.

  This function allows you to download all the files from a specific folder in
  a Git repository hosted on a Git server. You can specify the user, repository
  name, repository folder, and other optional parameters. The folders will
  be added to the path.

  Parameters:
      user (str): The username or organization name that owns the Git repository.
      repo (str): The name of the Git repository.
      repo_folder (str): The path to the folder in the repository to download.
      server (str, optional): The Git server hostname. Default is "github.com".
      branch (str, optional): The Git branch where the folder is located. Default is "main".
      folder (str | None, optional): The local folder where the files will be saved.
          If None, the files are saved in the current working directory. Default is None.

  Raises:
      RequestException: If the folder retrieval fails.

  Usage:
      download_git_folder("username", "repository_name", "folder/path")
  """

  if folder is None: folder = "."

  folder_url = f"https://{server}/{user}/{repo}/blob/{branch}/{repo_folder}"

  resp = requests.get(folder_url)
  if resp.status_code != 200:
      raise requests.exceptions.RequestException(
        f"Failed to retrieve folder({repo_folder}). Status code: {resp.status_code}")

  items = json.loads(resp.content)["payload"]["tree"]["items"]

  makedirs(folder, exist_ok=True)
  for item in items:
    if item['contentType'] == 'file':

      download_git_file(user, repo, repo_folder, item['name'],
                        server = server, branch = branch, folder = folder)
#############################
# QD
#############################
    elif item['contentType'] == 'symlink_file':
      repo_url = f"https://{server}/{user}/{repo}/blob/{branch}"
      symlink_url = f"{repo_url}/{repo_folder}/{item['name']}"

      resp = requests.get(symlink_url)
      if resp.status_code != 200:
        raise requests.exceptions.RequestException(
          f"Failed to retrieve folder({repo_folder}). Status code: {resp.status_code}")


      path = json.loads(resp.content)["payload"]["blob"]['rawLines'][0].split('/')
      folder_list = repo_folder.split('/')

      for  p in path[:-1]:
        if p == "..":
          if not folder_list: raise requests.exceptions.RequestException(f"SYMLINK ERROR")
          folder_list.pop()
        else:
          folder_list.append(p)

        if folder_list:
          resp = requests.get(f"{repo_url}/{'/'.join(folder_list)}")

          if resp.status_code != 200:
            if len(folder_list) == 1:
              resp = requests.get(f'{repo_url.replace("blob", "tree")}') #ToDo la dirección no puede contener blob!
            else:
              resp = requests.get(f"{repo_url}/{'/'.join(folder_list[:-1])}")

            item = find_dict(json.loads(resp.content)["payload"]["tree"]["items"], 'name', folder_list[-1])
            if not item: raise requests.exceptions.RequestException(f"SYMLINK ERROR")
            if item["contentType"]!='submodule': raise requests.exceptions.RequestException(f"SYMLINK ERROR")

            #ToDo: no puede contener la palabra tree
            repo_url_list = item["submoduleUrl"].split("/")
            repo_url_list.insert(-1,"blob")
            repo_url = "/".join(repo_url_list)
            folder_list = []

      if folder_list:
        file_url = f"{repo_url}/{'/'.join(folder_list)}/{path[-1]}"
      else:
        file_url = f"{repo_url}/{path[-1]}"

      
      resp = requests.get(file_url.replace("blob","raw"))
      if resp.status_code != 200:
        raise requests.exceptions.RequestException(
          f"Failed to retrieve file ({repo_folder}/{name}). Status code: {resp.status_code}")

      with open(f"{folder}/{path[-1]}","wb") as f:
        f.write(resp.content)

    ##############################
    # ToDo: elif sublmodule
#############################
    else:
      download_git_folder(user, repo, f"{repo_folder}/{item['name']}",
                          server = server, branch = branch,
                          folder = f"{folder}/{item['name']}")
      