import FWCore.ParameterSet.Config as cms
from subprocess import *
import FWCore.Utilities.FileUtils as FileUtils
process = cms.Process("MINIAODSKIM")
#Debug utils
#process.ProfilerService = cms.Service (
#      "ProfilerService",
#       firstEvent = cms.untracked.int32(2),
#       lastEvent = cms.untracked.int32(500),
#       paths = cms.untracked.vstring('schedule')
#)
#process.SimpleMemoryCheck = cms.Service(
#    "SimpleMemoryCheck",
#    ignoreTotal = cms.untracked.int32(1)
#)
#PDG IDs
A_PDGID = 36
Z_PDGID = 23
W_PDGID = 24
TAU_PDGID = 15
MU_PDGID = 13
NUMU_PDGID = 14
D_PDGID = 1
U_PDGID = 2
S_PDGID = 3
C_PDGID = 4
B_PDGID = 5
T_PDGID = 6
G_PDGID = 21
ANY_PDGID = 0

#tau decay types
TAU_HAD = 0
TAU_MU = 1
TAU_E = 2
TAU_ALL = 3

#tau hadronic decay types
TAU_ALL_HAD = -1
TAU_1PRONG_0NEUTRAL = 0
TAU_1PRONG_1NEUTRAL = 1
TAU_1PRONG_2NEUTRAL = 2
TAU_1PRONG_3NEUTRAL = 3
TAU_1PRONG_NNEUTRAL = 4
TAU_2PRONG_0NEUTRAL = 5
TAU_2PRONG_1NEUTRAL = 6
TAU_2PRONG_2NEUTRAL = 7
TAU_2PRONG_3NEUTRAL = 8
TAU_2PRONG_NNEUTRAL = 9
TAU_3PRONG_0NEUTRAL = 10
TAU_3PRONG_1NEUTRAL = 11
TAU_3PRONG_2NEUTRAL = 12
TAU_3PRONG_3NEUTRAL = 13
TAU_3PRONG_NNEUTRAL = 14
TAU_RARE = 15

#no consideration of pT rank
ANY_PT_RANK = -1

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)

process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True),
                SkipEvent = cms.untracked.vstring('ProductNotFound'))

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(*mylist))
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring())

process.source.inputCommands = cms.untracked.vstring("keep *")

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
process.GlobalTag.globaltag = cms.string('80X_dataRun2_2016SeptRepro_v4') # CMSSW 8
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")
#process.load("RecoTauTag.RecoTau.RecoTauPiZeroProducer_cfi")
process.load('Tools/CleanJets/cleanjets_cfi')

#define a parameter set to be passed to all modules that utilize GenTauDecayID for signal taus
AMuMuPSet = cms.PSet(momPDGID = cms.vint32(A_PDGID),
                                   chargedHadronPTMin = cms.double(0.0),
                                   neutralHadronPTMin = cms.double(0.0),
                                   chargedLeptonPTMin = cms.double(0.0),
                                   totalPTMin = cms.double(0.0))

ATauTauPSet=cms.PSet(momPDGID = cms.vint32(A_PDGID),
				   chargedHadronPTMin=cms.double(0.0),
				   neutralHadronPTMin = cms.double(0.0),
                                   chargedLeptonPTMin = cms.double(0.0),
                                   totalPTMin = cms.double(0.0))
# load the PAT config
process.load("PhysicsTools.PatAlgos.patSequences_cff")

#require event to fire IsoMu24_eta2p1
process.TriggerAnalyzer0=cms.EDAnalyzer("TriggerAnalyzer")

process.lumiTree = cms.EDAnalyzer("LumiTree",
    genEventInfo = cms.InputTag("generator"),
    nevents = cms.InputTag('lumiSummary','numberOfEvents'),
    summedWeights = cms.InputTag('lumiSummary','sumOfWeightedEvents')
)	

#from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
#
#updateJetCollection(
#   process,
#   jetSource = cms.InputTag('slimmedJets'),
#   labelName = 'UpdatedJEC',
#   jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']), 'None')  # Update: Safe to always add 'L2L3Residual' as MC contains dummy L2L3Residual corrections (always set to 1)
#)
#process.jecSequence = cms.Sequence(process.patJetCorrFactorsUpdatedJEC * process.updatedPatJetsUpdatedJEC)
#from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
#
#runMetCorAndUncFromMiniAOD(process,
#                           isData=False, # (or False),
#                           jetCollUnskimmed = "updatedPatJetsUpdatedJEC"
#)

