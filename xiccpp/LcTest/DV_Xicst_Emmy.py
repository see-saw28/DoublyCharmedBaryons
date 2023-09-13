the_year = '2017'

if ((the_year == '2017') | (the_year == '2018')):
##    rootInTES = '/Event/Charmmultibody/Turbo'
    rootInTES = '/Event/Charmspec/Turbo'
if ((the_year == '2015') | (the_year == '2016')):
    rootInTES = '/Event/Turbo'

the_line  = 'Hlt2CharmHadLcpToPpKmPipTurbo/Particles'

## use pre-filters to speedup
from PhysConf.Filters import LoKi_Filters
fltrs = LoKi_Filters (
        VOID_Code = """
            0 < CONTAINS('%s/%s')
                """ % ( rootInTES , the_line )
            )

###########################################################
decay0     = "[Lambda_c+ -> ^p+  ^K- ^pi+]CC"
decay      = "[D*_s+ ->  ^(Lambda_c+ -> ^p+  ^K- ^pi+) ^K-]CC"
decayWS    = "[D*_s+ ->  ^(Lambda_c+ -> ^p+  ^K- ^pi+) ^K+]CC"
decay1     = "[D*_s+ ->  ^(Lambda_c+ -> ^p+  ^K- ^pi+) ^K- ^pi+]CC"
decay1WS   = "[D*_s+ ->  ^(Lambda_c+ -> ^p+  ^K- ^pi+) ^K+ ^pi+]CC"
decay1WSBis= "[D*_s+ ->  ^(Lambda_c+ -> ^p+  ^K- ^pi+) ^K- ^pi-]CC"
decay2     = "[D*_s+ ->  ^(Lambda_c+ -> ^p+  ^K- ^pi+) ^(KS0 -> ^pi+ ^pi-)]CC"
#decay2WS      = "[D*_s+ ->  ^(Lambda_c+ -> ^p+  ^K- ^pi+) ^K]CC"
#decayWS    = "([D*_s+ ->  ^(D_s+ -> ^pi+ ^K+ ^K-) ^mu+ ^mu+]CC || [D*_s+ ->  ^(D_s+ -> ^pi+ ^K+ ^K-) ^mu- ^mu-]CC)"
#decay3     = "[D*_s+ ->  ^(D_s+ -> ^pi+ ^K+ ^K-) ^mu- ^mu-]CC"
############################################################

## (1) read data from Turbo:
from PhysConf.Selections import Selection
from PhysConf.Selections import AutomaticData
from PhysConf.Selections import PrescaleSelection, PrescaleEventSelection, MergedSelection


Lc = AutomaticData(the_line)
#Lc = AutomaticData('Hlt2DiMuonJPsiTurbo/Particles')

## (2) get pions form PersistReco 
#from StandardParticles import StdTightANNMuons as muons
from StandardParticles import StdTightANNKaons as kaons
## I.3.1   IMPOTANT: need to rebuild it!!
from PhysConf.Selections import RebuildSelection
kaons = RebuildSelection ( kaons )

from StandardParticles import StdTightANNPions as pions
pions = RebuildSelection ( pions )

from CommonParticles.StdLooseKs import StdLooseKsDD as looseksDD
looseksDD = RebuildSelection (looseksDD )

from CommonParticles.StdVeryLooseKs import StdVeryLooseKsLL as verylooseksLL
verylooseksLL = RebuildSelection ( verylooseksLL )

kshort = MergedSelection (
    'CombKshort' ,  
    RequiredSelections = [ verylooseksLL , looseksDD ] 
    )



## uncomment for debugging
## from PhysConf.Selections import PrintSelection
## pions = PrintSelection(pions)

## (4) insert momentum scaling
from PhysConf.Selections import MomentumScaling
Lcscaled = MomentumScaling ( Lc , Turbo = 'PERSISTRECO' , Year = the_year )
#muons = MomentumScaling ( muons , Turbo = 'PERSISTRECO' , Year = the_year )

from PhysConf.Selections import FilterSelection
Lc2pKpi =  FilterSelection (
    'Lc2pKpi'              ,
    [ Lcscaled ]      ,
    Code = "(BPVIPCHI2() < 9)"
    )

