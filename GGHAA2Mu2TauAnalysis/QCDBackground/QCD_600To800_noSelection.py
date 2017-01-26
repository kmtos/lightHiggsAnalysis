import FWCore.ParameterSet.Config as cms
from subprocess import *
import FWCore.Utilities.FileUtils as FileUtils
mylist=FileUtils.loadListFromFile('/afs/cern.ch/work/m/mshi/private/CMSSW_8_0_17/src/CollectEXO/QCD_600To800_noSelection.txt')
process = cms.Process("testOutput")


process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True),
                SkipEvent = cms.untracked.vstring('ProductNotFound'))

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(*mylist))
process.MuMuTauTauRecoAnalyzer=cms.EDAnalyzer(
        'MuMuTauTauRecoAnalyzer',
        tauTag=cms.InputTag('muHadTauSelector','','SKIM'),
        jetMuonMapTag=cms.InputTag('CleanJets','muonValMap','SKIM'),
        Mu1Mu2= cms.InputTag('Mu1Mu2EtaCut','','SKIM'),
        genParticleTag=cms.InputTag('genParticles'),
        muHadMassBins=cms.vdouble(1,2,3,4,12),
        FourBInvMassBins=cms.vdouble(0.0, 200.0,400.0,600.0, 800.0, 1000.0),
        outFileName=cms.string("QCD_600To800_noSelection.root"),
        tauHadIsoTag = cms.InputTag('hpsPFTauDiscriminationByRawCombinedIsolationDBSumPtCorr3Hits', '',
                                'SKIM'),
        particleFlow=cms.InputTag('particleFlow'),
        inputFile=cms.string('QCD_600To800_noSelection')
)
#require event to fire IsoMu24_eta2p1
process.noSelectionSequence = cms.Sequence(
  process.MuMuTauTauRecoAnalyzer
)

process.TFileService = cms.Service("TFileService",
    fileName =  cms.string('tes.root')
)
process.noSelectedOutput = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string('condensed.root'),
    SelectEvents=cms.untracked.PSet(SelectEvents = cms.vstring('p'))
    )
#no selection path
process.p = cms.Path(process.noSelectionSequence)
process.e = cms.EndPath(process.noSelectedOutput)
