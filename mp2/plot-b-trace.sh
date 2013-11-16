#!/bin/sh

i=0
iter="b-trace" # data file name prefix
format="pdf" # format can be eps, pdf, png, aqua, x11
style="2"
title="Sequene Number vs. Time"
xlabel="Time (ms)"
ylabel="Sequence Number (bytes)"
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
    #PT="pdfcairo font \"Gill Sans,7\" linewidth 3 rounded fontscale 1.0"
    # Slightly bigger and more bold, better for presentation
    PT="pdfcairo font \"Gill Sans,9\" linewidth 2 rounded fontscale 1.0"
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
  
  #set xtics 5 
  #set ytics 100
  #set xrange [0:]    #set x and y range
  #set yrange [0:]
  
  #set format y "10^{%g}"
  #set mxtics 10
  set mytics 2

  set style line 1 lt rgb "#A00000" lw 1 pt 1
  set style line 2 lt rgb "#00A000" lw 1 pt 6
  set style line 3 lt rgb "#5060D0" lw 1 pt 2
  set style line 4 lt rgb "#F25900" lw 1 pt 9

  unset key
  #set key top left

  set title 'Loss Pattern 0'
  set label 1 "SlowStart ends" at 13.695801, 4100 rotate by 0 front tc rgb "#505050" center
  set arrow 1 from  13.695801,3900 to 13.695801,1000
  plot "$iter-0" using 1:(\$2+1) with lp ls 1 ps 0.2 pt 6
    #"< echo '13.695801 900'" with p ls 2 ps 0.4 pt 7
  

  set title 'Loss Pattern 1'
  set label 1 "Fast Retransmission" at 25.526123, 4100 rotate by 0 front tc rgb "#505050" center
  set arrow 1 from  25.526123,3900 to 25.526123,1600
  plot "$iter-1" using 1:(\$2+1) with lp ls 2 ps 0.2 pt 6
  

  set title 'Loss Pattern 2'
  set log x
  set xlabel "Time (ms) - Logarithmic scale"
  set xrange[:50000]
  set mxtics 10
  set label 1 "Timeout Retransmission" at 500,3000 rotate by 0 front tc rgb "#505050" center 
  set arrow 1 from 20.054932,2000 to 20.054932,200
  set arrow 2 from 56.677002,2000 to 56.677002,200
  set arrow 3 from 125.142090,2000 to 125.142090,200
  set arrow 4 from 261.272217,2000 to 261.272217,200
  set arrow 5 from 532.777100,2000 to 532.777100,200
  set arrow 6 from 1074.931152,2000 to 1074.931152,200
  set arrow 7 from 2158.501221,2000 to 2158.501221,200
  set arrow 8 from 4325.047119,2000 to 4325.047119,200
  set arrow 9 from 8658.822021,2000 to 8658.822021,200
  set arrow 10 from 17322.761963,2000 to 17322.761963,200
  set arrow 11 from 23649.888916,2000 to 34649.888916,400 

  plot "$iter-2" using 1:(\$2+1) with lp ls 3 ps 0.2
EOF
done

