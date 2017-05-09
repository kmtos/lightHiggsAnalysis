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
inDir_= '/eos/cms/store/user/mshi/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/'
getFileList(inDir_,inputName_)

