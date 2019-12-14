import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, as_completed
from os import listdir, path
import numpy as np
import collections

import argparse, os, traceback
os.system('ulimit -c 0')

import csv
import subprocess
import sys
import time
from tqdm import tqdm
import youtube_dl

parser = argparse.ArgumentParser()
parser.add_argument('--jobs', help='Number of jobs to run in parallel', default=4, type=int)
parser.add_argument('--file', help='CSV file containing data', required=True)
parser.add_argument("--output_dir", help="Folder where final videos will be downloaded", required=True)
args = parser.parse_args()

data = {}

ydl_opts = {
	'format': 'best',
	'quiet': True,
	'ignoreerrors': True,
	'retries': 10000000,
	'socket_timeout': 99999999,
	'outtmpl': os.path.join(args.output_dir,'%(id)s.%(ext)s'),
	'no-check-certificate' : True 
}

def format_time(t):
	h = '%.2d'%(t//3600)
	m = '%.2d'%((t%3600)//60)
	s = '%.2f'%(t%60)
	return h + ":" + m + ":" + s

def yt_download(d):

	# youtube id, start time, x, y
	yid = d[0]
	path_dir = path.join(args.output_dir, yid)

	if path.isdir(path_dir) and len(os.listdir(path_dir)) > 0: return

	url = 'https://www.youtube.com/watch?v='+yid
	
	
	print("Start Downloading ",yid)
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		try:
			info_dict = ydl.extract_info(url, download=True)
			ext = "." + info_dict['ext']
			try:
				if not path.isdir(path_dir): os.mkdir(path_dir)
			except OSError:
				print ("Creation of the directory %s failed" % path)
		except:
			info_dict = None
			ext = None
	
	if info_dict != None:
		for start, end, x, y in d[1]:
			st = format_time(float(start))
			et = format_time(float(end))
			command = 'ffmpeg -hide_banner -loglevel panic -ss {} -to {} -i {} -vcodec copy -acodec copy {}'.format(st,
							 et, path_dir + ext, path.join(args.output_dir,yid,yid+"_"+start+"_"+end+ext))

			subprocess.call(command, shell=True)
	try:
		os.remove(path_dir + ext)
	except:
		print("File already deleted or was not downloaded")

def preprocess():
	### Preprocessing
	with open(args.file) as f:
		csv_data = csv.reader(f,delimiter=",")

		for row in csv_data:
			yid = row[0]
			if yid in data:
				data[yid].append(row[1:])
			else:
				data[yid] = [row[1:]]

	if not path.isdir(args.output_dir):
		os.mkdir(args.output_dir)

def main():
	preprocess()
	p = ThreadPoolExecutor(args.jobs)
	threads = [p.submit(yt_download,row) for row in data.items()]
	_ = [r.result() for r in tqdm(as_completed(threads), total=len(threads))]

if __name__ == '__main__':
	main()
