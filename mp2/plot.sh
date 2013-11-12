#!/bin/sh

i=0
iter=$1 # data file name prefix
format=$2 # format can be eps, pdf, png, aqua, x11
title=$3
xlabel=$4
ylabel=$5
timefrom=$6
timeupto=$7
for count in 1
do
  # delete filename.format
  rm -f "$iter.$format"
  # for eps we have its pdf version too
  if [ "$format" = "eps" ]; then
    rm -f "$iter.pdf" 
  fi
  echo "Drawing $iter.$format"
  i=`expr $i+1`
  
  # set the terminal
  if [ "$format" = "pdf" ]; then
    PT="pdfcairo font \"Gill Sans,7\" linewidth 3 rounded"
    # Slightly bigger and more bold, better for presentation
    #PT="$PT pdfcairo font \"Gill Sans,9\" linewidth 4 rounded fontscale 1.0
  elif [ "$format" = "png" ]; then
    PT="pngcairo size 3600, 1600 font \"Gill Sans,40\" linewidth 3 rounded"
  elif [ "$format" = "eps" ]; then
    PT="postscript"
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
  
  #set log x
  #set log y
  #set format x "%g"
  #set mxtics 10
  #set mytics 2

  set style line 1 lt rgb "#A00000" lw 1 pt 1
  set style line 2 lt rgb "#00A000" lw 1 pt 6
  set style line 3 lt rgb "#5060D0" lw 1 pt 2
  set style line 4 lt rgb "#F25900" lw 1 pt 9

  set key off
  #set key top left

  #plot "$iter.hist" using 1:2 with boxes lc rgb '#202090'
  plot "$iter" using (\$1):(\$2) with l ls 1, \
       "$iter" using 1:2 with p pointsize 0.35 pt 7
  plot "$iter" using 1:3 with lp pointsize 0.5 pt 7
  #plot bar chart and the value labels on the bars
EOF

if [ "$format" = "eps" ]; then
  echo "Converting $iter.eps to $iter.pdf"
  ps2pdf "$iter.eps"
fi
done

