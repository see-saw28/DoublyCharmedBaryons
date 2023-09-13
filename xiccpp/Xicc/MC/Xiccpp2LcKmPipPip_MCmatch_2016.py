from DecayTreeTuple.Configuration import *
the_year = '2016' 
polarity = 'MD' 

#SOURCE
"https://gitlab.cern.ch/lhcb-charm/lhcb-ana-2020-060/-/blob/master/DVscripts/2016/MC/signal_channel/ResModel/26165854_uDST.py"

from PhysConf.Filters import LoKi_Filters
fltrs = LoKi_Filters (
   HLT2_Code = "HLT_PASS_RE('Hlt2CharmHadXiccpp2LcpKmPipPip_Lcp2PpKmPipTurboDecision') | HLT_PASS_RE('Hlt2CharmHadLcpToPpKmPipTurboDecision')"
)


def fillTuple(tuple, myBranches, myTriggerList):

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
    tuple.addTool(TupleToolDecay, name = 'Lc')
    tuple.addTool(TupleToolDecay, name = 'Xicc')

    # TISTOS for Lc+
    tuple.Lc.ToolList+=[ "TupleToolTISTOS" ]
    tuple.Lc.addTool(TupleToolTISTOS, name="TupleToolTISTOS" )
    tuple.Lc.TupleToolTISTOS.Verbose=True
    tuple.Lc.TupleToolTISTOS.TriggerList = myTriggerList

    # TISTOS for Xicc+
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

triggerListHlt2 = [ "Hlt2Topo2BodyDecision",
                    "Hlt2Topo3BodyDecision",
                    "Hlt2Topo4BodyDecision",
                    "Hlt2CharmHadLcpToPpKmPipTurboDecision",
                    "Hlt2CharmHadXiccpp2LcpKmPipPip_Lcp2PpKmPipTurboDecision"
                    ]

myTriggerList = triggerListL0 + triggerListHlt1 + triggerListHlt2




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
from StandardParticles import StdAllNoPIDsProtons as Protons

from PhysConf.Selections import RebuildSelection
Pions = RebuildSelection(Pions)#### 
Protons = RebuildSelection(Protons)
Kaons = RebuildSelection(Kaons)





##########################

# Build Lc candidates

##########################

Lc_daughters = {
       'p+'  : "mcMatch('[Lambda_c+ ==> pi+ K- ^p+]CC')",
       'K-'  : "mcMatch('[Lambda_c+ ==> pi+ ^K- p+]CC')",
       'pi+' : "mcMatch('[Lambda_c+ ==> ^pi+ K- p+]CC')"
       }

Lc_mother = ("mcMatch('[Lambda_c+]CC')")

Lc_sel = CombineSelection(
        'Sel_Lc',
        [Kaons, Pions, Protons],
        DecayDescriptor = "[Lambda_c+ -> pi+ K- p+]cc",
        Preambulo = MyPreambulo,
        DaughtersCuts=Lc_daughters,
        CombinationCut='AALL',
        MotherCut=Lc_mother
)






#########################

# Xicc reconstruction 

#########################


Xicc_mc = "mcMatch('[Xi_cc++]CC')"
Xicc_dc = {
        'K-' : "mcMatch('[Xi_cc++ => Lambda_c+ ^K- pi+ pi+]CC')",  
        'pi+' : "mcMatch('[Xi_cc++ => Lambda_c+ K- ^pi+ ^pi+]CC')"
        }


Xicc_sel  = CombineSelection(
    'Sel_Xicc',
    [Lc_sel, Pions, Kaons],
    DecayDescriptor = '[Xi_cc++ -> Lambda_c+ K- pi+ pi+]cc',
    Preambulo = MyPreambulo,
    DaughtersCuts = Xicc_dc,
    MotherCut = "ALL",
    CombinationCut = "AALL")

Xicc_sel = CheckPVSelection(Xicc_sel)
Xicc_sel = ValidBPVSelection(Xicc_sel)