process.HLTEle =cms.EDFilter("HLTHighLevel",
    TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
    #HLTPaths = cms.vstring("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*", "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v*" ),
    #HLTPaths = cms.vstring("HLT_Mu7p5_Track7_Upsilon_v*", "HLT_Mu7p5_Track3p5_Upsilon_v*","HLT_Mu7p5_Track2_Upsilon_v*", "HLT_Mu7p5_L2Mu2_Upsilon_v*","HLT_Dimuon8_Upsilon_Barrel_v*","HLT_Dimuon13_Upsilon_v*","HLT_Dimuon0_Upsilon_Muon_v*" ),
    HLTPaths = cms.vstring("HLT_IsoMu24_v*","HLT_IsoTkMu24_v*"),
    eventSetupPathsKey = cms.string(''),
    andOr = cms.bool(True), #----- True = OR, False = AND between the HLTPaths
    throw = cms.bool(False) # throw exception on unknown path names
)

process.RandomNumberGeneratorService = cms.Service(
    "RandomNumberGeneratorService",
    RochesterCorr = cms.PSet(
    initialSeed = cms.untracked.uint32(3),
    engineName = cms.untracked.string('TRandom3')
    ),
)
process.RochesterCorr=cms.EDProducer("Rochester",
    muonCollection = cms.InputTag("slimmedMuons"),
    identifier = cms.string("DATA_80X_13TeV"),
    isData = cms.bool(False),
    initialSeed = cms.untracked.uint32(89),
    engineName = cms.untracked.string('TRandom3'),
    fp=cms.FileInPath("Rochester/Rochester/data/rcdata.2016.v3/config.txt")
)

process.PreMuons = cms.EDFilter('PTETACUT',
            muonTag=cms.InputTag("RochesterCorr","RochesterMu", "MINIAODSKIM"),
            Eta=cms.double(2.4),
            Pt=cms.double(3.0),
            minNumObjsToPassFilter=cms.uint32(3)
)

process.MuonsIDdxydz=cms.EDFilter(
  'MuonsID',
  muonTag = cms.InputTag('PreMuons'),
  muonID = cms.string('loose')
)

process.TrigMuMatcher=cms.EDFilter(
        'TrigMuMatcher',
        muonsTag = cms.InputTag('MuonsIDdxydz'),
        bits = cms.InputTag("TriggerResults","","HLT"),
        prescales = cms.InputTag("patTrigger"),
        triggerObjects = cms.InputTag("selectedPatTrigger"),
        trigNames = cms.vstring("HLT_IsoMu24_v","HLT_IsoTkMu24_v"),
        dRCut = cms.double(.15),
        mu1PtCut = cms.double(25.0)
)

process.GetMuOne = cms.EDFilter(
       'GetHighestPt',
       muonTag = cms.InputTag('TrigMuMatcher')
)

process.Mu2Iso=cms.EDFilter(
  'Mu2Iso',
  muonTag = cms.InputTag('MuonsIDdxydz'),
  mu1Tag = cms.InputTag('GetMuOne'),
  ptCut = cms.double(0.0),
  relIsoCutVal = cms.double(0.25), # .25 for iso, -1 for ignoring iso
  passRelIso = cms.bool(True) #False = Non-Iso DiMu, True = Iso-DiMu
)

process.DiMuSigndRSelector=cms.EDFilter(
                'DiMuSigndRSelector',
                mu1Tag = cms.InputTag('GetMuOne'),
	        muonsTag = cms.InputTag('Mu2Iso'),
                dRCut = cms.double(1.0),
                passdR = cms.bool(True),
                oppositeSign = cms.bool(True) # False for SameSignDiMu, True regular
)

process.GetMuTwo = cms.EDFilter(
       'GetSmallestdR',
       muonTag = cms.InputTag('DiMuSigndRSelector'),
       matchedToTag = cms.InputTag("GetMuOne")
)

process.Mu1Mu2 = cms.EDFilter(
	'CombineMu1Mu2',
        mu1Tag = cms.InputTag('GetMuOne'),
	mu2Tag = cms.InputTag('GetMuTwo')
)

