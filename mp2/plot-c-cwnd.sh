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
  set ytics 200
  set xrange [:110]    #set x and y range
  set yrange [:1800]
  
  #set log x
  #set log y
  #set format y "10^{%g}"
  set mxtics 5
  set mytics 2

  set style line 1 lt rgb "#A00000" lw 1 pt 6 ps 0.2
  set style line 2 lt rgb "#00A000" lw 1 pt 6 ps 0.2
  set style line 3 lt rgb "#5060D0" lw 1 pt 2 ps 0.2
  set style line 4 lt rgb "dark-violet" lw 1 pt 9
  set style arrow 5 head filled size screen 0.02,10,60 ls 4
  set key off

  set title "Loss Pattern 0"
  set label 1 "SlowStart ends" at 15.112793, 1330 rotate by 0 front tc rgb "#505050" center
  set arrow 1 from  10.112793,1300 to 10.112793,1020 as 5
  plot "$iter-0" using 1:2 with lp ls 1
  
  set title "Loss Pattern 1"
  set label 1 "FastRecovery begins" at 19.762939, 1200 rotate by 0 front tc rgb "#505050" center
  set arrow 1 from  19.762939,1150 to 19.762939,900 as 5
  set label 2 "FastRecovery ends" at 21.739990, 250 rotate by 0 front tc rgb "#505050" center
  set arrow 2 from  21.739990,300 to 21.739990,500 as 5
  plot "$iter-1" using 1:2 with lp ls 2
  
   
  set title "Loss Pattern 2"
  set log x
  set mxtics 10
  set xlabel "Time (ms) - Logarithmic scale"
  set xrange[0.001:50000]
  set label 1 "SlowStart after first timeout" at 19.934082, 600 rotate by 0 front tc rgb "#505050" center
  set arrow 1 from  19.934082,500 to 19.934082,100 as 5
  set label 2 ''
  set arrow 2 from 1,-1 to 1,-1
  #set mxtics 10
  plot "$iter-2" using 1:2 with lp ls 3
EOF
done

