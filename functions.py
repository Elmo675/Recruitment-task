#!/usr/bin/python3
import multiprocessing
import re
import urllib.request
import itertools as it
from bs4 import BeautifulSoup

def reduce_None(element):
    return [x for x in element if x is not None]   

def group(seq,items):
    iters  = [iter(seq)] * items
    result = it.zip_longest(*iters)      
    result = map(lambda element : "".join(reduce_None(element)) if isinstance(element[0],str) else reduce_None(element) ,result)
    return result
 
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

def grab_text(Url,status,data_out):
    #try to connect 3 times
    COUNTER = 3
    while(COUNTER !=0):
        try:
            html = urllib.request.urlopen(Url)
            break
        except:
            COUNTER-=1
            continue
    if COUNTER == 0:
        status.value = -1
        return
    status.value = 1
    soup = BeautifulSoup(html)
    data = soup.findAll(text=True)
    result = filter(visible, data)
    status.value = 2
    for item in result:
        data_out.append(str(item))
    status.value = 3
    return

def grab_photo():
    None



