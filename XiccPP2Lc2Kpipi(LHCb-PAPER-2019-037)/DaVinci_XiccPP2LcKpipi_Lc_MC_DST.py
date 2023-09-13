def fillTuple( tuple, myBranches, myTriggerList ):

    tuple.Branches = myBranches
    
    tuple.ToolList = [
        "TupleToolAngles",
        "TupleToolANNPID",           # Different tuning...
        "TupleToolEventInfo",
        "TupleToolGeometry",
        "TupleToolL0Data",
        "TupleToolKinematic",
        "TupleToolPid",
        "TupleToolPrimaries",
        "TupleToolPropertime" ,
        "TupleToolRecoStats",
        "TupleToolTrackInfo"
        ]

    # RecoStats for filling SpdMult, etc
    from Configurables import TupleToolRecoStats
    tuple.addTool(TupleToolRecoStats, name="TupleToolRecoStats")
    tuple.TupleToolRecoStats.Verbose=True

    from Configurables import TupleToolTISTOS, TupleToolDecay
    tuple.addTool(TupleToolDecay, name = 'Lc')
    tuple.addTool(TupleToolDecay, name = 'C')
    
    # TISTOS for Lc
    tuple.Lc.ToolList+=[ "TupleToolTISTOS" ]
    tuple.Lc.addTool(TupleToolTISTOS, name="TupleToolTISTOS" )
    tuple.Lc.TupleToolTISTOS.Verbose=True
    tuple.Lc.TupleToolTISTOS.TriggerList = myTriggerList

    tuple.C.ToolList+=[ "TupleToolTISTOS" ]
    tuple.C.addTool(TupleToolTISTOS, name="TupleToolTISTOS" )
    tuple.C.TupleToolTISTOS.Verbose=True
    tuple.C.TupleToolTISTOS.TriggerList = myTriggerList

    # DecayTree 
    from Configurables import TupleToolDecayTreeFitter
    tuple.C.ToolList +=  [ "TupleToolDecayTreeFitter/PVFit",          # fit with PV constraint
                           "TupleToolDecayTreeFitter/MassFit",        # fit with J/psi mass constraint
                           "TupleToolDecayTreeFitter/FullFit"         # fit with both
                           ]       

    tuple.C.addTool(TupleToolDecayTreeFitter("PVFit"))
    tuple.C.PVFit.Verbose = True
    tuple.C.PVFit.constrainToOriginVertex = True
    
    tuple.C.addTool(TupleToolDecayTreeFitter("MassFit"))
    tuple.C.MassFit.constrainToOriginVertex = False
    tuple.C.MassFit.daughtersToConstrain = [ "Lambda_c+" ]
    
    tuple.C.addTool(TupleToolDecayTreeFitter("FullFit"))
    tuple.C.FullFit.Verbose = True
    tuple.C.FullFit.constrainToOriginVertex = True
    tuple.C.FullFit.daughtersToConstrain = [ "Lambda_c+" ]

    #LoKi one
    from Configurables import LoKi__Hybrid__TupleTool
    LoKi_All=LoKi__Hybrid__TupleTool("LoKi_All")
    LoKi_All.Variables = {
        "ETA"                  : "ETA",
        "Y"                    : "Y"  ,
        "LOKI_IPCHI2"          : "BPVIPCHI2()"
        }
    tuple.ToolList+=["LoKi::Hybrid::TupleTool/LoKi_All"]
    tuple.addTool(LoKi_All)


    LoKi_B=LoKi__Hybrid__TupleTool("LoKi_B")
    LoKi_B.Variables = {
            "LOKI_FDCHI2"          : "BPVVDCHI2",
            "LOKI_FDS"             : "BPVDLS",
            "LOKI_DIRA"            : "BPVDIRA",
            "LV01"                 : "LV01",
            "LV02"                 : "LV02",
            "DTF_CHI2NDOF"         : "DTF_CHI2NDOF (     True , strings ( [ 'Lambda_c+' ] ) )", 
            "DTF_M"                : "DTF_FUN      ( M , True , strings ( [ 'Lambda_c+' ] ) )",
            "DTF_CTAU"             : "DTF_CTAU     ( 0 , True , strings ( [ 'Lambda_c+' ] ) )",            
            "DTF_CTAUERR"          : "DTF_CTAUERR  ( 0 , True , strings ( [ 'Lambda_c+' ] ) )",
            "DTF_CTAUS"            : "DTF_CTAUSIGNIFICANCE ( 0 , True , strings ( [ 'Lambda_c+' ] ) )", 
            "Lc_DTF_CTAU"          : "DTF_CTAU     ( 'Lambda_c+' == ABSID  , True , strings ( [ 'Lambda_c+' ] ) )",
            "Lc_DTF_CTAUERR"       : "DTF_CTAUERR  ( 'Lambda_c+' == ABSID  , True , strings ( [ 'Lambda_c+' ] ) )",
            "Lc_DTF_CTAUS"         : "DTF_CTAUSIGNIFICANCE ( 'Lambda_c+' == ABSID  , True , strings ( [ 'Lambda_c+' ] ) )",
            "DTF_DM"               : "(DTF_FUN( M , True ) - DTF_FUN( CHILD(1,M) , True ))",
            "DTF_PV_CTAU"          : "DTF_CTAU     ( 0 , True )",            
            "DTF_PV_CTAUERR"       : "DTF_CTAUERR  ( 0 , True )",            
            "SumXicIPCHI2"         : "( CHILD(MIPCHI2DV(), 1, 1) + CHILD(MIPCHI2DV(), 1, 2) + CHILD(MIPCHI2DV(), 1, 3) )",
            "SumXiccIPCHI2"        : "( CHILD(MIPCHI2DV(), 1, 1) + CHILD(MIPCHI2DV(), 1, 2) + CHILD(MIPCHI2DV(), 1, 3)  + CHILD(MIPCHI2DV(), 2) )",
            "SumXicPT"             : "( CHILD(PT, 1, 1) + CHILD(PT, 1, 2) + CHILD(PT, 1, 3) )",
            "SumXiccPT"            : "( CHILD(PT, 1, 1) + CHILD(PT, 1, 2) + CHILD(PT, 1, 3) + CHILD(PT, 2) )",
            }
    
    tuple.C.ToolList+=["LoKi::Hybrid::TupleTool/LoKi_B"]
    tuple.C.addTool(LoKi_B)

    
    """
    MC information
    """
    from Configurables import TupleToolMCTruth
    tuple.ToolList += [
        "TupleToolMCBackgroundInfo",
        "TupleToolMCTruth"
        ]

    MCTruth = TupleToolMCTruth()
    MCTruth.ToolList =  [
        "MCTupleToolAngles"
        , "MCTupleToolHierarchy"
        , "MCTupleToolKinematic"
        , "MCTupleToolReconstructed"
        ]
    tuple.addTool(MCTruth)

    

