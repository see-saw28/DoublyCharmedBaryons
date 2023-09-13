# This option aims to reconstruct decay chain from mdst

from PhysSelPython.Wrappers import Selection, SelectionSequence
from PhysSelPython.Wrappers import DataOnDemand, AutomaticData
from GaudiKernel.SystemOfUnits import *
from Gaudi.Configuration import *
from Configurables import GaudiSequencer
from Configurables import CombineParticles

## Used for mcMatch
#MyPreambulo = [
#    'from LoKiPhysMC.decorators import *',
#    'from LoKiPhysMC.functions import mcMatch',
#    'from LoKiCore.functions import monitor',
#]


"""
Make LambdaC
"""
#from StandardParticles import StdAllNoPIDsMuons as Muons
from StandardParticles import StdAllNoPIDsKaons as Kaons
from StandardParticles import StdAllNoPIDsPions as Pions
from StandardParticles import StdAllNoPIDsProtons as Protons

# These are the important lines
from PhysConf.Selections import RebuildSelection
#Muons = RebuildSelection(Muons) 
Kaons = RebuildSelection(Kaons)
Pions = RebuildSelection(Pions)
Protons = RebuildSelection(Protons)

# Build the lambdac
importOptions("$STDOPTS/PreloadUnits.opts")
Lc_cc = "(in_range(2211,AM,2362)) &((APT1+APT2+APT3)>3000) &(AHASCHILD(PT>1000)) &(ANUM(PT>400)>=2) &(AHASCHILD((MIPCHI2DV(PRIMARY))>16.)) &(ANUM(MIPCHI2DV(PRIMARY)>9.)>=2)"
Lc_mc = "(VFASPF(VCHI2PDOF) < 10) &(BPVDIRA > lcldira ) &(BPVLTIME() > 0.15*picosecond )"
Lc_trk_cuts = "(TRCHI2DOF<3)&(PT>200.)&(P>1000.)&(MIPCHI2DV(PRIMARY)>6.)"
Lc_pream = [ "import math", "lcldira = math.cos(0.010)" ]
simLambdaC = CombineParticles("simLambdaC",
        DecayDescriptors = ["[Lambda_c+ -> p+ K- pi+]cc"],
        MotherCut = (Lc_mc),
        CombinationCut = (Lc_cc),
        DaughtersCuts = { 
            'p+' : "(P>10000.)"+"&"+Lc_trk_cuts,
            'pi+' : Lc_trk_cuts,
            'K-' : Lc_trk_cuts 
            }, 
        Preambulo = Lc_pream )
#    Preambulo = MyPreambulo+Lc_pream )

simSelLambdaC = Selection("simSelLambdaC", 
        Algorithm = simLambdaC, 
        RequiredSelections = [Kaons,Pions,Protons] )
simSelLambdaCSeq = SelectionSequence("simSelLambdaCSeq", TopSelection =  simSelLambdaC)

"""
Now the Xicc
"""
from Configurables import DaVinci__N4BodyDecays
Xicc_cc12  = "( AM < 4.0 * GeV ) " \
        "& ( ACHI2DOCA(1,2) < 10.0 ) "
Xicc_cc123 = "( AM < 4.0*GeV )& ((APT2 > 250) | (APT3 > 250))& ( ACHI2DOCA(1,3) < 10 ) & ( ACHI2DOCA(2,3) < 10 )"
Xicc_cc = ( " (in_range( 3.1 * GeV, AM, 4.0 * GeV ))" \
        "& (ANUM( ISBASIC & (PT > 250.0 * MeV) ) >= 1)" \
        "& (ANUM( ISBASIC & (PT > 250.0 * MeV) ) >= 2)" \
        "& ( APT > 2.0 * GeV )" \
        "& ( ACHI2DOCA(1,4) < 10.0 ) " \
        "& ( ACHI2DOCA(2,4) < 10.0 ) " \
        "& ( ACHI2DOCA(3,4) < 10.0 ) " )

Xicc_mc = "(VFASPF(VCHI2PDOF) < 60.0)" \
        "& (CHILD(VFASPF(VZ),1) - VFASPF(VZ) > 0.01 * mm)" \
        "& (BPVVDCHI2 > -1.0 )" \
        "& (BPVDIRA > lcldira )"
Xicc_pream = [
        "import math"
        ,"lcldira = math.cos( math.pi / 2.0 )"
        ]
Xicc_trk_cuts = "(TRCHI2DOF<3)&(PT>500.)&(P>1000.)"
simXicc = DaVinci__N4BodyDecays("simXicc",
        DecayDescriptor = "[Xi_cc++ -> Lambda_c+ K- pi+ pi+]cc",
        Preambulo = Xicc_pream,
        DaughtersCuts = {
            'Lambda_c+' : 'ALL',
            'K-' : Xicc_trk_cuts,
            'pi+' : Xicc_trk_cuts
            },
        MotherCut = Xicc_mc,
        CombinationCut = Xicc_cc,
        Combination12Cut = Xicc_cc12,
        Combination123Cut = Xicc_cc123 )
