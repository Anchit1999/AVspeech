import argparse
import json
import os

import lib.config as config
import lib.parallel_download as parallel

def maybe_create_dirs():
	"""
	Create directories for training, validation and testing videos if they do not exist.
	:return:    None.
	"""

	for path in [config.TRAIN_ROOT, config.VALID_ROOT, config.TEST_ROOT]:
		if not os.path.exists(path):
			try:
				os.makedirs(path)
			except FileExistsError:
				pass

def download(num_workers, failed_save_file, compress, verbose, skip, log_file):
	
	with open(config.TRAIN_METADATA_PATH) as file:
		data = json.load(file)
	
	# print(data)
	pool = parallel.Pool(data, config.TRAIN_ROOT, num_workers, failed_save_file, compress, verbose, skip, log_file=log_file)
	pool.start_workers()
	pool.feed_videos()
	pool.stop_workers()

def main(args):

	download(args.num_workers, args.failed_log, args.compress, args.verbose, args.skip, args.log_file)

if __name__ == "__main__":

	maybe_create_dirs()
	parser = argparse.ArgumentParser("Download AVSpeech videos in the mp4 format.")

	parser.add_argument("--num-workers", type=int, default=4, help="number of downloader processes")
	parser.add_argument("--failed-log", default="dataset/failed.txt", help="where to save list of failed videos")
	parser.add_argument("--compress", default=False, action="store_true", help="compress videos using gzip (not recommended)")
	parser.add_argument("-v", "--verbose", default=False, action="store_true", help="print additional info")
	parser.add_argument("-s", "--skip", default=False, action="store_true", help="skip classes that already have folders")
	parser.add_argument("-l", "--log-file", help="log file for youtube-dl (the library used to download YouTube videos)")

	parsed = parser.parse_args()
	main(parsed)
