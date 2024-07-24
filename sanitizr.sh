#!/bin/bash

logo() {
  printf """
${yellow}
███████╗ █████╗ ███╗   ██╗██╗████████╗██╗███████╗██████╗ 
██╔════╝██╔══██╗████╗  ██║██║╚══██╔══╝██║╚══███╔╝██╔══██╗
███████╗███████║██╔██╗ ██║██║   ██║   ██║  ███╔╝ ██████╔╝
╚════██║██╔══██║██║╚██╗██║██║   ██║   ██║ ███╔╝  ██╔══██╗
███████║██║  ██║██║ ╚████║██║   ██║   ██║███████╗██║  ██║
╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝   ╚═╝╚══════╝╚═╝  ╚═╝
                               [Created by: get_right]{reset}
"""
}
# Default extensions to filter out
default_extlist=("jpeg" "jpg" "png" "woff" "woff2" "ttf" "mp4" "mp3" "svg" "eot" "css" "otf" "txt" "gif" "avi" "mov" "wmv" "mkv" "wav" "ogg" "webm" "ico")
additional_extlist=()
whitelist_extlist=()
stringlist=()
whitelist_strings=()
silent=false
verbose=false
output_file=""
bred='\033[1;31m'
bblue='\033[1;34m'
yellow='\033[0;33m'
reset='\033[0m'
red='\033[0;31m'
blue='\033[0;34m'

usage() {
  logo
  printf """\n
A simple wrapper around grep with predefined filters to remove unwanted entries from your wayback output

Flags:
  -e : extension filter
  -w : whitelist extension filter
  -s : string filter
  -v : verbose mode
  -o : output file
  -q : quiet mode
  -h : help message

Example Usage:                                                               

[*] To use default filters
        cat urls.txt | noshit

[*] To specify additional blacklist extension
        cat urls.txt | noshit -e 'php|js|txt'

[*] To whitelist extensions
        cat urls.txt | noshit -w 'html|json'

[*] To filter output via additional string
  cat urls.txt | noshit -s 'string1|string2'

[*] Quiet mode, suitable to pipe output to another tool
  cat urls.txt | noshit -q -e 'php|jsp' -s 'assets|static'

[*] Save filtered output to a file
  cat urls.txt | noshit -o filtered_urls.txt
"""
}

filter() {

  extlist=$(IFS='|'; echo "${default_extlist[*]}|${additional_extlist[*]}")
  

  if [ ${#whitelist_extlist[@]} -ne 0 ]; then
    whitelist_exts=$(IFS='|'; echo "${whitelist_extlist[*]}")
    extlist="(?<!($whitelist_exts))$extlist"
  fi

  
  if [ ${#whitelist_strings[@]} -ne 0 ]; then
    whitelist_strs=$(IFS='|'; echo "${whitelist_strings[*]}")
    stringlist="(?<!($whitelist_strs))$stringlist"
  fi

  
  if [ ! -t 0 ]; then
    if $silent; then
      if [ ${#stringlist[@]} -ne 0 ]; then
        filtered_output=$(cat - | egrep -iv "($extlist)|(${stringlist[*]})" | sort -u)
      else
        filtered_output=$(cat - | egrep -iv "($extlist)" | sort -u)
      fi
    else
      logo
      if [ ${#stringlist[@]} -ne 0 ]; then
        printf "\n\n${blue}Ext filters: ${yellow}[$red$extlist$yellow]\n${blue}String filters: ${yellow}[$red${stringlist[*]}$yellow]$reset\n\n"
        filtered_output=$(cat - | egrep -iv "($extlist)|(${stringlist[*]})" | sort -u)
      else
        printf "\n\n$blueExt filters: $yellow[$red$extlist$yellow]$reset\n\n"
        filtered_output=$(cat - | egrep -iv "($extlist)" | sort -u)
      fi
    fi

    if [ -n "$output_file" ]; then
      echo "$filtered_output" > "$output_file"
      [ $verbose = true ] && echo "Filtered output saved to $output_file"
    else
      echo "$filtered_output"
    fi
  else
    usage
  fi
}

while getopts "e:w:s:vo:qh" opt; do
  case $opt in
    e)
      IFS='|' read -ra additional_extlist <<< "$OPTARG"
      ;;
    w)
      IFS='|' read -ra whitelist_extlist <<< "$OPTARG"
      ;;
    s)
      IFS='|' read -ra stringlist <<< "$OPTARG"
      ;;
    v)
      verbose=true
      ;;
    o)
      output_file="$OPTARG"
      ;;
    q)
      silent=true
      ;;
    h)
      usage
      exit 0
      ;;
    \?)
      usage
      exit 1
      ;;
    :)
      usage
      exit 1
      ;;
  esac
done

filter
