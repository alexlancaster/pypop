#!/bin/csh
# 
# usage:  GMTPlotData.sh freqfile.txt
#
# GMT general flags
# -J projection
# -R region of interest
# -D resolution of coastline data
# -L draw scale
# -O overlay
# -S paint wet areas
# -W Draw coastlines
# -K postscript will be added

set XYZFile=$1

set W=-175   #-10
set E=180   #55
set S=-60    #25
set N=75    #73
set LowBound=0 # 0 for frequency data, u for likelihood data
set ContourInterval=$XYZFile.cpt #0.5
set AnnotationInterval=0
set Proj=m.025 #m.025  #w0/1:240000000 #m.025 #M6i #B100/45/20/30/6i

blockmean $XYZFile -R$W/$E/$S/$N -I3 | surface  -R$W/$E/$S/$N -G$XYZFile.grd -I.5 -T.7 -Ll0
#nearneighbor -R$W/$E/$S/$N -I5 -S40 -G$XYZFile.grd $XYZFile.xyz

grd2cpt $XYZFile.grd -Cseis -I -L0/`cut -d " " -f 3 $XYZFile |sort -nr |head -1` > $XYZFile.cpt			#cut is used to get the upper bound
psbasemap -J$Proj -R$W/$E/$S/$N -B0:."`echo $XYZFile| sed 's/-/*/g'`": -G255 -K > $XYZFile.ps			#echo|sed is used to get the correct allele name for map title

pscoast -J$Proj -R$W/$E/$S/$N -A100000 -B0 -G200 -W0.5p -O -K >> $XYZFile.ps
psscale -D0.1i/1.1i/2i/0.3i -C$XYZFile.cpt -L -O -K >> $XYZFile.ps

pscoast -J$Proj -R$W/$E/$S/$N -A100000 -Gc -O -K >> $XYZFile.ps
#pscontour -J$Proj -R$W/$E/$S/$N -C$XYZFile.cpt -W -O -K >> $XYZFile.ps
psmask $XYZFile -R$W/$E/$S/$N -I3 -J$Proj -S16 -O -K >> $XYZFile.ps


grdimage $XYZFile.grd -C$XYZFile.cpt  -J$Proj -R$W/$E/$S/$N -O -K >> $XYZFile.ps

grdcontour $XYZFile.grd -J$Proj -C$ContourInterval -A- -R$W/$E/$S/$N  -O -K >> $XYZFile.ps   #-A$AnnotationInterval
#psmask -C >> $XYZFile.ps
psxy $XYZFile -R$W/$E/$S/$N -J$Proj -A -G255 -W0.5p -Sc.05 -O -K >>$XYZFile.ps

pscoast -J$Proj -R$W/$E/$S/$N -A10000 -W.5p -O  >> $XYZFile.ps
