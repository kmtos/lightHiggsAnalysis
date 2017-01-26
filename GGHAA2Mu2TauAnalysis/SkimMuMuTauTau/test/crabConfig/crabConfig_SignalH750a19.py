from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'request_SignalH750a19_Skim_all_EXO2'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../SignalDiMuSelectionSkim.py'

config.Data.inputDataset = ''
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outLFNDirBase = '/store/group/phys_higgs/HiggsExo/mshi'
config.Data.publication = True
config.Data.outputDatasetTag = 'CRAB3_SignalH750a19_skim'

config.Site.storageSite = 'T2_CH_CERN'
