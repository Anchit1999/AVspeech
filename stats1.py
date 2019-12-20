from glob import glob
import os

avspeech_dir = '/home/anchit/IIIT/cvit/kinetics700/kd/dataset/train'

mp4s = glob(avspeech_dir + '*/*/*.*')
# print(mp4s)
t = 0.

for m in mp4s:
	f = os.path.basename(m)
	start = float(f.split('_')[-2])
	end = float(f.split('_')[-1].split('.')[0])
	t += (end - start)

print(t / 3600.)