#################
# Initialization
#################
import FWCore.ParameterSet.Config as cms
import FWCore.Utilities.FileUtils as FileUtils
process = cms.Process("CleanJetsAnalyzer")
mylist = FileUtils.loadListFromFile('/afs/cern.ch/user/k/ktos/NewSkimDir/CMSSW_8_0_30/src/GGHAA2Mu2TauAnalysis/SkimMuMuTauTau/test/SkimSequence/SummedWeightsFiles/TXT_INPUT_FILE')

###################################################
# initialize MessageLogger and output report
###################################################
process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)
process.options   = cms.untracked.PSet( 
		wantSummary = cms.untracked.bool(True), 
		SkipEvent = cms.untracked.vstring('ProductNotFound')
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

####################
# Input File List
####################
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(*mylist))

process.lumiTree = cms.EDAnalyzer("LumiTree",
    genEventInfo = cms.InputTag("generator"),
    nevents = cms.InputTag('lumiSummary','numberOfEvents'),
    summedWeights = cms.InputTag('lumiSummary','sumOfWeightedEvents')
)

process.antiSelectedOutput = cms.OutputModule(
    "PoolOutputModule",
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('p')),
    fileName = cms.untracked.string('FINAL_DIRNAME.root')
    )
process.TFileService = cms.Service("TFileService",
    fileName =  cms.string('TFiledataZ.root')
)

#########################################################
# this will produce a ref to the original muon collection
#########################################################
process.p = cms.Path(process.lumiTree)
process.e = cms.EndPath(process.antiSelectedOutput)

