#!/bin/bash
./plot.sh cwnd pdf 1 2 "0.2" "cwnd vs Time" "Time (ms)" "cwnd (bytes)" $1 $2 
./plot.sh trace pdf 3 2 "0.2" "Sequence Number vs Time" "Time (ms)" "Sequence Number" $1 $2

