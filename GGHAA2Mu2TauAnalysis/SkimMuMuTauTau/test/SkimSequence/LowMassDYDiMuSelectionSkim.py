import FWCore.ParameterSet.Config as cms
from subprocess import *
import FWCore.Utilities.FileUtils as FileUtils
mylist=FileUtils.loadListFromFile('/afs/cern.ch/work/m/mshi/private/CMSSW_8_0_17/src/GGHAA2Mu2TauAnalysis/DrellYan.txt')
process = cms.Process("SKIM")

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

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(*mylist))

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
process.GlobalTag.globaltag = cms.string('80X_mcRun2_asymptotic_v14') # CMSSW 8
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

# Configure PAT to use PF2PAT instead of AOD sources
# this function will modify the PAT sequences. 
from PhysicsTools.PatAlgos.tools.pfTools import *
from PhysicsTools.PatAlgos.tools.metTools import *


# to use tau-cleaned jet collection uncomment the following: 
#getattr(process,"pfNoTau"+postfix).enable = True

# to switch default tau to HPS tau uncomment the following: 
#adaptPFTaus(process,"hpsPFTau",postfix=postfix)


#output commands
skimEventContent = cms.PSet(
    outputCommands = cms.untracked.vstring(
    "keep *",
    "drop *_*ak7*_*_*",
    "drop *_*ak5*_*_*",
    "drop *_*ak8*_*_*",
    "drop *_*GenJets_*_*",
    "drop *_ak4CaloJets*_*_*",
    "drop *_ak4TrackJets*_*_*",
    "drop *_*jetCentral*_*_*",
    "drop *_fixedGridRho*_*_*",
    "drop *_hfEMClusters_*_*",
    "drop *_eid*_*_*",
    "drop *_muonMETValueMapProducer_muCorrData_*",
    "drop *_muons_muonShowerInformation_*",
    "drop *_muons_combined_*",
    "drop *_muons_csc_*",
    "drop *_muons_dt_*",
    "drop l1extraL1HFRings_*_*_*",
    "drop *_muonsFromCosmics*_*_*",
    "drop recoCaloClusters_*_*_*",
    "drop recoPreshowerCluster*_*_*_*",
    "drop *_hfRecoEcalCandidate_*_*",
    "drop *_generalV0Candidates_*_*",
    "drop *_selectDigi_*_*",
    "drop *_*BJetTags*_*_RECO",
    "drop *_castorreco_*_*",
    "drop *_reduced*RecHits*_*_*",
    "drop *_PhotonIDProd_*_*",
    "drop *_*_*photons*_*",
    "drop *_dedx*_*_*",
    "drop *_*_cosmicsVeto_*",
    "drop *_muonMETValueMapProducer_*_*",
    "drop *_BeamHaloSummary_*_*",
    "drop *_GlobalHaloData_*_*",
    "drop *_*_uncleanOnly*_*",
    "drop recoCaloMET_*_*_*",
    "drop recoConversion_*_*_*",
    "drop *_CastorTowerReco_*_*",
    "drop *_uncleanedOnlyGsfElectron*_*_*",
    "drop recoJPTJet_*_*_*",
    "drop recoPFMET_*_*_*",
    "drop *_photons_*_*",
    "drop *_photonCore_*_*",
    "drop *_hpsPFTauDiscrimination*_*_RECO",
    "drop *_hpsPFTauProducer_*_RECO",
    "drop *_recoTauAK4PFJets08Region_*_SKIM",
    "drop *_combinatoricRecoTaus_*_SKIM",
    "drop *_hpsPFTauProducerSansRefs_*_SKIM",
    "drop *_pfRecoTauTagInfoProducer_*_SKIM",
    "drop *_recoTauPileUpVertices_*_SKIM",
    "drop *_correctedHybridSuperClusters_*_*",
    "drop *_correctedMulti5x5SuperClustersWithPreshower_*_*",
    "drop *_*phPFIsoValue*04PFIdPFIso_*_*",
    "drop *_*TagInfos*_*_*",
    "drop *_*NoNu_*_*",
    "drop *_clusterSummaryProducer_*_*",
    "drop *_hcalnoise_*_*",
    "drop *_castorDigis_*_*",
    "drop *_hcalDigis_*_*",
    "drop *_tevMuons_*_*",
    "drop *_logErrorHarvester_*_*",
    "drop *_particleFlowTmp_*_*",
    "drop *_particleFlowRecHit*_*_*"
    )
  ) 

