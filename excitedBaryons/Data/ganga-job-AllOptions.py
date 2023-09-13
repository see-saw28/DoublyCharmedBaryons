# years = [2016,2017,2018]
years = [2016,2017]
polarities = ['MD','MU']


for the_year in years:
    for polarity in polarities:
        print( f"Preparing job for  {the_year} {polarity}"  )

        j = Job(name=f'Excited-RS-WS-Xiccpp-Data-{the_year}-{polarity}')
        myApp = GaudiExec()
        myApp.directory = "/afs/cern.ch/user/p/pgaigne/xiccpp/Xicc/DaVinciDev_v46r5"
        j.application = myApp
        j.application.options = [f'ExcitedBaryons_Collision_Run2_AllOptions.py']
        j.application.extraOpts = (
                        "import sys, os\n"
                        "sys.path.append(os.getcwd())\n"
                        "from ExcitedBaryons_Collision_Run2_AllOptions import Setup_options\n"
                        "Setup_options('{y}','{m}')\n"
                    ).format(
                        y=the_year,
                        m=polarity
                    ) 
        j.inputfiles = [LocalFile("TMVAClassification_BDT.weights.xml")]
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
            j.splitter = SplitByFiles(filesPerJob=50)#6k files 
        j.outputfiles = [DiracFile('*.root'), LocalFile('stdout')]
        #j.postprocessors.append(RootMerger(files = ['DV_Xiccpp_MC_2016.root'],args='-fk'))
        j.submit()
