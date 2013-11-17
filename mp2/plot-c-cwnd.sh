#!/bin/sh

i=0
iter="c-cwnd" # data file name prefix
format="pdf" # format can be eps, pdf, png, aqua, x11
style="2"
title="cwnd vs. time"
xlabel="Time (ms)"
ylabel="cwnd (bytes)"
timefrom=""
timeupto=""
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
    #PT="pdfcairo font \"Gill Sans,7\" linewidth 3 rounded"
    # Slightly bigger and more bold, better for presentation
    PT="$PT pdfcairo font \"Gill Sans,9\" linewidth 2 rounded fontscale 1.0"
  elif [ "$format" = "png" ]; then
    PT="pngcairo size 3600, 1600 font \"Gill Sans,40\" linewidth 3 rounded"
  elif [ "$format" = "eps" ]; then
    #PT="postscript eps size 3.5, 2.62 enhanced color font 'Helvetica,20' linewidth 3"
    PT="postscript eps enhanced color font 'Helvetica,20' linewidth 3"
  
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
  
  set xtics 10
  #set ytics 1000
  set xrange [:110]    #set x and y range
  set yrange [:1800]
  
  #set log x
  #set log y
  #set format y "10^{%g}"
  #set mxtics 10
  #set mytics 2

  set style line 1 lt rgb "#A00000" lw 1 pt 1
  set style line 2 lt rgb "#00A000" lw 1 pt 6
  set style line 3 lt rgb "#5060D0" lw 1 pt 2
  set style line 4 lt rgb "#F25900" lw 1 pt 9

  set key off

  set title "Loss Pattern 0"
  set label 1 "SlowStart ends" at 15.112793, 1400 rotate by 0 front tc rgb "#505050" center
  set arrow 1 from  10.112793,1300 to 10.112793,1020
  plot "$iter-0" using 1:2 with lp ls 1 ps 0.2 pt 6
    #"< echo '10.112793 900'" with p ls 2 ps 0.4 pt 7
  
  
  set title "Loss Pattern 1"
  plot "$iter-1" using 1:(\$2+1) with lp ls 2 ps 0.2 #title 'Loss Pattern 1'
  
   
  set title "Loss Pattern 2"
  set log x
  set xlabel "Time (ms) - Logarithmic scale"
  set xrange[0.001:50000]
  #set mxtics 10
  plot "$iter-2" using 1:(\$2+1) with lp ls 3 ps 0.2 #title 'Loss Pattern 2'
EOF
done

