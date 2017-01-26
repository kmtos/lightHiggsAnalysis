# MuMuTauTauSkimmer
In CMSSW8

This Skimmer do basically job to skim down dataset to what we are interested. test/SignalDiMuSelectionSkim.py is the corresponding

python file.


Reciepe: 

cmsrel CMSSW_8_0_17

cd CMSSW_8_0_17/src

cmsenv

mkdir GGHAA2Mu2TauAnalysis

cd GGHAA2Mu2TauAnalysis

git clone https://github.com/MengyaoShi/MuMuTautauSkimmerCmssw8 

mv MuMuTautauSkimmerCmssw8 MuMuTauTauSkimmer

vim DAS_test_Signal.txt

i

copy paste this into txt

root://144.92.180.64:31094///store/mc/RunIISpring16DR80/SUSYGluGluToHToAA_AToMuMu_AToTauTau_M-9_TuneCUETP8M1_13TeV_madgraph_pythia8/AODSIM/premix_withHLT_80X_mcRun2_asymptotic_v14-v1/60000/04052E3D-19A3-E611-A7C5-0CC47AA9906E.root



:wq

cd ..

git clone https://github.com/MengyaoShi/Tools

Before scram b, change mshi to ktos in SignalDiMuSelectionSkim.py and make sure the path being correct

Ok, now double check, you have CMSSW_8_0_17/src , inside this folder there are only two folders GGHAA2Mu2TauAnalysis and Tools, inside GGHAA2Mu2TauAnlysis there is only MuMuTauTauSkimmer and DAS_test_Signal.txt

scram b
cd MuMuTauTauSkimmer/test
cmsRun SignalDiMuSelectionSkim.py

You should add b tagging code in SignalDiMuSelectionSkim.py


