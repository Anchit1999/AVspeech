#!/bin/bash
#SBATCH -A research
#SBATCH --qos=medium
#SBATCH -n 4
#SBATCH --gres=gpu:1
#SBATCH --mem-per-cpu=2048
#SBATCH --time=1-00:00:00
#SBATCH --mail-type=END

module load ffmpeg/4.2.1
root_dir="/ssd_scratch/cvit/anchit/"

# covert seconds to hh:mm:ss.ffffff format
format_time() {
	h=$(bc <<< "${1}/3600")
	m=$(bc <<< "(${1}%3600)/60")
	s=$(bc <<< "${1}%60")
	printf "%02d:%02d:%09.6f\n" "$h" "$m" "$s"
}

check() {

	IFS=',' read -r yid start end x y <<< "$1"

	url="https://www.youtube.com/watch?v=${yid}"
	start_time=$(format_time "$start")
	end_time=$(format_time "$end")

	if [ ! -d "/ssd_scratch/cvit/anchit/${yid}" ]
	then
		# check if video exists
		if youtube-dl --get-filename --ignore-errors -f best "$url" 2>&1 1>/dev/null;
		then

			# -- to handle filename staring with -(dash)
			if youtube-dl --retries infinite --socket-timeout 99999999 -o '/ssd_scratch/cvit/anchit/%(id)s.%(ext)s' -f best "$url" 2>&1 1>/dev/null;
			then
				ext=$(youtube-dl --get-filename -o '%(ext)s' -f best "$url")
				mkdir "/ssd_scratch/cvit/anchit/${yid}"
				ffmpeg -hide_banner -loglevel panic -ss "$start_time" -to "$end_time" -i "/ssd_scratch/cvit/anchit/${yid}"."$ext" -vcodec copy -acodec copy "/ssd_scratch/cvit/anchit/${yid}"/"$yid".mp4
				rm "/ssd_scratch/cvit/anchit/${yid}"."$ext"
				echo "Downlad complete ${yid}"
			else
				echo "Error ${yid}"
			fi
		else
			echo "Cannot download ${yid}"
		fi
	else
		echo "Skipped, Already downloaded ${yid}"
	fi
	
}

export -f format_time check

cat "$1" | parallel --jobs "$2" check

