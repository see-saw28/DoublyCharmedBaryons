j = Job()
debug = 0
max_files = -1
files_per_job = 100
if debug:
    max_files = 2
    files_per_job = 4
# First time
#https://lhcb.github.io/first-analysis-steps/davinci-grid.html
myApp = prepareGaudiExec('DaVinci','v44r7', myPath='.')
# myApp = GaudiExec()
# myApp.directory = "../Xicc/DaVinciDev_v46r5"
j.application = myApp
#j.application.options = ["Xicst_Spectroscopy_LcK_Turbo2016.py"]
j.application.options = ["DV_Xicst_Emmy.py"]
# j.application.platform = 'x86_64_v2-centos7-gcc11-opt'
#j = Job(t)
j.backend=Dirac()
j.splitter=SplitByFiles(filesPerJob=files_per_job, maxFiles = max_files, ignoremissing = True)
j.outputfiles = [DiracFile('*.root'), LocalFile('stdout')]
#j.outputfiles = [LocalFile('*.root')]
j.do_auto_resubmit = True
###################
#j.name = 'Xicst_2015'
##j.application.readInputData("~/Data_LHCb/Turbo/2015/LHCbCollision15Beam6500GeV-VeloClosed-MagDownRealDataTurbo02RawRemoved94000000TURBOMDST.py")
#j.inputdata = BKQuery('/LHCb/Collision15/Beam6500GeV-VeloClosed-MagDown/Real Data/Turbo02/RawRemoved/94000000/TURBO.MDST').getDataset()
#j.submit()
#j = j.copy()
##j.application.readInputData("~/Data_LHCb/Turbo/2015/LHCbCollision15Beam6500GeV-VeloClosed-MagUpRealDataTurbo02RawRemoved94000000TURBOMDST.py")
#j.inputdata = BKQuery('/LHCb/Collision15/Beam6500GeV-VeloClosed-MagUp/Real Data/Turbo02/RawRemoved/94000000/TURBO.MDST').getDataset()
#j.submit()
########
# j.name = 'Xicst_2016'
#j.application.readInputData("~/Data_LHCb/Turbo/2016/LHCbCollision16Beam6500GeV-VeloClosed-MagDownRealDataTurbo0394000000CHARMSPECPARKEDMDST.py")
#j.inputdata = BKQuery('/LHCb/Collision16/Beam6500GeV-VeloClosed-MagDown/Real Data/Turbo03a/94000000/CHARMSPECPARKED.MDST').getDataset()
#j.submit()
#j = j.copy()
##j.application.readInputData("~/Data_LHCb/Turbo/2016/LHCbCollision16Beam6500GeV-VeloClosed-MagUpRealDataTurbo0394000000CHARMSPECPARKEDMDST.py")
# j.inputdata = BKQuery('/LHCb/Collision16/Beam6500GeV-VeloClosed-MagUp/Real Data/Turbo03a/94000000/CHARMSPECPARKED.MDST').getDataset()
# j.submit()
########
j.name = 'Xicst_2017_oldDV'
#j.inputdata = BKQuery('/LHCb/Collision17/Beam6500GeV-VeloClosed-MagDown/Real Data/Turbo04/94000000/CHARMSPEC.MDST').getDataset()
#j.submit()
#j = j.copy()
j.inputdata = BKQuery('/LHCb/Collision17/Beam6500GeV-VeloClosed-MagUp/Real Data/Turbo04/94000000/CHARMSPEC.MDST').getDataset()
j.submit()
