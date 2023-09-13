# Signal mode:  Hlt2CharmHadLcpToPpKmPipTurbo 

## --->>>
# Create Ntuple
from os import environ
from GaudiKernel.SystemOfUnits import *
from Gaudi.Configuration import *
from Configurables import GaudiSequencer, CombineParticles, FilterDesktop
from Configurables import DecayTreeTuple, EventTuple
from Configurables import TupleToolTrigger, TupleToolTISTOS,TupleToolPrimaries, TupleToolDecay
from Configurables import TupleToolVtxIsoln, TupleToolPid, TupleToolRecoStats, TupleToolVeto, TupleToolDecayTreeFitter
from Configurables import BackgroundCategory, EventCountHisto
from Configurables import LoKi__Hybrid__TupleTool, LoKi__Hybrid__EvtTupleTool

# There are three related lines. Give them human-readable names
nameRS = 'RS'
tupleNames = [ nameRS ]

# Now make the corresponding ntuples.
# Store them in ntpMap (keyed by name)
# and also in a flat list tupleListAll.
tupleListAll = []
ntpMap = {}
for ntpName in tupleNames:
	ntp = DecayTreeTuple(ntpName)
	ntpMap[ntpName] = ntp
	tupleListAll += [ ntp ]

# Ntuple setup
strInputRS  = 'Hlt2CharmHadLcpToPpKmPipTurbo/Particles'
strDecayRS  = '[Lambda_c+ -> ^p+ ^K- ^pi+]CC'
# Specify their input locations:
ntpMap[nameRS].Inputs  = [ strInputRS ]
# Specify their decay descriptors:
ntpMap[nameRS].Decay  = strDecayRS

# Each has different branches, according to the decay descriptor:
branchesRS = {
    "Lc"   : '^([Lambda_c+ -> p+ K- pi+]CC)',
    "LcP"  : '[Lambda_c+ -> ^p+ K- pi+]CC',
    "LcK"  : '[Lambda_c+ -> p+ ^K- pi+]CC',
    "LcPi" : '[Lambda_c+ -> p+ K- ^pi+]CC',
}

# Specify branches:
ntpMap[nameRS].Branches  = branchesRS

# TupleTools
MyToolList = [
    "TupleToolKinematic"
    ,"TupleToolPid"
    ,"TupleToolTrackInfo"
    ,"TupleToolPrimaries"
    ,"TupleToolPropertime"
    ,"TupleToolEventInfo"
    ,"TupleToolTrackInfo"
    ,"TupleToolRecoStats"
    ,"TupleToolGeometry"
]

# Trigger list
triggerListL0 = [ "L0HadronDecision",
                  "L0MuonDecision",
                  "L0DiMuonDecision",
                  "L0PhotonDecision",
                  "L0ElectronDecision"]
triggerListHlt1 = [ "Hlt1TrackAllL0Decision",
                    # Run2
                    "Hlt1TrackMVADecision",
                    "Hlt1TrackMVALooseDecision",
                    "Hlt1TwoTrackMVADecision",
                    "Hlt1TwoTrackMVALooseDecision",
                    "Hlt1L0AnyDecision",
                    "Hlt1MBNoBiasDecision" ]
#triggerListHlt2 = ["Hlt2CharmHadLcpToPpKmPipTurboDecision"]
## Together
myTriggerList = triggerListL0 + triggerListHlt1 #+ triggerListHlt2

# LoKi
LoKi_Kine = LoKi__Hybrid__TupleTool("LoKi_Kine")
LoKi_Kine.Variables = {
    "MAXDOCA" : "DOCAMAX",
    "DOCA12"  : "DOCACHI2MAX",
    "Y"       : "Y",
    "ETA"     : "ETA",
}

for dtt in tupleListAll:
    # Primaries
#    dtt.addTool(TupleToolPrimaries)
#    dtt.TupleToolPrimaries.InputLocation= "/Event/Turbo/Primary"

    # TISTOS for Lc
    dtt.addTool(TupleToolDecay, name='Lc')
    dtt.Lc.ToolList += [ "TupleToolTISTOS" ]
    dtt.Lc.addTool(TupleToolTISTOS, name="TupleToolTISTOS" )
    dtt.Lc.TupleToolTISTOS.Verbose=True
    dtt.Lc.TupleToolTISTOS.VerboseHlt1=True
    #dtt.Lc.TupleToolTISTOS.VerboseHlt2=True
    dtt.Lc.TupleToolTISTOS.TriggerList = myTriggerList