Lc2pKpiPrescaled = PrescaleSelection ( Lc2pKpi , prescale = 0.2 )

## (3) create Lambda-b candidates 
#from PhysConf.Selections import Combine3BodySelection
#Ds1 = Combine3BodySelection (
from PhysConf.Selections import CombineSelection
Xicst = CombineSelection (
    'Xicst2LcK'       , ## the name 
    [ Lc2pKpi , kaons ] , ## input
    DecayDescriptors = ["[D*_s+ -> Lambda_c+ K-]cc", "[D*_s+ -> Lambda_c+ K+]cc"],
    CombinationCut  = "(AM -AM1 < 1300)", 
    MotherCut = """
    (M - M1 < 1100) & 
    (VFASPF(VCHI2PDOF) < 20) 
    """,
    InputPrimaryVertices = 'Primary',
    CheckOverlapTool = "LoKi::CheckOverlap",
    ReFitPVs        = "True",
    DaughtersCuts = {
    "K+": "(BPVIPCHI2() < 9) & (TRGHOSTPROB<0.3) & (PROBNNk>0.1) & (PT>250)"
    }
    )
#PROBNNmu not available in 2015 Turbo(++)


Xicst2LcKpi = CombineSelection (
    'Xicst2LcKpi'       , ## the name 
    [ Lc2pKpi , kaons, pions ] , ## input
    DecayDescriptors = ["[D*_s+ -> Lambda_c+ K- pi+]cc", "[D*_s+ -> Lambda_c+ K+ pi+]cc", "[D*_s+ -> Lambda_c+ K- pi-]cc" ],
    CombinationCut  = "(AM -AM1 < 1300)", 
    MotherCut = """
    (M - M1 < 1100) & 
    (VFASPF(VCHI2PDOF) < 20) 
    """,
    InputPrimaryVertices = 'Primary',
    CheckOverlapTool = "LoKi::CheckOverlap",
    ReFitPVs        = "True",
    DaughtersCuts = {
        "K+": "(BPVIPCHI2() < 9) & (TRGHOSTPROB<0.3) & (PROBNNk>0.1) & (PT>250)",
        "pi+": "(BPVIPCHI2() < 9) & (TRGHOSTPROB<0.3) & (PROBNNpi>0.1)"
    }
    )

Xicst2LcK0s = CombineSelection (
    'Xicst2LcK0s'       , ## the name 
    [ Lc2pKpi , kshort] , ## input
    DecayDescriptors = ["[D*_s+ -> Lambda_c+ KS0]cc"],
    CombinationCut  = "(AM -AM1 < 1300)", 
    MotherCut = """
    (M - M1 < 1100) & 
    (VFASPF(VCHI2PDOF) < 20) 
    """,
    InputPrimaryVertices = 'Primary',
    CheckOverlapTool = "LoKi::CheckOverlap",
    ReFitPVs        = "True",
    DaughtersCuts = {
        "KS0": "(BPVIPCHI2() < 25)"
    }
    )

##################################################################

##################################################
#
#     Lc -> p K pi TREE
#
##################################################

from Configurables import CondDB
CondDB ( LatestGlobalTagByDataType = the_year ) 

## (5) fill tuple
from Configurables import DecayTreeTuple, TupleToolPrimaries
Lc2pKpiTree = DecayTreeTuple("Lc2pKpiTree")
Lc2pKpiTree.Inputs = [Lc2pKpiPrescaled.outputLocation()]
Lc2pKpiTree.Decay = decay0
Lc2pKpiTree.ToolList = [
    "TupleToolKinematic",
    "TupleToolPid",
    "TupleToolANNPID",
    "TupleToolPropertime",
    "TupleToolGeometry",
    "TupleToolPrimaries",
    "TupleToolTrackInfo",
    "TupleToolEventInfo",
    "TupleToolRecoStats"#,
    ]
Lc2pKpiTree.Branches = {
    "Lc"    :"[Lambda_c+ -> p+  K- pi+]CC",
    "p"     :"[Lambda_c+ -> ^p+  K- pi+]CC",
    "Km"    :"[Lambda_c+ -> p+  ^K- pi+]CC",
    "pip"   :"[Lambda_c+ -> p+  K- ^pi+]CC",
    }