year = "2016"

# Cuts from Turbo 
LcCom = "(in_range( 2201.0, AM, 2553.0 )) & ((APT1+APT2+APT3) > 3000.0 ) & (AHASCHILD(PT > 1000.0)) & (ANUM(PT > 400.0) >= 2) & (AHASCHILD((MIPCHI2DV(PRIMARY)) > 16.0)) & (ANUM(MIPCHI2DV(PRIMARY) > 9.0) >= 2)"

LcMom = "(VFASPF(VCHI2PDOF) < 10.0) & (BPVDIRA > lcldira ) & (BPVLTIME() > 0.00015 ) & (in_range( 2201.0, M, 2553.0 )) & (SUMTREE(PT, ISBASIC, 0.0) > 3000.0 ) & (MAXTREE( ISBASIC, PT ) > 1000.0 ) & (NINTREE( ISBASIC & (PT > 9.0) ) > 1 ) & (MINTREE( ISBASIC, PT ) > 200.0 ) & (MINTREE( ISBASIC, MIPCHI2DV(PRIMARY) ) > 6.0 ) & (MAXTREE( ISBASIC, MIPCHI2DV(PRIMARY) ) > 16.0 ) & (NINTREE( ISBASIC & (MIPCHI2DV(PRIMARY) > 9.0) ) > 1 ) & (VFASPF(VCHI2PDOF) < 10.0) & (BPVDIRA > lcldira ) & (BPVLTIME() > 0.00015 ) & in_range( 2211.0 , M , 2362.0 )"

