import subprocess
def getLogFile(inDir):
    tempfile = open('tmpFile.txt','w')
    cmd_all='find ' + inDir + ' -maxdepth 5 -mindepth 5 -name log'
    print cmd_all
    process_all=subprocess.Popen(cmd_all.split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    tempfile.write(process_all.communicate()[0])
    tempfile.close()
inDir='/eos/cms/store/group/phys_higgs/HiggsExo/mshi'
#inDir='/eos/cms/store/user/mshi'
getLogFile(inDir)