########################################################################
#from Configurables import TupleToolKinematic
#Lc2pKpiTree.addTool( TupleToolKinematic,name = "TupleToolKinematic" )
#Lc2pKpiTree.TupleToolKinematic.Verbose = True

#from Configurables import TupleToolGeometry
#Lc2pKpiTree.addTool( TupleToolGeometry, name = "TupleToolGeometry" )
#Lc2pKpiTree.TupleToolGeometry.Verbose = True

from Configurables import TupleToolRecoStats
Lc2pKpiTree.addTool(TupleToolRecoStats, name="TupleToolRecoStats")
Lc2pKpiTree.TupleToolRecoStats.Verbose = True
##################################################
from Configurables import TupleToolDecay
Lc2pKpiTree.addTool(TupleToolDecay, name = 'Lc')
from Configurables import LoKi__Hybrid__TupleTool
Lc2pKpiTree.Lc.ToolList =  ["LoKi::Hybrid::TupleTool/LoKi_All0"]
###################################################
LoKiTuple0 = LoKi__Hybrid__TupleTool("LoKi_All0")
LoKiTuple0.Variables =  {
    "M_DTF_PV":"DTF_FUN( M, True )"
    ,"CHI2NDOF_DTF_PV":"DTF_CHI2NDOF(True)"
    ,"M12_DTF_Lc_PV":"DTF_FUN( M12, True, strings( 'Lambda_c+') )"
    ,"M13_DTF_Lc_PV":"DTF_FUN( M13, True, strings( 'Lambda_c+') )"
    ,"M23_DTF_Lc_PV":"DTF_FUN( M23, True, strings( 'Lambda_c+') )"
    ,"CHI2NDOF_DTF_Lc_PV":"DTF_CHI2NDOF(True, strings( 'Lambda_c+'))"
    ,"BPVVDCHI2":"BPVVDCHI2"
    }
Lc2pKpiTree.Lc.addTool(LoKiTuple0)

Lc2pKpiTree_tuple_sel = Selection("Lc2PKPiTree",
                                  Algorithm = Lc2pKpiTree,
                                  RequiredSelections = [Lc2pKpiPrescaled])

##################################################
#
#     Xicc -> Lc K TREE
#
##################################################

###################################################
LcKTree = Lc2pKpiTree.clone("LcKTree")
LcKTree.Inputs = [Xicst.outputLocation()]
LcKTree.Decay = decay
###################################################
LcKTree.Branches = {
    "Xicst" :"[D*_s+ -> (Lambda_c+ -> p+  K- pi+) [K-]CC]CC",
    "Lc"    :"[D*_s+ -> ^(Lambda_c+ -> p+  K- pi+) [K-]CC]CC",
    "p"     :"[D*_s+ -> (Lambda_c+ -> ^p+  K- pi+) [K-]CC]CC",
    "Km"    :"[D*_s+ -> (Lambda_c+ -> p+  ^K- pi+) [K-]CC]CC",
    "pip"   :"[D*_s+ -> (Lambda_c+ -> p+  K- ^pi+) [K-]CC]CC",
    "Kbach":"[D*_s+ -> (Lambda_c+ -> p+  K- pi+) ^[K-]CC]CC"
    }
