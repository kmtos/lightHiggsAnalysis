arr_path=(/eos/cms/store/group/phys_higgs/HiggsExo/mshi/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/CRAB3_QCD_pt_15to20_no_Skim/170116_102502/0000/log
/eos/cms/store/group/phys_higgs/HiggsExo/mshi/QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/CRAB3_QCD_pt_20to30_no_Skim/170116_102307/0000/log
/eos/cms/store/group/phys_higgs/HiggsExo/mshi/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/CRAB3_QCD_pt_30to50_no_Skim/170116_102147/0000/log
/eos/cms/store/group/phys_higgs/HiggsExo/mshi/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/CRAB3_QCD_pt_50to80_no_Skim/170116_102007/0000/log
/eos/cms/store/group/phys_higgs/HiggsExo/mshi/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/CRAB3_QCD_pt_80to120_no_Skim/170116_101834/0000/log
/eos/cms/store/group/phys_higgs/HiggsExo/mshi/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/CRAB3_QCD_pt_120to170_no_Skim/170116_101652/0000/log
/eos/cms/store/group/phys_higgs/HiggsExo/mshi/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/CRAB3_QCD_pt_170to300_no_Skim/170116_101456/0000/log
/eos/cms/store/group/phys_higgs/HiggsExo/mshi/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/CRAB3_QCD_pt_300to470_no_Skim/170116_101304/0000/log
/eos/cms/store/group/phys_higgs/HiggsExo/mshi/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/CRAB3_QCD_pt_600to800_no_Skim/170116_100743/0000/log
/eos/cms/store/group/phys_higgs/HiggsExo/mshi/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/CRAB3_QCD_pt_800to1000_no_Skim/170116_100605/0000/log
/eos/cms/store/group/phys_higgs/HiggsExo/mshi/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/CRAB3_QCD_pt_1000toInf_no_Skim/170116_095638/0000/log)

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
  for iJob in "${arr[@]}"
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
  rm *.log
done
exit 0 

