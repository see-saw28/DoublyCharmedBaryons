from DecayTreeTuple.Configuration import *
the_year = '2017' 
polarity = 'MD' 
ganga = False

from Configurables import CondDB
CondDB ( LatestGlobalTagByDataType = the_year ) 

def fillTuple( tuple, myTriggerList ):

    tuple.ToolList = [
        "TupleToolAngles",
        "TupleToolANNPID",           # Different tuning...
        "TupleToolEventInfo",
        "TupleToolGeometry",
        # "TupleToolL0Data",
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
    tuple.addTool(TupleToolDecay, name = 'Xicc')
    
    # TISTOS for Lc
    tuple.Lc.ToolList+=[ "TupleToolTISTOS" ]
    tuple.Lc.addTool(TupleToolTISTOS, name="TupleToolTISTOS" )
    tuple.Lc.TupleToolTISTOS.Verbose=True
    tuple.Lc.TupleToolTISTOS.TriggerList = myTriggerList

    tuple.Xicc.ToolList+=[ "TupleToolTISTOS" ]
    tuple.Xicc.addTool(TupleToolTISTOS, name="TupleToolTISTOS" )
    tuple.Xicc.TupleToolTISTOS.Verbose=True
    tuple.Xicc.TupleToolTISTOS.TriggerList = myTriggerList

    """
    # DecayTree 
    from Configurables import TupleToolDecayTreeFitter
    tuple.Xicc.ToolList +=  [ "TupleToolDecayTreeFitter/PVFit",          # fit with PV constraint
                           "TupleToolDecayTreeFitter/MassFit",        # fit with J/psi mass constraint
                           "TupleToolDecayTreeFitter/FullFit"         # fit with both
                           ]       

    tuple.Xicc.addTool(TupleToolDecayTreeFitter("PVFit"))
    tuple.Xicc.PVFit.Verbose = True
    tuple.Xicc.PVFit.constrainToOriginVertex = True
    
    tuple.Xicc.addTool(TupleToolDecayTreeFitter("MassFit"))
    tuple.Xicc.MassFit.constrainToOriginVertex = False
    tuple.Xicc.MassFit.daughtersToConstrain = [ "Lambda_c+" ]
    
    tuple.Xicc.addTool(TupleToolDecayTreeFitter("FullFit"))
    tuple.Xicc.FullFit.Verbose = True
    tuple.Xicc.FullFit.constrainToOriginVertex = True
    tuple.Xicc.FullFit.daughtersToConstrain = [ "Lambda_c+" ]
    """

    #LoKi one
    from Configurables import LoKi__Hybrid__TupleTool
    LoKi_All=LoKi__Hybrid__TupleTool("LoKi_All")
    LoKi_All.Variables = {
        "ETA"                  : "ETA",
        "Y"                    : "Y"  ,
        "LTIME"                : "BPVLTIME()",
        "LOKI_IPCHI2"          : "BPVIPCHI2()"
        }
    tuple.ToolList+=["LoKi::Hybrid::TupleTool/LoKi_All"]
    tuple.addTool(LoKi_All)


    LoKi_B=LoKi__Hybrid__TupleTool("LoKi_B")
    LoKi_B.Variables = {
            "M_DTF":"DTF_FUN( M, False)",
            "M_DTF_Lc":"DTF_FUN( M, False, strings( 'Lambda_c+'))",
            "M_DTF_PV":"DTF_FUN( M, True)",
            "M_DTF_Lc_PV":"DTF_FUN( M, True, strings( 'Lambda_c+'))",
            "CHI2NDOF_DTF":"DTF_CHI2NDOF(False)",
            "CHI2NDOF_DTF_Lc":"DTF_CHI2NDOF(False, strings( 'Lambda_c+'))",
            "CHI2NDOF_DTF_PV":"DTF_CHI2NDOF(True)",
            "CHI2NDOF_DTF_Lc_PV":"DTF_CHI2NDOF(True, strings( 'Lambda_c+'))",            
            "SumXiccPT"            : "( CHILD(PT, 1, 1) + CHILD(PT, 1, 2) + CHILD(PT, 1, 3) + CHILD(PT, 2) )",
            }
    
    tuple.Xicc.ToolList+=["LoKi::Hybrid::TupleTool/LoKi_B"]
    tuple.Xicc.addTool(LoKi_B)

from PhysConf.Filters import LoKi_Filters
fltrs = LoKi_Filters (
   HLT2_Code = "HLT_PASS_RE('Hlt2CharmHadInclLcpToKmPpPipBDTTurboDecision') | HLT_PASS_RE('Hlt2CharmHadLcpToPpKmPipTurboDecision')"
)


Lc2pKpiBranches = {
    "Lc"     :  "^([ Lambda_c+ -> p+  K-  pi+ ]CC)",
    "LcP"    :  "[ Lambda_c+ ->^p+  K-  pi+ ]CC",
    "LcK"    :  "[ Lambda_c+ -> p+ ^K-  pi+ ]CC",
    "LcPi"   :  "[ Lambda_c+ -> p+  K- ^pi+ ]CC"
}

XiccpBranches = {
            "Xicc":"[Xi_cc++ -> (Lambda_c+ -> K- p+ pi+) K- pi+ pi+]CC" ,
            "Lc" : "[Xi_cc++ -> ^(Lambda_c+ -> p+ K- pi+) K- pi+ pi+]CC",
            "LcP": "[Xi_cc++ -> (Lambda_c+ -> ^p+ K- pi+) K- pi+ pi+]CC",
            "LcK": "[Xi_cc++ -> (Lambda_c+ -> p+ ^K- pi+) K- pi+ pi+]CC",
            "LcPi": "[Xi_cc++ -> (Lambda_c+ -> p+ K- ^pi+) K- pi+ pi+]CC",
            "XiccK": "[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) ^K- pi+ pi+]CC",
            "XiccPi1": "[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) K- ^pi+ pi+]CC",
            "XiccPi2": "[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) K- pi+ ^pi+]CC"
            }

myToolList = [
    "TupleToolKinematic",
    "TupleToolPid",
    "TupleToolANNPID",
    "TupleToolPropertime",
    "TupleToolGeometry",
    "TupleToolPrimaries",
    "TupleToolTrackInfo",
    "TupleToolEventInfo",
    "TupleToolRecoStats"#,
#    "TupleToolMCBackgroundInfo",
#    "TupleToolMCTruth"#,
    ]

## (5) fill tuple
myTriggerList = [
    # # L0
    # "L0ElectronDecision",
    # "L0PhotonDecision",
    # "L0HadronDecision",
    # # L0 Muon
    # "L0MuonDecision",
    # "L0MuonHighDecision",
    # "L0DiMuonDecision",
    
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


from Configurables import GaudiSequencer, CombineParticles
from PhysSelPython.Wrappers import Selection, SelectionSequence
from PhysConf.Selections import Selection
from PhysSelPython.Wrappers import DataOnDemand, AutomaticData
from GaudiKernel.SystemOfUnits import *
from PhysConf.Selections import CheckPVSelection, ValidBPVSelection
from PhysConf.Selections import CombineSelection, PrescaleSelection


MyPreambulo = [
    'from LoKiPhysMC.decorators import *',
    'from LoKiPhysMC.functions import mcMatch',
    'from LoKiCore.functions import monitor',
    ]


from StandardParticles import StdAllLooseANNKaons as Kaons 
from StandardParticles import StdAllLooseANNPions as Pions 
#from StandardParticles import StdAllNoPIDsProtons as Protons

from PhysConf.Selections import RebuildSelection
Pions = RebuildSelection(Pions)#### 
Kaons = RebuildSelection(Kaons)
#Protons = RebuildSelection(Protons)

##########################

# Build Lc from Turbo line

##########################
if (the_year == '2016')| (the_year =='2017'):
    Lc_line = 'Hlt2CharmHadLcpToPpKmPipTurbo/Particles'

else :
    Lc_line = 'Hlt2CharmHadInclLcpToKmPpPipBDTTurbo/Particles'


Lc = AutomaticData(Lc_line)

TURBO_Lc = DecayTreeTuple('Lambdac_TURBO') 
#TURBO_Lc.Inputs = [Lc.outputLocation()] 
TURBO_Lc.Decay = '[Lambda_c+ -> ^p+ ^K- ^pi+]CC'
#TURBO_Lc.Decay = '[Lambda_c+]CC'
TURBO_Lc.Branches = Lc2pKpiBranches

tuple_sel_Lc = Selection("tuple_sel_Lc",
                         Algorithm = TURBO_Lc,
                         RequiredSelections = [Lc])

##########################

# Build Xicc from Turbo line

##########################
Xicc_line = 'Hlt2CharmHadXiccpp2LcpKmPipPip_Lcp2PpKmPipTurbo/Particles'

Xicc = AutomaticData(Xicc_line)

TURBO_Xicc = DecayTreeTuple('Xicc_TURBO') 
#TURBO_Xicc.Inputs = [Xicc.outputLocation()] 
TURBO_Xicc.Decay = '[Xi_cc++ -> ^(Lambda_c+ -> ^p+ ^K- ^pi+) ^K- ^pi+ ^pi+]CC'
TURBO_Xicc.Branches = XiccpBranches
TURBO_Xicc.ToolList = myToolList

fillTuple(TURBO_Xicc, myTriggerList)

tuple_sel_Xicc = Selection("tuple_sel_Xicc",
                           Algorithm = TURBO_Xicc,
                           RequiredSelections = [Xicc])



#########################

# Xicc reconstruction 

#########################


Xicc_cdc = '(TRCHI2DOF<3)&(MIPCHI2DV(PRIMARY)>1.)&(TRGHOSTPROB<0.4)'
Xicc_mc = '(VFASPF(VCHI2PDOF) < 25)&(MIPCHI2DV(PRIMARY)<25.)&(BPVDIRA>0.99)'
Xicc_cc = '(APT>2*GeV) & (in_range(3300,AM,3900))'

Xiccsel = CombineSelection(
    'simXicc',
    [Lc, Pions, Kaons],
    DecayDescriptor = '[Xi_cc++ -> Lambda_c+ K- pi+ pi+]cc',
    Preambulo = MyPreambulo,
    DaughtersCuts = {
        'Lambda_c+' : 'ALL',
        'K-' : Xicc_cdc + '&(PT>0.25*GeV)&(PROBNNk>0.1)',  
        'pi+' : Xicc_cdc + '&(PT>0.20*GeV)&(PROBNNpi>0.2)'
        },
    CheckOverlapTool = "LoKi::CheckOverlap",
    MotherCut = Xicc_mc,
    CombinationCut = Xicc_cc)

REC = DecayTreeTuple("Xicc_REC",
                     #                     Inputs = [Xiccsel.outputLocation()],
                     Decay = '[Xi_cc++ -> ^(Lambda_c+ -> ^K- ^p+ ^pi+) ^K- ^pi+ ^pi+]CC',
                     Branches = { "Xicc":"[Xi_cc++ -> (Lambda_c+ -> K- p+ pi+) K- pi+ pi+]CC" ,
                                  "Lc" : "[Xi_cc++ -> ^(Lambda_c+ -> p+ K- pi+) K- pi+ pi+]CC",
                                  "LcP": "[Xi_cc++ -> (Lambda_c+ -> ^p+ K- pi+) K- pi+ pi+]CC",
                                  "LcK": "[Xi_cc++ -> (Lambda_c+ -> p+ ^K- pi+) K- pi+ pi+]CC",
                                  "LcPi": "[Xi_cc++ -> (Lambda_c+ -> p+ K- ^pi+) K- pi+ pi+]CC",
                                  "XiccK": "[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) ^K- pi+ pi+]CC",
                                  "XiccPi1": "[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) K- ^pi+ pi+]CC",
                                  "XiccPi2": "[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) K- pi+ ^pi+]CC"
                                  }
                     )



fillTuple(REC, myTriggerList)


"""
XiccselPrescaled = PrescaleSelection ( Xiccsel , prescale = 0.1)

tuple_sel_prescaled = Selection("tuple_sel_rec_prescaled",
                      Algorithm = REC,
                      RequiredSelections = [XiccselPrescaled])
"""

tuple_sel = Selection("tuple_sel_rec",
                      Algorithm = REC,
                      RequiredSelections = [Xiccsel])

#########################

# Xicc WS reconstruction 

#########################


Xicc_cdc = '(TRCHI2DOF<3)&(MIPCHI2DV(PRIMARY)>1.)&(TRGHOSTPROB<0.4)'
Xicc_mc = '(VFASPF(VCHI2PDOF) < 25)&(MIPCHI2DV(PRIMARY)<25.)&(BPVDIRA>0.99)'
Xicc_cc = '(APT>2*GeV) & (in_range(3300,AM,3900))'

XiccWSsel = CombineSelection(
    'simXiccWS',
    [Lc, Pions, Kaons],
    DecayDescriptor = '[Xi_cc++ -> Lambda_c+ K- pi- pi+]cc',
    Preambulo = MyPreambulo,
    DaughtersCuts = {
        'Lambda_c+' : 'ALL',
        'K-' : Xicc_cdc + '&(PT>0.25*GeV)&(PROBNNk>0.1)',  
        'pi+' : Xicc_cdc + '&(PT>0.20*GeV)&(PROBNNpi>0.2)'
        },
    CheckOverlapTool = "LoKi::CheckOverlap",
    MotherCut = Xicc_mc,
    CombinationCut = Xicc_cc)

REC_WS = DecayTreeTuple("XiccWS_REC",
                     #                     Inputs = [Xiccsel.outputLocation()],
                     Decay = '[Xi_cc++ -> ^(Lambda_c+ -> ^K- ^p+ ^pi+) ^K- ^pi- ^pi+]CC',
                     Branches = { "Xicc":"[Xi_cc++ -> (Lambda_c+ -> K- p+ pi+) K- pi- pi+]CC" ,
                                  "Lc" : "[Xi_cc++ -> ^(Lambda_c+ -> p+ K- pi+) K- pi- pi+]CC",
                                  "LcP": "[Xi_cc++ -> (Lambda_c+ -> ^p+ K- pi+) K- pi- pi+]CC",
                                  "LcK": "[Xi_cc++ -> (Lambda_c+ -> p+ ^K- pi+) K- pi- pi+]CC",
                                  "LcPi": "[Xi_cc++ -> (Lambda_c+ -> p+ K- ^pi+) K- pi- pi+]CC",
                                  "XiccK": "[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) ^K- pi- pi+]CC",
                                  "XiccPi1": "[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) K- ^pi- pi+]CC",
                                  "XiccPi2": "[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) K- pi- ^pi+]CC"
                                  }
                     )

fillTuple(REC_WS, myTriggerList)


XiccWSselPrescaled = PrescaleSelection ( XiccWSsel , prescale = 0.5)

tuple_sel_WS = Selection("tuple_sel_rec_WS",
                      Algorithm = REC_WS,
                      RequiredSelections = [XiccWSselPrescaled])

"""
tuple_sel_WS = Selection("tuple_sel_rec_WS",
                      Algorithm = REC_WS,
                      RequiredSelections = [XiccWSsel])
"""
## (6) build the final selection sequence
from PhysConf.Selections import SelectionSequence
seq0 = SelectionSequence('SEQ0', tuple_sel_Lc )
seq1 = SelectionSequence('SEQ1', tuple_sel_Xicc )
seq2 = SelectionSequence('SEQ2', tuple_sel )
seq3 = SelectionSequence('SEQ3', tuple_sel_WS )

from Configurables import DstConf, TurboConf 
DstConf().Turbo = True 
TurboConf().PersistReco = True 
TurboConf().DataType = the_year



# Configure DaVinci
from Configurables import DaVinci


DaVinci().EventPreFilters = fltrs.filters('Filter')
# DaVinci().UserAlgorithms = [seq0.sequence(), seq1.sequence(), seq2.sequence()] 
DaVinci().UserAlgorithms = [seq2.sequence()]#,seq3.sequence()]
# DaVinci().UserAlgorithms = [seq1.sequence()]
DaVinci().InputType = 'MDST' 
DaVinci().TupleFile = f'DV_Xiccpp_Collision_{the_year}_{polarity}.root' 
DaVinci().PrintFreq = 5000 
DaVinci().DataType = the_year 
DaVinci().Simulation = False

if ((the_year == '2015') | (the_year == '2016')):
    rootInTES = '/Event/Turbo'

elif (the_year == '2017') :
    rootInTES = '/Event/Charmspec/Turbo'
    
elif (the_year == '2018'):
    rootInTES = '/Event/Charminclbaryon/Turbo'



DaVinci().RootInTES = rootInTES
DaVinci().Turbo = True 

# Only ask for luminosity information when not using simulated data
DaVinci().Lumi = not DaVinci().Simulation 
if ganga:
    DaVinci().EvtMax = -1
else:
    DaVinci().EvtMax = 10000
DaVinci().SkipEvents = 0


# Use the local input data
if not ganga :
    from Gaudi.Configuration import *
    from GaudiConf import IOHelper
    #IOHelper().inputFiles(['~/xiccpp/00071452_00000051_7.AllStreams.dst',
    #                       '~/xiccpp/00071452_00000095_7.AllStreams.dst'], clear=True)

    if the_year == '2016':
        if polarity == 'MD':
            IOHelper().inputFiles(['/afs/cern.ch/work/p/pgaigne/DST/00076510_00000086_1.charmspecparked.mdst'], clear=True)
        else :
            IOHelper().inputFiles(['/afs/cern.ch/work/p/pgaigne/DST/00076439_00000377_1.charmspecparked.mdst'], clear=True)

    elif the_year == '2017':
        if polarity == 'MD':
            #IOHelper().inputFiles(['/afs/cern.ch/work/p/pgaigne/DST/00066595_00000006_1.charmspec.mdst'], clear=True)
            IOHelper().inputFiles(['/afs/cern.ch/work/p/pgaigne/DST/00066595_00001021_1.charmspec.mdst'], clear=True)
            
        else :
            print('no dst file')
            # IOHelper().inputFiles(['/afs/cern.ch/work/p/pgaigne/DST/00076439_00000377_1.charmspecparked.mdst'], clear=True)

    elif the_year == '2018':
        if polarity == 'MD':
            # IOHelper().inputFiles(['/afs/cern.ch/work/p/pgaigne/DST/00080042_00003088_1.charmmultibody.mdst'], clear=True)
            IOHelper().inputFiles(['/afs/cern.ch/work/p/pgaigne/DST/00080042_00003856_1.charminclbaryon.mdst'], clear=True)
            
        else :
            print('no dst file')
            # IOHelper().inputFiles(['/afs/cern.ch/work/p/pgaigne/DST/00076439_00000377_1.charmspecparked.mdst'], clear=True)
