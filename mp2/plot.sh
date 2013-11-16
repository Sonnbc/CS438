#!/bin/sh

i=0
iter=$1 # data file name prefix
format=$2 # format can be eps, pdf, png, aqua, x11
style=$3
linewidth=$4
pointsize=$5
title=$6
xlabel=$7
ylabel=$8
timefrom=$9
timeupto=${10}
for count in 1
do
  rm -rf "$iter.$format"
  rm -rf "$iter.pdf" 
  echo "Drawing $iter.$format"
  i=`expr $i+1`
  
  if [ "$format" = "pdf" ]; then
    PT="pdfcairo font \"Gill Sans,9\" linewidth $linewidth rounded fontscale 1.0"
  elif [ "$format" = "png" ]; then
    PT="pngcairo size 3600, 1600 font \"Gill Sans,40\" linewidth $linewidth rounded"
  elif [ "$format" = "eps" ]; then
    PT="postscript eps enhanced color font 'Helvetica,20' linewidth $linewidth"
  else
    PT="$format"
  fi
  gnuplot << EOF
  reset
  set term $PT
  # Line style for axes
  set style line 80 lt rgb "#808080"
  # Line style for grid
  set style line 81 lt 0  # dashed
  set style line 81 lt rgb "#808080"  # grey

  set grid back linestyle 81
  set border 3 back linestyle 80 
               # Remove border on top and right.  These
               # borders are useless and make it harder
               # to see plotted lines near the border.
               # Also, put it in grey; no need for so much emphasis on a border.
  set xtics nomirror
  set ytics nomirror
  
  set output "$iter.$format"  
  set xlabel "$xlabel"    #set x and y label
  set ylabel "$ylabel"
  set title "$title"
  
  #set xtics 1
  #set ytics 100
  set xrange [$timefrom:$timeupto]    #set x and y range
  set yrange [0:]
  
  #set format x "%g"
  #set mxtics 10
  #set mytics 2

  set style line 1 lt rgb "#A00000" lw 1 pt 1
  set style line 2 lt rgb "#00A000" lw 1 pt 6
  set style line 3 lt rgb "#5060D0" lw 1  pt 2
  set style line 4 lt rgb "#F25900" lw 1 pt 9

  set key off
  #set key top left

  plot "$iter" using (\$1):(\$2) with lp ls $style ps $pointsize 
EOF
done

