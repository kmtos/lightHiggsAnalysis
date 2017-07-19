mapfile -t arr_path < tmpFile.txt
for path in "${arr_path[@]}"
do
  path_str=${path}
  echo $path_str
  prefix='root://eoscms/'
  middle="/cmsRun_"
  afterfix=".log.tar.gz"
  arr=($(eos ls $path_str))
  arr=("${arr[@]/cmsRun_/}")
  arr=("${arr[@]/.log.tar.gz/}")
  for file in "${arr[@]}"
  do
    after=/cmsRun_$file$afterfix
    xrdcp $prefix$path_str$after .
    tar -xvzf cmsRun_${file}.log.tar.gz
    rm cmsRun_${file}.log.tar.gz
    rm FrameworkJobReport-${file}.xml
    rm cmsRun-stderr-${file}.log 
  done

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
  nHighestPtAndMuonSignDRSelector=0
  nMu1Mu2PtRankMuonID=0
  nMu1Mu2EtaCut=0
  nIsolate=0
  nPtEtaCut=0
  nMu45Selector=0
  nMu3=0
  nMu3ID=0
  ntauMuonPtSelector=0
  nmuHadTauSelector=0
  nmuHadNonIsoTauSelector=0
  nMassCut=0
  
  nTotalTot=0
  nMuonIWantTot=0
  nHighestPtAndMuonSignDRSelectorTot=0
  nMu1Mu2MassSelectionTot=0
  nMu1Mu2PtRankMuonIDTot=0
  nMu1Mu2EtaCutTot=0
  nIsolateTot=0
  nPtEtaCutTot=0
  nMu45SelectorTot=0
  nMu3Tot=0
  nMu3IDTot=0
  ntauMuonPtSelectorTot=0
  nmuHadTauSelectorTot=0
  nmuHadNonIsoTauSelectorTot=0
  nMassCutTot=0
  for iJob in "${arr[@]}"
    do
    nTotal=`grep MuonIWant ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*0[ ]*\([0-9]*\)[ ]*[0-9]*.*%\1%"`
    nMuonIWant=`grep MuonIWant ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*0[ ]*[0-9]*[ ]*\([0-9]*\).*%\1%"`
    nHighestPtAndMuonSignDRSelector=`grep '0 HighestPtAndMuonSignDRSelector' ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*1[ ]*[0-9]*[ ]*\([0-9]*\).*%\1%"`
    nMu1Mu2PtRankMuonID=`grep '0 Mu1Mu2PtRankMuonID' ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*2[ ]*[0-9]*[ ]*\([0-9]*\).*%\1%"`
    nMu1Mu2EtaCut=`grep Mu1Mu2EtaCut ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*3[ ]*[0-9]*[ ]*\([0-9]*\).*%\1%"`
    nIsolate=`grep Isolate ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*4[ ]*[0-9]*[ ]*\([0-9]*\).*%\1%"`
    nPtEtaCut=`grep PtEtaCut ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*5[ ]*[0-9]*[ ]*\([0-9]*\).*%\1%"`
    nMu45Selector=`grep Mu45Selector ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*6[ ]*[0-9]*[ ]*\([0-9]*\).*%\1%"`
    nMu3=`grep "0 Mu3" ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*7[ ]*[0-9]*[ ]*\([0-9]*\).*%\1%"`
    nMu3ID=`grep Mu3ID ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*8[ ]*[0-9]*[ ]*\([0-9]*\).*%\1%"`
    ntauMuonPtSelector=`grep tauMuonPtSelector ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*9[ ]*[0-9]*[ ]*\([0-9]*\).*%\1%"`
    nmuHadTauSelector=`grep muHadTauSelector ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*126[ ]*[0-9]*[ ]*\([0-9]*\).*%\1%"`
    nmuHadNonIsoTauSelector=`grep muHadNonIsoTauSelector ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*127[ ]*[0-9]*[ ]*\([0-9]*\).*%\1%"`
    nMassCut=`grep MassCut ${filePrefix}${iJob}${suffix} | head -n 1 | sed -e "s%TrigReport[ ]*1[ ]*128[ ]*[0-9]*[ ]*\([0-9]*\).*%\1%"`
  
    #increment totals
    nTotalTot=`expr $nTotalTot + $nTotal`
    nMuonIWantTot=`expr $nMuonIWantTot + $nMuonIWant`
    nHighestPtAndMuonSignDRSelectorTot=`expr $nHighestPtAndMuonSignDRSelectorTot + $nHighestPtAndMuonSignDRSelector`
    nMu1Mu2PtRankMuonIDTot=`expr $nMu1Mu2PtRankMuonIDTot + $nMu1Mu2PtRankMuonID`
    nMu1Mu2EtaCutTot=`expr $nMu1Mu2EtaCutTot + $nMu1Mu2EtaCut`
    nIsolateTot=`expr $nIsolateTot + $nIsolate`
    nPtEtaCutTot=`expr $nPtEtaCutTot + $nPtEtaCut`
    nMu45SelectorTot=`expr $nMu45SelectorTot + $nMu45Selector`
    nMu3Tot=`expr $nMu3Tot + $nMu3`
    nMu3IDTot=`expr $nMu3IDTot + $nMu3ID`
    ntauMuonPtSelectorTot=`expr $ntauMuonPtSelectorTot + $ntauMuonPtSelector`
    nmuHadTauSelectorTot=`expr $nmuHadTauSelectorTot + $nmuHadTauSelector`
    nmuHadNonIsoTauSelectorTot=`expr $nmuHadNonIsoTauSelectorTot + $nmuHadNonIsoTauSelector`
    nMassCutTot=`expr $nMassCutTot + $nMassCut`
  done
  
  #print totals
  echo "nTotal = $nTotalTot"
  echo "nMuonIWant = $nMuonIWantTot"
  echo "nHighestPtAndMuonSignDRSelector = $nHighestPtAndMuonSignDRSelectorTot"
  echo "nMu1Mu2PtRankMuonID = $nMu1Mu2PtRankMuonIDTot"
  echo "nMu1Mu2EtaCut= $nMu1Mu2EtaCutTot"
  echo "nIsolate= $nIsolateTot"
  echo "nPtEtaCut = $nPtEtaCutTot"
  echo "nMu45Selector = $nMu45SelectorTot"
  echo "nMu3 = $nMu3Tot"
  echo "nMu3ID = $nMu3IDTot"
  echo "ntauMuonPtSelector = $ntauMuonPtSelectorTot"
  echo "nmuHadTauSelector = $nmuHadTauSelectorTot"
  echo "nmuHadNonIsoTauSelector = $nmuHadNonIsoTauSelectorTot"
  echo "nMassCut = $nMassCutTot"
  rm *.log
done
exit 0 

