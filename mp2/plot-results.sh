#!/bin/sh
./plot.sh cwnd pdf 1 0.25 "cwnd vs Time" "Time (ms)" "cwnd (bytes)" $1 $2 
./plot.sh trace pdf 3 0.25 "Sequence Number vs Time" "Time (ms)" "Sequence Number" $1 $2
