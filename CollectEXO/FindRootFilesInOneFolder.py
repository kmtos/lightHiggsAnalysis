import subprocess
import sys
import fileinput
def getFileList(inDir, inputName):
    tempfile = open(inputName,'a+')
    cmd = 'find ' + inDir + ' -name *selection*.root'
    print cmd
    process = subprocess.Popen(cmd.split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    tempfile.write(process.communicate()[0])
    tempfile.close()
    for line in fileinput.input([inputName], inplace=True):
        sys.stdout.write('root://eoscms/{l}'.format(l=line))
    

inputName_='testscript.txt'
inDir_= '/eos/cms/store/group/phys_higgs/HiggsExo/mshi/SingleMuon/data_RegionBWithMassCut/170519_234905'
getFileList(inDir_,inputName_)

