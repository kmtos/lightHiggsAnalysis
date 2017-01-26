# lightHiggsAnalysis

This analysis repository is a search for a light higgs particle could potentially be found using Large Hadron Collider data collected by CERN. The following instruction is a guide to install this package on your working computer correctly. I will introduce function of specific packages after the instruction.

-Go to https://github.com/MengyaoShi/lightHiggsAnalysis.git and click "Fork" in the upper right-hand corner

- Execute

cd ~

cmsrel CMSSW_8_0_17

cd CMSSW_8_0_17/src

cmsenv

git clone https://github.com/YOUR-GITHUB-USERNAME/lightHiggsAnalysis.git

mv lightHiggsAnalysis ..

cd ..

rm -r src

mv lightHiggsAnalysis src

cd src

git remote add upstream https://github.com/MengyaoShi/lightHiggsAnalysis.git

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


rm -rf ~/Tau

scram b -j16

***********************************************************************

Folders are organized as following: 

##1. GGHAA2Mu2TauAnalysis 

Contains our major analysis code 

###SkimSequence folder

https://github.com/MengyaoShi/lightHiggsAnalysis/blob/master/GGHAA2Mu2TauAnalysis/SkimMuMuTauTau/test/SkimSequence/ is where our selection sequence developed. If can skim officially generated MC background down to order 10^-6 while keep most of signal.    

Recently we focus on using ABCD method to get estimation of QCD, TTBar, DrellYan backgrounds, and two non-correlated parameters defining these four regions are di-mu relative isolation, di-tau isolation. 

Region A: di-mu relative isolation: 0~1.0, di-tau isolation: tau id using MVA "hpsPFTauDiscriminationByMediumIsolationMVArun2v1DBoldDMwLT"

Region B: di-mu relative isolation: 0~1.0, di-tau anti-isolation: anti tau id using MVA "hpsPFTauDiscriminationByMediumIsolationMVArun2v1DBoldDMwLT"

Region C: di-mu relative isolationL: >1.0, di-tau isolation: tau id using MVA defined above.

Region D: di-mu relative isolation: >1.0, di-tau anti-isolation: anti tau id.

To know what this MVA method is, check out this link https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePFTauID

And pleas notice, all the variables can be defined by user. 

di-mu isolation



process.Isolate=cms.EDFilter('CustomDimuonSelector',

                                muonTag=cms.InputTag('Mu1Mu2EtaCut'),
                                
                                isoMax=cms.double(1.0),
                                
                                isoMin=cms.double(0.0),
                                
                                baseMuonTag=cms.InputTag('muons'),
                                
                                particleFlow=cms.InputTag('particleFlow'),
                                
                                minNumObjsToPassFilter=cms.uint32(2)
)

process.muHadNonIsoTauSelector = cms.EDFilter(

    'CustomTauSepFromMuonSelector',
    
    tauTag = cms.InputTag('muHadTauSelector','','SKIM'),
    
    baseTauTag = cms.InputTag('hpsPFTauProducer', '', 'SKIM'),
    
    tauHadIsoTag = cms.InputTag('hpsPFTauDiscriminationByCombinedIsolationDeltaBetaCorrRaw3Hits', '',
    
                                'SKIM'),
                                
    tauDiscriminatorTags = cms.VInputTag(
    
    cms.InputTag('hpsPFTauDiscriminationByMediumIsolationMVArun2v1DBoldDMwLT', '', 'SKIM')
    
    ),
    
    jetTag = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'SKIM'),
    
    muonRemovalDecisionTag = cms.InputTag('CleanJets','valMap','SKIM'),
    
    overlapCandTag = cms.InputTag('Mu45Selector'),
    
    overlapCandTag1=cms.InputTag('Mu1Mu2EtaCut','','SKIM'),
    
    passDiscriminator = cms.bool(False),
    
    pTMin=cms.double(10.0),
    
    etaMax = cms.double(2.4),
    
    isoMax = cms.double(-1.0),
    
    dR = cms.double(0.5),
    
    minNumObjsToPassFilter = cms.uint32(1),
    
    outFileName=cms.string('muHadNoIsoTauSelector.root')
    
)

Specifically, change passDiscriminator from "False" to "True" will yield isolatioon instead of anti-isolation. You can also speficy isoMax, and default is -1, which is no limit.



Detailed information to get this piece of selection work: type

cd <path_to_the_following_folder>/GGHAA2Mu2TauAnalysis/SkimMuMuTauTau/test/SkimSequence/

cmsRun RegionBSkim.py

You will obtain a .root file named "RegionB_selection.root" that stores events after this selection sequence. In particular, this RegionBSkim.py gives you selection sequence of getting B region data defined as "isolated di-mu and non-isolated di-tau selection plus passing general selection sequence".

###AMuTriggerAnalyzer and MuMuTauTauRecoAnalyzer 

Contains analyzers targeting for analyze di-muon behavior.

### Plotting

we have plotting scripts that can give us correctly normalized plots of stack of all background. How to use it is that you cd into src/GGHAA2Mu2TauAnalysis/TauAnalyzer/test

and type into following command

 ./runStandardAnalysis.sh 1

It is still under development. It aims to produce more maybe all plots that we are interested in just one go.  

### QCDBackground
Specifically analyze MC QCD background


##3. CollectEXO

It contains all the files of background and signal Monte Carlo after selection sequence. These MC results are stored on eos space of higgs Exotic group.

##4.GetStatistics

Everytime you submit job to crab, it divide one single job to smaller jobs, and since selection sequence table is written in log files, this scirpt collects all these tables from your entire job area, and calculate the final statistics. 

You need to change https://github.com/MengyaoShi/lightHiggsAnalysis/blob/master/GetStatistics/Files.txt to sepecify where your log files are store at. Currently it focus on getting selection table for QCD Monte Carlo. But it's flexible and you can study anything you are interested in.

##5. Tools 

package has a separate readme https://github.com/MengyaoShi/lightHiggsAnalysis/blob/master/Tools/README.md It contains packages has more general functions support this analysis. 




