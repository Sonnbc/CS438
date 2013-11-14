./plot.sh cwnd eps 1 "cwnd vs Time" "Time (ms)" "cwnd (bytes)" $1 $2 
ps2pdf cwnd.eps && echo "Converted to pdf"
