#!/bin/bash
arr=( $(find /afs/cern.ch/work/m/mshi/private/CMSSW_8_0_17/src/CollectEXO/AllRootFiles -type f) )
arrlength=${#arr[@]}
suffix='.txt'
for (( i=0; i<${arrlength}; i++ ));
do
    arr[i]="${arr[i]##*/}"
    arr[i]=${arr[i]%$suffix}
done

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
    bsub -q 1nd -J $i < $file2
done


