#!/bin/bash

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

	# check if video exists
	# er=$(youtube-dl --get-filename --ignore-errors -f best "$url" 2>&1 1>/dev/null)
	if youtube-dl --get-filename --ignore-errors -f best "$url" 2>&1 1>/dev/null;
	then

		title=$(youtube-dl --get-filename --ignore-errors -f best "$url" 2>&1)
		ext=$(youtube-dl --get-filename -o '%(ext)s' --ignore-errors -f best "$url" 2>&1)
		while [ $? -ne 0 ]
		do
			title=$(youtube-dl --get-filename --ignore-errors -f best "$url" 2>&1)
			ext=$(youtube-dl --get-filename -o '%(ext)s' --ignore-errors -f best "$url" 2>&1)
		done
		echo "$title"

		# -- to handle filename staring with -(dash)
		mkdir -- "$yid"
		vid=$(youtube-dl -f best "$url" 2>&1 1>/dev/null)
		while [ $? -ne 0 ] && [ ! -f "$title" ]
		do
			vid=$(youtube-dl -f best "$url" 2>&1 1>/dev/null)
		done
		start_time=$(format_time "$start")
		end_time=$(format_time "$end")
		ffmpeg -ss "$start_time" -to "$end_time" -i ./"$title" -vcodec copy -acodec copy ./"$yid"/"$yid"."$ext"
		rm ./"$title"
		echo "Downlad complete ${yid}"
	else
		echo "$yid"
		echo "Can not download this file"
	fi
	
}

export -f format_time check

cat "$1" | parallel --jobs 0 check