simSelXicc = Selection("simSelXicc",
        Algorithm = simXicc,
        RequiredSelections = [simSelLambdaC, Kaons, Pions])
simSelXiccSeq = SelectionSequence("simSelXiccSeq", TopSelection = simSelXicc)

"""
Tuple
"""
# Build by ourselvs
from Configurables import DecayTreeTuple
from DecayTreeTuple.Configuration import *
REC = DecayTreeTuple("REC",
        Inputs = [simSelXiccSeq.outputLocation()],
        Decay = '[Xi_cc++ -> ^(Lambda_c+ -> ^K- ^p+ ^pi+) ^K- ^pi+ ^pi+]CC',
        Branches = { "C":"[Xi_cc++ -> (Lambda_c+ -> K- p+ pi+) K- pi+ pi+]CC" ,
            "Lc" :     "[Xi_cc++ -> ^(Lambda_c+ -> p+ K- pi+) K- pi+ pi+]CC",
            "LcP":     "[Xi_cc++ -> (Lambda_c+ -> ^p+ K- pi+) K- pi+ pi+]CC",
            "LcK":     "[Xi_cc++ -> (Lambda_c+ -> p+ ^K- pi+) K- pi+ pi+]CC",
            "LcPi":    "[Xi_cc++ -> (Lambda_c+ -> p+ K- ^pi+) K- pi+ pi+]CC",
            "XiccK":   "[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) ^K- pi+ pi+]CC",
            "XiccPi1": "[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) K- ^pi+ pi+]CC",
            "XiccPi2": "[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) K- pi+ ^pi+]CC"
            }
        )

# Configure tools
myToolList = [ "TupleToolAngles",
        "TupleToolEventInfo",
        "TupleToolGeometry",
        "TupleToolKinematic",
        "TupleToolPid",
        "TupleToolPrimaries",
        "TupleToolTrackInfo",
        "TupleToolRecoStats",
        "TupleToolMCBackgroundInfo"
        ]
myTriggerList = [
        "L0HadronDecision",
        "L0ElectronDecision",
        "L0PhotonDecision",
        "L0HadronDecision",
        "L0MuonDecision",
        "L0MuonHighDecision",
        "L0DiMuonDecision",
        "L0PhysDecision",
        "L0GlobalDecision",

        "Hlt1TrackMVADecision",
        "Hlt1TrackMVALooseDecision",
        "Hlt1TwoTrackMVADecision",
        "Hlt1TwoTrackMVALooseDecision",
        ]
from Configurables import LoKi__Hybrid__TupleTool
LoKi_Kine = LoKi__Hybrid__TupleTool("LoKi_Kine")
LoKi_Kine.Variables = {
        "MAXDOCA" : "DOCAMAX",
        "DOCA12"  : "DOCACHI2MAX",
        "Y"  : "Y",
        "ETA"  : "ETA",
        }

from Configurables import MCMatchObjP2MCRelator
import DecayTreeTuple.Configuration
# Work around for Turbo locations being included in the default list    
# of relations table locations, which triggers Turbo unpacking and    
# seg. faults
default_rel_locs = MCMatchObjP2MCRelator().getDefaultProperty('RelTableLocations')
rel_locs = [loc for loc in default_rel_locs if 'Turbo' not in loc]

mctruth = REC.addTupleTool('TupleToolMCTruth/mctruth')
mctruth.addTool(MCMatchObjP2MCRelator)
mctruth.MCMatchObjP2MCRelator.RelTableLocations = rel_locs
mctruth.ToolList += [ "MCTupleToolKinematic","MCTupleToolHierarchy"]


from Configurables import TupleToolDecayTreeFitter
tupleList = [REC]
for dtt in tupleList:
    dtt.ToolList += myToolList
#    dtt.addTupleTool('TupleToolMCTruth').ToolList = [
#        "MCTupleToolAngles",
#        "MCTupleToolHierarchy",
#        "MCTupleToolKinematic",
#        "MCTupleToolReconstructed"
#        ]
    dtt.ToolList += ["LoKi::Hybrid::TupleTool/LoKi_Kine"]
    dtt.addTool(LoKi_Kine)
    from Configurables import TupleToolTISTOS
    dtt.ToolList += [ "TupleToolTISTOS" ]
    dtt.addTool(TupleToolTISTOS, name="TupleToolTISTOS" )
    dtt.TupleToolTISTOS.Verbose=True
    dtt.TupleToolTISTOS.VerboseHlt1=True
    #dtt.TupleToolTISTOS.VerboseHlt2=True
    dtt.TupleToolTISTOS.TriggerList = myTriggerList
    dtt.addTool(TupleToolDecay, name='C')
    dtt.C.ToolList += ["TupleToolDecayTreeFitter/PVFit1"]
    dtt.C.addTool(TupleToolDecayTreeFitter("PVFit1"))
    dtt.C.PVFit1.Verbose = True
    dtt.C.PVFit1.constrainToOriginVertex = True
    dtt.C.PVFit1.UpdateDaughters = True
    #dtt.C.PVFit1.daughtersToConstrain = ["Lambda_c+"]

    dtt.C.ToolList += ["TupleToolDecayTreeFitter/PVFit2"]
    dtt.C.addTool(TupleToolDecayTreeFitter("PVFit2"))
    dtt.C.PVFit2.Verbose = True
    #dtt.C.PVFit2.constrainToOriginVertex = True
    dtt.C.PVFit2.UpdateDaughters = True
    dtt.C.PVFit2.daughtersToConstrain = ["Lambda_c+"]

    dtt.C.ToolList += ["TupleToolDecayTreeFitter/PVFit3"]
    dtt.C.addTool(TupleToolDecayTreeFitter("PVFit3"))
    dtt.C.PVFit3.Verbose = True
    dtt.C.PVFit3.constrainToOriginVertex = True
    dtt.C.PVFit3.UpdateDaughters = True
    dtt.C.PVFit3.daughtersToConstrain = ["Lambda_c+"]

    dtt.C.ToolList += ["TupleToolDecayTreeFitter/PVFit0"]
    dtt.C.addTool(TupleToolDecayTreeFitter("PVFit0"))
    dtt.C.PVFit0.Verbose = True
    #dtt.C.PVFit0.constrainToOriginVertex = True
    dtt.C.PVFit0.UpdateDaughters = True
    #dtt.C.PVFit0.daughtersToConstrain = ["Lambda_c+"]



