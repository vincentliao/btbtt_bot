# -*- coding: utf-8 -*-
import urllib

def download(url, filename):    
    urllib.urlretrieve(url, filename)
