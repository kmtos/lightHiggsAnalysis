from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'RequestName'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../SkimSequence/Background_Sequence.py'

config.Data.inputDataset = 'InputDataset'
config.Data.inputDBS = 'global'
config.Data.splitting = 'WhichBased'
config.Data.unitsPerJob = 100
config.Data.outLFNDirBase = '/store/group/phys_higgs/HiggsExo/mshi'
config.Data.publication = True
config.Data.outputDatasetTag = 'OutputName'

config.Site.storageSite = 'T2_CH_CERN'
