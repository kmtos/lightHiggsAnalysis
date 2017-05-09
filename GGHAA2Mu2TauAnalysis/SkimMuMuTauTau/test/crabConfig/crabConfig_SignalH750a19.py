from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'SignalH750a19_SameSign_IsoDiTau'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../SkimSequence/FakeRateFromQCD_Signal.py'

config.Data.inputDataset = ''
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outLFNDirBase = '/store/user/mshi'
config.Data.publication = True
config.Data.outputDatasetTag = 'SignalH750a19_SameSign_IsoDiTau'

config.Site.storageSite = 'T2_CH_CERN'
