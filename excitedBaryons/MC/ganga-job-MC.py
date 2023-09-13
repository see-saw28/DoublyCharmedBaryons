"""if len(sys.argv)>1:
    the_year = sys.argv[1]
    polarity = sys.argv[2]
    mass = sys.argv[3]

    if the_year not in ['2016','2017','2018']:
        print ("\n## THIS SCRIPT IS FOR RUN2 ONLY ##\n")
        sys.exit()
    if polarity not in ['MU', 'MD']:
        print ("\n## THIS SCRIPT IS FOR MagUp and MagDown ##\n")
        sys.exit()

    if mass not in ['3800', '3900', '4000']:
        print ("\n## Please select mass of (3800, 3900, 4000) ##\n")
        sys.exit()
    
    else :
        if mass == '3800':
            evt_type = 26167051
        elif mass == '3900':
            evt_type = 26167052
        elif mass == '4000':
            evt_type = 26167053
            """



the_year = 2016
polarity = 'MU'
evt_type = 26167051

if evt_type == 26167051:
    mass = '3800'
elif evt_type == 26167052:
    mass = '3900'
elif evt_type == 26167053:
    mass = '4000'

if evt_type == 26167054:
    mass = '4150'
elif evt_type == 26167055:
    mass = '4250'
elif evt_type == 26167056:
    mass = '4350'

if evt_type<26167054:
    j = Job(name=f'Xiccp{mass}-MC-{the_year}-{polarity}')
else :
    j = Job(name=f'Omegaccp{mass}-MC-{the_year}-{polarity}')

    
myApp = GaudiExec()
myApp.directory = "/afs/cern.ch/user/p/pgaigne/xiccpp/Xicc/DaVinciDev_v46r5"
j.application = myApp
j.application.options = ['ExcitedBaryons_MC_Run2.py']
j.inputfiles = [LocalFile("TMVAClassification_BDT_diff.weights.xml")]
j.application.platform = 'x86_64_v2-centos7-gcc11-opt'


if the_year == 2016 :
    if polarity == 'MD':
        bkPath = f'MC/2016/Beam6500GeV-2016-MagDown-Nu1.6-25ns-GenXiccPythia8/Sim10b/Trig0x6139160F/Reco16/Turbo03a/Stripping28r2NoPrescalingFlagged/{evt_type}/ALLSTREAMS.MDST'
    else :
        bkPath = f'MC/2016/Beam6500GeV-2016-MagUp-Nu1.6-25ns-GenXiccPythia8/Sim10b/Trig0x6139160F/Reco16/Turbo03a/Stripping28r2NoPrescalingFlagged/{evt_type}/ALLSTREAMS.MDST'
if the_year == 2017 :
    if polarity == 'MD':
        bkPath = f'MC/2017/Beam6500GeV-2017-MagDown-Nu1.6-25ns-GenXiccPythia8/Sim10b/Trig0x62661709/Reco17/Turbo04a-WithTurcal/Stripping29r2NoPrescalingFlagged/{evt_type}/ALLSTREAMS.MDST'
    else :
        bkPath = f'MC/2017/Beam6500GeV-2017-MagUp-Nu1.6-25ns-GenXiccPythia8/Sim10b/Trig0x62661709/Reco17/Turbo04a-WithTurcal/Stripping29r2NoPrescalingFlagged/{evt_type}/ALLSTREAMS.MDST'
if the_year == 2018 :
    if polarity == 'MD':
        bkPath = f'MC/2018/Beam6500GeV-2018-MagDown-Nu1.6-25ns-GenXiccPythia8/Sim10b/Trig0x617d18a4/Reco18/Turbo05-WithTurcal/Stripping34NoPrescalingFlagged/{evt_type}/ALLSTREAMS.MDST'
    else :
        bkPath = f'MC/2018/Beam6500GeV-2018-MagUp-Nu1.6-25ns-GenXiccPythia8/Sim10b/Trig0x617d18a4/Reco18/Turbo05-WithTurcal/Stripping34NoPrescalingFlagged/{evt_type}/ALLSTREAMS.MDST'



data  = BKQuery(bkPath, dqflag=['OK']).getDataset()
j.inputdata = data
j.backend = Dirac()
# j.backend.settings['BannedSites'] = ['LCG.CSCS.ch','LCG.Beijing.cn']
j.splitter = SplitByFiles(filesPerJob=1)
j.outputfiles = [DiracFile('*.root'), LocalFile('stdout')]
#j.postprocessors.append(RootMerger(files = ['DV_Xiccpp_MC_2016.root'],args='-fk'))
j.submit()
