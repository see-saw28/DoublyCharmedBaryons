from GaudiConf import IOHelper
from Configurables import DaVinci, DecayTreeTuple
from DecayTreeTuple.Configuration import *

# Stream and stripping line we want to use
stream = 'AllStreams'
#line = 'XiccSLXicc2LambdacMuNuLine'
line = 'Hlt2CharmHadLcpToPpKmPipTurboLine'

# Create an ntuple to capture D*+ decays from the StrippingLine line
dtt = DecayTreeTuple('TupleDstToLambdac')
dtt.Inputs = ['/Event/{0}/Phys/{1}/Particles'.format(stream, line)]
# Note that we mark all particles, otherwise the branches won't work
dtt.Decay = '[Lambda_c+ -> ^p+ ^K- ^pi+]CC' 
track_tool = dtt.addTupleTool('TupleToolTrackInfo')
track_tool.Verbose = True
dtt.addTupleTool('TupleToolPrimaries')


dtt.addBranches({
    'Lambdac': '[Lambda_c+ -> p+ K- pi+]CC' ,
    'p': '[Lambda_c+ -> ^p+ K- pi+]CC' ,
    'Kminus': '[Lambda_c+ -> p+ ^K- pi+]CC' ,
    'Piplus': '[Lambda_c+ -> p+ K- ^pi+]CC' 
})


# Configure DaVinci
DaVinci().UserAlgorithms += [dtt]
DaVinci().InputType = 'DST'
DaVinci().TupleFile = 'DVntuple1.root'
DaVinci().PrintFreq = 1000
DaVinci().DataType = '2016'
DaVinci().Simulation = True
# Only ask for luminosity information when not using simulated data
DaVinci().Lumi = not DaVinci().Simulation
DaVinci().EvtMax = -1
DaVinci().CondDBtag = 'sim-20161124-2-vc-md100'
DaVinci().DDDBtag = 'dddb-20150724'


# Use the local input data
#IOHelper().inputFiles([('root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb/MC/2016/ALLSTREAMS.DST/00062298/0000/00062298_00000112_7.AllStreams.dst')], clear=True)
#IOHelper().inputFiles([('root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb/MC/2016/ALLSTREAMS.DST/00071452/0000/00071452_00000095_7.AllStreams.dst')], clear=True)
IOHelper().inputFiles([('00071452_00000051_7.AllStreams.dst')], clear=True)