LcKTree.addTool(TupleToolDecay, name = 'Xicst')
LcKTree.Xicst.ToolList =  ["LoKi::Hybrid::TupleTool/LoKi_All"]
###################################################
LoKiTuple = LoKi__Hybrid__TupleTool("LoKi_All")
LoKiTuple.Variables =  {
    "M_DTF_Lc_PV":"DTF_FUN( M, True, strings( 'Lambda_c+'))"
    ,"CHI2NDOF_DTF_Lc_PV":"DTF_CHI2NDOF(True, strings( 'Lambda_c+'))"
    #    ,"PX_DTF_Lc_PV":"DTF_FUN( PX, True, strings( 'Lambda_c+'))"
    #    ,"PY_DTF_Lc_PV":"DTF_FUN( PY, True, strings( 'Lambda_c+'))"
    #    ,"PZ_DTF_Lc_PV":"DTF_FUN( PZ, True, strings( 'Lambda_c+'))"
    ,"M_DTF_Lc":"DTF_FUN( M, False, strings( 'Lambda_c+'))"
    ,"CHI2NDOF_DTF_Lc":"DTF_CHI2NDOF(False, strings( 'Lambda_c+'))"
    #    ,"PX_DTF_Lc":"DTF_FUN( PX, False, strings( 'Lambda_c+'))"
    #    ,"PY_DTF_Lc":"DTF_FUN( PY, False, strings( 'Lambda_c+'))"
    #    ,"PZ_DTF_Lc":"DTF_FUN( PZ, False, strings( 'Lambda_c+'))"
    ,"M_DTF_PV":"DTF_FUN( M, True)"
    ,"CHI2NDOF_DTF_PV":"DTF_CHI2NDOF(True)"
        # Systematics Momentum Calibration
    ,"Dau1_Dau1_M_DTF_Lc_PV":"DTF_FUN( CHILD(M,1,1), True , strings( 'Lambda_c+'))"
    ,"Dau1_Dau1_PX_DTF_Lc_PV":"DTF_FUN( CHILD(PX,1,1), True , strings( 'Lambda_c+'))"
    ,"Dau1_Dau1_PY_DTF_Lc_PV":"DTF_FUN( CHILD(PY,1,1), True , strings( 'Lambda_c+'))"
    ,"Dau1_Dau1_PZ_DTF_Lc_PV":"DTF_FUN( CHILD(PZ,1,1), True , strings( 'Lambda_c+'))"
    ,"Dau1_Dau1_PE_DTF_Lc_PV":"DTF_FUN( CHILD(E,1,1), True , strings( 'Lambda_c+'))"
    ,"Dau1_Dau1_PT_DTF_Lc_PV":"DTF_FUN( CHILD(PT,1,1), True , strings( 'Lambda_c+'))"
    ,"Dau1_Dau1_P_DTF_Lc_PV":"DTF_FUN( CHILD(P,1,1), True , strings( 'Lambda_c+'))"

    ,"Dau1_Dau2_M_DTF_Lc_PV":"DTF_FUN( CHILD(M,1,2), True , strings( 'Lambda_c+'))"
    ,"Dau1_Dau2_PX_DTF_Lc_PV":"DTF_FUN( CHILD(PX,1,2), True , strings( 'Lambda_c+'))"
    ,"Dau1_Dau2_PY_DTF_Lc_PV":"DTF_FUN( CHILD(PY,1,2), True , strings( 'Lambda_c+'))"
    ,"Dau1_Dau2_PZ_DTF_Lc_PV":"DTF_FUN( CHILD(PZ,1,2), True , strings( 'Lambda_c+'))"
    ,"Dau1_Dau2_PE_DTF_Lc_PV":"DTF_FUN( CHILD(E,1,2), True , strings( 'Lambda_c+'))"
    ,"Dau1_Dau2_PT_DTF_Lc_PV":"DTF_FUN( CHILD(PT,1,2), True , strings( 'Lambda_c+'))"
    ,"Dau1_Dau2_P_DTF_Lc_PV":"DTF_FUN( CHILD(P,1,2), True , strings( 'Lambda_c+'))"

    ,"Dau1_Dau3_M_DTF_Lc_PV":"DTF_FUN( CHILD(M,1,3), True , strings( 'Lambda_c+'))"
    ,"Dau1_Dau3_PX_DTF_Lc_PV":"DTF_FUN( CHILD(PX,1,3), True , strings( 'Lambda_c+'))"
    ,"Dau1_Dau3_PY_DTF_Lc_PV":"DTF_FUN( CHILD(PY,1,3), True , strings( 'Lambda_c+'))"
    ,"Dau1_Dau3_PZ_DTF_Lc_PV":"DTF_FUN( CHILD(PZ,1,3), True , strings( 'Lambda_c+'))"
    ,"Dau1_Dau3_PE_DTF_Lc_PV":"DTF_FUN( CHILD(E,1,3), True , strings( 'Lambda_c+'))"
    ,"Dau1_Dau3_PT_DTF_Lc_PV":"DTF_FUN( CHILD(PT,1,3), True , strings( 'Lambda_c+'))"
    ,"Dau1_Dau3_P_DTF_Lc_PV":"DTF_FUN( CHILD(P,1,3), True , strings( 'Lambda_c+'))"

    ,"Dau2_M_DTF_Lc_PV":"DTF_FUN( CHILD(M,2), True , strings( 'Lambda_c+'))"
    ,"Dau2_PX_DTF_Lc_PV":"DTF_FUN( CHILD(PX,2), True , strings( 'Lambda_c+'))"
    ,"Dau2_PY_DTF_Lc_PV":"DTF_FUN( CHILD(PY,2), True , strings( 'Lambda_c+'))"
    ,"Dau2_PZ_DTF_Lc_PV":"DTF_FUN( CHILD(PZ,2), True , strings( 'Lambda_c+'))"
    ,"Dau2_PE_DTF_Lc_PV":"DTF_FUN( CHILD(E,2), True , strings( 'Lambda_c+'))"
    ,"Dau2_PT_DTF_Lc_PV":"DTF_FUN( CHILD(PT,2), True , strings( 'Lambda_c+'))"
    ,"Dau2_P_DTF_Lc_PV":"DTF_FUN( CHILD(P,2), True , strings( 'Lambda_c+'))"
    }
