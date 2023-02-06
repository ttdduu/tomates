#!/usr/bin/zsh

# Names to display
files_array=(
	"notas"
	"diario"
	"config"
	"vimwiki"
	"pdf"
	"tomate"
	# "nvim"
	# "sxhk"
	# "bspwm"
	# "polybar"
	# "vifm"
	)

# Format de names to display
files=$''
for f in "${files_array[@]}"; do
	files=$f$'\n'$files
done

# Dmenu
choose_file=$(echo "$files" | dmenu -h 35 -i -p "Brainhub")


