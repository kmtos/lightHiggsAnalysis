#!/bin/bash

declare -a arr=("QCD_1000ToInf_noSelection"
		"QCD_800To1000_noSelection"
		"QCD_600To800_noSelection"
 		"QCD_300To470_noSelection"
		"QCD_170To300_noSelection"
		"QCD_120To170_noSelection"
		"QCD_80To120_noSelection"
		"QCD_50To80_noSelection"
		"QCD_30To50_noSelection"
		"QCD_20To30_noSelection"
		"QCD_15To20_noSelection")
afterfix=".py"
afterfix2=".sh"
afterfix3=".txt"
for i in "${arr[@]}"
do
    file="$i"$afterfix
    file2="$i"$afterfix2
    echo $file2
    sed "s/CopiedFileName/$i/g" "test_skimmed.py" > $file
    sed "s/Copy/$i/g" "lxplusbatchscript.sh"> $file2
    bsub -q 8nh -J $i < $file2
done


