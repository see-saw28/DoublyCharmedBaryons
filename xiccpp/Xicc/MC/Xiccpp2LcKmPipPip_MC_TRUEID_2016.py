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
        ,'MCTupleToolPID']

mct.ToolList += mctl

mcTuple_sel = Selection("MCTree",
                        Algorithm = mct,
                        RequiredSelections = [])


##########################

# Build Lc from Turbo line

##########################

Lc_line = 'Hlt2CharmHadLcpToPpKmPipTurbo/Particles'

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

tuple_sel_Xicc = Selection("tuple_sel_Xicc",
                           Algorithm = TURBO_Xicc,
                           RequiredSelections = [Xicc])

#########################

# Xicc reconstruction 

#########################



#Xicc_mc = "mcMatch('[Xi_cc++]CC')"
#Xicc_dc = {
#        'Lambda_c+' : "mcMatch('[Xi_cc++ => ^Lambda_c+ K- pi+ pi+]CC')",
#        'K-' : "mcMatch('[Xi_cc++ => Lambda_c+ ^K- pi+ pi+]CC')",  
#        'pi+' : "mcMatch('[Xi_cc++ => Lambda_c+ K- ^pi+ ^pi+]CC')"
#        }

Xicc_dc = {
        'Lambda_c+' : "ABSID == 4122",
        'K-' : "ABSID == 321",  
        'pi+' : "ABSID == 211"
        }



Xiccsel = CombineSelection(
    'simXicc',
    [Lc, Pions, Kaons],
    DecayDescriptor = '[Xi_cc++ -> Lambda_c+ K- pi+ pi+]cc',
    Preambulo = MyPreambulo,
    DaughtersCuts = Xicc_dc,
    MotherCut = "(in_range(3200,M,4000))",
    CombinationCut = "AALL")



REC = DecayTreeTuple("Xicc_REC",
        Decay = '[Xi_cc++ -> ^(Lambda_c+ -> ^K- ^p+ ^pi+) ^K- ^pi+ ^pi+]CC',
        Branches = { 
            "Xicc":"[Xi_cc++ -> (Lambda_c+ -> K- p+ pi+) K- pi+ pi+]CC" ,
            "Lc" : "[Xi_cc++ -> ^(Lambda_c+ -> p+ K- pi+) K- pi+ pi+]CC",
            "LcP": "[Xi_cc++ -> (Lambda_c+ -> ^p+ K- pi+) K- pi+ pi+]CC",
            "LcK": "[Xi_cc++ -> (Lambda_c+ -> p+ ^K- pi+) K- pi+ pi+]CC",
            "LcPi": "[Xi_cc++ -> (Lambda_c+ -> p+ K- ^pi+) K- pi+ pi+]CC",
            "XiccK": "[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) ^K- pi+ pi+]CC",
            "XiccPi1": "[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) K- ^pi+ pi+]CC",
            "XiccPi2": "[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) K- pi+ ^pi+]CC"
            }
)


REC.ToolList += myToolList

from Configurables import TupleToolTISTOS, TupleToolDecay
REC.addTool(TupleToolDecay, name = 'Xicc')
# DTF
from Configurables import TupleToolDecayTreeFitter
REC.Xicc.ToolList +=  ["TupleToolDecayTreeFitter/Fit",
                        "TupleToolDecayTreeFitter/PVFit",
                        "TupleToolDecayTreeFitter/MassFit",
                        "TupleToolDecayTreeFitter/MassPVFit"
                        ]

REC.Xicc.ToolList += ["TupleToolDecayTreeFitter/Fit"]
REC.Xicc.addTool(TupleToolDecayTreeFitter("Fit"))
REC.Xicc.Fit.Verbose = True
REC.Xicc.Fit.UpdateDaughters = True

REC.Xicc.ToolList += ["TupleToolDecayTreeFitter/PVFit"]
REC.Xicc.addTool(TupleToolDecayTreeFitter("PVFit"))
REC.Xicc.PVFit.Verbose = True
REC.Xicc.PVFit.constrainToOriginVertex = True
REC.Xicc.PVFit.UpdateDaughters = True

