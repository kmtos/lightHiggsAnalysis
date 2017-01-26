#!/bin/bash


#arguments
minJob=$1
maxJob=$2
exclString=$3
dataDir=$4

#macros
filePrefix="cmsRun-stdout-"
suffix=".log"

#totals
nTotal=0
nMuonIWant=0
nHighestPtAndMuonOppositeSignDRSelector=0
nMu1Mu2PtRankMuonID=0
nMu1Mu2EtaCut=0
nPtEtaCut=0
nMu45Selector=0
nMu3=0
nMu3ID=0
ntauMuonPtSelector=0
nmuHadTauSelector=0

nTotalTot=0
nMuonIWantTot=0
nHighestPtAndMuonOppositeSignDRSelectorTot=0
nMu1Mu2MassSelectionTot=0
nMu1Mu2PtRankMuonIDTot=0
nMu1Mu2EtaCutTot=0
nPtEtaCutTot=0
nMu45SelectorTot=0
nMu3Tot=0
nMu3IDTot=0
ntauMuonPtSelectorTot=0
nmuHadTauSelectorTot=0
Jobs="1 10 11 12 13 14 15 16 18 19 2 20 21 22 23 24 25 26 27 28 29 3 4 5 6 7 8 9"
for iJob in ${Jobs}
  do
  nTotal=`grep MuonIWant ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*0[ ]*\([0-9]*\)[ ]*[0-9]*.*%\1%"`
  nMuonIWant=`grep MuonIWant ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*0[ ]*[0-9]*[ ]*\([0-9]*\).*%\1%"`
  nHighestPtAndMuonOppositeSignDRSelector=`grep '0 HighestPtAndMuonOppositeSignDRSelector' ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*1[ ]*[0-9]*[ ]*\([0-9]*\).*%\1%"`
  nMu1Mu2PtRankMuonID=`grep '0 Mu1Mu2PtRankMuonID' ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*2[ ]*[0-9]*[ ]*\([0-9]*\).*%\1%"`
  nMu1Mu2EtaCut=`grep Mu1Mu2EtaCut ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*3[ ]*[0-9]*[ ]*\([0-9]*\).*%\1%"`
  nPtEtaCut=`grep PtEtaCut ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*4[ ]*[0-9]*[ ]*\([0-9]*\).*%\1%"`
  nMu45Selector=`grep Mu45Selector ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*5[ ]*[0-9]*[ ]*\([0-9]*\).*%\1%"`
  nMu3=`grep "0 Mu3" ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*6[ ]*[0-9]*[ ]*\([0-9]*\).*%\1%"`
  nMu3ID=`grep Mu3ID ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*7[ ]*[0-9]*[ ]*\([0-9]*\).*%\1%"`
  ntauMuonPtSelector=`grep tauMuonPtSelector ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*8[ ]*[0-9]*[ ]*\([0-9]*\).*%\1%"`
  nmuHadTauSelector=`grep muHadTauSelector ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*125[ ]*[0-9]*[ ]*\([0-9]*\).*%\1%"`

  #increment totals
  nTotalTot=`expr $nTotalTot + $nTotal`
  nMuonIWantTot=`expr $nMuonIWantTot + $nMuonIWant`
  nHighestPtAndMuonOppositeSignDRSelectorTot=`expr $nHighestPtAndMuonOppositeSignDRSelectorTot + $nHighestPtAndMuonOppositeSignDRSelector`
  nMu1Mu2PtRankMuonIDTot=`expr $nMu1Mu2PtRankMuonIDTot + $nMu1Mu2PtRankMuonID`
  nMu1Mu2EtaCutTot=`expr $nMu1Mu2EtaCutTot + $nMu1Mu2EtaCut`
  nPtEtaCutTot=`expr $nPtEtaCutTot + $nPtEtaCut`
  nMu45SelectorTot=`expr $nMu45SelectorTot + $nMu45Selector`
  nMu3Tot=`expr $nMu3Tot + $nMu3`
  echo ${iJob}
  nMu3IDTot=`expr $nMu3IDTot + $nMu3ID`
  ntauMuonPtSelectorTot=`expr $ntauMuonPtSelectorTot + $ntauMuonPtSelector`
  nmuHadTauSelectorTot=`expr $nmuHadTauSelectorTot + $nmuHadTauSelector`
done

#print totals
echo "nTotal = $nTotalTot"
echo "nMuonIWant = $nMuonIWantTot"
echo "nHighestPtAndMuonOppositeSignDRSelector = $nHighestPtAndMuonOppositeSignDRSelectorTot"
echo "nMu1Mu2PtRankMuonID = $nMu1Mu2PtRankMuonIDTot"
echo "nMu1Mu2EtaCut= $nMu1Mu2EtaCutTot"
echo "nPtEtaCut = $nPtEtaCutTot"
echo "nMu45Selector = $nMu45SelectorTot"
echo "nMu3 = $nMu3Tot"
echo "nMu3ID = $nMu3IDTot"
echo "ntauMuonPtSelector = $ntauMuonPtSelectorTot"
echo "nmuHadTauSelector = $nmuHadTauSelectorTot"
exit 0