# b-tagging general configuration
process.load("RecoBTag.Configuration.RecoBTag_cff")
process.load("RecoJets.JetAssociationProducers.ak4JTA_cff")
# configure the softMuonByIP3d ESProducer and EDProducer
from RecoBTag.Configuration.RecoBTag_cff import *
from RecoBTag.SoftLepton.softLepton_cff import *
from RecoBTag.ImpactParameter.impactParameter_cff import *
from RecoBTag.SecondaryVertex.secondaryVertex_cff import *
process.impactParameterTagInfos=process.impactParameterTagInfos.clone()
process.impactParameterTagInfos.jetTracks = cms.InputTag("ak4JetTracksAssociatorAtVertex")
process.ak4JetTracksAssociatorAtVertex.jets = cms.InputTag('CleanJets','ak4PFJetsNoMu','SKIM')
process.ak4JetTracksAssociatorAtVertex.tracks = cms.InputTag("generalTracks")

	
process.btagging = cms.Sequence(
    process.ak4JetTracksAssociatorAtVertex*
    # impact parameters and IP-only algorithms
    process.impactParameterTagInfos*
    (process.trackCountingHighEffBJetTags +
     process.trackCountingHighPurBJetTags +
     process.jetProbabilityBJetTags +
     process.jetBProbabilityBJetTags +
     # SV tag infos depending on IP tag infos, and SV (+IP) based algos
     process.secondaryVertexTagInfos*
     (process.simpleSecondaryVertexHighEffBJetTags +
      process.simpleSecondaryVertexHighPurBJetTags 
#+
     # process.combinedSecondaryVertexBJetTags
     ) +
     process.ghostTrackVertexTagInfos*
     process.ghostTrackBJetTags)##  +
##     process.softPFMuonsTagInfos*
##     process.softPFMuonBJetTags *
##     process.softPFElectronsTagInfos*
##     process.softPFElectronBJetTags
)
#only proceed if event is a true W-->munu event

#require event to fire IsoMu24_eta2p1
process.TriggerAnalyzer0=cms.EDAnalyzer("TriggerAnalyzer")
process.MuonIWant = cms.EDFilter('MuonRefSelector',
                                 src = cms.InputTag('muons'),
                                 cut = cms.string('pt > 0.0'),
                                 filter = cms.bool(True)
)
process.HighestPtAndMuonOppositeSignDRSelector=cms.EDFilter('HighestPtAndMuonOppositeSignDRSelector',
                                               muonTag=cms.InputTag('MuonIWant'),
					       dRCut=cms.double(1.5),
                                               Mu2PtCut=cms.double(15.0)
)

process.Mu1Mu2PtRankMuonID=cms.EDFilter(
  'HighestSecondHighestPtSelector',
  muonTag=cms.InputTag('HighestPtAndMuonOppositeSignDRSelector'),
  vtxTag= cms.InputTag('offlinePrimaryVertices'),
  muon1ID=cms.string('tightNew'),
  muon2ID=cms.string('loose')#tightNew is another option
)

