from DecayTreeTuple.Configuration import *
the_year = '2018' 
polarity = 'MD' 
evt_id = 26266052
ganga = False



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
    "TupleToolRecoStats",
    "TupleToolMCBackgroundInfo",
    "TupleToolMCTruth"#,
    ]




from Configurables import GaudiSequencer, CombineParticles
from PhysSelPython.Wrappers import Selection, SelectionSequence
from PhysSelPython.Wrappers import DataOnDemand, AutomaticData
from GaudiKernel.SystemOfUnits import *
from PhysConf.Selections import CheckPVSelection, ValidBPVSelection
from PhysConf.Selections import CombineSelection


MyPreambulo = [
    'from LoKiPhysMC.decorators import *',
    'from LoKiPhysMC.functions import mcMatch',
    'from LoKiCore.functions import monitor',
    ]


from StandardParticles import StdAllNoPIDsKaons as Kaons 
from StandardParticles import StdAllNoPIDsPions as Pions 
#from StandardParticles import StdAllNoPIDsProtons as Protons

from PhysConf.Selections import RebuildSelection
Pions = RebuildSelection(Pions)#### 
#Protons = RebuildSelection(Protons)
Kaons = RebuildSelection(Kaons)


########################

#       MC TREE

########################

mct = MCDecayTreeTuple('mctupleLc') 
mct.Decay = '[Xi_cc++ ==> ^(Lambda_c+ ==> ^p+ ^K- ^pi+) ^K- ^pi+ ^pi+]CC' 
mct.addBranches( {
    'Xicc': '[Xi_cc++ => (Lambda_c+ ==> K- p+ pi+) K- pi+ pi+]CC',
    'Lc': '[Xi_cc++ => ^(Lambda_c+ ==> K- p+ pi+) K- pi+ pi+]CC',
    'XiccK': '[Xi_cc++ => (Lambda_c+ ==> K- p+ pi+) ^K- pi+ pi+]CC',
    'LcK': '[Xi_cc++ => (Lambda_c+ ==> ^K- p+ pi+) K- pi+ pi+]CC',
    'XiccPi1': '[Xi_cc++ => (Lambda_c+ ==> K- p+ pi+) K- ^pi+ pi+]CC',
    'XiccPi2': '[Xi_cc++ => (Lambda_c+ ==> K- p+ pi+) K- pi+ ^pi+]CC',
    'LcPi': '[Xi_cc++ => (Lambda_c+ ==> K- p+ ^pi+) K- pi+ pi+]CC',
    'LcP': '[Xi_cc++ => (Lambda_c+ ==> K- ^p+ pi+) K- pi+ pi+]CC'} )

mctl = ['MCTupleToolHierarchy'
        ,'MCTupleToolKinematic'
        ,'MCTupleToolPrimaries'
        ,'MCTupleToolPID',
        "LoKi::Hybrid::MCTupleTool/LoKi_Photos"]

mct.ToolList = mctl

mct.addTupleTool("LoKi::Hybrid::TupleTool/LoKi_Photos").Variables = {
    "M" : "MCM"
}



mcTuple_sel = Selection("MCTree",
                        Algorithm = mct,
                        RequiredSelections = [])


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

# ############
# # MC TRUTH
# ############

# from Configurables import TupleToolMCTruth
# MCTruth = TupleToolMCTruth()
# MCTruth.ToolList = [ "MCTupleToolKinematic",
#                      "MCTupleToolHierarchy" ]

# TURBO_Lc.addTool(MCTruth)

# from TeslaTools import TeslaTruthUtils

# mc_tools = [
#     'MCTupleToolKinematic',
#     'MCTupleToolHierarchy'
#     ]

# # Lc OK
# relations = TeslaTruthUtils.getRelLocs() + [
#     TeslaTruthUtils.getRelLoc(''),
#     # Location of the truth tables for PersistReco objects
#     'Relations/Hlt2/Protos/Charged'
# ]

# # not working
# # relations = [
# #     TeslaTruthUtils.getRelLoc(''),
# #     # Location of the truth tables for PersistReco objects
# #     '/Event/Turbo/Relations/Hlt2/Protos/Charged'
# #     ]

# TeslaTruthUtils.makeTruth(TURBO_Lc, relations, mc_tools)

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

