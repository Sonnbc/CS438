#!/bin/bash
if [ -f cwnd ];
then
./plot.sh cwnd $1 1 2 "0.2" "cwnd vs Time" "Time (ms)" "cwnd (bytes)" $2 $3 
fi

if [ -f trace ];
then
./plot.sh trace $1 3 2 "0.2" "Sequence Number vs Time" "Time (ms)" "Sequence Number" $2 $3
fi


