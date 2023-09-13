def fillTuple( tuple, myTriggerList ):

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


year = "2016"

## (1) read data from Turbo: 
from PhysConf.Selections import AutomaticData
Lc = AutomaticData('Hlt2CharmHadLcpToPpKmPipTurbo/Particles')

## (2) get pions form PersistReco 
from StandardParticles import StdAllLooseANNPions as Pions
from StandardParticles import StdAllLooseANNKaons as Kaons

## This is the important lines ... 
from PhysConf.Selections import RebuildSelection
Pions = RebuildSelection(Pions)
Kaons = RebuildSelection(Kaons) 

## uncomment for debugging
## from PhysConf.Selections import PrintSelection
## pions = PrintSelection(pions)
## Lc    = PrintSelection(Lc   )

## (3) create Lambda-b candidates 
from PhysConf.Selections import CombineSelection
Xicc = CombineSelection (
    'Xicc'       , ## the name 
    [ Lc , Kaons, Pions ] , ## input
    DecayDescriptor = '[Xi_cc++  ->  Lambda_c+ K- pi- pi+ ]cc',    
    CombinationCut  = "(APT>2*GeV)", 
    MotherCut = """
    (VFASPF(VCHI2/VDOF) < 25.) & 
    (BPVDIRA> 0.99) & 
    (BPVIPCHI2()<25) &
    (in_range( 3.52*GeV, DTF_FUN( M , True , strings ( [ 'Lambda_c+' ] ) ), 3.72*GeV ))
    """,
    CheckOverlapTool = "LoKi::CheckOverlap",
    DaughtersCuts = {
        "K-"  : "(PROBNNk > 0.1) & (PT>250*MeV) & (TRGHOSTPROB<0.4) & (MIPCHI2DV(PRIMARY)>1.)", 
        "pi+" : "(PROBNNpi> 0.2) & (PT>200*MeV) & (TRGHOSTPROB<0.4) & (MIPCHI2DV(PRIMARY)>1.)"
    }
)

## (4) insert momentum scaling
from PhysConf.Selections import MomentumScaling
Xicc = MomentumScaling ( Xicc , Turbo = 'PersistReco' , Year = year )

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


from PhysConf.Selections import TupleSelection
Xicc_Tuple = TupleSelection (
    'XiccTuple'      ,
    [ Xicc ] ,
    Decay = "[ Xi_cc++ ->^( Lambda_c+ ->^p+ ^K- ^pi+ ) ^K- ^pi- ^pi+ ]CC",   
    Branches = {
        "LcP"    :  "[ Xi_cc++ -> ( Lambda_c+ ->^p+  K-  pi+ ) K- pi- pi+ ]CC",
        "LcK"    :  "[ Xi_cc++ -> ( Lambda_c+ -> p+ ^K-  pi+ ) K- pi- pi+ ]CC",
        "LcPi"   :  "[ Xi_cc++ -> ( Lambda_c+ -> p+  K- ^pi+ ) K- pi- pi+ ]CC",
        "Lc"     :  "[ Xi_cc++ ->^( Lambda_c+ -> p+  K-  pi+ ) K- pi- pi+ ]CC",
        "XiccK"  :  "[ Xi_cc++ -> ( Lambda_c+ -> p+  K-  pi+ )^K- pi- pi+ ]CC",
        "XiccPi1":  "[ Xi_cc++ -> ( Lambda_c+ -> p+  K-  pi+ ) K-^pi- pi+ ]CC",
        "XiccPi2":  "[ Xi_cc++ -> ( Lambda_c+ -> p+  K-  pi+ ) K- pi-^pi+ ]CC",
        "C"      :"^([ Xi_cc++ -> ( Lambda_c+ -> p+  K-  pi+ ) K- pi- pi+ ]CC)"
    } 
)

tuple = Xicc_Tuple.algorithm() 
fillTuple( tuple, myTriggerList)

## (6) build the final selection sequence
from PhysConf.Selections import SelectionSequence
seq = SelectionSequence('SEQ', Xicc_Tuple )


## (7) configure DaVinci
from Configurables import DaVinci 
dv = DaVinci(
    DataType   = year           ,
    InputType  = 'MDST'         , ## ATTENTION! 
    RootInTES  = "/Event/Turbo" , ## ATTENTION!
    Turbo      = True           , ## ATTENTION!
    ##
    Lumi       = True           , 
    Simulation = False          ,
    ## 
    TupleFile  = 'Tuple.root'   ,
    EvtMax     = -1
 )

## (8) insert our sequence into DaVinci
"""
Only use 0.5
"""
from Configurables import DeterministicPrescaler
Prescaler = DeterministicPrescaler("Prescaler")
Prescaler.AcceptFraction = 0.5


from Configurables import GaudiSequencer
MySeq = GaudiSequencer("MySeq")
MySeq.Members += [ Prescaler, seq.sequence() ]

dv.UserAlgorithms = [ MySeq ]

## Database tags
DaVinci().DDDBtag    = 'dddb-20171030-3'
DaVinci().CondDBtag  = 'cond-20181204'
DaVinci().DQFLAGStag = 'dq-20170829'

# =============================================================================
# Stuff specifif for Persist Reco, not needed for "plain" Turbo
# =============================================================================

## (9) specific for persis reco
from Configurables import DstConf, TurboConf
DstConf   () .Turbo       = True
TurboConf () .PersistReco = True
TurboConf () .DataType    = year

## II.2 fix for persist reco, not needed if "plain" Turbo is used
from Configurables import DataOnDemandSvc
dod = DataOnDemandSvc( Dump = True )
from Configurables import Gaudi__DataLink as Link
for  name , target , what  in [
    ( 'LinkHlt2Tracks' , '/Event/Turbo/Hlt2/TrackFitted/Long' , '/Event/Hlt2/TrackFitted/Long'     ) ,
    ( 'LinkDAQ'        , '/Event/Turbo/DAQ'                   , '/Event/DAQ'                       ) ,
#    ( 'LinkPPs'        , '/Event/Turbo/Rec/ProtoP/Charged'    , '/Event/Turbo/Hlt2/Protos/Charged' )
    ] :
    dod.AlgMap [ target ] = Link ( name , Target = target , What = what , RootInTES = '' )
    
