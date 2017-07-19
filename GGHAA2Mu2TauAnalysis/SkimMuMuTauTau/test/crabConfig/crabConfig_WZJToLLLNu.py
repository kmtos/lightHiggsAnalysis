from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'WZJToLLLNu_Skim_EXO'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../SkimSequence/TestRegionsSkim_Crab.py'

config.Data.inputDataset = '/WZJToLLLNu_TuneCUETP8M1_13TeV-amcnlo-pythia8/RunIISpring16reHLT80-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/AODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outLFNDirBase = '/store/group/phys_higgs/HiggsExo/ktos'
config.Data.publication = True
config.Data.outputDatasetTag = 'WZJToLLLNu_skim'

config.Site.storageSite = 'T2_CH_CERN'
