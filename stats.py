from glob import glob
import os

avspeech_dir = '/scratch/cvit/rudra/avspeech/'

mp4s = glob(avspeech_dir + '*/*.*')

t = 0.

for m in mp4s:
	f = os.path.basename(m)
	start = float(f.split('_')[-2])
	end = float(f.split('_')[-1].split('.')[0])
	t += (end - start)

print(t / 3600.)