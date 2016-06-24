#!/bin/sh
# Author:         Ray Chen <chenrano2002@163.com>
# Creation Date:  06/28/2008
# Version:        0.3
# Description:    Comare files or directories using meld (support archive files)
# Copy this script in your ~/.gnome2/nautilus-scripts directory

# NAUTILUS_SCRIPT_SELECTED_FILE_PATHS : 
#       Nautilus variables----newline-delimited paths for selected files.
# Here, just replace newline to blank using sed commands
file_paths_list=(`echo $NAUTILUS_SCRIPT_SELECTED_FILE_PATHS | sed -e "s/\n/ /g"`)
support_archive_file_type=(tar gz bz2 zip rar)
install_comand="yum -y install"

function check_prog
{
    result=`which $1`
    if [ ! $? = 0 ];then
        zenity --info --text "$1 is not found on your system!\nThis program is needed to run \
this script.\n\nFor Fedora, you can get it from command \"$install_comand $1\"."
        exit 1
    fi
}

check_prog "meld"
check_prog "file-roller"

# Check whether input file is an archive file
function is_archive
{
    file_path=$1
    if [ "$file_path" == "" ];then
        return 1 
    fi
    archive_keyword='archive|zip'
    result=`file $file_path | cut -d\: -f2 | grep -iE $archive_keyword`
    if [ "$result" == "" ];then
        # file is not archive file
        return 1
    else
        # file not archive file
        return 0
    fi
}

# unzip archive files to temp directory
count=0
real_paths_list=()
for one_file in ${file_paths_list[*]}
do
    is_archive "$one_file"
    if [ $? -eq 0 ];then
        #zenity --info --text "is archive"
        tempdir=`mktemp -d /tmp/meld_tempdirXXXXXX`
        file-roller -e $tempdir $one_file
        real_paths_list=( "${real_paths_list[@]}" "$tempdir" )
    else
        real_paths_list=( "${real_paths_list[@]}" "$one_file" )                
    fi

    let "count +=1"
done

#zenity --info --text "${real_paths_list[*]}"

#main function
if [ "${#real_paths_list[*]}" -eq "0" ];then
    zenity --info --text "No files Selected!"
    exit 1
else
    # Run
    meld ${real_paths_list[*]}
fi

# Remove temp directories
rm -fr "/tmp/meld_tempdir"*

exit 0

