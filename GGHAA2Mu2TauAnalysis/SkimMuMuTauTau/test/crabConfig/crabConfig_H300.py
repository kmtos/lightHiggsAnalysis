from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'MiniAOD_SIG_h300a21_MedIsoMu2_TauDMAntiMedIso_APR30'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../SkimSequence/NewMiniAOD_Skim.py' #_HLT2.py'

config.Data.inputDataset = '/SUSYGluGluToHToAA_AToMuMu_AToTauTau_M-300_M-21_TuneCUETP8M1_13TeV_madgraph_pythia8/dntaylor-2017-11-03_Skim_MuMuTauTau_v4_MINIAODoutput-a6b69b8e27a72c8d16ba62a9c88868dd/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/group/phys_higgs/HiggsExo/ktos/' #'/store/group/phys_higgs/HiggsExo/ktos/' #'/store/group/phys_higgs/HiggsExo/ktos/' #'/store/group/phys_higgs/HiggsExo/ktos/'
config.Data.publication = True
config.Data.outputDatasetTag = 'MiniAOD_SIG_h300a21_MedIsoMu2_TauDMAntiMedIso_APR30'

config.Site.storageSite = 'T2_CH_CERN'
#config.Site.blacklist = ['T2_CH_CSCS_HPC']
