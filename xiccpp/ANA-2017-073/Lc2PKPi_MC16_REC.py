from os import environ

from GaudiKernel.SystemOfUnits import *
from Gaudi.Configuration import *
from Configurables import ( GaudiSequencer
                            ,CombineParticles
                            ,DecayTreeTuple
                            ,TupleToolTrigger
                            ,TupleToolTISTOS
                            ,FilterDesktop
                            ,TupleToolPrimaries
                            ,MCDecayTreeTuple
                            ,BackgroundCategory
                            ,TupleToolDecay
                            ,TupleToolVtxIsoln
                            ,TupleToolPid
                            ,TupleToolRecoStats
                            ,TupleToolPropertime
                            ,TupleToolVeto
                            ,LoKi__Hybrid__TupleTool
                            ,ReadHltReport )
from DecayTreeTuple.Configuration import *

from PhysSelPython.Wrappers import Selection, SelectionSequence
from PhysSelPython.Wrappers import DataOnDemand, AutomaticData

# REC 
from StandardParticles import StdAllNoPIDsKaons as Kaons
from StandardParticles import StdAllNoPIDsPions as Pions
from StandardParticles import StdAllNoPIDsProtons as Protons
from PhysConf.Selections import RebuildSelection

Kaons = RebuildSelection(Kaons)
Pions = RebuildSelection(Pions)
Protons = RebuildSelection(Protons)

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
        'p+'  : "(P>10000.)"+"&"+Lc_trk_cuts,
        'pi+' : Lc_trk_cuts,
        'K-'  : Lc_trk_cuts
        },
    Preambulo = Lc_pream )
simSelLambdaC = Selection("simSelLambdaC",
                          Algorithm = simLambdaC,
                          RequiredSelections = [Kaons,Pions,Protons] )
simSelLambdaCSeq = SelectionSequence("simSelLambdaCSeq", TopSelection =  simSelLambdaC)

REC = DecayTreeTuple( "REC", Inputs = [simSelLambdaCSeq.outputLocation()] )


# MCMATCH
MyPreambulo = [
    'from LoKiPhysMC.decorators import *',
    'from LoKiPhysMC.functions import mcMatch',
    'from LoKiCore.functions import monitor'
    ]

mcsimLambdaC = CombineParticles("mcsimLambdaC",
    DecayDescriptors = ["[Lambda_c+ -> p+ K- pi+]cc"],
    MotherCut = "mcMatch( '[Lambda_c+ => p+ K- pi+]CC' )",
    CombinationCut = 'AALL',
#    DaughtersCuts = {'p+':'ALL','pi+':'ALL','K-':'ALL'},
    DaughtersCuts = {
        'p+' :  "mcMatch ( 'Lambda_c+ => ^p+ K- pi+' )",
        'pi+' : "mcMatch ( 'Lambda_c+ => p+ K- ^pi+' )",
        'K-' :  "mcMatch ( 'Lambda_c+ => p+ ^K- pi+' )",
        'p~-' :  "mcMatch ( 'Lambda_c~- => ^p~- K+ pi-' )",
        'pi-' : "mcMatch ( 'Lambda_c~- => p~- K+ ^pi-' )",
        'K+' :  "mcMatch ( 'Lambda_c~- => p~- ^K+ pi-' )"
        },
    Preambulo = MyPreambulo )
mcsimSelLambdaC = Selection("mcsimSelLambdaC",
                          Algorithm = mcsimLambdaC,
                          RequiredSelections = [Kaons,Pions,Protons] )
mcsimSelLambdaCSeq = SelectionSequence("mcsimSelLambdaCSeq", TopSelection =  mcsimSelLambdaC)

MCMATCH = DecayTreeTuple( "MCMATCH", Inputs = [mcsimSelLambdaCSeq.outputLocation()] )


# TURBO
hlt2_line = "Hlt2CharmHadLcpToPpKmPipTurbo"
TURBO = DecayTreeTuple( "TURBO", Inputs = ["/Event/Turbo/{0}/Particles".format(hlt2_line)] )


# Add tuple tools
decay_mode = "[ Lambda_c+ ->^p+ ^K- ^pi+ ]CC"
Lc2pKpiBranches = {
    "Lc"     :  "^([ Lambda_c+ -> p+  K-  pi+ ]CC)",
    "LcP"    :  "[ Lambda_c+ ->^p+  K-  pi+ ]CC",
    "LcK"    :  "[ Lambda_c+ -> p+ ^K-  pi+ ]CC",
    "LcPi"   :  "[ Lambda_c+ -> p+  K- ^pi+ ]CC"
}