LcKTree.Xicst.addTool(LoKiTuple)

LcKTree_tuple_sel = Selection("LCKTree",
                              Algorithm = LcKTree,
                              RequiredSelections = [ Xicst ])
##################################################
LcKTreeWS = LcKTree.clone("LcKTreeWS")
LcKTreeWS.Inputs = [Xicst.outputLocation()]
LcKTreeWS.Decay = decayWS

LcKTreeWS_tuple_sel = Selection("LCKTreeWS",
                              Algorithm = LcKTreeWS,
                              RequiredSelections = [ Xicst ])



##################################################
#
#     Xicc -> Lc K pi TREE
#
##################################################

LcKpiTree = LcKTree.clone("LcKpiTree")
LcKpiTree.Inputs = [Xicst2LcKpi.outputLocation()]
LcKpiTree.Decay = decay1
###################################################
LcKpiTree.Branches = {
    "Xicst" :"[D*_s+ -> (Lambda_c+ -> p+  K- pi+) [K-]CC [pi+]CC]CC",
    "Lc"    :"[D*_s+ -> ^(Lambda_c+ -> p+  K- pi+) [K-]CC [pi+]CC]CC",
    "p"     :"[D*_s+ -> (Lambda_c+ -> ^p+  K- pi+) [K-]CC [pi+]CC]CC",
    "Km"    :"[D*_s+ -> (Lambda_c+ -> p+  ^K- pi+) [K-]CC [pi+]CC]CC",
    "pip"   :"[D*_s+ -> (Lambda_c+ -> p+  K- ^pi+) [K-]CC [pi+]CC]CC",
    "Kbach":"[D*_s+ -> (Lambda_c+ -> p+  K- pi+) ^[K-]CC [pi+]CC]CC",
    "pibach":"[D*_s+ -> (Lambda_c+ -> p+  K- pi+) [K-]CC ^[pi+]CC]CC"
    }
LcKpiTree.addTool(TupleToolDecay, name = 'Xicst')

LcKpiTree.Xicst.ToolList +=  ["LoKi::Hybrid::TupleTool/LoKi_All3"]
###################################################
LoKiTuple3 = LoKi__Hybrid__TupleTool("LoKi_All3")
LoKiTuple3.Variables =  {
    "Dau3_M_DTF_Lc_PV":"DTF_FUN( CHILD(M,3), True , strings( 'Lambda_c+'))"
    ,"Dau3_PX_DTF_Lc_PV":"DTF_FUN( CHILD(PX,3), True , strings( 'Lambda_c+'))"
    ,"Dau3_PY_DTF_Lc_PV":"DTF_FUN( CHILD(PY,3), True , strings( 'Lambda_c+'))"
    ,"Dau3_PZ_DTF_Lc_PV":"DTF_FUN( CHILD(PZ,3), True , strings( 'Lambda_c+'))"
    ,"Dau3_PE_DTF_Lc_PV":"DTF_FUN( CHILD(E,3), True , strings( 'Lambda_c+'))"
    ,"Dau3_PT_DTF_Lc_PV":"DTF_FUN( CHILD(PT,3), True , strings( 'Lambda_c+'))"
    ,"Dau3_P_DTF_Lc_PV":"DTF_FUN( CHILD(P,3), True , strings( 'Lambda_c+'))"
    }
