#!/usr/bin/python3
import multiprocessing
import re
import requests
import os
from bs4 import BeautifulSoup

 
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

def url_to_soup(Url,status,data_out):
    #try to connect 3 times
    COUNTER = 3
    while(COUNTER !=0):
        try:
            response = requests.get(Url)
            break
        except:
            COUNTER-=1
            continue
    if COUNTER == 0:
        status.value = -1
        return None
    status.value = 1
    return BeautifulSoup(response.text,features="html.parser")

def grab_text(Url,status,data_out):
    soup = url_to_soup(Url,status,data_out)
    if soup == None:
        return
    data = soup.findAll(text=True)
    result = filter(visible, data)
    status.value = 2
    for item in result:
        data_out.append(str(item))
    status.value = 3
    return

def grab_photo(Url,status,data_out):
    soup = url_to_soup(Url,status,data_out)
    if soup == None:
        return
    directory = "photo\ " + Url.split('/')[2]
    try:
        os.mkdir(directory)
    except FileExistsError:
        None
    except:
        status.value = -2
        return
    img_tags = soup.find_all('img')
    urls = [img['src'] for img in img_tags if 'src' in img  ]
    status.value = 2
    for url in urls:
        if url is None:
            continue
        filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
        if filename == None:
            continue
        with open(os.path.join(directory, filename.group(1)), 'wb') as f:
            if 'http' not in url:
                url = '{}{}'.format(Url, url)
            response = requests.get(url)
            f.write(response.content)
    status.value = 3
    return