trk_cuts = "(TRCHI2DOF < 3.0 )& (PT > 200.0)& (P > 1000.0) & (MIPCHI2DV(PRIMARY) > 6.0)"

#
# MC matching
#
matchLcProton   = "(mcMatch('[ Lambda_c+ ==>^p+  K-  pi+ ]CC', 1 ))"
matchLcKaon     = "(mcMatch('[ Lambda_c+ ==> p+ ^K-  pi+ ]CC', 1 ))"
matchLcPion     = "(mcMatch('[ Lambda_c+ ==> p+  K- ^pi+ ]CC', 1 ))"

matchXiccLc     = "(mcMatch('[ Xi_cc++ =>^Lambda_c+  K-  pi+ pi+ ]CC', 1 ))"
matchXiccKaon   = "(mcMatch('[ Xi_cc++ => Lambda_c+ ^K-  pi+ pi+ ]CC', 1 ))"
matchXiccPion   = "(mcMatch('[ Xi_cc++ => Lambda_c+  K- ^pi+^pi+ ]CC', 1 ))"

# MakeLc
from Configurables import CombineParticles
MakeLc = CombineParticles("MakeLc")
MakeLc.Inputs = [ "Phys/StdAllNoPIDsPions/Particles",
                  "Phys/StdAllNoPIDsKaons/Particles",
                  'Phys/StdAllNoPIDsProtons/Particles'
                    ]
MakeLc.DecayDescriptor =  "[ Lambda_c+ -> p+  K-  pi+ ]cc"
MakeLc.DaughtersCuts = { "p+"  : matchLcProton + "& (P>10000.)" + "&" + trk_cuts,
                         "K-"  : matchLcKaon   + "&" + trk_cuts,
                         "pi+" : matchLcPion   + "&" + trk_cuts
                         }
MakeLc.CombinationCut  = LcCom
MakeLc.MotherCut = LcMom
MakeLc.Preambulo = [
    "from LoKiPhysMC.decorators import *",
    "from PartProp.Nodes import CC",
    "import math",
    "lcldira = math.cos(0.010)"
    ]

# MakeXicc
MakeXicc = CombineParticles("MakeXicc")
MakeXicc.Inputs = [ "Phys/MakeLc/Particles",
                    "Phys/StdAllNoPIDsPions/Particles",
                    "Phys/StdAllNoPIDsKaons/Particles"
                    ]
MakeXicc.DecayDescriptor =  "[ Xi_cc++ -> Lambda_c+ K- pi+ pi+]cc"
MakeXicc.DaughtersCuts = { "Lambda_c+"  : matchXiccLc,
                           "K-"         : matchXiccKaon + "& (PROBNNk > 0.1) & (PT>250*MeV) & (TRGHOSTPROB<0.4) & (MIPCHI2DV(PRIMARY)>1.)",
                           "pi+"        : matchXiccPion + "& (PROBNNpi> 0.2) & (PT>200*MeV) & (TRGHOSTPROB<0.4) & (MIPCHI2DV(PRIMARY)>1.)"
                           }
MakeXicc.CombinationCut  = "(APT>2*GeV)"
MakeXicc.MotherCut = """
    (VFASPF(VCHI2/VDOF) < 25.) & 
    (BPVDIRA> 0.99) & 
    (BPVIPCHI2()<25)    
    """
MakeXicc.Preambulo = [
    "from LoKiPhysMC.decorators import *",
    "from PartProp.Nodes import CC" ]