##########
#  DTF
##########
from Configurables import TupleToolDecay
TURBO_Xicc.addTool(TupleToolDecay, name = 'Xicc')
TURBO_Xicc.Xicc.ToolList +=  ["LoKi::Hybrid::TupleTool/LoKi_All0"]
from Configurables import LoKi__Hybrid__TupleTool
###################################################
LoKiTuple0 = LoKi__Hybrid__TupleTool("LoKi_All0")
LoKiTuple0.Variables =  {
    "M_DTF":"DTF_FUN( M, False)",
    "M_DTF_Lc":"DTF_FUN( M, False, strings( 'Lambda_c+'))",
    "M_DTF_PV":"DTF_FUN( M, True)",
    "M_DTF_Lc_PV":"DTF_FUN( M, True, strings( 'Lambda_c+'))",
    "CHI2NDOF_DTF":"DTF_CHI2NDOF(False)",
    "CHI2NDOF_DTF_Lc":"DTF_CHI2NDOF(False, strings( 'Lambda_c+'))",
    "CHI2NDOF_DTF_PV":"DTF_CHI2NDOF(True)",
    "CHI2NDOF_DTF_Lc_PV":"DTF_CHI2NDOF(True, strings( 'Lambda_c+'))"
    }

TURBO_Xicc.Xicc.addTool(LoKiTuple0)

############
# MC TRUTH
############

from Configurables import TupleToolMCTruth
MCTruth = TupleToolMCTruth()
MCTruth.ToolList = [ "MCTupleToolKinematic",
                     "MCTupleToolHierarchy" ]

TURBO_Xicc.addTool(MCTruth)

from TeslaTools import TeslaTruthUtils

mc_tools = [
    'MCTupleToolKinematic',
    'MCTupleToolHierarchy'
    ]

relations = [
    TeslaTruthUtils.getRelLoc(''),
    # Location of the truth tables for PersistReco objects
    '/Event/Turbo/Relations/Hlt2/Protos/Charged'
    ]


relations = TeslaTruthUtils.getRelLocs() + [
    TeslaTruthUtils.getRelLoc(''),
    # Location of the truth tables for PersistReco objects
    'Relations/Hlt2/Protos/Charged'
]

TeslaTruthUtils.makeTruth(TURBO_Xicc, relations, mc_tools)

tuple_sel_Xicc = Selection("tuple_sel_Xicc",
                           Algorithm = TURBO_Xicc,
                           RequiredSelections = [Xicc])

#########################

# Xicc reconstruction 

#########################


Xicc_cdc = '(TRCHI2DOF<3)&(MIPCHI2DV(PRIMARY)>1.)&(TRGHOSTPROB<0.4)'
Xicc_mc = '(VFASPF(VCHI2PDOF) < 25)&(MIPCHI2DV(PRIMARY)<25.)&(BPVDIRA>0.99)&(BPVLTIME() > 0.15*ps)'
Xicc_cc = '((APT1+APT2+APT3+APT4)>2*GeV) & (in_range(3200,AM,4000))'

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
    MotherCut = Xicc_mc,
    CombinationCut = Xicc_cc)



