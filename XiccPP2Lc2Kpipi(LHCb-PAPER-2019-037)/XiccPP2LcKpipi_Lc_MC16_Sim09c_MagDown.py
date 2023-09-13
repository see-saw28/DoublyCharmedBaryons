myJobName = 'XiccPP2L2Kpipi_Lc_MC16_Sim09c_MagDown'
myApplication = GaudiExec()
myApplication.platform = 'x86_64-slc6-gcc62-opt'
myApplication.directory = '/afs/ihep.ac.cn/users/j/jibo/cmtuser/DaVinciDev_v44r7'
myApplication.options   = [ 'DaVinci_XiccPP2LcKpipi_Lc_MC_DST.py',
                            'DB_MC16_Sim09c_MagDown.py'
                            ]

data = BKQuery('/MC/2016/Beam6500GeV-2016-MagDown-Nu1.6-25ns-GenXiccPythia8/Sim09c/Trig0x6138160F/Reco16/Turbo03/Stripping28r1NoPrescalingFlagged/26266050/ALLSTREAMS.DST',
               dqflag=['OK']).getDataset() 

mySplitter = SplitByFiles( filesPerJob = 10, maxFiles = -1, ignoremissing = True, bulksubmit=False )

myBackend = Dirac()
j = Job (
    name         = myJobName,
    application  = myApplication,
    splitter     = mySplitter,
    outputfiles  = [ LocalFile('Tuple.root')
                     ],
    backend      = myBackend,
    inputdata    = data,
    do_auto_resubmit = False
    )
j.submit(keep_going=True, keep_on_fail=True)