process.Mu1Mu2EtaCut=cms.EDFilter('PTETACUT',
                                 muonTag=cms.InputTag('Mu1Mu2PtRankMuonID'),
                                 Eta=cms.double(2.4),
                                 Pt=cms.double(0.0),
                                 minNumObjsToPassFilter=cms.uint32(2)

)
process.Mu1Mu2Analyzer=cms.EDAnalyzer(
  'Mu1Mu2Analyzer',
  genParticleTag=cms.InputTag('genParticles'),
  Mu1Mu2=cms.InputTag('Mu1Mu2EtaCut'),
  particleFlow=cms.InputTag('particleFlow'),
  Mu2PtBins=cms.vdouble(0.0,3.0, 6.0, 9.0, 12.0,15.0, 18.0, 21.0, 24.0, 27.0, 30.0, 33.0, 36.0, 39.0, 42.0, 48.0, 54.0, 60.0, 66.0, 72.0, 78.0, 84.0, 90.0, 96.0, 102.0, 108.0,116.0, 124.0, 130.0, 136.0, 142.0, 148.0, 154.0, 160.0, 166.0, 172.0, 180.0, 186.0, 192.0, 200.0 ),
  invMassBins=cms.vdouble(0.0 ,20.0,40.0,60.0, 80.0,100.0,120.0,140,160,180,200,500)

)
process.PtEtaCut = cms.EDFilter('PTETACUT',
                                 muonTag=cms.InputTag('Mu1Mu2EtaCut'),
                                 Eta=cms.double(2.1),
                                 Pt=cms.double(45.0),
                                 minNumObjsToPassFilter=cms.uint32(1)
)
process.genAMuSelector=cms.EDFilter(
 'GenObjectProducer',
    genParticleTag = cms.InputTag('genParticles'),
    absMatchPDGIDs = cms.vuint32(MU_PDGID),     #choose a gen muon...
    sisterAbsMatchPDGID = cms.uint32(MU_PDGID), #...whose sister is another gen muon...
    genTauDecayIDPSet = AMuMuPSet,              #...and whose mother is a pseudoscalar a
    primaryTauDecayType = cms.uint32(TAU_ALL),  #choose TAU_ALL when the gen particle is not a tau
    sisterTauDecayType = cms.uint32(TAU_ALL),   #choose TAU_ALL when the gen particle sister is not a tau
    primaryTauPTRank = cms.int32(ANY_PT_RANK),  #should always be ANY_PT_RANK
    primaryTauHadronicDecayType = cms.int32(TAU_ALL_HAD), #choose TAU_ALL_HAD when the gen particle is not a tau
    sisterHadronicDecayType = cms.int32(TAU_ALL_HAD),     #choose TAU_ALL_HAD when the gen particle sister is not a tau
    primaryTauAbsEtaMax = cms.double(-1.0), #no cut on gen particle |eta|
    primaryTauPTMin = cms.double(-1.0),     #no cut on gen particle pT
    countSister = cms.bool(True),           #True if you want to put both muons in the output collection, False if just one
    applyPTCuts = cms.bool(False),          #should always be False
    countKShort = cms.bool(False),          #should always be False
    minNumGenObjectsToPassFilter = cms.uint32(2), #EDFilter only returns true if >=2 muons are found
    makeAllCollections = cms.bool(False) #should always be False
    )
process.genTauMuSelector = cms.EDFilter(
    'GenObjectProducer',
    genParticleTag = cms.InputTag('genParticles'),
    absMatchPDGIDs = cms.vuint32(TAU_PDGID),     #choose a gen tau...
    sisterAbsMatchPDGID = cms.uint32(TAU_PDGID), #...whose sister is another gen tau...
    genTauDecayIDPSet = ATauTauPSet,             #...and whose mother is a pseudoscalar a
    primaryTauDecayType = cms.uint32(TAU_MU),    #primary tau decay mode is mu...
    sisterTauDecayType = cms.uint32(TAU_HAD),    #...sister tau decay mode is hadronic
    primaryTauPTRank = cms.int32(ANY_PT_RANK),  #should always be ANY_PT_RANK
    primaryTauHadronicDecayType = cms.int32(TAU_ALL_HAD), #choose TAU_ALL_HAD when the tau decay type is non-hadronic
    sisterHadronicDecayType = cms.int32(TAU_ALL_HAD),     #choose TAU_ALL_HAD when the tau decay type is hadronic and you want any hadronic mode
    primaryTauAbsEtaMax = cms.double(2.1),  #|eta| < 2.1 on muon from tau-->mu
    primaryTauPTMin = cms.double(5.0),      #pT > 5 GeV on muon from tau-->mu
    countSister = cms.bool(False),          #only put the muon from tau-->mu in the output collection (i.e. the object in the output collection will be the gen particle with |PDG ID| = 13 and status = 1 that is decayed from the tau
    applyPTCuts = cms.bool(False),          #should always be False
    countKShort = cms.bool(False),          #should always be False
    minNumGenObjectsToPassFilter = cms.uint32(1), #EDFilter only returns true if >=1 tau-->mu is found satisfying pT, |eta|, and decay mode cuts
    makeAllCollections = cms.bool(False) #should always be False
    )


process.filter_1 = hlt.hltHighLevel.clone(
    TriggerResultsTag=cms.InputTag("TriggerResults", "","HLT" ),
    HLTPaths = [ 'HLT_Mu45_eta2p1_v3'],
    throw = True
    )