REC = DecayTreeTuple("Xicc_REC",
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


REC.ToolList = myToolList


##########
#  DTF
##########
from Configurables import TupleToolDecay
REC.addTool(TupleToolDecay, name = 'Xicc')
REC.Xicc.ToolList +=  ["LoKi::Hybrid::TupleTool/LoKi_All0"]
from Configurables import LoKi__Hybrid__TupleTool
###################################################
LoKiTuple0 = LoKi__Hybrid__TupleTool("LoKi_All0")
LoKiTuple0.Variables =  {
    "M_DTF":"DTF_FUN( M, False)",
    "M_DTF_Lc":"DTF_FUN( M, False, strings( 'Lambda_c+'))",
    "M_DTF_PV":"DTF_FUN( M, True)",
    "M_DTF_Lc_PV":"DTF_FUN( M, True, strings( 'Lambda_c+'))",
    "CHI2NDOF_DTF":"DTF_CHI2NDOF(False)",
    "CHI2NDOF_DTF_Lc":"DTF_CHI2NDOF(False, strings( 'Lambda_c+'))",
    "CHI2NDOF_DTF_PV":"DTF_CHI2NDOF(True)",
    "CHI2NDOF_DTF_Lc_PV":"DTF_CHI2NDOF(True, strings( 'Lambda_c+'))"
    }

REC.Xicc.addTool(LoKiTuple0)

############
# MC TRUTH
############

from Configurables import TupleToolMCTruth
MCTruth = TupleToolMCTruth()
MCTruth.ToolList = [ "MCTupleToolKinematic",
                     "MCTupleToolHierarchy" ]

REC.addTool(MCTruth)

from TeslaTools import TeslaTruthUtils

mc_tools = [
    'MCTupleToolKinematic',
    'MCTupleToolHierarchy'
    ]

# Lc OK
relations = TeslaTruthUtils.getRelLocs() + [
    TeslaTruthUtils.getRelLoc(''),
    # Location of the truth tables for PersistReco objects
    'Relations/Hlt2/Protos/Charged'
]

# not working
# relations = [
#     TeslaTruthUtils.getRelLoc(''),
#     # Location of the truth tables for PersistReco objects
#     '/Event/Turbo/Relations/Hlt2/Protos/Charged'
#     ]

TeslaTruthUtils.makeTruth(REC, relations, mc_tools)

tuple_sel = Selection("tuple_sel_rec",
                       Algorithm = REC,
                       RequiredSelections = [Xiccsel])






# Configure DaVinci
from Configurables import DaVinci

from PhysConf.Selections import SelectionSequence
seq0 = SelectionSequence('SEQ0', tuple_sel_Lc )
seq1 = SelectionSequence('SEQ1', tuple_sel_Xicc )
seq2 = SelectionSequence('SEQ2', tuple_sel )
seq3 = SelectionSequence('SEQ3', mcTuple_sel )



DaVinci().EventPreFilters = fltrs.filters('Filter')
# DaVinci().UserAlgorithms = [seq0.sequence(), seq1.sequence(), seq2.sequence(), seq3.sequence()]#, seq4.sequence()] 
DaVinci().UserAlgorithms = [seq0.sequence(), seq1.sequence(), seq2.sequence(), seq3.sequence()]#, seq4.sequence()] 
DaVinci().InputType = 'MDST' 
DaVinci().TupleFile = f'DV_Xiccpp_MC_{the_year}_{polarity}.root' 
DaVinci().PrintFreq = 2500 
DaVinci().DataType = the_year
DaVinci().Simulation = True

if ((the_year == '2015') | (the_year == '2016')):
    rootInTES = '/Event/Turbo'

elif (the_year == '2017') :
    rootInTES = '/Event/Charmspec/Turbo'
    
elif (the_year == '2018'):
    rootInTES = '/Event/Charminclbaryon/Turbo'

rootInTES = '/Event/Turbo'

DaVinci().RootInTES = rootInTES
DaVinci().Turbo = True 



# Only ask for luminosity information when not using simulated data
DaVinci().Lumi = not DaVinci().Simulation 
DaVinci().EvtMax = -1

if evt_id == 26266050 :
    if polarity == 'MD':
        DaVinci().CondDBtag = 'sim-20170721-2-vc-md100' 
    else :
        DaVinci().CondDBtag = 'sim-20170721-2-vc-mu100' 

    DaVinci().DDDBtag = 'dddb-20170721-3'
    
elif evt_id == 26266052 :
    tag = int(the_year)%10
    if polarity == 'MD':
        DaVinci().CondDBtag = f'sim-20201113-{tag}-vc-md100-Sim10' 
    else :
        DaVinci().CondDBtag = f'sim-20201113-{tag}-vc-mu100-Sim10' 

    DaVinci().DDDBtag = f'dddb-20210528-{tag}'

# Use the local input data
if not ganga :
    from Gaudi.Configuration import *
    from GaudiConf import IOHelper

    if evt_id == 26266050 :
        if polarity == 'MD':
            IOHelper().inputFiles(['/afs/cern.ch/work/p/pgaigne/DST/00071452_00000051_7.AllStreams.dst',
                                '/afs/cern.ch/work/p/pgaigne/DST/00071452_00000095_7.AllStreams.dst'], clear=True)
        else :
            IOHelper().inputFiles(['/afs/cern.ch/work/p/pgaigne/DST/00071450_00000822_7.AllStreams.dst'], clear=True)
        #IOHelper().inputFiles(['/afs/cern.ch/work/p/pgaigne/DST/00071452_00000051_7.AllStreams.dst'], clear=True)

    elif evt_id == 26266052 :
        if the_year == '2016' :
            if polarity == 'MD':
                IOHelper().inputFiles(['/afs/cern.ch/user/p/pgaigne/public/00137876_00000020_7.AllStreams.mdst'], clear=True)
            else :
                print('no input file')
        elif the_year == '2018' :
            if polarity == 'MD':
                IOHelper().inputFiles(['/afs/cern.ch/user/p/pgaigne/public/00138029_00000065_7.AllStreams.mdst'], clear=True)
            else :
                print('no input file')
            


