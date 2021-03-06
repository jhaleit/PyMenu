#!/bin/sh

export SDL_AUDIODRIVER=dsp
export SDL_NOMOUSE=1
export HOME=/mnt/int_sd
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PWD/python/usr/lib
export PATH=$PATH:$PWD/python/usr/bin

#run volume deamon
./setVolume &

#store device menu runs from
ln -sf $(mount | grep int_sd | cut -f 1 -d ' ') /tmp/.int_sd

FILE="/tmp/run"
while true
do
	if [ -f $FILE ]; then
		echo "File $FILE exists"
		sh $FILE > /dev/ttyS1 2> /dev/ttyS1
		rm $FILE
	else
		sh ./pymenu.sh > /dev/ttyS1 2> /dev/ttyS1
		echo "File $FILE does not exist"	
	fi
	sleep 1
done
