import os,sys

import argparse
import shutil

import threading
import socket
import urllib.request
 
timeout = 4
socket.setdefaulttimeout(timeout)

def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--url-list-path', type=str, help='url list path')
    parser.add_argument('--save-folder', type=str, help='save folder')

    return parser.parse_args(argv)

def download_and_save(url,savename):
    try:
        data = urllib.request.urlopen(url).read()
        fid=open(savename,'w+b')
        fid.write(data)
        print ("download succeed: "+ url)
        fid.close()
    except IOError:
        print ("download failed: "+ url)

def main(args):
    print('===> args:\n', args)
    url_list_path = args.url_list_path
    save_folder = args.save_folder
    i = 0
    with open(url_list_path) as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("Name"):
                continue

            line_list = line.split('\t')
            if len(line_list) != 5:
                print('type wrong: ' + str(line_list) + '\n')
                continue
 
            id_index = line_list[1]
            img_index = line_list[2]
            image_url = line_list[4].strip()
            id_folder = os.path.join(save_folder, id_index)
            if False == os.path.exists(id_folder):
                os.mkdir(id_folder)
            savefile = id_folder + '/' + img_index
            while True:
                if(len(threading.enumerate()) < 1000):
                    break
            t = threading.Thread(target=download_and_save,args=(image_url,savefile,))
            t.start()

if __name__ == '__main__':
    main(parse_args(sys.argv[1:]))

