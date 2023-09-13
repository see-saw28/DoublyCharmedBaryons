the_year = 2016
polarity = 'MU'
j = Job(name=f'Excited-WS-Data-{the_year}-{polarity}')
myApp = GaudiExec()
myApp.directory = "/afs/cern.ch/user/p/pgaigne/xiccpp/Xicc/DaVinciDev_v46r5"
j.application = myApp
j.application.options = [f'ExcitedBaryons_Collision_Run2.py']
j.inputfiles = [LocalFile("TMVAClassification_BDT_diff.weights.xml")]
j.application.platform = 'x86_64_v2-centos7-gcc11-opt'
j.parallel_submit = True
j.do_auto_resubmit = True
if the_year == 2016:
    if polarity == 'MD':
        bkPath = '/LHCb/Collision16/Beam6500GeV-VeloClosed-MagDown/Real Data/Turbo03a/94000000/CHARMSPECPARKED.MDST'
    else :
        bkPath = '/LHCb/Collision16/Beam6500GeV-VeloClosed-MagUp/Real Data/Turbo03a/94000000/CHARMSPECPARKED.MDST'

elif the_year == 2017:
    if polarity == 'MD':
        bkPath = '/LHCb/Collision17/Beam6500GeV-VeloClosed-MagDown/Real Data/Turbo04/94000000/CHARMSPEC.MDST'
    else :
        bkPath = '/LHCb/Collision17/Beam6500GeV-VeloClosed-MagUp/Real Data/Turbo04/94000000/CHARMSPEC.MDST'

elif the_year == 2018:
    if polarity == 'MD':
        bkPath = '/LHCb/Collision18/Beam6500GeV-VeloClosed-MagDown/Real Data/Turbo05/94000000/CHARMINCLBARYON.MDST'
    else :
        bkPath = '/LHCb/Collision18/Beam6500GeV-VeloClosed-MagUp/Real Data/Turbo05/94000000/CHARMINCLBARYON.MDST'


data  = BKQuery(bkPath).getDataset()
j.inputdata = data
j.backend = Dirac()
if the_year == 2016 :
    j.splitter = SplitByFiles(filesPerJob=100) #25-27k files 
elif the_year == 2017 :
    j.splitter = SplitByFiles(filesPerJob=50)#13k files 
else :
    j.splitter = SplitByFiles(filesPerJob=20)#6k files 
j.outputfiles = [DiracFile('*.root'), LocalFile('stdout')]
#j.postprocessors.append(RootMerger(files = ['DV_Xiccpp_MC_2016.root'],args='-fk'))
j.submit()
