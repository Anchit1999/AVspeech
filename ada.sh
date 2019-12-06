module load ffmpeg/4.2.1
root_dir="/scratch/cvit/rudra/AVSpeech/"
mkdir -p $root_dir

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

	if [ ! -d "/scratch/cvit/rudra/AVSpeech/${yid}" ]
	then
		# check if video exists
		if youtube-dl --get-filename --ignore-errors -f best "$url" 2>&1 1>/dev/null;
		then

			# -- to handle filename staring with -(dash)
			if youtube-dl --retries infinite --socket-timeout 99999999 -o '/scratch/cvit/rudra/AVSpeech/%(id)s.%(ext)s' -f best "$url" 2>&1 1>/dev/null;
			then
				ext=$(youtube-dl --get-filename -o '%(ext)s' -f best "$url")
				mkdir -p "/scratch/cvit/rudra/AVSpeech/${yid}"
				ffmpeg -hide_banner -loglevel panic -ss "$start_time" -to "$end_time" -i "/scratch/cvit/rudra/AVSpeech/${yid}"."$ext" -vcodec copy -acodec copy \
						"/scratch/cvit/rudra/AVSpeech/${yid}"/"$yid"_"$start_time"_"$end_time".mp4
				rm "/scratch/cvit/rudra/AVSpeech/${yid}"."$ext"
				echo "Download complete ${yid}"
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

