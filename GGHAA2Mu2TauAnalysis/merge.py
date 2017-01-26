import FWCore.ParameterSet.Config as cms
from subprocess import *

process = cms.Process("MERGE")

#verbosity
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
    )

#input
import FWCore.Utilities.FileUtils as FileUtils
mylist = FileUtils.loadListFromFile('testDrellYan.txt')
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
    )
process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(*mylist)
    )

#output
process.output = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string('MergeFilesDrellYan.root')
    )

#path
process.e = cms.EndPath(process.output)
