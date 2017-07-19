import FWCore.ParameterSet.Config as cms
from subprocess import *
import FWCore.Utilities.FileUtils as FileUtils
mylist=FileUtils.loadListFromFile('/afs/cern.ch/work/m/mshi/private/CMSSW_8_0_17/src/CollectEXO/AllRootFiles/CopiedFileName.txt')
process = cms.Process("ANALYSIS")


process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True),
                SkipEvent = cms.untracked.vstring('ProductNotFound'))

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(*mylist))
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
#for L1GtStableParametersRcd
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')

#for HLT selection
process.load('HLTrigger/HLTfilters/hltHighLevel_cfi')
import HLTrigger.HLTfilters.hltHighLevel_cfi as hlt
#for mu-less jets
process.load('Configuration.StandardSequences.MagneticField_cff') #I changed it from: process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff') # Kyle Added this
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi') # Kyle Added this
process.GlobalTag.globaltag = cms.string('80X_mcRun2_asymptotic_v14') # CMSSW 8
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")
#process.load("RecoTauTag.RecoTau.RecoTauPiZeroProducer_cfi")
process.load('Tools/CleanJets/cleanjets_cfi')
process.muHadNonIsoTauSelector=cms.EDFilter(
    'CustomTauSepFromMuonSelector',
    tauTag=cms.InputTag('muHadTauSelector','','SKIM'),
    baseTauTag=cms.InputTag('hpsPFTauProducer', '', 'SKIM'),
    tauHadIsoTag = cms.InputTag('hpsPFTauDiscriminationByCombinedIsolationDeltaBetaCorrRaw3Hits', '',
                                'SKIM'),
    tauDiscriminatorTags = cms.VInputTag(
    cms.InputTag('hpsPFTauDiscriminationByDecayModeFinding', '', 'SKIM'), 
    cms.InputTag('hpsPFTauDiscriminationByIsolationMVArun2v1PWnewDMwLTraw', '', 'SKIM')
    ),
    jetTag = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'SKIM'),
    muonRemovalDecisionTag = cms.InputTag('CleanJets', '', 'SKIM'),
    overlapCandTag = cms.InputTag('Mu45Selector','','SKIM'),
    passDiscriminator = cms.bool(False),
    outFileName=cms.string('muHadTauSelector.root'),
    pTMin = cms.double(20.0),
    etaMax = cms.double(2.3),
    isoMax = cms.double(-1.0),
    dR = cms.double(0.5),
    minNumObjsToPassFilter = cms.uint32(1)
    )

process.muHadTauSelector = process.muHadNonIsoTauSelector.clone()
process.muHadTauSelector.tauDiscriminatorTags = cms.VInputTag(
    cms.InputTag('hpsPFTauDiscriminationByDecayModeFinding', '', 'SKIM')
    )
process.muHadTauSelector.passDiscriminator=cms.bool(True)
process.muHadTauSelector.isoMax=cms.double(-1.0)

process.muHadIsoTauSelector = process.muHadNonIsoTauSelector.clone()
process.muHadIsoTauSelector.tauDiscriminatorTags = cms.VInputTag(
    cms.InputTag('hpsPFTauDiscriminationByIsolationMVArun2v1PWnewDMwLTraw', '', 'SKIM')
    )
process.muHadIsoTauSelector.passDiscriminator = cms.bool(True)
process.muHadIsoTauSelector.isoMax = cms.double(-1.0) #GeV


process.NonIsoBVetoFilter = cms.EDFilter(
    'BVetoFilter',
    tauTag = cms.InputTag('muHadNonIsoTauSelector'),
    oldJetTag = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'SKIM'),
    jetMuonMapTag = cms.InputTag('CleanJets', '', 'SKIM'),
    bTagInfoTag = cms.InputTag('pfCombinedInclusiveSecondaryVertexV2BJetTags', '', 'SKIM'),
    CSVMax = cms.double(0.679),
    passFilter = cms.bool(True),
    minNumObjsToPassFilter = cms.uint32(1)
    )


#for jet corrections
process.load('JetMETCorrections.Configuration.JetCorrectionServices_cff')
process.load('JetMETCorrections.Configuration.JetCorrectors_cff')

process.ak4PFchsCorrectedJets   = cms.EDProducer('CorrectedPFJetProducer',
    src         = cms.InputTag('ak4PFJets','','RECO'),
    correctors  = cms.VInputTag('ak4PFCHSL1FastL2L3Corrector')
    )
process.corrJetDistinctIsoTauSelector = cms.EDFilter(
    'CustomJetSelector',
    tauTag = cms.InputTag('IsoBVetoFilter'),
    overlapCandTag = cms.InputTag('Mu45Selector','','SKIM'),
    oldJetTag = cms.InputTag('ak4PFchsCorrectedJets'),
    jetMuonMapTag = cms.InputTag('CleanJets','muonValMap','SKIM'),
    pTMin = cms.double(30.0),
    absEtaMax = cms.double(4.7),
    dR = cms.double(0.3),
    minNumObjsToPassFilter = cms.uint32(0),
    maxNumObjsToPassFilter = cms.int32(-1)
    )
process.corrJetDistinctNonIsoTauSelector = process.corrJetDistinctIsoTauSelector.clone()
process.corrJetDistinctNonIsoTauSelector.tauTag = cms.InputTag('NonIsoBVetoFilter')
process.MuMuTauTauRecoAnalyzer=cms.EDAnalyzer(
        'MuMuTauTauRecoAnalyzer',
        tauTag=cms.InputTag('corrJetDistinctNonIsoTauSelector'),
        jetMuonMapTag=cms.InputTag('CleanJets','muonValMap','SKIM'),
        Mu1Mu2= cms.InputTag('Mu1Mu2EtaCut','','SKIM'),
        IsolatedMuon=cms.InputTag('Isolate','','SKIM'),
        Mu3ID=cms.InputTag('Mu3ID','','SKIM'),
        Jet=cms.InputTag('ak4PFJets','','RECO'), 
        Met=cms.InputTag('pfMet','','RECO'),
        #genParticleTag=cms.InputTag('genParticles'),
        muHadMassBins=cms.vdouble(1,2,3,4,12),
        FourBInvMassBins=cms.vdouble(0.0, 200.0,400.0,600.0, 800.0, 1000.0),
        outFileName=cms.string("CopiedFileName.root"),
        tauHadIsoTag = cms.InputTag('hpsPFTauDiscriminationByRawCombinedIsolationDBSumPtCorr3Hits', '',
                                'SKIM'),
        particleFlow=cms.InputTag('particleFlow'),
        inputFile=cms.string('CopiedFileName')
)
#require event to fire IsoMu24_eta2p1
process.tauAnalysisSequence = cms.Sequence(
  process.muHadNonIsoTauSelector*
  process.NonIsoBVetoFilter*
  process.ak4PFCHSL1FastL2L3CorrectorChain*
  process.ak4PFchsCorrectedJets*
  process.corrJetDistinctNonIsoTauSelector*
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
process.p = cms.Path(process.tauAnalysisSequence)
process.e = cms.EndPath(process.noSelectedOutput)
