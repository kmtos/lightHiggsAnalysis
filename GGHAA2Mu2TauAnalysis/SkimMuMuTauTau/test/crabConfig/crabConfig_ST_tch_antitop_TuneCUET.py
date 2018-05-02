from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'MiniAOD_ST_tch_antitop_TuneCUET_MedIsoMu2_TauDMAntiMedIso_APR30'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../SkimSequence/NewMiniAOD_Skim.py'

config.Data.inputDataset = '/ST_t-channel_antitop_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin/dntaylor-2017-11-03_Skim_MuMuTauTau_v4_MINIAODoutput-a6b69b8e27a72c8d16ba62a9c88868dd/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 20
config.Data.outLFNDirBase = '/store/group/phys_higgs/HiggsExo/ktos'
config.Data.publication = True
config.Data.outputDatasetTag = 'MiniAOD_ST_tch_antitop_TuneCUET_MedIsoMu2_TauDMAntiMedIso_APR30'

config.Site.storageSite = 'T2_CH_CERN'