LcKpiTree.Xicst.addTool(LoKiTuple3)



#LcKpiTree.Xicst2LcKpi.ToolList =  ["LoKi::Hybrid::TupleTool/LoKi_All"]
###################################################
#LcKpiTree.Xicst2LcKpi.addTool(LoKiTuple)

LcKpiTree_tuple_sel = Selection("LCKPiTree",
                              Algorithm = LcKpiTree,
                              RequiredSelections = [ Xicst2LcKpi ])
##################################################
LcKpiTreeWS = LcKpiTree.clone("LcKpiTreeWS")
LcKpiTreeWS.Inputs = [Xicst2LcKpi.outputLocation()]
LcKpiTreeWS.Decay = decay1WS

LcKpiTreeWS_tuple_sel = Selection("LCKPiTreeWS",
                              Algorithm = LcKpiTreeWS,
                              RequiredSelections = [ Xicst2LcKpi ])

##################################################
LcKpiTreeWSBis = LcKpiTree.clone("LcKpiTreeWSBis")
LcKpiTreeWSBis.Inputs = [Xicst2LcKpi.outputLocation()]
LcKpiTreeWSBis.Decay = decay1WSBis

LcKpiTreeWSBis_tuple_sel = Selection("LCKPiTreeWSBis",
                              Algorithm = LcKpiTreeWSBis,
                              RequiredSelections = [ Xicst2LcKpi ])


##################################################
#
#     Xicc -> Lc Kshort TREE
#
##################################################

#LcKS0Tree = Lc2pKpiTree.clone("LcKpiTree")
LcKS0Tree = Lc2pKpiTree.clone("LcKS0Tree")
LcKS0Tree.Inputs = [Xicst2LcK0s.outputLocation()]
LcKS0Tree.Decay = decay2
###################################################
LcKS0Tree.Branches = {
    "Xicst" :"[D*_s+ -> (Lambda_c+ -> p+  K- pi+) (KS0 -> pi+ pi- )]CC",
    "Lc"    :"[D*_s+ -> ^(Lambda_c+ -> p+  K- pi+) (KS0 -> pi+ pi- )]CC",
    "p"     :"[D*_s+ -> (Lambda_c+ -> ^p+  K- pi+) (KS0 -> pi+ pi- )]CC",
    "Km"    :"[D*_s+ -> (Lambda_c+ -> p+  ^K- pi+) (KS0 -> pi+ pi- )]CC",
    "pip"   :"[D*_s+ -> (Lambda_c+ -> p+  K- ^pi+) (KS0 -> pi+ pi- )]CC",
    "KS0"   :"[D*_s+ -> (Lambda_c+ -> p+  K- pi+) ^(KS0 -> pi+ pi- )]CC",
    "pipKS0":"[D*_s+ -> (Lambda_c+ -> p+  K- pi+) (KS0 -> ^pi+ pi- )]CC",
    "pimKS0":"[D*_s+ -> (Lambda_c+ -> p+  K- pi+) (KS0 -> pi+ ^pi- )]CC"
    }
LcKS0Tree.addTool(TupleToolDecay, name = 'Xicst')
LcKS0Tree.Xicst.ToolList =  ["LoKi::Hybrid::TupleTool/LoKi_AllK0S"]
###################################################