process.genMatchedSelector = cms.EDFilter(
    'GenMatchedMuonProducer',
    genParticleTag = cms.InputTag('genParticles'),
    selectedGenParticleTag = cms.InputTag('genAMuSelector'), #must be a reco::GenParticleRefVector
    recoObjTag = cms.InputTag('PtEtaCut'),              #must be a reco::MuonRefVector
    baseRecoObjTag = cms.InputTag('muons'),
    genTauDecayIDPSet = AMuMuPSet,      #need to know the pseudoscalar a mother
    applyPTCuts = cms.bool(False),        #should always be false
    countKShort = cms.bool(False),        #should always be false
    dR = cms.double(0.01),
    Bins=cms.vdouble(2.0,4.0),                 #dR criteria for matching
    minNumGenObjectsToPassFilter = cms.uint32(1) #EDFilter returns true if >=1 gen-matched reco muon is found
    )
                                

process.Mu45Selector = cms.EDFilter(
    'MuonTriggerObjectFilter',
    recoObjTag = cms.InputTag('PtEtaCut'),
    genParticleTag = cms.InputTag('genParticles'),
    triggerEventTag = cms.untracked.InputTag("hltTriggerSummaryAOD", "", "HLT"),#for sure it's HLT2 since this is the only tuple in edmDumpEventContent
    triggerResultsTag = cms.untracked.InputTag("TriggerResults", "", "HLT"),#selections are only SIM, RECO or HLT2
    MatchCut = cms.untracked.double(0.01),
    hltTags = cms.VInputTag(cms.InputTag("HLT_Mu45_eta2p1_v2", "", "HLT")
                            ),
    theRightHLTTag = cms.InputTag("HLT_Mu45_eta2p1_v2","","HLT"),#TTBar background is v2
    theRightHLTSubFilter1 = cms.InputTag("hltL3fL1sMu16orMu25L1f0L2f10QL3Filtered45e2p1Q","","HLT"),#v2
    # theRightHLTSubFilter1 = cms.InputTag("hltL3fL1sMu22Or25L1f0L2f10QL3Filtered45e2p1Q","","HLT"), #v3
    HLTSubFilters = cms.untracked.VInputTag(""),
    minNumObjsToPassFilter1= cms.uint32(1),
    outFileName=cms.string("Mu45Selector.root")
)

process.AMuTriggerAnalyzer=cms.EDAnalyzer(
   'AMuTriggerAnalyzer',
   GenMatchedRecoMuonTag= cms.InputTag('genMatchedSelector'),
   selectedGenParticleTag=cms.InputTag('genAMuSelector'),
   MuPassTrigger=cms.InputTag('Mu45Selector'),
   dRBins=cms.vdouble(0.0, 0.02, 0.04,0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18),
   PtBins=cms.vdouble(0.0,0.5, 10.0, 15.0, 20.0, 30.0,40.0,60.0,80.0, 100.0, 200.0,300.0,400.0,500.0),
   EtaBins=cms.vdouble(-5.0,-4.0,-3.0,-2.0,-1.8, -1.6, -1.4, -1.2, -1.0,-0.8, -0.6, -0.4, -0.2, 0.0,0.2, 0.4, 0.6, 0.8, 1.0,1.2, 1.4, 1.6, 1.8, 2.0,3.0,4.0,5.0)
)

process.Mu3=cms.EDFilter('VetoMuon',
  muonTag=cms.InputTag('MuonIWant'),
  vetoMuonTag=cms.InputTag('Mu1Mu2EtaCut'),
  dRCut=cms.double(0.5),
  genParticleTag = cms.InputTag('genParticles'),
  minNumObjsToPassFilter=cms.uint32(1)
)

process.Mu3ID = cms.EDFilter('CustomMuonSelector',
                                       baseMuonTag = cms.InputTag('muons'),
                                       muonTag = cms.InputTag('Mu3'),
                                       vtxTag = cms.InputTag('offlinePrimaryVertices'),
                                       muonID = cms.string('loose'),
                                       PFIsoMax = cms.double(-1),
                                       detectorIsoMax = cms.double(-1.0),
                                       PUSubtractionCoeff = cms.double(0.5),
                                       usePFIso = cms.bool(True),
                                       passIso = cms.bool(True),
                                       etaMax = cms.double(2.4),
                                       minNumObjsToPassFilter = cms.uint32(1)
                                       )
