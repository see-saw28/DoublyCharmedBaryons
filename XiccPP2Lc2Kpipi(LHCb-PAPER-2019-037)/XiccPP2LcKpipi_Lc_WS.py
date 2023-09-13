myJobName = 'XiccPP2L2Kpipi_Lc_WS'
myApplication = GaudiExec()
myApplication.platform = 'x86_64-slc6-gcc62-opt'
myApplication.directory = '/afs/ihep.ac.cn/users/j/jibo/cmtuser/DaVinciDev_v44r7'
myApplication.options   = [ 'DaVinci_XiccPP2LcKpipi_Lc_WS.py'
                            ]

data  = BKQuery('/LHCb/Collision16/Beam6500GeV-VeloClosed-MagDown/Real Data/Turbo03a/94000000/CHARMSPECPRESCALED.MDST',
               dqflag=['OK']).getDataset()
data1 = BKQuery('/LHCb/Collision16/Beam6500GeV-VeloClosed-MagUp/Real Data/Turbo03a/94000000/CHARMSPECPRESCALED.MDST',
               dqflag=['OK']).getDataset()
data.extend(data1)

mySplitter = SplitByFiles( filesPerJob = 50, maxFiles = -1, ignoremissing = True, bulksubmit=False )

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
