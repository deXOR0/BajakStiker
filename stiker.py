import argparse
import datetime
import re
import requests
import os
from bs4 import BeautifulSoup
from better_terminal import *

IMAGES_PATH = 'images'

parser = argparse.ArgumentParser(description='Program to download all images from a web page')

parser.add_argument('-s', '--site', type=str, metavar='', required=True, help='set web page url')

args = parser.parse_args()

def init():
    print('''
█▄▄ ▄▀█ ░░█ ▄▀█ █▄▀   █▀ ▀█▀ █ █▄▀ █▀▀ █▀█
█▄█ █▀█ █▄█ █▀█ █░█   ▄█ ░█░ █ █░█ ██▄ █▀▄
            Created by deXOR0
    ''')

    if not os.path.exists(IMAGES_PATH):
        warning('Image Directory is not found!')
        os.mkdir(IMAGES_PATH)
        success('Image Directory is created')

if __name__ == '__main__':

    init()

    if args.site:
        site = args.site

        response = requests.get(site)

        soup = BeautifulSoup(response.text, 'html.parser')

        urls = []

        for ele in soup.find_all('span', attrs={'class':'mdCMN09Image'}):
            pattern = re.compile('.*background-image:\s*url\((.*)\);')
            match = pattern.match(ele['style'])
            if match:
                urls.append(match.group(1))
        
        urls = urls[::2] # for some reasons it reads the image file twice, so i just do some lazy cleanup :))

        time = datetime.datetime.now()
        directory = f'{str(time)}-{site}'
        directory = directory.replace('/', '-').replace(':', '.').replace('\\', '-').replace('?', '')
        directory = os.path.join(IMAGES_PATH, directory)
        
        os.mkdir(directory)
        success(f'Created {directory}')

        for url in urls:
            filename = re.search(r'/([\w_-]+[.](jpg|gif|png))', url)
            if not filename:
                error("Regex didn't match with the url: {}".format(url))
                continue
            else:
                success(f'{filename}')

            time = datetime.datetime.now()

            with open(os.path.join(directory, f'{str(time).replace(":", ".")}-{filename.group(1)}'), 'wb') as f:
                if 'http' not in url:
                    # sometimes an image source can be relative 
                    # if it is provide the base url which also happens 
                    # to be the site variable atm. 
                    url = '{}{}'.format(site, url)
                response = requests.get(url)
                f.write(response.content)
    else:
        error('Site URL must be specified through arguments, run python img.py -h for more info')