process.tauMuonPtSelector=cms.EDFilter('PTETACUT',
                                 muonTag=cms.InputTag('Mu3ID'),
                                 Eta=cms.double(2.4),
                                 Pt=cms.double(5.0),
                                 minNumObjsToPassFilter=cms.uint32(1)
)
process.tauMuonAnalyzer=cms.EDAnalyzer(
 	'tauMuonAnalyzer',
 	genParticleTag = cms.InputTag('genParticles'),
	thirdHighestPtMuon=cms.InputTag('tauMuonPtSelector'),
	Mu1Mu2=cms.InputTag('Mu1Mu2MassSelection'),
        Mu3PtBins=cms.vdouble(0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0, 200.0, 300.0),
        Mu3dRBins=cms.vdouble(0.0, 0.4, 0.8, 1.2, 1.6,2.0, 2.4, 2.8, 3.2, 3.6, 4.0,  4.4, 4.8, 5.2)

)
process.genMatchedTauMuSelector = cms.EDFilter(
    'GenMatchedMuonProducer',
    genParticleTag = cms.InputTag('genParticles'),
    selectedGenParticleTag = cms.InputTag('genTauMuSelector'), #must be a reco::GenParticleRefVector
    recoObjTag = cms.InputTag('Mu3ID'),              #must be a reco::MuonRefVector
    baseRecoObjTag = cms.InputTag('muons'),
    genTauDecayIDPSet = AMuMuPSet,      #need to know the pseudoscalar a mother
    applyPTCuts = cms.bool(False),        #should always be false
    countKShort = cms.bool(False),        #should always be false
    dR = cms.double(0.05),
    Bins=cms.vdouble(2.0,4.0),                 #dR criteria for matching
    minNumGenObjectsToPassFilter = cms.uint32(1) #EDFilter returns true if >=1 gen-matched reco muon is found
    )
#search for a muon with pT > 25 GeV as in WHbb CMS AN-2012/349 and proceed if one can be found
#this will produce a ref to the original muon collection

#produce photon isolations

#search for a tight PF isolated tight muon in |eta| < 2.1 with pT > 25 GeV
#(see https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuonId#Muon_Isolation_AN1 for
#isolation definition; CMS AN-2012/349 uses loose isolation working point for WHbb muon selection)
#this will produce a ref to the original muon collection

#search for a muon with pT > 5 GeV as in HZZ4l analysis and proceed if one can be found
#this will produce a ref to the original muon collection

#search for soft muons
#(see https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuonId#Soft_Muon) not overlapping with
#the W muon in |eta| < 2.4
#this will produce a ref to the original muon collection

#clean the jets of soft muons, then rebuild the taus

process.CleanJets.muonSrc=cms.InputTag('tauMuonPtSelector') # 
process.CleanJets.PFCandSrc = cms.InputTag('particleFlow')
process.CleanJets.cutOnGenMatches = cms.bool(False)
process.CleanJets.outFileName = cms.string('CleanJets.root')
process.ak4PFJetTracksAssociatorAtVertex.jets = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'SKIM')
process.recoTauAK4PFJets08Region.src = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'SKIM')
process.ak4PFJetsLegacyHPSPiZeros.jetSrc = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'SKIM')
process.ak4PFJetsRecoTauChargedHadrons.jetSrc = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'SKIM')
process.combinatoricRecoTaus.jetSrc = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'SKIM')

process.recoTauCommonSequence = cms.Sequence(   process.Mu3*
						process.Mu3ID*
						process.tauMuonPtSelector*
						process.CleanJets*
						process.ak4PFJetTracksAssociatorAtVertex*
						process.recoTauAK4PFJets08Region*
						process.recoTauPileUpVertices*
						process.pfRecoTauTagInfoProducer
)

process.PFTau = cms.Sequence(process.recoTauCommonSequence*process.recoTauClassicHPSSequence) # Kyle Changed  This

from RecoBTag.Configuration.RecoBTag_cff import *
from RecoBTag.SoftLepton.softLepton_cff import *
from RecoBTag.ImpactParameter.impactParameter_cff import *
from RecoBTag.SecondaryVertex.secondaryVertex_cff import *
from RecoBTag.Combined.combinedMVA_cff import *
from RecoBTag.CTagging.RecoCTagging_cff import *
from RecoVertex.AdaptiveVertexFinder.inclusiveVertexing_cff import *
process.pfImpactParameterTagInfos.jets = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'SKIM')
process.softPFMuonsTagInfos.jets = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'SKIM')
process.softPFElectronsTagInfos.jets = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'SKIM')