REC = DecayTreeTuple("Xicc_REC",
        Decay = '[Xi_cc++ -> ^(Lambda_c+ -> ^K- ^p+ ^pi+) ^K- ^pi+ ^pi+]CC'
)





tuple_sel_rec = Selection("tuple_sel_rec",
                      Algorithm = REC,
                      RequiredSelections = [Xicc_sel])

fillTuple(REC, XiccpBranches, myTriggerList)



############################### Make MCDecayTree ###############################

mcdtt = MCDecayTreeTuple("mcntuple")
mcdtt.Decay = '[Xi_cc++ ==> ^(Lambda_c+ ==> ^p+ ^K- ^pi+) ^K- ^pi+ ^pi+]CC' 
mcdtt.addBranches( {
    'Xicc': '[Xi_cc++ => (Lambda_c+ ==> K- p+ pi+) K- pi+ pi+]CC',
    'Lc': '[Xi_cc++ => ^(Lambda_c+ ==> K- p+ pi+) K- pi+ pi+]CC',
    'XiccK': '[Xi_cc++ => (Lambda_c+ ==> K- p+ pi+) ^K- pi+ pi+]CC',
    'LcK': '[Xi_cc++ => (Lambda_c+ ==> ^K- p+ pi+) K- pi+ pi+]CC',
    'XiccPi1': '[Xi_cc++ => (Lambda_c+ ==> K- p+ pi+) K- ^pi+ pi+]CC',
    'XiccPi2': '[Xi_cc++ => (Lambda_c+ ==> K- p+ pi+) K- pi+ ^pi+]CC',
    'LcPi': '[Xi_cc++ => (Lambda_c+ ==> K- p+ ^pi+) K- pi+ pi+]CC',
    'LcP': '[Xi_cc++ => (Lambda_c+ ==> K- ^p+ pi+) K- pi+ pi+]CC'} )

mcdtt.ToolList += [
    "MCTupleToolKinematic",
    "MCTupleToolPrimaries",
    "MCTupleToolHierarchy",
    "MCTupleToolPID"]

mcTuple_sel = Selection("MCTree",
                    Algorithm = mcdtt,
                    RequiredSelections = [])

################################################################################

############################# MCMatchObjP2MCRelator ############################

from Configurables import MCMatchObjP2MCRelator
import DecayTreeTuple.Configuration
default_rel_locs = MCMatchObjP2MCRelator().getDefaultProperty('RelTableLocations')
rel_locs = [loc for loc in default_rel_locs if 'Turbo' not in loc]

mctruth = REC.addTupleTool('TupleToolMCTruth/mctruth')
mctruth.addTool(MCMatchObjP2MCRelator)
mctruth.MCMatchObjP2MCRelator.RelTableLocations = rel_locs
mctruth.ToolList += [ "MCTupleToolKinematic","MCTupleToolHierarchy"]

################################################################################

#from Configurables import DstConf, TurboConf
#TurboConf().PersistReco=True
#DstConf().Turbo=True

from Configurables import CheckPV
checkPV = CheckPV("checkPV")
checkPV.MinPVs = 1




# Configure DaVinci
from Configurables import DaVinci

from PhysConf.Selections import SelectionSequence

seq0 = SelectionSequence('SEQ0', mcTuple_sel )
seq1 = SelectionSequence('SEQ1', Lc_sel )
seq2 = SelectionSequence('SEQ2', Xicc_sel)
seq3 = SelectionSequence('SEQ3', tuple_sel_rec)



#DaVinci().EventPreFilters = fltrs.filters('Filter')
DaVinci().UserAlgorithms = [mcdtt, checkPV, seq1.sequence(), seq2.sequence(), seq3.sequence()] 
DaVinci().InputType = 'MDST' 
DaVinci().TupleFile = 'DV_Xiccpp_MCmatch_2016.root' 
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





