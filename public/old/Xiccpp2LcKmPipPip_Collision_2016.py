from DecayTreeTuple.Configuration import *
the_year = '2016' 
polarity = 'MD' 


from PhysConf.Filters import LoKi_Filters
fltrs = LoKi_Filters (
   HLT2_Code = "HLT_PASS_RE('Hlt2CharmHadXiccpp2LcpKmPipPip_Lcp2PpKmPipTurboDecision') | HLT_PASS_RE('Hlt2CharmHadLcpToPpKmPipTurboDecision')"
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



##########################

# Build Lc from Turbo line

##########################

Lc_line = 'Hlt2CharmHadLcpToPpKmPipTurbo/Particles'

Lc = AutomaticData(Lc_line)

TURBO_Lc = DecayTreeTuple('Lambdac_TURBO') 
TURBO_Lc.Inputs = [Lc.outputLocation()] 
TURBO_Lc.Decay = '[Lambda_c+ -> ^p+ ^K- ^pi+]CC'
#TURBO_Lc.Decay = '[Lambda_c+]CC'
TURBO_Lc.Branches = Lc2pKpiBranches


##########################

# Build Xicc from Turbo line

##########################


Xicc_line = 'Hlt2CharmHadXiccpp2LcpKmPipPip_Lcp2PpKmPipTurbo/Particles'

Xicc = AutomaticData(Xicc_line)

TURBO_Xicc = DecayTreeTuple('Xicc_TURBO') 
TURBO_Xicc.Inputs = [Xicc.outputLocation()] 
TURBO_Xicc.Decay = '[Xi_cc++ -> ^(Lambda_c+ -> ^p+ ^K- ^pi+) ^K- ^pi+ ^pi+]CC'
TURBO_Xicc.Branches = XiccpBranches
TURBO_Xicc.ToolList = myToolList


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

XiccSelSeq = SelectionSequence("simSelXiccSeq", TopSelection = Xiccsel)


REC = DecayTreeTuple("Xicc_REC",
        Inputs = [XiccSelSeq.outputLocation()],
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



from Configurables import DstConf, TurboConf 
DstConf().Turbo = True 
TurboConf().PersistReco = True 
TurboConf().DataType = the_year



# Configure DaVinci
from Configurables import DaVinci
from Configurables import CondDB


CondDB ( LatestGlobalTagByDataType = '2016')

DaVinci().EventPreFilters = fltrs.filters('Filter')
DaVinci().UserAlgorithms = [XiccSelSeq.sequence(), REC, TURBO_Xicc, TURBO_Lc] 
DaVinci().InputType = 'MDST' 
DaVinci().TupleFile = 'DV_Xiccpp_Collision_2016.root' 
DaVinci().PrintFreq = 2500 
DaVinci().DataType = '2016' 
DaVinci().Simulation = False

rootInTES = '/Event/Turbo'
DaVinci().RootInTES = rootInTES
DaVinci().Turbo = True 

# Only ask for luminosity information when not using simulated data
DaVinci().Lumi = not DaVinci().Simulation 
DaVinci().EvtMax = 5000
DaVinci().SkipEvents = 0
#DaVinci().CondDBtag = 'sim-20170721-2-vc-md100' 
#DaVinci().DDDBtag = 'dddb-20170721-3'

# Use the local input data

from Gaudi.Configuration import *
from GaudiConf import IOHelper
#IOHelper().inputFiles(['~/xiccpp/00071452_00000051_7.AllStreams.dst',
#                       '~/xiccpp/00071452_00000095_7.AllStreams.dst'], clear=True)

IOHelper().inputFiles(['~/xiccpp/Data/00076510_00000114_1.charmspecparked.mdst',
                       '~/xiccpp/Data/00076510_00000004_1.charmspecparked.mdst'], clear=True)

#IOHelper().inputFiles(['LFN:/lhcb/LHCb/Collision16/CHARMSPECPARKED.MDST/00076510/0000/00076510_00000086_1.charmspecparked.mdst'], clear=True)


