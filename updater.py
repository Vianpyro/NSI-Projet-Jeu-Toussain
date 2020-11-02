# Import included libraries
import urllib.request as dlurl
from os import path
from subprocess import check_call
from sys import executable

def install(package): check_call([executable, "-m", "pip", "install", package])

# Import installed libraries
try: from lxml import html
except:
    try:
        install('lxml')
        from lxml import html
    except:
        input('Unable to load the LXML library, please check that it is properly installed on this computer...')
        quit()

try: from requests import get
except:
    try:
        install('requests')
        from requests import get
    except:
        input('Unable to load the Requests library, please check that it is properly installed on this computer...')
        quit()

# Load the last online package version name
try:
    page = get('https://github.com/Vianpyro/NSI-saints-days-game-project/releases/latest')
    tree = html.fromstring(page.content)
    version = tree.xpath('/html/body/div[4]/div/main/div[2]/div/div[2]/div/div[1]/ul/li[1]/a/span/text()')[0]
except:
    input("Unable to connect to web page...")
    quit()

# Download the latest version
if not path.exists(f'{version}.zip'):
    dlurl.urlretrieve(
        f'https://github.com/Vianpyro/NSI-saints-days-game-project/archive/{version}.zip', 
        f'{version}.zip'
    )
