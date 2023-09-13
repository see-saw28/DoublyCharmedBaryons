from DecayTreeTuple.Configuration import *
the_year = '2016' 
polarity = 'MD' 



Lc2pKpiBranches = {
    "Lc"     :  "^([ Lambda_c+ -> p+  K-  pi+ ]CC)",
    "LcP"    :  "[ Lambda_c+ ->^p+  K-  pi+ ]CC",
    "LcK"    :  "[ Lambda_c+ -> p+ ^K-  pi+ ]CC",
    "LcPi"   :  "[ Lambda_c+ -> p+  K- ^pi+ ]CC"
}



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





############################### 

#      Make MCDecayTree 

###############################

#################
#### LAMBDAC ####
#################

mct = MCDecayTreeTuple('mctupleLc')
mct.Decay = "[ Lambda_c+ ==>^p+ ^K- ^pi+ ]CC"
mct.Branches = {
		"Lc"   : "^([ Lambda_c+ ==>p+ K- pi+ ]CC)",
		"LcP"  : "[ Lambda_c+ ==>^p+ K- pi+ ]CC",
		"LcK"  : "[ Lambda_c+ ==>p+ ^K- pi+ ]CC",
		"LcPi": "[ Lambda_c+ ==>p+ K- ^pi+ ]CC",
  }
mctl = [ 'MCTupleToolAngles'
        ,'TupleToolRecoStats'
        ,'MCTupleToolHierarchy'
        ,'MCTupleToolKinematic'
        ,'MCTupleToolPrimaries'
        ,'MCTupleToolReconstructed'
        ,'MCTupleToolInteractions' ]
#mct.ToolList = mctl

mcTuple_sel = Selection("MCTree",
                        Algorithm = mct,
                        RequiredSelections = [])
##########################

# Build from Turbo line

##########################

## Lambda_c line
line = 'Hlt2CharmHadLcpToPpKmPipTurbo/Particles'

Lc = AutomaticData(line)

TURBO_Lc = DecayTreeTuple('TURBO_Lambdac') 
TURBO_Lc.Inputs = [Lc.outputLocation()] 
#TURBO_Lc.Decay = '[Lambda_c+ -> ^p+ ^K- ^pi+]CC'
TURBO_Lc.Decay = '[Lambda_c+]CC'



# Configure DaVinci
from Configurables import DaVinci

from PhysConf.Selections import SelectionSequence
seq0 = SelectionSequence('SEQ0', mcTuple_sel )

DaVinci().UserAlgorithms = [TURBO_Lc, seq0.sequence()] 
DaVinci().InputType = 'MDST' 
DaVinci().TupleFile = 'TURBO_DVntuple.root' 
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
IOHelper().inputFiles(['~/xiccpp/00071452_00000051_7.AllStreams.dst'], clear=True)
#IOHelper().inputFiles(['00071452_00000095_7.AllStreams.dst'], clear=True)