process.pfBTagging = cms.Sequence(
    (
      # impact parameters and IP-only algorithms
      pfImpactParameterTagInfos *
      ( pfTrackCountingHighEffBJetTags +
        pfJetProbabilityBJetTags +
        pfJetBProbabilityBJetTags +

        # SV tag infos depending on IP tag infos, and SV (+IP) based algos
        pfSecondaryVertexTagInfos *
        ( pfSimpleSecondaryVertexHighEffBJetTags +
          pfCombinedSecondaryVertexV2BJetTags
        )
        + inclusiveCandidateVertexing *
        pfInclusiveSecondaryVertexFinderTagInfos *
        pfSimpleInclusiveSecondaryVertexHighEffBJetTags *
        pfCombinedInclusiveSecondaryVertexV2BJetTags

      ) +

      # soft lepton tag infos and algos
      softPFMuonsTagInfos *
      softPFMuonBJetTags
      + softPFElectronsTagInfos *
      softPFElectronBJetTags
    ) *

    # overall combined taggers
    ( #CSV + soft-lepton + jet probability discriminators combined
      pfCombinedMVAV2BJetTags

    )
)

#find taus in |eta| < 2.4 matched to muon-tagged cleaned jets
#this will produce a ref to the cleaned tau collection
process.muHadTauSelector = cms.EDFilter(
    'CustomTauSepFromMuonSelector',
    baseTauTag = cms.InputTag('hpsPFTauProducer', '', 'SKIM'),
    tauHadIsoTag = cms.InputTag('hpsPFTauDiscriminationByCombinedIsolationDeltaBetaCorrRaw3Hits', '',
                                'SKIM'),
    tauDiscriminatorTags = cms.VInputTag(
    cms.InputTag('hpsPFTauDiscriminationByDecayModeFindingNewDMs', '', 'SKIM')
    #cms.InputTag('hpsPFTauDiscriminationByMediumIsolationMVArun2v1DBnewDMwLT','','SKIM')
    ),
    jetTag = cms.InputTag('CleanJets', 'ak4PFJetsNoMu', 'SKIM'),
    muonRemovalDecisionTag = cms.InputTag('CleanJets','valMap','SKIM'),
    overlapCandTag = cms.InputTag('Mu45Selector'),
    overlapCandTag1= cms.InputTag('HighestPtAndMuonOppositeSignDR'),
    passDiscriminator = cms.bool(True),
    pTMin = cms.double(10.0),
    etaMax = cms.double(2.4),
    isoMax = cms.double(-1.0),
    dR = cms.double(0.5),
    minNumObjsToPassFilter = cms.uint32(1),
    outFileName=cms.string('muHadTauSelector.root')
    )
process.RECOAnalyze=cms.EDAnalyzer(
        'MuMuTauTauRecoAnalyzer',
        tauTag=cms.InputTag('muHadTauSelector','','SKIM'),
        jetMuonMapTag=cms.InputTag('CleanJets','muonValMap','SKIM'),
        Mu1Mu2= cms.InputTag('Mu1Mu2MassSelection'),
        genParticleTag=cms.InputTag('genParticles'),
        muHadMassBins=cms.vdouble(0.0, 2.0, 4.0, 6.0, 8.0, 10.0,12.0, 20.0),
        FourBInvMassBins=cms.vdouble(0.0, 200.0,400.0,600.0, 800.0, 1000.0)
)
#output
process.noSelectedOutput = cms.OutputModule(
    "PoolOutputModule",
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('p')),
    outputCommands = skimEventContent.outputCommands,
    fileName = cms.untracked.string('ZZ_data_no_selection.root')
    )

#sequences
process.MuMuSequenceSelector=cms.Sequence(
#       process.TriggerAnalyzer0*
	process.MuonIWant*
        process.HighestPtAndMuonOppositeSignDRSelector*
        process.Mu1Mu2PtRankMuonID*
        process.Mu1Mu2EtaCut*
        process.PtEtaCut*
        process.Mu45Selector
#        process.tauMuonAnalyzer
)

process.noSelectionSequence = cms.Sequence(process.MuMuSequenceSelector*
                                           process.PFTau*
                                           process.pfBTagging*
                                           process.muHadTauSelector
                                          # process.tauMuonAnalyzer*
                                          # process.btagging
                                          # process.RECOAnalyze
)

## #selection path
## process.p = cms.Path(process.selectionSequence)
## process.e = cms.EndPath(process.selectedOutput)

#anti-selection path
## process.p = cms.Path(process.antiSelectionSequence)
## process.e = cms.EndPath(process.antiSelectedOutput)
process.TFileService = cms.Service("TFileService",
    fileName =  cms.string('ZZ_HLTSubfilter_Tfile.root')
)
#no selection path
process.p = cms.Path(process.noSelectionSequence)
process.e = cms.EndPath(process.noSelectedOutput)
