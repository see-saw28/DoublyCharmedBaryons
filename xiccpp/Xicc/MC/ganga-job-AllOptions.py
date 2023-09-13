years = [2016,2017,2018]
# years = [2016]
polarities = ['MD','MU']
evt_types = [26266052]

for evt_type in evt_types:
    for the_year in years:
        for polarity in polarities:

            print( f"Preparing job for {evt_type} {the_year} {polarity}"  )

            j = Job(name=f'Xicc-MC-{evt_type}-{the_year}-{polarity}')
            myApp = GaudiExec()
            myApp.directory = "/afs/cern.ch/user/p/pgaigne/xiccpp/Xicc/DaVinciDev_v46r5"
            j.application = myApp
            j.application.options = ['Xiccpp2LcKmPipPip_MC_AllOptions.py']
            j.application.extraOpts = (
                        "import sys, os\n"
                        "sys.path.append(os.getcwd())\n"
                        "from Xiccpp2LcKmPipPip_MC_AllOptions import Setup_options\n"
                        "Setup_options('{y}','{m}',{id})\n"
                    ).format(
                        y=the_year,
                        m=polarity,
                        id=evt_type
                    ) 
            j.application.platform = 'x86_64_v2-centos7-gcc11-opt'

            if evt_type == 26266050 :
                if polarity == 'MD':
                    bkPath = 'MC/2016/Beam6500GeV-2016-MagDown-Nu1.6-25ns-GenXiccPythia8/Sim09c/Trig0x6138160F/Reco16/Turbo03/Stripping28r1NoPrescalingFlagged/26266050/ALLSTREAMS.DST'
                else :
                    bkPath = 'MC/2016/Beam6500GeV-2016-MagUp-Nu1.6-25ns-GenXiccPythia8/Sim09c/Trig0x6138160F/Reco16/Turbo03/Stripping28r1NoPrescalingFlagged/26266050/ALLSTREAMS.DST'

            elif evt_type == 26266052 :
                if the_year == 2016 :
                    if polarity == 'MD':
                        bkPath = 'MC/2016/Beam6500GeV-2016-MagDown-Nu1.6-25ns-GenXiccPythia8/Sim10a/Trig0x6139160F/Reco16/Turbo03a/Stripping28r2NoPrescalingFlagged/26266052/ALLSTREAMS.MDST'
                    else :
                        bkPath = 'MC/2016/Beam6500GeV-2016-MagUp-Nu1.6-25ns-GenXiccPythia8/Sim10a/Trig0x6139160F/Reco16/Turbo03a/Stripping28r2NoPrescalingFlagged/26266052/ALLSTREAMS.MDST'
                if the_year == 2017 :
                    if polarity == 'MD':
                        bkPath = 'MC/2017/Beam6500GeV-2017-MagDown-Nu1.6-25ns-GenXiccPythia8/Sim10a/Trig0x62661709/Reco17/Turbo04a-WithTurcal/Stripping29r2NoPrescalingFlagged/26266052/ALLSTREAMS.MDST'
                    else :
                        bkPath = 'MC/2017/Beam6500GeV-2017-MagUp-Nu1.6-25ns-GenXiccPythia8/Sim10a/Trig0x62661709/Reco17/Turbo04a-WithTurcal/Stripping29r2NoPrescalingFlagged/26266052/ALLSTREAMS.MDST'
                if the_year == 2018 :
                    if polarity == 'MD':
                        bkPath = 'MC/2018/Beam6500GeV-2018-MagDown-Nu1.6-25ns-GenXiccPythia8/Sim10a/Trig0x617d18a4/Reco18/Turbo05-WithTurcal/Stripping34NoPrescalingFlagged/26266052/ALLSTREAMS.MDST'
                    else :
                        bkPath = 'MC/2018/Beam6500GeV-2018-MagUp-Nu1.6-25ns-GenXiccPythia8/Sim10a/Trig0x617d18a4/Reco18/Turbo05-WithTurcal/Stripping34NoPrescalingFlagged/26266052/ALLSTREAMS.MDST'



            data  = BKQuery(bkPath, dqflag=['OK']).getDataset()
            j.inputdata = data
            j.backend = Dirac()
            j.backend.settings['BannedSites'] = ['LCG.CSCS.ch','LCG.Beijing.cn']
            j.splitter = SplitByFiles(filesPerJob=5) #26266050 ~800 files and 26266052 ~160 files
            j.outputfiles = [DiracFile('*.root'), LocalFile('stdout')]
            #j.postprocessors.append(RootMerger(files = ['DV_Xiccpp_MC_2016.root'],args='-fk'))
            j.submit()
