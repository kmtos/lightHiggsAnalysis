#!/bin/bash

export SCRAM_ARCH=slc6_amd64_gcc530
cd /afs/cern.ch/work/m/mshi/private/CMSSW_8_0_17/src
eval `scramv1 runtime -sh`
cd -
source /afs/cern.ch/cms/caf/setup.sh
CFG_FILE="Copy.py"
cmsRun /afs/cern.ch/work/m/mshi/private/CMSSW_8_0_17/src/GGHAA2Mu2TauAnalysis/SkimMuMuTauTau/test/QCDBackground/$CFG_FILE > Copy.txt
rfcp Copy.txt /afs/cern.ch/work/m/mshi/private/CMSSW_8_0_17/src/GGHAA2Mu2TauAnalysis/SkimMuMuTauTau/test/QCDBackground/Copy.txt
rfcp Copy.root /afs/cern.ch/work/m/mshi/private/CMSSW_8_0_17/src/GGHAA2Mu2TauAnalysis/SkimMuMuTauTau/test/QCDBackground/Copy.root

exit 0
