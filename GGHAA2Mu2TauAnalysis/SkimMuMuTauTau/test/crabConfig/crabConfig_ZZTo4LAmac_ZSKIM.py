from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'MiniAOD_ZZTo4LAmac_Mu1Only_ZSKIM_APR30'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../SkimSequence/NewMiniAOD_Skim_ZSKIM.py'

config.Data.inputDataset = '/ZZTo4L_13TeV-amcatnloFXFX-pythia8/dntaylor-2017-11-03_Skim_MuMuTauTau_v4_MINIAODoutputZSKIM-a6b69b8e27a72c8d16ba62a9c88868dd/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 20
config.Data.outLFNDirBase = '/store/group/phys_higgs/HiggsExo/ktos'
config.Data.publication = True
config.Data.outputDatasetTag = 'MiniAOD_ZZTo4LAmac_Mu1Only_ZSKIM_APR30'

config.Site.storageSite = 'T2_CH_CERN'