#    # DecayTreeFitter
#    # The Verbose option should create variables "for the head particle and its daughters too"
#    # There is a further UpdateDaughters option "to store the information from those tracks"
#    dtt.Lc.ToolList += ["TupleToolDecayTreeFitter/PVFit0"]
#    dtt.Lc.addTool(TupleToolDecayTreeFitter("PVFit0"))
#    dtt.Lc.PVFit0.Verbose = True
#    #dtt.C.PVFit0.constrainToOriginVertex = True
#    dtt.Lc.PVFit0.UpdateDaughters = True
#    #dttCC.PVFit0.daughtersToConstrain = ["Lambda_c+"]
#
#    dtt.Lc.ToolList += ["TupleToolDecayTreeFitter/PVFit1"]
#    dtt.Lc.addTool(TupleToolDecayTreeFitter("PVFit1"))
#    dtt.Lc.PVFit1.Verbose = True
#    dtt.Lc.PVFit1.constrainToOriginVertex = True
#    dtt.Lc.PVFit1.UpdateDaughters = True
#    #dttCC.PVFit1.daughtersToConstrain = ["Lambda_c+"]
#
#    dtt.Lc.ToolList += ["TupleToolDecayTreeFitter/PVFit2"]
#    dtt.Lc.addTool(TupleToolDecayTreeFitter("PVFit2"))
#    dtt.Lc.PVFit2.Verbose = True
#    #dtt.C.PVFit2.constrainToOriginVertex = True
#    dtt.Lc.PVFit2.UpdateDaughters = True
#    dtt.Lc.PVFit2.daughtersToConstrain = ["Lambda_c+"]

	## LoKi Tool
    dtt.ToolList += ["LoKi::Hybrid::TupleTool/LoKi_Kine"]
    dtt.addTool(LoKi_Kine)

    ## The following tool will cause error
    #LoKi_Event = LoKi__Hybrid__EvtTupleTool("LoKi_Event")
    #LoKi_Event.VOID_Variables={
    #        "nTracks" : "CONTAINS('Rec/Track/Best')"
    #        ,"nPVs"   : "CONTAINS('Rec/Vertex/Primary')"
    #}
    #dtt.addTool(LoKi_Event)
    #dtt.ToolList += [ "LoKi::Hybrid::EvtTupleTool/LoKi_Event" ]

    # Basic
    # Should not configure RootInTES for indivadual useralgorithm 
    #dtt.RootInTES = "/Event/Turbo"
    #dtt.WriteP2PVRelations = False

    dtt.ToolList += MyToolList

# Necessary from DaVinci v40r1 onward
from Configurables import DstConf, TurboConf
TurboConf().PersistReco=True
DstConf().Turbo=True

#from Configurables import DaVinci,  LoKi__HDRFilter, CheckPV
#checkPV = CheckPV("checkPV")
#SeqPhys = GaudiSequencer("SeqPhys")
#SeqPhys.Members += [checkPV]

# Momentum scale
from PhysConf.Selections import MomentumScaling, AutomaticData, TupleSelection
my_sels = [
     AutomaticData ("Hlt2CharmHadLcpToPpKmPipTurbo/Particles")
     ]
my_selection = [ MomentumScaling ( sel, Turbo = True , Year = '2016' ) for sel in my_sels]
from PhysConf.Selections import SelectionSequence
selseq = [ SelectionSequence ('MomScale'+str(ii), my_selection[ii]).sequence() for ii in range(len(my_selection))]
#selseq = [ SelectionSequence ('MomScale', sel).sequence() for sel in my_selection ]

from Configurables import DataOnDemandSvc
dod = DataOnDemandSvc()
from Configurables import Gaudi__DataLink as Link
rawEvt1 = Link ( 'LinkRawEvent1', What = '/Event/DAQ/RawEvent', Target = '/Event/Trigger/RawEvent' )
dod.AlgMap [ rawEvt1.Target ] = rawEvt1

# --->>>
# DaVinci configuration
from Configurables import DaVinci
from Configurables import CondDB

CondDB ( LatestGlobalTagByDataType = '2016')
DaVinci().DataType = '2016'
#DaVinci().DDDBtag ="dddb-20150526"
#DaVinci().CondDBtag = "cond-20160522"
# Process
DaVinci().UserAlgorithms = selseq + tupleListAll
#DaVinci().UserAlgorithms = tupleListAll
DaVinci().PrintFreq = 5000
DaVinci().SkipEvents = 0
DaVinci().Simulation = False
DaVinci().Lumi = not DaVinci().Simulation
DaVinci().EvtMax = -1
# Input
DaVinci().InputType = 'MDST'
DaVinci().Turbo = True
DaVinci().RootInTES = '/Event/Turbo'
# Output
DaVinci().HistogramFile = "DVHistos.root"
DaVinci().TupleFile = 'Tuple.root'

## XML summary
#from Configurables import LHCbApp
#LHCbApp().XMLSummary="summary.xml"

## --->>>
## Local test only
#DaVinci().EvtMax = 5000
DaVinci().PrintFreq = 500
from Gaudi.Configuration import *
from GaudiConf import IOHelper
IOHelper().inputFiles(['~/xiccpp/Data/00076510_00000114_1.charmspecparked.mdst',
                       '~/xiccpp/Data/00076510_00000004_1.charmspecparked.mdst'], clear=True)