mtriglist= [
  # L0
  "L0ElectronDecision",
  "L0PhotonDecision",
  "L0HadronDecision",
  # L0 Muon
  "L0MuonDecision",
  "L0MuonHighDecision",
  "L0DiMuonDecision",
  # Hlt1 track    
  "Hlt1TrackAllL0Decision",
  "Hlt1TrackMuonDecision",
  "Hlt1TrackPhotonDecision",
  # Run-II
  "Hlt1TrackMVADecision",
  "Hlt1TrackMVALooseDecision",
  "Hlt1TwoTrackMVADecision",
  "Hlt1TwoTrackMVALooseDecision",
  "Hlt1L0AnyDecision",
  "Hlt1MBNoBiasDecision",
  #Hlt2
  "Hlt2CharmHadLcpToPpKmPipTurboDecision"
]

tl= [ "TupleToolKinematic"
      ,"TupleToolPid"
      ,"TupleToolL0Data"
      ,"TupleToolEventInfo"
      ,"TupleToolTrackInfo"
      ,"TupleToolRecoStats"
      ,"TupleToolGeometry"
      ,"TupleToolPrimaries"
      ,"TupleToolPropertime"
      ,"TupleToolMCTruth"
      ,"TupleToolMCBackgroundInfo" ]

MCTruth = TupleToolMCTruth()
MCTruth.ToolList = [
    "MCTupleToolAngles"
    ,"MCTupleToolHierarchy"
    ,"MCTupleToolKinematic"
    ,"MCTupleToolReconstructed"
	]

# LoKi
LoKi_Kine = LoKi__Hybrid__TupleTool("LoKi_Kine")
LoKi_Kine.Variables = {
    "MAXDOCA" : "DOCAMAX",
    "DOCA12"  : "DOCACHI2MAX",
    "Y"       : "Y",
    "ETA"     : "ETA",
}

# Loop for all tuples
tuple_list = [REC, MCMATCH, TURBO]
for dtt in tuple_list:
    dtt.Decay = decay_mode
    dtt.addBranches(Lc2pKpiBranches)
    dtt.ToolList += tl
    dtt.addTool(MCTruth)
    dtt.ToolList += ["LoKi::Hybrid::TupleTool/LoKi_Kine"]
    dtt.addTool(LoKi_Kine)

    # TISTOS for Lc
    dtt.addTool(TupleToolDecay, name='Lc')
    dtt.Lc.ToolList += [ "TupleToolTISTOS" ]
    dtt.Lc.addTool(TupleToolTISTOS, name="TupleToolTISTOS")
    dtt.Lc.TupleToolTISTOS.Verbose=True
    dtt.Lc.TupleToolTISTOS.VerboseHlt1=True
    dtt.Lc.TupleToolTISTOS.VerboseHlt2=True
    dtt.Lc.TupleToolTISTOS.TriggerList = mtriglist


# MCDecayTree
mct = MCDecayTreeTuple('mctuple')
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

# CheckPV
from Configurables import LoKi__HDRFilter, CheckPV
checkPV = CheckPV("checkPV")
#checkPV.MinPVs = 1
SeqPhys = GaudiSequencer("SeqPhys")
SeqPhys.Members += [ checkPV
                     ,simSelLambdaCSeq.sequence()
                     ,REC
                     ,mcsimSelLambdaCSeq.sequence()
                     ,MCMATCH]

#checkPV1 = CheckPV("checkPV1")
#SeqPhys1 = GaudiSequencer("SeqPhys1")
#SeqPhys1.Members += [checkPV1, mcsimSelLambdaCSeq.sequence(), MCMATCH]

# Tags
from Configurables import CondDB
CondDB ( LatestGlobalTagByDataType = '2016')

# DaVinci
from Configurables import DaVinci
DaVinci().UserAlgorithms = [SeqPhys, mct, TURBO]
DaVinci().InputType = 'DST'
DaVinci().TupleFile = "Tuple.root"
DaVinci().PrintFreq = 5000
DaVinci().EvtMax = -1
DaVinci().DataType = "2016"
DaVinci().Simulation = True
DaVinci().Lumi = False
DaVinci().SkipEvents = 0
#DaVinci().DDDBtag ="dddb-20150724"
#DaVinci().CondDBtag = "sim-20161124-2-vc-md100"
DaVinci().HistogramFile = "DVHistos.root"
#DaVinci().Turbo = True
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


## BEGIN DATA BIT, USED ONLY FOR LOCAL TESTING
#DaVinci().EvtMax = 5000
#DaVinci().PrintFreq = 500
#from GaudiConf import IOHelper
#IOHelper().inputFiles([
#    '/afs/cern.ch/user/a/axu/eos/DST/MC16/25103000_Sim09b_Trig0x6138160F/00059810_00000001_7.AllStreams.dst'
#    ,'/afs/cern.ch/user/a/axu/eos/DST/MC16/25103000_Sim09b_Trig0x6138160F/00059810_00000002_7.AllStreams.dst'
#], clear=True)
## END DATA BIT
