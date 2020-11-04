# Import included libraries
import urllib.request as dlurl
from os import path
from json import loads

# Get latest released version
try: resp = dlurl.urlopen('https://api.github.com/repos/Vianpyro/NSI-saints-days-game-project/releases/latest')
except:
    input('Unable to connect to web page, please check your internet connection.')
    quit()

resp = dlurl.urlopen('https://api.github.com/repos/Vianpyro/NSI-saints-days-game-project/releases/latest')
data = loads(resp.read())
version = data['html_url'].split('/')[-1]

# Download the latest version
if not path.exists(f'{version}.zip'):
    dlurl.urlretrieve(
        f'https://github.com/Vianpyro/NSI-saints-days-game-project/archive/{version}.zip', 
        f'{version}.zip'
    )
