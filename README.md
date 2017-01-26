# lightHiggsAnalysis

-Go to https://github.com/MengyaoShi/lightHiggsAnalysis.git and click "Fork" in the upper right-hand corner
- Execute
cd ~
cmsrel CMSSW_8_0_17
cd CMSSW_8_0_17/src
cmsenv
git clone https://github.com/YOUR-GITHUB-USERNAME/lightHiggsAnalysis.git
cd Tools
git remote add upstream https://github.com/MengyaoShi/lightHiggsAnalysis.git
cd ..

mkdir ~/Tau
cd ~/Tau
cmsrel CMSSW_8_0_17
cd CMSSW_8_0_17/src
cmsenv
git cms-addpkg DataFormats/HepMCCandidate
git cms-addpkg DataFormats/MuonReco
git cms-addpkg DataFormats/JetReco
git cms-addpkg DataFormats/TauReco
cp -r DataFormats ~/CMSSW_8_0_17/src
cd ~/CMSSW_8_0_17/src/DataFormats
cp /afs/cern.ch/work/m/mshi/public/CMSSW_8_0_17/src/DataFormats/HepMCCandidate/src/classes* HepMCCandidate/src
cp /afs/cern.ch/work/m/mshi/public/CMSSW_8_0_17/src/DataFormats/JetReco/src/classes* JetReco/src
cp /afs/cern.ch/work/m/mshi/public/CMSSW_8_0_17/src/DataFormats/MuonReco/src/classes* MuonReco/src
cp /afs/cern.ch/work/m/mshi/public/CMSSW_8_0_17/src/DataFormats/TauReco/src/classes* TauReco/src
cd ..
scram b -j16

