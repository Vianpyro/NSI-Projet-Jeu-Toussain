# Import included libraries
import urllib.request as dlurl
from os import path
from json import loads
from zipfile import ZipFile

# Get latest released version
try: resp = dlurl.urlopen('https://api.github.com/repos/Vianpyro/NSI-saints-days-game-project/releases/latest')
except:
    print('Unable to connect to web page, please check your internet connection.')
    quit()

data = loads(resp.read())
version = data['html_url'].split('/')[-1]

# Download the latest version
if path.exists(f'{version}.zip'):
    print(f'Your game is running on the latest release ({version})!')
else:
    if __name__ == "__main__":
        print(f'Downloading {version}...')
        dlurl.urlretrieve(
            f'https://github.com/Vianpyro/NSI-saints-days-game-project/archive/{version}.zip', 
            f'{version}.zip'
        )
        print(f'Downloaded {version} successfully.')

        if not path.exists(f'NSI-saints-days-game-project-{version[1:]}'):
            print(f'Extracting {version}...')
            with ZipFile(f'{version}.zip', 'r') as zipf:
                zipf.extractall()
                zipf.close()
                print(f'Extracted {version} successfully.')
    else:
        print(f"Une nouvelle version est peut être disponible : {version}, utilisez l'updater pour télécharger la dernière version!")
        print(f'A new version may be available: {version}, use the updater to download the latest version!')