process.MassCut=cms.EDFilter('Mu1Mu2MassFilter',
                              Mu1Mu2=cms.InputTag('Mu1Mu2'),
                              minMass=cms.double(60), #3   or 81
                              maxMass=cms.double(120) #3.2 or 101
)

process.Mu3=cms.EDFilter('VetoMuon',
        muonTag=cms.InputTag('MuonsIDdxydz'),
        vetoMuonTag=cms.InputTag('Mu1Mu2'),
	dRCut=cms.double(0.4),
	minNumObjsToPassFilter=cms.uint32(1)
)

process.Mu3ID = cms.EDFilter('CustomMuonSelector',
        baseMuonTag = cms.InputTag('slimmedMuons'),
        muonTag = cms.InputTag('Mu3'),
        vtxTag = cms.InputTag('offlineSlimmedPrimaryVertices'),
        muonID = cms.string('loose'),
        PFIsoMax = cms.double(-1),
        detectorIsoMax = cms.double(-1.0),
        PUSubtractionCoeff = cms.double(0.5),
        usePFIso = cms.bool(True),
        passIso = cms.bool(True),
        etaMax = cms.double(2.4),
        minNumObjsToPassFilter = cms.uint32(1)
)

#find taus in |eta| < 2.4 matched to muon-tagged cleaned jets
#this will produce a ref to the cleaned tau collection
process.muHadTauDMSelector = cms.EDFilter(
    'CustomTauSepFromMuonSelector',
    baseTauTag = cms.InputTag('slimmedTausMuonCleaned'),
    tauHadIsoTag = cms.string('hpsPFTauDiscriminationByIsolationMVArun2v1DBnewDMwLTraw'),
    overlapMuonTag = cms.InputTag('Mu1Mu2'),
    muons = cms.InputTag('Mu3'),
    tauDiscriminatorTags = cms.vstring('decayModeFinding'),
    passDiscriminator = cms.bool(True),
    pTMin = cms.double(10.0),
    etaMax = cms.double(2.4),
    isoMax = cms.double(-1.0),
    dROverlapMin = cms.double(0.8),
    minNumObjsToPassFilter = cms.uint32(1),
    diTaudRMax = cms.double(0.8)
    )

process.muHadTauDMIsoSelector = cms.EDFilter(
    'CustomTauSepFromMuonSelector',
    baseTauTag = cms.InputTag('muHadTauDMSelector'),
    tauHadIsoTag = cms.string('hpsPFTauDiscriminationByIsolationMVArun2v1DBnewDMwLTraw'),
    overlapMuonTag = cms.InputTag('Mu1Mu2'),
    muons = cms.InputTag('Mu3'),
#    tauDiscriminatorTags = cms.vstring('ByMediumIsolationMVA3oldDMwoLT'),
    tauDiscriminatorTags = cms.vstring('byMediumIsolationMVArun2v1DBoldDMwLT'),
    passDiscriminator = cms.bool(True),
    pTMin = cms.double(10.0),
    etaMax = cms.double(2.4),
    isoMax = cms.double(-1.0),
    dROverlapMin = cms.double(0.8),
    minNumObjsToPassFilter = cms.uint32(1),
    diTaudRMax = cms.double(0.8)
    )



process.GetRunNumber = cms.EDAnalyzer('GetRunNumber')
#sequences
process.MuMuSequenceSelector=cms.Sequence(
        process.lumiTree*
        process.HLTEle*
        process.RochesterCorr*
        process.PreMuons*
        process.MuonsIDdxydz*
        process.TrigMuMatcher*
	process.GetMuOne*
        process.Mu2Iso*
        process.DiMuSigndRSelector*
        process.GetMuTwo*
        process.Mu1Mu2*
        process.Mu3*
#        process.Mu3ID*
#        process.MassCut*
        process.muHadTauDMSelector*
        process.muHadTauDMIsoSelector
)


process.antiSelectionSequence = cms.Sequence(process.MuMuSequenceSelector
)


process.antiSelectedOutput = cms.OutputModule(
    "PoolOutputModule",
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('p')),
    fileName = cms.untracked.string('RegionB_selection.root')
    )
#sequences
process.TFileService = cms.Service("TFileService",
    fileName =  cms.string('TFiledataZ.root')
)
#no selection path
process.p = cms.Path(process.antiSelectionSequence)
process.e = cms.EndPath(process.antiSelectedOutput)
