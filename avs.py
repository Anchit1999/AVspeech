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
# def my_hook(d):
# 	print(d)
# 	if d['status'] == 'finished':
# 		ffmpeg -hide_banner -loglevel panic -ss "$start_time" -to "$end_time" -i "/scratch/cvit/rudra/AVSpeech/${yid}"."$ext" -vcodec copy -acodec copy \
# 						"/scratch/cvit/rudra/AVSpeech/${yid}"/"$yid"_"$start_time"_"$end_time".mp4
# 		command = 'ffmpeg -i {} -i {} -strict -2 {}'.format(args.audio, path.join(args.results_dir, 'result.avi'), 
# 														path.join(args.results_dir, 'result_voice.mp4'))
# 		subprocess.call(command, shell=True)
# 		y_id = d['filename'].split('.')[0]
# 		count2[y_id] += 1




ydl_opts = {
	'format': 'best',
	'quiet': True,
	'ignoreerrors': True,
	'retries': 10000000,
	'download_archive': os.path.join(args.output_dir,'archive.txt'),
	'socket_timeout': 99999999,
	'outtmpl': os.path.join(args.output_dir,'%(id)s.%(ext)s'),
	# 'progress_hooks': [my_hook],  
}

def format_time(t):
	h = '%.2d'%(t//3600)
	m = '%.2d'%((t%3600)//60)
	s = '%.2f'%(t%60)
	return h + ":" + m + ":" + s

def yt_download(d):

	# youtube id, start time, x, y
	yid = d[0]
	url = 'https://www.youtube.com/watch?v='+yid
	path_dir = path.join(args.output_dir, yid)
	
	# to check if video exists
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		try:
			check = ydl.extract_info(url, download=False)
		except:
			check = None
	
	if check != None:
		print("Start Downloading ",yid)
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			try:
				downloading_start[yid] = True
				info_dict = ydl.extract_info(url, download=True)
				ext = "." + info_dict['ext']
				try:
					os.mkdir(path_dir)
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
				data[yid] = []

	if not path.isdir(args.output_dir):
		os.mkdir(args.output_dir)

def main():
	preprocess()
	p = ThreadPoolExecutor(args.jobs)
	threads = [p.submit(yt_download,row) for row in data.items()]
	_ = [r.result() for r in tqdm(as_completed(threads), total=len(threads))]

if __name__ == '__main__':
	main()
