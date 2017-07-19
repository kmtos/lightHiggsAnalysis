from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'LowMassDYOld_Skim_all_EXO'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../LowMassDYDiMuSelectionSkim.py'

config.Data.inputDataset = '/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16DR80-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/AODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outLFNDirBase = '/store/group/phys_higgs/HiggsExo/ktos'
config.Data.publication = True
config.Data.outputDatasetTag = 'LowMassDYOld_skim'

config.Site.storageSite = 'T2_CH_CERN'
