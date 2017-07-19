from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'TTBar_NoIsoDiTau_MAY25'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../SkimSequence/TestRegionsSkim_Crab_HLT2.py'

config.Data.inputDataset = '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16reHLT80-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/AODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 9700
config.Data.totalUnits = 3000000
config.Data.outLFNDirBase = '/store/group/phys_higgs/HiggsExo/ktos'
config.Data.publication = True
config.Data.outputDatasetTag = 'TTBar_NoIsoDiTau_MAY25'

config.Site.storageSite = 'T2_CH_CERN'
