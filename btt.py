#! /usr/local/bin/python
# -*- coding: utf-8 -*-
# coding: utf-8
import sys
import util
import requests
import re
import os
import logging
logging.basicConfig(level=logging.INFO)

def get_all_episodes(url, filename, folder):
    res = requests.get(url)
    if res.status_code == 200:
        content = res.content.decode('utf-8')
        findall_pattern = ur'<a href="(attach-dialog-[a-z0-9.-]+)" target="_blank" rel="nofollow"><img src="/view/image/filetype/torrent.gif" width="16" height="16"/>(%s)</a>' % filename
        episode_list = re.findall(findall_pattern, content, re.UNICODE)
        URL_BASE = 'http://btbtt.co/'

        logging.debug(episode_list)
        for ep_dl_url, name in episode_list:
            if os.path.exists(folder + name):
                logging.info('.')
                continue
            logging.info('filename:' + name)
            logging.info('ep_dl_url:' + ep_dl_url)
            fetch_torrent_file(URL_BASE + ep_dl_url, name, folder)

def fetch_torrent_file(episode_url, torrent_name, folder):
    logging.debug('fetch_torrent_file():' + episode_url)
    URL_DOWNLOAD_BASE = 'http://btbtt.me/'
    r = requests.get(episode_url)
    if r.status_code == 200:
        content = r.content.decode('utf-8')
        dl_url_pattern = ur'<a href="(attach-[a-z0-9.-]+)" target="_blank".*>'
        url = re.findall(dl_url_pattern, content, re.UNICODE)
        logging.debug(url)
        torrent_file_url = URL_DOWNLOAD_BASE + url[0]

        if not os.path.exists(folder):
            os.mkdir(folder)
        util.download(torrent_file_url, folder + torrent_name)

if __name__ == '__main__':
    config_file = sys.argv[1]
    config = open(config_file).readlines()
    collect_url = eval(config[0].decode('UTF-8'))
    filename = eval(config[1].decode('UTF-8'))
    torrent_folder = eval(config[2].decode('UTF-8')) + '/'

    # test sample
    #collect_url = 'http://www.btbtt.co/thread-index-fid-981-tid-4347813-page-1-scrollbottom-1.htm'
    #filename = ur'【極影字幕社】 ★4月新番 【進擊的巨人 2】【Shingeki no Kyojin 2】 【[0-9v]+】BIG5 MP4_720P.torrent'

    logging.debug(collect_url)
    logging.debug(filename)
    logging.info(torrent_folder)
    get_all_episodes(collect_url, filename, torrent_folder)
    logging.info('------ end ------')
