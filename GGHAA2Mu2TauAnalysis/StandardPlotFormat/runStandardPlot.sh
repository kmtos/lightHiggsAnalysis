#!/bin/bash

#usage
if [ $# -ne 4 ]
    then
    echo "Usage: ./runStandardPlot.sh <PlotTitle> <PlotX> <PlotY> <LegendTitle>"
    exit 0
fi

#version
PlotTitle=$1
PlotX=$2
PlotY=$3
LegendTitle=$4

#setup
eval `scramv1 runtime -sh`


#run--order matters here!
root -l 'FormatPlotH2.C( "'${PlotTitle}'", "'${PlotX}'", "'${PlotY}'","'${LegendTitle}'")'
exit 0