LoKiTuple_K0S = LoKi__Hybrid__TupleTool("LoKi_AllK0S")
LoKiTuple_K0S.Variables =  {
    "M_DTF_Lc_K0s_PV":"DTF_FUN( M, True, strings( 'Lambda_c+', 'KS0'))"
    ,"CHI2NDOF_DTF_Lc_K0s_PV":"DTF_CHI2NDOF(True, strings( 'Lambda_c+', 'KS0'))"
    #    ,"PX_DTF_Lc_K0s_PV":"DTF_FUN( PX, True, strings( 'Lambda_c+'))"
    #    ,"PY_DTF_Lc_K0s_PV":"DTF_FUN( PY, True, strings( 'Lambda_c+'))"
    #    ,"PZ_DTF_Lc_K0s_PV":"DTF_FUN( PZ, True, strings( 'Lambda_c+'))"
    ,"M_DTF_Lc_K0s":"DTF_FUN( M, False, strings( 'Lambda_c+', 'KS0'))"
    ,"CHI2NDOF_DTF_Lc_K0s":"DTF_CHI2NDOF(False, strings( 'Lambda_c+', 'KS0'))"
    #    ,"PX_DTF_Lc":"DTF_FUN( PX, False, strings( 'Lambda_c+'))"
    #    ,"PY_DTF_Lc":"DTF_FUN( PY, False, strings( 'Lambda_c+'))"
    #    ,"PZ_DTF_Lc":"DTF_FUN( PZ, False, strings( 'Lambda_c+'))"
    ,"M_DTF_PV":"DTF_FUN( M, True)"
    ,"CHI2NDOF_DTF_PV":"DTF_CHI2NDOF(True)"
        # Systematics Momentum Calibration
    ,"Dau1_Dau1_M_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(M,1,1), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau1_Dau1_PX_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(PX,1,1), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau1_Dau1_PY_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(PY,1,1), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau1_Dau1_PZ_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(PZ,1,1), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau1_Dau1_PE_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(E,1,1), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau1_Dau1_PT_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(PT,1,1), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau1_Dau1_P_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(P,1,1), True , strings( 'Lambda_c+', 'KS0'))"

    ,"Dau1_Dau2_M_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(M,1,2), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau1_Dau2_PX_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(PX,1,2), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau1_Dau2_PY_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(PY,1,2), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau1_Dau2_PZ_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(PZ,1,2), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau1_Dau2_PE_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(E,1,2), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau1_Dau2_PT_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(PT,1,2), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau1_Dau2_P_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(P,1,2), True , strings( 'Lambda_c+', 'KS0'))"

    ,"Dau1_Dau3_M_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(M,1,3), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau1_Dau3_PX_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(PX,1,3), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau1_Dau3_PY_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(PY,1,3), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau1_Dau3_PZ_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(PZ,1,3), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau1_Dau3_PE_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(E,1,3), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau1_Dau3_PT_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(PT,1,3), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau1_Dau3_P_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(P,1,3), True , strings( 'Lambda_c+', 'KS0'))"

    ,"Dau2_Dau1_M_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(M,2,1), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau2_Dau1_PX_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(PX,2,1), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau2_Dau1_PY_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(PY,2,1), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau2_Dau1_PZ_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(PZ,2,1), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau2_Dau1_PE_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(E,2,1), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau2_Dau1_PT_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(PT,2,1), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau2_Dau1_P_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(P,2,1), True , strings( 'Lambda_c+', 'KS0'))"

    ,"Dau2_Dau2_M_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(M,2,2), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau2_Dau2_PX_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(PX,2,2), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau2_Dau2_PY_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(PY,2,2), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau2_Dau2_PZ_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(PZ,2,2), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau2_Dau2_PE_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(E,2,2), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau2_Dau2_PT_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(PT,2,2), True , strings( 'Lambda_c+', 'KS0'))"
    ,"Dau2_Dau2_P_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(P,2,2), True , strings( 'Lambda_c+', 'KS0'))"

     #,"Dau2_M_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(M,2), True , strings( 'Lambda_c+', 'KS0'))"
     #,"Dau2_PX_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(PX,2), True , strings( 'Lambda_c+', 'KS0'))"
     #,"Dau2_PY_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(PY,2), True , strings( 'Lambda_c+', 'KS0'))"
     #,"Dau2_PZ_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(PZ,2), True , strings( 'Lambda_c+', 'KS0'))"
     #,"Dau2_PE_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(E,2), True , strings( 'Lambda_c+', 'KS0'))"
     #,"Dau2_PT_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(PT,2), True , strings( 'Lambda_c+', 'KS0'))"
     #,"Dau2_P_DTF_Lc_K0s_PV":"DTF_FUN( CHILD(P,2), True , strings( 'Lambda_c+', 'KS0'))"
    
    #"M_DTF_L0_Xi_K0S_PV":"DTF_FUN( M, True, strings( 'Lambda_c+', 'KS0'))"
    #,"CHI2NDOF_DTF_L0_Xi_K0S_PV":"DTF_CHI2NDOF(True, strings( 'Lambda0', 'Xi-', 'KS0'))"
    #,"M_DTF_L0_Xi_K0S":"DTF_FUN( M, False, strings( 'Lambda0', 'Xi-', 'KS0'))"
    #,"CHI2NDOF_DTF_L0_Xi_K0S":"DTF_CHI2NDOF(False, strings( 'Lambda0', 'Xi-', 'KS0'))"
    }

