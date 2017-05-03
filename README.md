# gpsplot.py - A tiny program to plot GPS output

Use a GPS data file to plot your track:
![GNUplot 5 output file](#)

### GPS data file
I've used a GPS output file of the following format:
![GPS data](#)

### GNU plot
You can visualize it using GNU plot and the following commands:
```gnuplot
$ gnuplot
gnuplot> set grid
gnuplot> unset logscale x
gnuplot> unset logscale y
gnuplot> set xlabel "Distance in km"
gnuplot> set ylabel "Height in m"
gnuplot> set terminal png
gnuplot> set output "track.png"
gnuplot> plot "gpsplot.gp" using 3:7 notitle with lines linetype 3
```
Then open track.png in your folder.

### Limitations
You need to change file names in script. Also this doesn't work yet if a time difference between two data points is more than 24h.  Other than that have fun!

### Disclaimer
This was an assignment I did during my Masters program at [TU Chemnitz](https://www.tu-chemnitz.de/index.html.en "Technical University Chemnitz"). The following was provided:

* `diff_dist()` function
