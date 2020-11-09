# Import included libraries
import urllib.request as dlurl
from os import path
from json import loads
import zipfile

# Get latest released version
try: resp = dlurl.urlopen('https://api.github.com/repos/Vianpyro/NSI-saints-days-game-project/releases/latest')
except:
    print('Unable to connect to web page, please check your internet connection.')
    quit()

resp = dlurl.urlopen('https://api.github.com/repos/Vianpyro/NSI-saints-days-game-project/releases/latest')
data = loads(resp.read())
version = data['html_url'].split('/')[-1]

# Download the latest version
if path.exists(f'{version}.zip'):
    print(f'Your game is running on the latest release ({version[1:]})!')
else:
    if __name__ == "__main__":
        dlurl.urlretrieve(
            f'https://github.com/Vianpyro/NSI-saints-days-game-project/archive/{version}.zip', 
            f'{version}.zip'
        )
        print(f'Version {version[1:]} successfully downloaded.')

        if not path.exists(f'NSI-saints-days-game-project-{version[1:]}'):
            print(f'Extracting {version}...')
            with zipfile.ZipFile(f'{version}.zip', 'r') as zipf:
                zipf.extractall()
                zipf.close()
    else:
        print(f"Une nouvelle version est peut être disponible : {version[1:]}, utilisez l'updater pour télécharger la dernière version!")
        print(f'A new version may be available: {version[1:]}, use the updater to download the latest version!')
