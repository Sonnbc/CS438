#!/bin/bash

format=$1
if [ "$format" == "" ];
then
  echo "You did not specify format. Assuming eps by default."
  echo "Recommended format is eps, pdf, or png. pdf or png requires cairo library."
  echo "Format can also be anything that gnuplot can work with."
  echo "For example, you can specify dumb, latex, or gif."
  format="eps"
fi

if [ -f cwnd ];
then
./plot.sh cwnd $format 1 2 "0.2" "cwnd vs Time" "Time (ms)" "cwnd (bytes)" $2 $3 
fi

if [ -f trace ];
then
./plot.sh trace $format 3 2 "0.2" "Sequence Number vs Time" "Time (ms)" "Sequence Number" $2 $3
fi


