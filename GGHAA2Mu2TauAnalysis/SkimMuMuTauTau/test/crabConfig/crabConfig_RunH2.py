from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'SameSign_RunH2_MedIsoMu2_TauDMAntiMedIso_APR22'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../SkimSequence/NewMiniAOD_Skim.py' 
config.JobType.numCores = 4
config.JobType.maxMemoryMB = 8000

config.Data.inputDataset = '/SingleMuon/ktos-SameSign_MiniAOD_Run2016H-PromptReco-v2_MINIAODoutput-4b7f5c12d9d2a42a12c7cbb69b70e9f8/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'Automatic'
config.Data.unitsPerJob = 1080
config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
config.Data.outLFNDirBase = '/store/user/ktos/' 
config.Data.publication = True
config.Data.outputDatasetTag = 'SameSign_RunH2_MedIsoMu2_TauDMAntiMedIso_APR22'

config.Site.storageSite = 'T2_CH_CERN'
