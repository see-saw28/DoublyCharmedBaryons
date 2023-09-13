
the_year = '2016'
polarity = 'MD'

########################################################################
#
# The MC truth Tuple
#
from PhysConf.Selections import Selection
from Configurables import MCDecayTreeTuple, TupleToolTrigger, TupleToolTISTOS
mcTuple = MCDecayTreeTuple("MCTuple")
#mcTuple.Decay = '[Xi_cc++ -> ^(Lambda_c+ -> ^p+ ^K- ^pi+) ^K- ^pi+ ^pi+]CC'
#mcTuple.Decay = '[Xi_cc++ -> ^Lambda_c+ ^K- ^pi+ ^pi+]CC'
mcTuple.Decay = '[Xi_cc++]CC'

#mcTuple.ToolList = [ "MCTupleToolKinematic", "MCTupleToolHierarchy"  ]

mcTuple.Branches = {
    "Xiccpp"   :"[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) K- pi+ pi+]CC",
    "Lcp"  :"[Xi_cc++ -> ^(Lambda_c+ -> p+ K- pi+) K- pi+ pi+]CC",
    "Km_Xicc"    :"[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) ^K- pi+ pi+]CC",
    "pip_Xicc1"   :"[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) K- ^pi+ pi+]CC",
    "pip_Xicc2"    :"[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) K- pi+ ^pi+]CC",
    "Km_Lcp"    :"[Xi_cc++ -> (Lambda_c+ -> p+ ^K- pi+) K- pi+ pi+]CC",
    "proton":"[Xi_cc++ -> (Lambda_c+ -> ^p+ K- pi+) K- pi+ pi+]CC",
    "pip_Lcp"   :"[Xi_cc++ -> (Lambda_c+ -> p+ K- ^pi+) K- pi+ pi+]CC",
    
    }

mcTuple_sel = Selection("MCTree",
                        Algorithm = mcTuple,
                        RequiredSelections = [])


rootInTES = '/Event/Turbo'



from Configurables import DecayTreeTuple 
from DecayTreeTuple.Configuration import * 
from GaudiConf import IOHelper
from PhysConf.Selections import AutomaticData

# Stream and stripping line we want to use
stream = 'AllStreams' 

## Xi_cc++ line
#line = 'Hlt2CharmHadXiccpp2LcpKmPipPip_Lcp2PpKmPipTurbo/Particles'

#line = 'Hlt2CharmHadXic0ToPpKmKmPipTurbo'

## Lambda_c line
line = 'Hlt2CharmHadLcpToPpKmPipTurbo/Particles'


Lc = AutomaticData(line)

# Create an ntuple to capture Xicc++  decays from TurboLine
dtt = DecayTreeTuple('TupleXiccppToLcpKmPipPip') 
#dtt.Inputs = ['{0}/Particles'.format(line)] 
dtt.Inputs = [Lc.outputLocation()] 
#dtt.Decay = '[Xi_cc++]CC' 
#dtt.Decay = '[Xi_cc++ -> ^(Lambda_c+ -> ^p+ ^K- ^pi+) ^K- ^pi+ ^pi+]CC'
dtt.Decay = '[Lambda_c+]CC'

################################################# 
## (6) build the final selection sequence
from PhysConf.Selections import SelectionSequence
seq0 = SelectionSequence('SEQ0', mcTuple_sel )

# Configure DaVinci
from Configurables import DaVinci

DaVinci().UserAlgorithms += [dtt] 
DaVinci().InputType = 'MDST' 
DaVinci().TupleFile = 'RD_DVntuple.root' 
DaVinci().PrintFreq = 2500 
DaVinci().DataType = '2016' 
DaVinci().Simulation = False
DaVinci().RootInTES = rootInTES
DaVinci().Turbo = True 

# Only ask for luminosity information when not using simulated data
DaVinci().Lumi = not DaVinci().Simulation 
DaVinci().EvtMax = 3000 
#DaVinci().CondDBtag = 'sim-20170721-2-vc-md100' 
#DaVinci().DDDBtag = 'dddb-20170721-3'

# Use the local input data
IOHelper().inputFiles(['00076510_00000004_1.charmspecparked.mdst'], clear=True)



