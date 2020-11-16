# Import included libraries
import urllib.request as dlurl
from os import path, remove
from json import loads
from zipfile import ZipFile

# Parameters
auto_update = True
auto_download = True
github_user = 'Vianpyro'
github_repo = 'NSI-saints-days-game-project'

source_website = 'https://api.github.com'

# Updater parameters (Don't change this if you want to be aware of published updates)
updater_auto_update = True
updater_auto_download = True
updater_user = 'Vianpyro'
updater_repo = 'Python-Updater'

# Program variable (for imports)
up_to_date = False
latest_version = ''
updater_up_to_date = False
updater_latest_version = ''

# Creation of a list containing the variables in order to be able to process "easily" the link(s) to be processed
parameters = [
    [auto_update, auto_download, github_user, github_repo],
    [updater_auto_update, updater_auto_download, updater_user, updater_repo]
]

for i in range(len(parameters)):
    # Searching for the latest version if the program is set to auto update
    if parameters[i][0]:
        try:
            resp = dlurl.urlopen(
                f'{source_website}/repos/{parameters[i][2]}/{parameters[i][3]}/releases/latest'
            )
            data = loads(resp.read())
            name = data['name']
            version = data['html_url'].split('/')[-1]

            if parameters[i][3] == updater_repo: updater_latest_version = version
            else: latest_version = version

            if parameters[i][1]:
                if path.exists(f'{name}.zip') or path.exists(f'{parameters[i][3]}-{version}') or path.exists(f'{parameters[i][3]}-{version[1:]}'):
                    if parameters[i][3] == updater_repo: updater_up_to_date = True
                    else: up_to_date = True
                    print(f'{parameters[i][2]}/{parameters[i][3]} is already running on the most recent version: {name}!')
                elif __name__ == "__main__":
                    try:
                        print(f'Downloading {parameters[i][3]} {name}...')
                        dlurl.urlretrieve(
                            f'https://github.com/{parameters[i][2]}/{parameters[i][3]}/archive/{version}.zip',
                            f'{parameters[i][3]} {name}.zip'
                        )
                        print(f'Downloaded {parameters[i][3]} {name} successfully.')
                    except:
                        print(
                            f'Could not download {source_website}/{parameters[i][2]}/{parameters[i][3]}/archive/{version}.zip'
                        )
                    
                    try:
                        if not path.exists(f'{github_repo}-{version}'):
                            print(f'Extracting {parameters[i][3]} {name}...')
                            with ZipFile(f'{parameters[i][3]} {name}.zip', 'r') as zipf:
                                zipf.extractall()
                                zipf.close()
                                remove(f'{parameters[i][3]} {name}.zip')
                                print(f'Extracted {parameters[i][3]} {name} successfully.')
                    except:
                        print(
                            f'Could not extract {name}.'
                        )
                else:
                    print(
                        f'A new version of {parameters[i][2]}/{parameters[i][3]} may be available: {name}.'
                    )
        except: 
            print(
                f'Unable to locate package: "{source_website}/repos/{parameters[i][2]}/{parameters[i][3]}/releases/latest"...'
            )
    if updater_user == github_user and updater_repo == github_repo and __name__ == "__main__":
        quit()