#LcKS0Tree.Xicst2LcK0s.addTool(LoKiTuple)
LcKS0Tree.Xicst.addTool(LoKiTuple_K0S)


LcKS0Tree_tuple_sel = Selection("LCKS0Tree",
                              Algorithm = LcKS0Tree,
                              RequiredSelections = [ Xicst2LcK0s ])
##################################################
#LcKS0TreeWS = LcKS0Tree.clone("LcKS0TreeWS")
#LcKS0TreeWS.Inputs = [Xicst2LcK0s.outputLocation()]
#LcKS0TreeWS.Decay = decay2

#LcKS0TreeWS_tuple_sel = Selection("LCKS0TreeWS",
#                              Algorithm = LcKS0TreeWS,
#                              RequiredSelections = [ Xicst2LcK0s ])
##################################################





################################################### 
## (6) build the final selection sequence
from PhysConf.Selections import SelectionSequence
seq1 = SelectionSequence('SEQ1', Lc2pKpiTree_tuple_sel )
seq2 = SelectionSequence('SEQ2', LcKTree_tuple_sel )
seq3 = SelectionSequence('SEQ3', LcKTreeWS_tuple_sel )
seq4 = SelectionSequence('SEQ4', LcKpiTree_tuple_sel )
seq5 = SelectionSequence('SEQ5', LcKpiTreeWS_tuple_sel )
seq6 = SelectionSequence('SEQ6', LcKpiTreeWSBis_tuple_sel )
seq7 = SelectionSequence('SEQ7', LcKS0Tree_tuple_sel )
#seq7 = SelectionSequence('SEQ7', LcKS0TreeWS_tuple_sel )
#seq2 = SelectionSequence('SEQ2', Xicst )
#seq3 = SelectionSequence('SEQ3', Lc1WS_tuple )

## (7) configure DaVinci
from Configurables import DaVinci 
dv = DaVinci(
    PrintFreq  = 25000          ,
    DataType   = the_year       ,
    InputType  = 'MDST'         , ## ATTENTION! 
    RootInTES  = rootInTES      , ## ATTENTION! 
    ##
    EventPreFilters = fltrs.filters('FILTER') , 
    Lumi       = True           , 
    Simulation = False          ,
    ## 
    TupleFile  = 'LcK_Turbo_240118.root'   , 
    Turbo      = True      
 )

## (8) insert our sequence into DaVinci 
#dv.UserAlgorithms = [ seq1.sequence(), seq2.sequence(), seq3.sequence(), seq4.sequence(), seq5.sequence(), seq6.sequence(), seq7.sequence() ]
dv.UserAlgorithms = [ seq1.sequence(), seq2.sequence()]#, seq3.sequence(), seq4.sequence(), seq5.sequence(), seq6.sequence(), seq7.sequence() ]


## (9) number of event and input data

dv.EvtMax = -1
#DaVinci().Input = [
#    'PFN:root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb/LHCb/Collision16/CHARMSPECPRESCALED.MDST/00053752/0000/00053752_00001193_1.charmspecprescaled.mdst'
#    ]


# =============================================================================
# Stuff specifif for Persist Reco, not needed for "plain" Turbo
# =============================================================================

## (9) specific for persis reco
from Configurables import DstConf, TurboConf
DstConf   () .Turbo       = True
TurboConf () .PersistReco = True
TurboConf () .DataType    = the_year

