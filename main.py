import time
import platform
from selenium import webdriver
import zipfile
import os


def os_checker():
    if platform.uname().system == 'Darwin':
        if platform.uname().machine == 'arm64':
            return 'Mac'
        else:
            return 'Mac'
    elif platform.uname().system == 'Windows':
        return 'Windows'
    else:
        return 'Linux'


addon_list = []  # kvp - AddonName, Website URL
if os_checker() == 'Mac':
    addon_dir = '/Applications/World of Warcraft/_retail_/Interface/AddOns/'  # directory for addons - make environment variable or hard code
    working_dir = '/tmp/tempAddonDir/'
elif os_checker() == 'Windows':
    pass # TODO: Figure out what the windows default paths are
    addon_dir = "C:\ProgramFiles(x86)\WorldofWarcraft\_retail_\Interface\AddOns\\"  # have someone check this
    working_dir = os.environ.get('HOME') + '/tempAddonDir/'
else:
    addon_dir = os.environ.get('HOME') + '/Games/world-of-warcraft/drive_c/Program Files (x86)/World of Warcraft/_retail_/Interface/AddOns/'
    working_dir = '/tmp/tempAddonDir/'


addon_list = {"name": ["DBM", "Details", "elvui", "handynotes", "weakauras"], "url": ["https://www.curseforge.com/wow/addons/omen-threat-meter/download","https://www.curseforge.com/wow/addons/deadly-boss-mods/download", "https://www.curseforge.com/wow/addons/details/download", "https://www.curseforge.com/wow/addons/handynotes/download", "https://www.curseforge.com/wow/addons/weakauras-2/download"], "version": [1964, 69]}


# TODO: Add functionality to install the Gecko Drivers to the working path

def pop_list():
    pass  # pass for now - we'll add something to parse the addon_dir and assemble addon_list in the future


def download_addon():
    if os.path.exists(working_dir):
        print('Path already exists... not creating it!')
    else:
        os.mkdir(working_dir)
    options = webdriver.FirefoxOptions()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", working_dir)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    urllist = addon_list['url']
    for url in urllist:
        driver.get(url)
        time.sleep(6)
        print("Downloaded the file from: {url}".format(url = url))

def extract_to_addon_directory(directory):
    f = []
    # Walk the working_dir return only files (should only be Addon.zip) place in list
    for (dirpath, dirnames, filenames) in os.walk(working_dir):
        f.extend(filenames)
        break
    print(f)
    # for each file in the list, extract to wow AddOn Folder
    for file in f:
        print("Extracting contents of {file} to the WoW addon folder".format(file=file))
        with zipfile.ZipFile(working_dir + file, 'r') as zip_ref:
            zip_ref.extractall(directory)

def main():
    download_addon()
    extract_to_addon_directory(addon_dir)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
