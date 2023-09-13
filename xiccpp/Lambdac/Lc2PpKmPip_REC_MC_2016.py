from DecayTreeTuple.Configuration import *
the_year = '2016' 
polarity = 'MD' 


def fillTuple(tuple, myBranches, myTriggerList, Xicc=False):

    tuple.Branches = myBranches

    tuple.ToolList = [
                "TupleToolTrackInfo"
               ,"TupleToolEventInfo"
               ,"TupleToolKinematic"
               ,"TupleToolAngles"
               ,"TupleToolGeometry"
               ,"TupleToolPid"
               ,"TupleToolPrimaries"
               ,"TupleToolPropertime"
               ,"TupleToolMCBackgroundInfo"
               ,"TupleToolL0Data"
               ,"TupleToolRecoStats"
               ]

    #MCTruth = TupleToolMCTruth()
    #MCTruth.ToolList = [ "MCTupleToolKinematic", "MCTupleToolHierarchy"]
    #tuple.addTool(MCTruth)

    # RecoStats for filling SpdMult, etc
    from Configurables import TupleToolRecoStats
    tuple.addTool(TupleToolRecoStats, name="TupleToolRecoStats")
    tuple.TupleToolRecoStats.Verbose=True

    from Configurables import TupleToolTISTOS, TupleToolDecay
    tuple.addTool(TupleToolDecay, name = 'Lambdac')
    if Xicc:
        tuple.addTool(TupleToolDecay, name = 'Xicc')

    # TISTOS for Xic+
    tuple.Lambdac.ToolList+=[ "TupleToolTISTOS" ]
    tuple.Lambdac.addTool(TupleToolTISTOS, name="TupleToolTISTOS" )
    tuple.Lambdac.TupleToolTISTOS.Verbose=True
    tuple.Lambdac.TupleToolTISTOS.TriggerList = myTriggerList

    # TISTOS for Xicc++
    if Xicc:
        tuple.Xicc.ToolList+=[ "TupleToolTISTOS" ]
        tuple.Xicc.addTool(TupleToolTISTOS, name="TupleToolTISTOS" )
        tuple.Xicc.TupleToolTISTOS.Verbose=True
        tuple.Xicc.TupleToolTISTOS.TriggerList = myTriggerList

    # DTF
        from Configurables import TupleToolDecayTreeFitter
        tuple.Xicc.ToolList +=  ["TupleToolDecayTreeFitter/Fit",
                            "TupleToolDecayTreeFitter/PVFit",
                            "TupleToolDecayTreeFitter/MassFit",
                            "TupleToolDecayTreeFitter/MassPVFit"
                            ]

        tuple.Xicc.ToolList += ["TupleToolDecayTreeFitter/Fit"]
        tuple.Xicc.addTool(TupleToolDecayTreeFitter("Fit"))
        tuple.Xicc.Fit.Verbose = True
        tuple.Xicc.Fit.UpdateDaughters = True

        tuple.Xicc.ToolList += ["TupleToolDecayTreeFitter/PVFit"]
        tuple.Xicc.addTool(TupleToolDecayTreeFitter("PVFit"))
        tuple.Xicc.PVFit.Verbose = True
        tuple.Xicc.PVFit.constrainToOriginVertex = True
        tuple.Xicc.PVFit.UpdateDaughters = True

        tuple.Xicc.ToolList += ["TupleToolDecayTreeFitter/MassFit"]
        tuple.Xicc.addTool(TupleToolDecayTreeFitter("MassFit"))
        tuple.Xicc.MassFit.Verbose = True
        tuple.Xicc.MassFit.UpdateDaughters = True
        tuple.Xicc.MassFit.daughtersToConstrain = [ "Lambda_c+" ]

        tuple.Xicc.ToolList += ["TupleToolDecayTreeFitter/MassPVFit"]
        tuple.Xicc.addTool(TupleToolDecayTreeFitter("MassPVFit"))
        tuple.Xicc.MassPVFit.daughtersToConstrain = [ "Lambda_c+" ]
        tuple.Xicc.MassPVFit.constrainToOriginVertex = True
        tuple.Xicc.MassPVFit.Verbose = True
        tuple.Xicc.MassPVFit.UpdateDaughters = True

    #LoKi
    from Configurables import LoKi__Hybrid__TupleTool
    LoKi_DOCA = LoKi__Hybrid__TupleTool("LoKi_DOCA")
    LoKi_DOCA.Variables = {
            "MAXDOCA"     : "DOCAMAX",
            "MINDOCA"     : "LoKi.Particles.PFunA(AMINDOCA('LoKi::TrgDistanceCalculator'))",
            "LOKI_IPCHI2" : "BPVIPCHI2()",
            "DOCA12"      : "DOCACHI2MAX",
            "Y"           : "Y",
            "ETA"         : "ETA"}

    tuple.ToolList+=["LoKi::Hybrid::TupleTool/LoKi_DOCA"]
    tuple.addTool(LoKi_DOCA)

################################# Trigger List #################################

triggerListL0 = [ "L0HadronDecision",
                  "L0DiMuonDecision",
                  "L0MuonDecision",
                  "L0PhotonDecision",
                  "L0ElectronDecision"]

triggerListHlt1 = [ "Hlt1TrackMVADecision",
                    "Hlt1TwoTrackMVADecision",
                    "Hlt1TrackMVALooseDecision",
                    "Hlt1TwoTrackMVALooseDecision",
                    "Hlt1L0AnyDecision",
                    "Hlt1MBNoBiasDecision"]

