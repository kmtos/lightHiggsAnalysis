import subprocess
import sys
import fileinput
import os
def getFileList(inDir, inputName):
    tempfile = open(inputName,'w')
    cmd = 'find ' + inDir + ' -mindepth 2 -maxdepth 2'+' -name *TFile*.root'
    #cmd = 'find ' + inDir + ' -mindepth 2 -maxdepth 2'+' -name *Tfile*.root'
    print cmd
    process = subprocess.Popen(cmd.split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    tempfile.write(process.communicate()[0])
    tempfile.close()
    for line in fileinput.input([inputName], inplace=True):
        sys.stdout.write('root://eoscms/{l}'.format(l=line))
    

inputName_='testscript.txt'
#inDir_='/eos/cms/store/group/phys_higgs/HiggsExo/mshi/SingleMuon/data_RegionB_Zhadd_Mu1Mu2ptCut1/170815_175327/'
#inDir_='/eos/cms/store/group/phys_higgs/HiggsExo/mshi/SingleMuon/data_RegionB_Zhadd_Mu1Mu2ptCut1_Mu50/170816_162814/'
#inDir_='/eos/cms/store/group/phys_higgs/HiggsExo/mshi/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/DYHighMass_Mu1Mu2PtCut/170815_174714'
#inDir_='/eos/cms/store/group/phys_higgs/HiggsExo/mshi/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/DYHighMass_Mu1Mu2PtCut_Mu50/170816_162938'
#inDir_='/eos/cms/store/group/phys_higgs/HiggsExo/mshi/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/DYHighMass_Double/170829_212552'
inDir_='/eos/cms/store/group/phys_higgs/HiggsExo/mshi/DoubleMuon/data_RegionC_DoubleLooseIsoNewNLOCorr4/170912_223047'
getFileList(inDir_,inputName_)