## (5) fill tuple
myTriggerList = [
    # L0
    "L0ElectronDecision",
    "L0PhotonDecision",
    "L0HadronDecision",
    # L0 Muon
    "L0MuonDecision",
    "L0MuonHighDecision",
    "L0DiMuonDecision",
    
    # Hlt1 track    
    "Hlt1TrackAllL0Decision",
    "Hlt1TrackMuonDecision",
    "Hlt1TrackPhotonDecision",

    "Hlt1TrackMVADecision",
    "Hlt1TwoTrackMVADecision",
    
    # Hlt2 Run-1 Name...
    "Hlt2CharmHadLambdaC2KPPiDecision",
    "Hlt2Topo2BodyBBDTDecision",
    "Hlt2Topo3BodyBBDTDecision",
    "Hlt2Topo4BodyBBDTDecision",

    # Hlt2 Run-2 Name... 
    "Hlt2CharmHadLcpToPpKmPipTurboDecision",
    "Hlt2Topo2BodyDecision",
    "Hlt2Topo3BodyDecision",
    "Hlt2Topo4BodyDecision"
    ]

XiccPP2LcKpipiBranches = {
    "LcP"    :  "[ Xi_cc++ -> ( Lambda_c+ ->^p+  K-  pi+ ) K- pi+ pi+ ]CC",
    "LcK"    :  "[ Xi_cc++ -> ( Lambda_c+ -> p+ ^K-  pi+ ) K- pi+ pi+ ]CC",
    "LcPi"   :  "[ Xi_cc++ -> ( Lambda_c+ -> p+  K- ^pi+ ) K- pi+ pi+ ]CC",
    "Lc"     :  "[ Xi_cc++ ->^( Lambda_c+ -> p+  K-  pi+ ) K- pi+ pi+ ]CC",
    "XiccK"  :  "[ Xi_cc++ -> ( Lambda_c+ -> p+  K-  pi+ )^K- pi+ pi+ ]CC",
    "XiccPi1":  "[ Xi_cc++ -> ( Lambda_c+ -> p+  K-  pi+ ) K-^pi+ pi+ ]CC",
    "XiccPi2":  "[ Xi_cc++ -> ( Lambda_c+ -> p+  K-  pi+ ) K- pi+^pi+ ]CC",
    "C"      :"^([ Xi_cc++ -> ( Lambda_c+ -> p+  K-  pi+ ) K- pi+ pi+ ]CC)"
}

from Configurables import DecayTreeTuple
XiccPP2LcKpipiTuple = DecayTreeTuple("XiccPP2LcKpipiTuple")
XiccPP2LcKpipiTuple.Decay ="[ Xi_cc++ ->^( Lambda_c+ ->^p+ ^K- ^pi+ ) ^K- ^pi+ ^pi+ ]CC"
XiccPP2LcKpipiTuple.Inputs = [ "Phys/MakeXicc/Particles" ]
fillTuple( XiccPP2LcKpipiTuple, XiccPP2LcKpipiBranches, myTriggerList )

# CheckPV
from Configurables import CheckPV
checkPV = CheckPV("checkPV")
checkPV.MinPVs = 1

from Configurables import GaudiSequencer 
SeqXiccPP2LcKpipi = GaudiSequencer("SeqXiccPP2LcKpipi")
SeqXiccPP2LcKpipi.Members += [ checkPV,                            
                               MakeLc,
                               MakeXicc,
                               XiccPP2LcKpipiTuple ]


from Configurables import DaVinci
DaVinci().EvtMax = -1                          # Number of events
DaVinci().SkipEvents = 0                       # Events to skip
DaVinci().PrintFreq = 1000
DaVinci().DataType = "2016"
DaVinci().Simulation    = True
DaVinci().HistogramFile = "DVHistos.root"      # Histogram file
DaVinci().TupleFile = "Tuple.root"             # Ntuple
DaVinci().UserAlgorithms = [ SeqXiccPP2LcKpipi ]        # The algorithms

# Get Luminosity
DaVinci().Lumi = False