REC.Xicc.ToolList += ["TupleToolDecayTreeFitter/MassFit"]
REC.Xicc.addTool(TupleToolDecayTreeFitter("MassFit"))
REC.Xicc.MassFit.Verbose = True
REC.Xicc.MassFit.UpdateDaughters = True
REC.Xicc.MassFit.daughtersToConstrain = [ "Lambda_c+" ]

REC.Xicc.ToolList += ["TupleToolDecayTreeFitter/MassPVFit"]
REC.Xicc.addTool(TupleToolDecayTreeFitter("MassPVFit"))
REC.Xicc.MassPVFit.daughtersToConstrain = [ "Lambda_c+" ]
REC.Xicc.MassPVFit.constrainToOriginVertex = True
REC.Xicc.MassPVFit.Verbose = True
REC.Xicc.MassPVFit.UpdateDaughters = True

"""
MC information
"""
from Configurables import TupleToolMCTruth
REC.ToolList += [
    "TupleToolMCBackgroundInfo",
    "TupleToolMCTruth"
    ]

MCTruth = TupleToolMCTruth()
MCTruth.ToolList =  [
    "MCTupleToolAngles"
    , "MCTupleToolHierarchy"
    , "MCTupleToolKinematic"
    ]
REC.addTool(MCTruth)



tuple_sel = Selection("tuple_sel_rec",
                      Algorithm = REC,
                      RequiredSelections = [Xiccsel])


############################# MCMatchObjP2MCRelator ############################

from Configurables import MCMatchObjP2MCRelator
import DecayTreeTuple.Configuration
default_rel_locs = MCMatchObjP2MCRelator().getDefaultProperty('RelTableLocations')
rel_locs = [loc for loc in default_rel_locs if 'Turbo' not in loc]

mctruth = REC.addTupleTool('TupleToolMCTruth/mctruth')
mctruth.addTool(MCMatchObjP2MCRelator)
mctruth.MCMatchObjP2MCRelator.RelTableLocations = rel_locs
mctruth.ToolList += [ "MCTupleToolKinematic","MCTupleToolHierarchy"]



# Configure DaVinci
from Configurables import DaVinci

from PhysConf.Selections import SelectionSequence
seq0 = SelectionSequence('SEQ0', tuple_sel_Lc )
seq1 = SelectionSequence('SEQ1', tuple_sel_Xicc )
seq2 = SelectionSequence('SEQ2', tuple_sel )
seq3 = SelectionSequence('SEQ3', mcTuple_sel )

DaVinci().EventPreFilters = fltrs.filters('Filter')
DaVinci().UserAlgorithms = [seq0.sequence(), seq1.sequence(), seq2.sequence(), seq3.sequence()] 
DaVinci().InputType = 'MDST' 
DaVinci().TupleFile = 'DV_Xiccpp_MC_TRUEID_2016.root' 
DaVinci().PrintFreq = 2500 
DaVinci().DataType = '2016' 
DaVinci().Simulation = True

rootInTES = '/Event/Turbo'
DaVinci().RootInTES = rootInTES
DaVinci().Turbo = True 

# Only ask for luminosity information when not using simulated data
DaVinci().Lumi = not DaVinci().Simulation 
DaVinci().EvtMax = -1
DaVinci().CondDBtag = 'sim-20170721-2-vc-md100' 
DaVinci().DDDBtag = 'dddb-20170721-3'

# Use the local input data

from Gaudi.Configuration import *
from GaudiConf import IOHelper
IOHelper().inputFiles(['/afs/cern.ch/work/p/pgaigne/DST/00071452_00000051_7.AllStreams.dst',
                       '/afs/cern.ch/work/p/pgaigne/DST/00071452_00000095_7.AllStreams.dst'], clear=True)

#IOHelper().inputFiles(['/afs/cern.ch/work/p/pgaigne/DST/00071452_00000051_7.AllStreams.dst'], clear=True)





