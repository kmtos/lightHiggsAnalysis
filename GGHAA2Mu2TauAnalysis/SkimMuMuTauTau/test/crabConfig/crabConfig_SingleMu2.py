from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'MiniAOD_SingleMu2_MedIsoMu2_TauDMAntiMedIso_APR30'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../SkimSequence/NewMiniAOD_Skim.py' 

config.Data.inputDataset = '/SingleMuon/dntaylor-2017-11-03_Skim_MuMuTauTau_v4_MINIAODoutput-9408cb376698ca4c8373be9e4ccdc2e4/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 100
config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
config.Data.outLFNDirBase = '/store/group/phys_higgs/HiggsExo/ktos/' #'/store/group/phys_higgs/HiggsExo/ktos/' #'/store/group/phys_higgs/HiggsExo/ktos/' #'/store/group/phys_higgs/HiggsExo/ktos/'
config.Data.publication = True
config.Data.outputDatasetTag = 'MiniAOD_SingleMu2_MedIsoMu2_TauDMAntiMedIso_APR30'

config.Site.storageSite = 'T2_CH_CERN'