triggerListHlt2_Lc = [ "Hlt2Topo2BodyDecision",
                    "Hlt2Topo3BodyDecision",
                    "Hlt2Topo4BodyDecision",
                    "Hlt2CharmHadLcpToPpKmPipTurboDecision",
                    ]

myTriggerList = triggerListL0 + triggerListHlt1 + triggerListHlt2_Lc

Lc2pKpiBranches = {
    "Lc"     :  "^([ Lambda_c+ -> p+  K-  pi+ ]CC)",
    "LcP"    :  "[ Lambda_c+ ->^p+  K-  pi+ ]CC",
    "LcK"    :  "[ Lambda_c+ -> p+ ^K-  pi+ ]CC",
    "LcPi"   :  "[ Lambda_c+ -> p+  K- ^pi+ ]CC"
}


XiccpBranches = { 
            "Xicc":"[Xi_cc++ -> (Lambda_c+ -> K- p+ pi+) K- pi+ pi+]CC" ,
            "Lc" :     "[Xi_cc++ -> ^(Lambda_c+ -> p+ K- pi+) K- pi+ pi+]CC",
            "LcP":     "[Xi_cc++ -> (Lambda_c+ -> ^p+ K- pi+) K- pi+ pi+]CC",
            "LcK":     "[Xi_cc++ -> (Lambda_c+ -> p+ ^K- pi+) K- pi+ pi+]CC",
            "LcPi":    "[Xi_cc++ -> (Lambda_c+ -> p+ K- ^pi+) K- pi+ pi+]CC",
            "XiccK":   "[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) ^K- pi+ pi+]CC",
            "XiccPi1": "[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) K- ^pi+ pi+]CC",
            "XiccPi2": "[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) K- pi+ ^pi+]CC"
            }

from Configurables import GaudiSequencer, CombineParticles
from PhysSelPython.Wrappers import Selection, SelectionSequence
from PhysSelPython.Wrappers import DataOnDemand, AutomaticData
from GaudiKernel.SystemOfUnits import *
from PhysConf.Selections import CheckPVSelection, ValidBPVSelection
from PhysConf.Selections import CombineSelection

from StandardParticles import StdAllNoPIDsKaons as Kaons 
from StandardParticles import StdAllNoPIDsPions as Pions 
from StandardParticles import StdAllNoPIDsProtons as Protons 

from PhysConf.Selections import RebuildSelection 
Kaons = RebuildSelection(Kaons) 
Pions = RebuildSelection(Pions) 
Protons = RebuildSelection(Protons) 

MyPreambulo = [
    'from LoKiPhysMC.decorators import *',
    'from LoKiPhysMC.functions import mcMatch',
    'from LoKiCore.functions import monitor',
    ]

####################################

#       Build from scratch

####################################

Lambdac_daughters = {
       'p+'  : "mcMatch('[Lambda_c+ ==> pi+ K- ^p+]CC')",
       'K-'  : "mcMatch('[Lambda_c+ ==> pi+ ^K- p+]CC')",
       'pi+' : "mcMatch('[Lambda_c+ ==> ^pi+ K- p+]CC')"
       }

Lambdac_mother = ("mcMatch('[Lambda_c+]CC')")

Lambdac_sel = CombineSelection(
        'Sel_Lambdac',
        [Kaons, Pions, Protons],
        DecayDescriptor = "[Lambda_c+ -> pi+ K- p+]cc",
        Preambulo = MyPreambulo,
        DaughtersCuts=Lambdac_daughters,
        CombinationCut='AALL',
        MotherCut=Lambdac_mother
)

Lambdac_seq = SelectionSequence("Lambdac_seq", TopSelection=Lambdac_sel)

REC_Lc = DecayTreeTuple('LambdacToPpKmPip',
        Inputs = [Lambdac_seq.outputLocation()],
        Decay = '[Lambda_c+ -> ^p+ ^K- ^pi+]CC')

fillTuple(REC_Lc, Lc2pKpiBranches, myTriggerList)


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
mct.ToolList = mctl

##############
#### XICC ####
##############

mcdtt = MCDecayTreeTuple("mcntupleXicc")
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

fillTuple(TURBO_Lc, Lc2pKpiBranches, myTriggerList)


############################# MCMatchObjP2MCRelator ############################

from Configurables import MCMatchObjP2MCRelator
import DecayTreeTuple.Configuration
default_rel_locs = MCMatchObjP2MCRelator().getDefaultProperty('RelTableLocations')
rel_locs = [loc for loc in default_rel_locs if 'Turbo' not in loc]
print(default_rel_locs)

mctruth = REC_Lc.addTupleTool('TupleToolMCTruth/mctruth')
mctruth.addTool(MCMatchObjP2MCRelator)
mctruth.MCMatchObjP2MCRelator.RelTableLocations = rel_locs
mctruth.ToolList += [ "MCTupleToolKinematic","MCTupleToolHierarchy"]



from Configurables import CheckPV
checkPV = CheckPV("checkPV")
checkPV.MinPVs = 1


# Configure DaVinci
from Configurables import DaVinci

DaVinci().appendToMainSequence([mct, checkPV, Lambdac_seq.sequence(), REC_Lc])
#DaVinci().UserAlgorithms = [seq0.sequence(), dtt] 
DaVinci().InputType = 'MDST' 
DaVinci().TupleFile = 'REC_DVntuple.root' 
DaVinci().PrintFreq = 2500 
DaVinci().DataType = '2016' 
DaVinci().Simulation = True


rootInTES = '/Event/Turbo'
#DaVinci().RootInTES = rootInTES
#DaVinci().Turbo = True 

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