"""
Make MCDecayTree
"""
# MCDecayTree
mcdtt = MCDecayTreeTuple("mcntuple")
mcdtt.Decay = '[Xi_cc++ => ^(Lambda_c+ ==> ^K- ^p+ ^pi+) ^K- ^pi+ ^pi+]CC'
mcdtt.addBranches( {'C':   '[Xi_cc++ => (Lambda_c+ ==> K- p+ pi+) K- pi+ pi+]CC',
    'Lc':      '[Xi_cc++ => ^(Lambda_c+ ==> K- p+ pi+) K- pi+ pi+]CC',
    'XiccK':   '[Xi_cc++ => (Lambda_c+ ==> K- p+ pi+) ^K- pi+ pi+]CC',
    'LcK':     '[Xi_cc++ => (Lambda_c+ ==> ^K- p+ pi+) K- pi+ pi+]CC',
    'XiccPi1': '[Xi_cc++ => (Lambda_c+ ==> K- p+ pi+) K- ^pi+ pi+]CC',
    'XiccPi2': '[Xi_cc++ => (Lambda_c+ ==> K- p+ pi+) K- pi+ ^pi+]CC',
    'LcPi':    '[Xi_cc++ => (Lambda_c+ ==> K- p+ ^pi+) K- pi+ pi+]CC',
    'LcP':     '[Xi_cc++ => (Lambda_c+ ==> K- ^p+ pi+) K- pi+ pi+]CC'} )
mcdtt.ToolList += [
        "TupleToolRecoStats",
        "MCTupleToolKinematic",
        "MCTupleToolPrimaries",
        #     "MCTupleToolEventType",
        #     "MCTupleToolAngles",
        'MCTupleToolHierarchy',
        #     "MCTupleToolPID",
        #     "MCTupleToolPrompt",
        #     "MCTupleToolReconstructed"
        ]

## necessary for DaVinci v40r1 onwards
#from Configurables import DstConf, TurboConf
#TurboConf().PersistReco=True
#DstConf().Turbo=True

from Configurables import DaVinci
DaVinci().appendToMainSequence( [mcdtt,simSelLambdaCSeq.sequence(),
    simSelXiccSeq.sequence(),
    REC] )
DaVinci().EvtMax = -1                         # Number of events
DaVinci().SkipEvents = 0                      # Events to skip
DaVinci().PrintFreq = 5000
DaVinci().DataType = "2016"                    # Default is "DC06"
DaVinci().Simulation  = True
DaVinci().Lumi = not DaVinci().Simulation
#DaVinci().DDDBtag ="dddb-20150724"
#DaVinci().CondDBtag = "sim-20161124-2-vc-md100"
DaVinci().HistogramFile = "DVHistos.root"      # Histogram file
DaVinci().TupleFile = "Tuple.root"             # Ntuple
DaVinci().InputType = "DST"
#DaVinci().RootInTES = 'AllStreams'
#DaVinci().RootInTES = '/Event/Turbo'

DaVinci().CondDBtag = 'sim-20170721-2-vc-md100'
DaVinci().DDDBtag = 'dddb-20170721-3'

# Use the local input data



"""
For local test only
"""
#DaVinci().EvtMax = 5000
#DaVinci().PrintFreq = 5000
#
from Gaudi.Configuration import *
from GaudiConf import IOHelper
IOHelper().inputFiles(['~/xiccpp/00071452_00000051_7.AllStreams.dst'], clear=True)
#IOHelper().inputFiles([
#     '/afs/cern.ch/user/a/axu/eos/DST/MC16/00059106_00000001_7.AllStreams.dst'
#    ,'/afs/cern.ch/user/a/axu/eos/DST/MC16/00059106_00000002_7.AllStreams.dst'
#    ], clear=True)
