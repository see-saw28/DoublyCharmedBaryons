from DecayTreeTuple.Configuration import *
the_year = '2016' 
polarity = 'MU' 
evt_id = 26167055
ganga = True


from PhysConf.Filters import LoKi_Filters
fltrs = LoKi_Filters (
   HLT2_Code = "HLT_PASS_RE('Hlt2CharmHadInclLcpToKmPpPipBDTTurbo') | HLT_PASS_RE('Hlt2CharmHadLcpToPpKmPipTurboDecision')"
)

def fillTuple( tuple, excited=True, WS=False ):

    tuple.ToolList = [
        "TupleToolAngles",
        #"TupleToolANNPID",           # Different tuning...
        "TupleToolEventInfo",
        "TupleToolGeometry",
        # "TupleToolL0Data",
        "TupleToolKinematic",
        "TupleToolPid",
        "TupleToolPrimaries",
        "TupleToolPropertime" ,
        "TupleToolRecoStats",
        "TupleToolTrackInfo"
        ]

    # RecoStats for filling SpdMult, etc
    from Configurables import TupleToolRecoStats
    tuple.addTool(TupleToolRecoStats, name="TupleToolRecoStats")
    tuple.TupleToolRecoStats.Verbose=True

    from Configurables import TupleToolTISTOS, TupleToolDecay
    tuple.addTool(TupleToolDecay, name = 'Lc')
    tuple.addTool(TupleToolDecay, name = 'Xicc')

    from Configurables import LoKi__Hybrid__TupleTool

    if excited :
        tuple.addTool(TupleToolDecay, name = 'C')
        
        LoKi_C=LoKi__Hybrid__TupleTool("LoKi_C")
        LoKi_C.Variables = {
                "M_DTF":"DTF_FUN( M, False)",
                "M_DTF_Xicc":"DTF_FUN( M, False, strings( 'Xi_cc++'))",
                "M_DTF_PV":"DTF_FUN( M, True)",
                "M_DTF_Xicc_PV":"DTF_FUN( M, True, strings( 'Xi_cc++'))",
                "CHI2NDOF_DTF":"DTF_CHI2NDOF(False)",
                "CHI2NDOF_DTF_Xicc":"DTF_CHI2NDOF(False, strings( 'Xi_cc++'))",
                "CHI2NDOF_DTF_PV":"DTF_CHI2NDOF(True)",
                "CHI2NDOF_DTF_Xicc_PV":"DTF_CHI2NDOF(True, strings( 'Xi_cc++'))",            
                }
        
        tuple.C.ToolList+=["LoKi::Hybrid::TupleTool/LoKi_C"]
        tuple.C.addTool(LoKi_C)

        verbose = True
        update = False

        from Configurables import LoKi__Hybrid__DictOfFunctors
        from Configurables import LoKi__Hybrid__Dict2Tuple
        from Configurables import LoKi__Hybrid__DTFDict as DTFDict

        DictTuple = tuple.C.addTupleTool(LoKi__Hybrid__Dict2Tuple, "DTFTuple")

        # We need a DecayTreeFitter. DTFDict will provide the fitter and the connection to the tool chain
        # we add it as a source of data to the Dict2Tuple
        DictTuple.addTool(DTFDict,name="KaonDTF")
        DictTuple.Source = "LoKi::Hybrid::DTFDict/KaonDTF"
        DictTuple.NumVar = 15     # reserve a suitable size for the dictionaire

        # configure the DecayTreeFitter in the usual way
        DictTuple.KaonDTF.constrainToOriginVertex = True
        DictTuple.KaonDTF.daughtersToConstrain = ["Xi_cc++"]

        # Add LoKiFunctors to the tool chain, just as we did to the Hybrid::TupleTool above
        # these functors will be applied to the refitted(!) decay tree
        # they act as a source to the DTFDict
        DictTuple.KaonDTF.addTool(LoKi__Hybrid__DictOfFunctors,"dict")
        DictTuple.KaonDTF.Source = "LoKi::Hybrid::DictOfFunctors/dict"

        DictTuple.KaonDTF.dict.Variables = {
            "C_PT"            : "PT",
            "C_M"             : "M",
            "C_IPCHI2"        : "MIPCHI2DV()",
            "C_CHI2NDOF"      : "VFASPF(VCHI2PDOF)",
            "Xicc_PT"         : "CHILD(PT,1)",
            "Xicc_M"          : "CHILD(M,1)",
            "Xicc_IPCHI2"     : "CHILD(MIPCHI2DV(),1)",
            "Xicc_CHI2NDOF"   : "CHILD(VFASPF(VCHI2PDOF),1)",
            "K_PT"            : "CHILD(PT,2)",
            "K_M"             : "CHILD(M,2)",
            "K_ID"            : "CHILD(ID,2)",
            "K_IPCHI2"        : "CHILD(MIPCHI2DV(),2)",
            "K_CHI2NDOF"      : "CHILD(VFASPF(VCHI2PDOF),2)"
           
        }

     
             

    #LoKi one
    LoKi_All=LoKi__Hybrid__TupleTool("LoKi_All")
    LoKi_All.Variables = {
        "ETA"                  : "ETA",
        "Y"                    : "Y"  ,
        "LOKI_IPCHI2"          : "BPVIPCHI2()"
        }
    tuple.ToolList+=["LoKi::Hybrid::TupleTool/LoKi_All"]
    tuple.addTool(LoKi_All)


    LoKi_B=LoKi__Hybrid__TupleTool("LoKi_B")
    LoKi_B.Variables = {
            "M_DTF":"DTF_FUN( M, False)",
            "M_DTF_Lc":"DTF_FUN( M, False, strings( 'Lambda_c+'))",
            "M_DTF_PV":"DTF_FUN( M, True)",
            "M_DTF_Lc_PV":"DTF_FUN( M, True, strings( 'Lambda_c+'))",
            "CHI2NDOF_DTF":"DTF_CHI2NDOF(False)",
            "CHI2NDOF_DTF_Lc":"DTF_CHI2NDOF(False, strings( 'Lambda_c+'))",
            "CHI2NDOF_DTF_PV":"DTF_CHI2NDOF(True)",
            "CHI2NDOF_DTF_Lc_PV":"DTF_CHI2NDOF(True, strings( 'Lambda_c+'))",            
            "SumXiccPT"            : "( CHILD(PT, 1, 1) + CHILD(PT, 1, 2) + CHILD(PT, 1, 3) + CHILD(PT, 2) )",
            }
    
    tuple.Xicc.ToolList+=["LoKi::Hybrid::TupleTool/LoKi_B"]
    tuple.Xicc.addTool(LoKi_B)

def applyMVAvalue( branch,
                name, 
                MVAVars,
                MVAxmlFile
                ):
    from MVADictHelpers import addTMVAclassifierTuple
    
    addTMVAclassifierTuple(branch, MVAxmlFile, MVAVars,
                       Name=name, Keep=True, Preambulo=[""])


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
from StandardParticles import StdAllNoPIDsPions as PionsNoPID
from StandardParticles import StdAllNoPIDsKaons as KaonsNoPID

from PhysConf.Selections import RebuildSelection
Pions = RebuildSelection(Pions)#### 
#Protons = RebuildSelection(Protons)
Kaons = RebuildSelection(Kaons)
KaonsNoPID = RebuildSelection(KaonsNoPID)

#%% MC

########################

#       MC TREE

########################
mct = MCDecayTreeTuple('mctupleLc') 

if evt_id<26167054: 

    mct.Decay = '[Xi_cc+ ==> ^(Xi_cc++ ==> ^(Lambda_c+ ==> ^p+ ^K- ^pi+) ^K- ^pi+ ^pi+) ^pi-]CC' 
    mct.addBranches( {
        'C': '[Xi_cc+ => (Xi_cc++ => (Lambda_c+ ==> K- p+ pi+) K- pi+ pi+) pi-]CC',
        'Pi': '[Xi_cc+ => (Xi_cc++ => ^(Lambda_c+ ==> K- p+ pi+) K- pi+ pi+) ^pi-]CC',
        'Xicc': '[Xi_cc+ => ^(Xi_cc++ => (Lambda_c+ ==> K- p+ pi+) K- pi+ pi+) pi-]CC',
        'Lc': '[Xi_cc+ => (Xi_cc++ => ^(Lambda_c+ ==> K- p+ pi+) K- pi+ pi+) pi-]CC',
        'XiccK': '[Xi_cc+ => (Xi_cc++ => (Lambda_c+ ==> K- p+ pi+) ^K- pi+ pi+) pi-]CC',
        'LcK': '[Xi_cc+ => (Xi_cc++ => (Lambda_c+ ==> ^K- p+ pi+) K- pi+ pi+) pi-]CC',
        'XiccPi1': '[Xi_cc+ => (Xi_cc++ => (Lambda_c+ ==> K- p+ pi+) K- ^pi+ pi+) pi-]CC',
        'XiccPi2': '[Xi_cc+ => (Xi_cc++ => (Lambda_c+ ==> K- p+ pi+) K- pi+ ^pi+) pi-]CC',
        'LcPi': '[Xi_cc+ => (Xi_cc++ => (Lambda_c+ ==> K- p+ ^pi+) K- pi+ pi+) pi-]CC',
        'LcP': '[Xi_cc+ => (Xi_cc++ => (Lambda_c+ ==> K- ^p+ pi+) K- pi+ pi+) pi-]CC'} )
    
else :
    mct.Decay = '[Omega_cc+ ==> ^(Xi_cc++ ==> ^(Lambda_c+ ==> ^p+ ^K- ^pi+) ^K- ^pi+ ^pi+) ^K-]CC' 
    mct.addBranches( {
        'C': '[Omega_cc+ => (Xi_cc++ => (Lambda_c+ ==> K- p+ pi+) K- pi+ pi+) K-]CC',
        'K': '[Omega_cc+ => (Xi_cc++ => ^(Lambda_c+ ==> K- p+ pi+) K- pi+ pi+) ^K-]CC',
        'Xicc': '[Omega_cc+ => ^(Xi_cc++ => (Lambda_c+ ==> K- p+ pi+) K- pi+ pi+) K-]CC',
        'Lc': '[Omega_cc+ => (Xi_cc++ => ^(Lambda_c+ ==> K- p+ pi+) K- pi+ pi+) K-]CC',
        'XiccK': '[Omega_cc+ => (Xi_cc++ => (Lambda_c+ ==> K- p+ pi+) ^K- pi+ pi+) K-]CC',
        'LcK': '[Omega_cc+ => (Xi_cc++ => (Lambda_c+ ==> ^K- p+ pi+) K- pi+ pi+) K-]CC',
        'XiccPi1': '[Omega_cc+ => (Xi_cc++ => (Lambda_c+ ==> K- p+ pi+) K- ^pi+ pi+) K-]CC',
        'XiccPi2': '[Omega_cc+ => (Xi_cc++ => (Lambda_c+ ==> K- p+ pi+) K- pi+ ^pi+) K-]CC',
        'LcPi': '[Omega_cc+ => (Xi_cc++ => (Lambda_c+ ==> K- p+ ^pi+) K- pi+ pi+) K-]CC',
        'LcP': '[Omega_cc+ => (Xi_cc++ => (Lambda_c+ ==> K- ^p+ pi+) K- pi+ pi+) K-]CC'} )
    

mctl = ['MCTupleToolHierarchy'
        ,'MCTupleToolKinematic'
        ,'MCTupleToolPrimaries'
        ,'MCTupleToolPID',
        "LoKi::Hybrid::MCTupleTool/LoKi_Photos"]

mct.ToolList = mctl

mct.addTupleTool("LoKi::Hybrid::TupleTool/LoKi_Photos").Variables = {
    "M" : "MCM"
}



mcTuple_sel = Selection("MCTree",
                        Algorithm = mct,
                        RequiredSelections = [])

#%% Lc turbo

##########################

# Build Lc from Turbo line

##########################

if the_year == '2016':
    Lc_line = 'Hlt2CharmHadLcpToPpKmPipTurbo/Particles'

else :
    Lc_line = 'Hlt2CharmHadInclLcpToKmPpPipBDTTurbo/Particles'

Lc = AutomaticData(Lc_line)

TURBO_Lc = DecayTreeTuple('Lambdac_TURBO') 
#TURBO_Lc.Inputs = [Lc.outputLocation()] 
TURBO_Lc.Decay = '[Lambda_c+ -> ^p+ ^K- ^pi+]CC'
#TURBO_Lc.Decay = '[Lambda_c+]CC'
TURBO_Lc.Branches = Lc2pKpiBranches

tuple_sel_Lc = Selection("tuple_sel_Lc",
                         Algorithm = TURBO_Lc,
                         RequiredSelections = [Lc])

#%% Xiccpp turbo

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

##########
#  DTF
##########
from Configurables import TupleToolDecay
TURBO_Xicc.addTool(TupleToolDecay, name = 'Xicc')
TURBO_Xicc.Xicc.ToolList +=  ["LoKi::Hybrid::TupleTool/LoKi_All0"]
from Configurables import LoKi__Hybrid__TupleTool
###################################################
LoKiTuple0 = LoKi__Hybrid__TupleTool("LoKi_All0")
LoKiTuple0.Variables =  {
    "M_DTF":"DTF_FUN( M, False)",
    "M_DTF_Lc":"DTF_FUN( M, False, strings( 'Lambda_c+'))",
    "M_DTF_PV":"DTF_FUN( M, True)",
    "M_DTF_Lc_PV":"DTF_FUN( M, True, strings( 'Lambda_c+'))",
    "CHI2NDOF_DTF":"DTF_CHI2NDOF(False)",
    "CHI2NDOF_DTF_Lc":"DTF_CHI2NDOF(False, strings( 'Lambda_c+'))",
    "CHI2NDOF_DTF_PV":"DTF_CHI2NDOF(True)",
    "CHI2NDOF_DTF_Lc_PV":"DTF_CHI2NDOF(True, strings( 'Lambda_c+'))"
    }

TURBO_Xicc.Xicc.addTool(LoKiTuple0)

############
# MC TRUTH
############

from Configurables import TupleToolMCTruth
MCTruth = TupleToolMCTruth()
MCTruth.ToolList = [ "MCTupleToolKinematic",
                     "MCTupleToolHierarchy" ]

TURBO_Xicc.addTool(MCTruth)

from TeslaTools import TeslaTruthUtils

mc_tools = [
    'MCTupleToolKinematic',
    'MCTupleToolHierarchy'
    ]

relations = [
    TeslaTruthUtils.getRelLoc(''),
    # Location of the truth tables for PersistReco objects
    '/Event/Turbo/Relations/Hlt2/Protos/Charged'
    ]

'''
relations = TeslaTruthUtils.getRelLocs() + [
    TeslaTruthUtils.getRelLoc(''),
    # Location of the truth tables for PersistReco objects
    'Relations/Hlt2/Protos/Charged'
]
'''
TeslaTruthUtils.makeTruth(TURBO_Xicc, relations, mc_tools)

tuple_sel_Xicc = Selection("tuple_sel_Xicc",
                           Algorithm = TURBO_Xicc,
                           RequiredSelections = [Xicc])
#%% Xiccpp reconstruction

#########################

# Xicc reconstruction 

#########################


Xicc_cdc = '(TRCHI2DOF<3)&(MIPCHI2DV(PRIMARY)>1.)&(TRGHOSTPROB<0.4)'
Xicc_mc = '(VFASPF(VCHI2PDOF) < 25)&(MIPCHI2DV(PRIMARY)<25.)&(BPVDIRA>0.99)&(BPVLTIME() > 0.15*ps)'
Xicc_cc = '((APT1+APT2+APT3+APT4)>2*GeV) & (in_range(3200,AM,4000))'

Xiccsel = CombineSelection(
    'simXicc',
    [Lc, Pions, Kaons],
    DecayDescriptor = '[Xi_cc++ -> Lambda_c+ K- pi+ pi+]cc',
    Preambulo = MyPreambulo,
    DaughtersCuts = {
        'Lambda_c+' : 'ALL',
        'K-' : Xicc_cdc + '&(PT>0.25*GeV)&(PROBNNk>0.1)',  
        'pi+' : Xicc_cdc + '&(PT>0.20*GeV)&(PROBNNpi>0.2)'
        },
    MotherCut = Xicc_mc,
    CombinationCut = Xicc_cc)



REC = DecayTreeTuple("Xicc_REC",
        Decay = '[Xi_cc++ -> ^(Lambda_c+ -> ^K- ^p+ ^pi+) ^K- ^pi+ ^pi+]CC',
        Branches = { "Xicc":"[Xi_cc++ -> (Lambda_c+ -> K- p+ pi+) K- pi+ pi+]CC" ,
            "Lc" : "[Xi_cc++ -> ^(Lambda_c+ -> p+ K- pi+) K- pi+ pi+]CC",
            "LcP": "[Xi_cc++ -> (Lambda_c+ -> ^p+ K- pi+) K- pi+ pi+]CC",
            "LcK": "[Xi_cc++ -> (Lambda_c+ -> p+ ^K- pi+) K- pi+ pi+]CC",
            "LcPi": "[Xi_cc++ -> (Lambda_c+ -> p+ K- ^pi+) K- pi+ pi+]CC",
            "XiccK": "[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) ^K- pi+ pi+]CC",
            "XiccPi1": "[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) K- ^pi+ pi+]CC",
            "XiccPi2": "[Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) K- pi+ ^pi+]CC"
            }
)


REC.ToolList = myToolList

##########
#  DTF
##########
from Configurables import TupleToolDecay
REC.addTool(TupleToolDecay, name = 'Xicc')
REC.Xicc.ToolList +=  ["LoKi::Hybrid::TupleTool/LoKi_All0"]
from Configurables import LoKi__Hybrid__TupleTool
###################################################
LoKiTuple0 = LoKi__Hybrid__TupleTool("LoKi_All0")
LoKiTuple0.Variables =  {
    "M_DTF":"DTF_FUN( M, False)",
    "M_DTF_Lc":"DTF_FUN( M, False, strings( 'Lambda_c+'))",
    "M_DTF_PV":"DTF_FUN( M, True)",
    "M_DTF_Lc_PV":"DTF_FUN( M, True, strings( 'Lambda_c+'))",
    "CHI2NDOF_DTF":"DTF_CHI2NDOF(False)",
    "CHI2NDOF_DTF_Lc":"DTF_CHI2NDOF(False, strings( 'Lambda_c+'))",
    "CHI2NDOF_DTF_PV":"DTF_CHI2NDOF(True)",
    "CHI2NDOF_DTF_Lc_PV":"DTF_CHI2NDOF(True, strings( 'Lambda_c+'))"
    }

REC.Xicc.addTool(LoKiTuple0)

############
# MC TRUTH
############

from Configurables import TupleToolMCTruth
MCTruth = TupleToolMCTruth()
MCTruth.ToolList = [ "MCTupleToolKinematic",
                     "MCTupleToolHierarchy" ]

REC.addTool(MCTruth)

from TeslaTools import TeslaTruthUtils

mc_tools = [
    "MCTupleToolKinematic",
    "MCTupleToolHierarchy"
    ]


'''relations = TeslaTruthUtils.getRelLocs() + [
    TeslaTruthUtils.getRelLoc(''),
    # Location of the truth tables for PersistReco objects
    'Relations/Hlt2/Protos/Charged'
]'''

relations = [
    TeslaTruthUtils.getRelLoc(''),
    # Location of the truth tables for PersistReco objects
    '/Event/Turbo/Relations/Hlt2/Protos/Charged'
    ]

TeslaTruthUtils.makeTruth(REC, relations, mc_tools)

tuple_sel = Selection("tuple_sel_rec",
                       Algorithm = REC,
                       RequiredSelections = [Xiccsel])


#%% Xiccpst reconstruction
#########################

# Xiccpst reconstruction 

#########################



Omegaccpsel = CombineSelection(
    'simOmegaccp',
    [Xiccsel, KaonsNoPID],
    DecayDescriptor = '[Omega_cc+ -> Xi_cc++ K-]cc',
    Preambulo = MyPreambulo,
    DaughtersCuts = {
        'Xi_cc++' : 'ALL',
        'K-' : '(TRGHOSTPROB<0.3) & (MIPCHI2DV(PRIMARY)<16.)'
        },
    CheckOverlapTool = "LoKi::CheckOverlap",
    MotherCut = '(VFASPF(VCHI2PDOF) < 25)&(M - M1 < 1000)',
    CombinationCut = "(AM - AM1 < 1100)")

Omegaccp_REC = DecayTreeTuple("Omegaccp_REC",
                     #                     Inputs = [Xiccsel.outputLocation()],
                     Decay = '[Omega_cc+ -> ^(Xi_cc++ -> ^(Lambda_c+ -> ^K- ^p+ ^pi+) ^K- ^pi+ ^pi+) ^K-]CC',
                     Branches = { "C":"[Omega_cc+ -> (Xi_cc++ -> (Lambda_c+ -> K- p+ pi+) K- pi+ pi+) K-]CC" ,
                                  "Xicc" : "[Omega_cc+ -> ^(Xi_cc++ -> (Lambda_c+ -> K- p+ pi+) K- pi+ pi+) K-]CC",
                                  "Lc" : "[Omega_cc+ -> (Xi_cc++ -> ^(Lambda_c+ -> K- p+ pi+) K- pi+ pi+) K-]CC",
                                  "LcP" : "[Omega_cc+ -> (Xi_cc++ -> (Lambda_c+ -> K- ^p+ pi+) K- pi+ pi+) K-]CC",
                                  "LcPi" : "[Omega_cc+ -> (Xi_cc++ -> (Lambda_c+ -> K- p+ ^pi+) K- pi+ pi+) K-]CC",
                                  "LcK" : "[Omega_cc+ -> (Xi_cc++ -> (Lambda_c+ -> ^K- p+ pi+) K- pi+ pi+) K-]CC",
                                  "XiccK" : "[Omega_cc+ -> (Xi_cc++ -> (Lambda_c+ -> K- p+ pi+) ^K- pi+ pi+) K-]CC",
                                  "XiccPi1" : "[Omega_cc+ -> (Xi_cc++ -> (Lambda_c+ -> K- p+ pi+) K- ^pi+ pi+) K-]CC",
                                  "XiccPi2" : "[Omega_cc+ -> (Xi_cc++ -> (Lambda_c+ -> K- p+ pi+) K- pi+ ^pi+) K-]CC",
                                  "K": "[Omega_cc+ -> (Xi_cc++ -> (Lambda_c+ -> K- p+ pi+) K- pi+ pi+) ^K-]CC"
                                  }
                     )

fillTuple(Omegaccp_REC)

############
# MC TRUTH
############

from Configurables import TupleToolMCTruth
MCTruth = TupleToolMCTruth()
MCTruth.ToolList = [ "MCTupleToolKinematic",
                     "MCTupleToolHierarchy" ]

Omegaccp_REC.addTool(MCTruth)

from TeslaTools import TeslaTruthUtils

mc_tools = [
    'MCTupleToolKinematic',
    'MCTupleToolHierarchy'
    ]


relations = TeslaTruthUtils.getRelLocs() + [
    TeslaTruthUtils.getRelLoc(''),
    # Location of the truth tables for PersistReco objects
    'Relations/Hlt2/Protos/Charged'
]

# relations = [
#     TeslaTruthUtils.getRelLoc(''),
#     # Location of the truth tables for PersistReco objects
#     '/Event/Turbo/Relations/Hlt2/Protos/Charged'
#     ]

TeslaTruthUtils.makeTruth(Omegaccp_REC, relations, mc_tools)

XiccXmlDiff = "TMVAClassification_BDT_diff.weights.xml"

XiccVarsDiff = {  
    "log_Xicc_IPCHI2_OWNPV"                 : "log(BPVIPCHI2())" ,
    "acos_Xicc_DIRA_OWNPV"                  : "acos(BPVDIRA)",
    "log_Xicc_FDCHI2_OWNPV"               : "log(BPVVDCHI2)",
    "log_Xicc_ENDVERTEX_CHI2_NDOF" : "log(VFASPF(VCHI2PDOF))",
    "Lc_ENDVERTEX_CHI2_NDOF" : "CHILD(VFASPF(VCHI2PDOF),1)",
    "log_Xicc_CHI2NDOF_DTF_PV"              : "log(DTF_CHI2NDOF(True))",

    "LcP_PIDp"       : "CHILD(PIDp,1, 2)",
    "LcK_PIDK"       : "CHILD(PIDK,1, 1)",
    "LcPi_PIDK"      : "CHILD(PIDK,1, 3)",
    "XiccK_PIDK"     : "CHILD(PIDK,2)",
    "XiccPi_PIDK_sum"   : "CHILD(PIDK,3)+CHILD(PIDK,4)",
    "XiccPi_PIDK_diff"   : "abs(CHILD(PIDK,3)-CHILD(PIDK,4))",
    
    "min_Xicc_Daughters_PT"   : "min( min(CHILD(PT,1), CHILD(PT,2)),  min(CHILD(PT,3),CHILD(PT,4) ) )"   ,
    
    "Lc_PT"         : "CHILD(PT,1)",
    "XiccK_PT"      : "CHILD(PT,2)",
    "XiccPi_PT_sum"    : "CHILD(PT,3)+CHILD(PT,4)",
    "XiccPi_PT_diff"    : "abs(CHILD(PT,3)-CHILD(PT,4))",     

    "log_Lc_IPCHI2_OWNPV"       : "log(CHILD(MIPCHI2DV(),1))",
    "log_XiccK_IPCHI2_OWNPV"    : "log(CHILD(MIPCHI2DV(),2))",
    "log_XiccPi_IPCHI2_OWNPV_sum"  : "log(CHILD(MIPCHI2DV(),3)+CHILD(MIPCHI2DV(),4))",
    "log_XiccPi_IPCHI2_OWNPV_diff"  : "log(abs(CHILD(MIPCHI2DV(),3)-CHILD(MIPCHI2DV(),4)))",

}


applyMVAvalue( Omegaccp_REC.Xicc,
                "BDTXicc",
                MVAVars     = XiccVarsDiff,
                MVAxmlFile  = XiccXmlDiff
                )


tuple_sel_Omegaccp = Selection("tuple_sel_Omegaccp",
                       Algorithm = Omegaccp_REC,
                       RequiredSelections = [Omegaccpsel])


print("RELATIONS" ,relations)

#########################

# Xiccpst WS reconstruction 

#########################



OmegaccpselWS = CombineSelection(
    'simOmegaccpWS',
    [Xiccsel, KaonsNoPID],
    DecayDescriptor = '[Omega_cc+ -> Xi_cc++ K+]cc',
    Preambulo = MyPreambulo,
    DaughtersCuts = {
        'Xi_cc++' : 'ALL',
        'K+' : '(TRGHOSTPROB<0.3) & (MIPCHI2DV(PRIMARY)<16.)'
        },
    CheckOverlapTool = "LoKi::CheckOverlap",
    MotherCut = '(VFASPF(VCHI2PDOF) < 25)&(M - M1 < 1000)',
    CombinationCut = "(AM - AM1 < 1100)")

Omegaccp_REC_WS = DecayTreeTuple("Omegaccp_REC_WS",
                     #                     Inputs = [Xiccsel.outputLocation()],
                     Decay = '[Omega_cc+ -> ^(Xi_cc++ -> ^(Lambda_c+ -> ^K- ^p+ ^pi+) ^K- ^pi+ ^pi+) ^K+]CC',
                     Branches = { "C":"[Omega_cc+ -> (Xi_cc++ -> (Lambda_c+ -> K- p+ pi+) K- pi+ pi+) K+]CC" ,
                                  "Xicc" : "[Omega_cc+ -> ^(Xi_cc++ -> (Lambda_c+ -> K- p+ pi+) K- pi+ pi+) K+]CC",
                                  "Lc" : "[Omega_cc+ -> (Xi_cc++ -> ^(Lambda_c+ -> K- p+ pi+) K- pi+ pi+) K+]CC",
                                  "LcP" : "[Omega_cc+ -> (Xi_cc++ -> (Lambda_c+ -> K- ^p+ pi+) K- pi+ pi+) K+]CC",
                                  "LcPi" : "[Omega_cc+ -> (Xi_cc++ -> (Lambda_c+ -> K- p+ ^pi+) K- pi+ pi+) K+]CC",
                                  "LcK" : "[Omega_cc+ -> (Xi_cc++ -> (Lambda_c+ -> ^K- p+ pi+) K- pi+ pi+) K+]CC",
                                  "XiccK" : "[Omega_cc+ -> (Xi_cc++ -> (Lambda_c+ -> K- p+ pi+) ^K- pi+ pi+) K+]CC",
                                  "XiccPi1" : "[Omega_cc+ -> (Xi_cc++ -> (Lambda_c+ -> K- p+ pi+) K- ^pi+ pi+) K+]CC",
                                  "XiccPi2" : "[Omega_cc+ -> (Xi_cc++ -> (Lambda_c+ -> K- p+ pi+) K- pi+ ^pi+) K+]CC",
                                  "K": "[Omega_cc+ -> (Xi_cc++ -> (Lambda_c+ -> K- p+ pi+) K- pi+ pi+) ^K+]CC"
                                  }
                     )



fillTuple(Omegaccp_REC_WS, WS=True)

############
# MC TRUTH
############

from Configurables import TupleToolMCTruth
MCTruth = TupleToolMCTruth()
MCTruth.ToolList = [ "MCTupleToolKinematic",
                     "MCTupleToolHierarchy" ]

Omegaccp_REC_WS.addTool(MCTruth)

from TeslaTools import TeslaTruthUtils

mc_tools = [
    'MCTupleToolKinematic',
    'MCTupleToolHierarchy'
    ]


relations = TeslaTruthUtils.getRelLocs() + [
    TeslaTruthUtils.getRelLoc(''),
    # Location of the truth tables for PersistReco objects
    'Relations/Hlt2/Protos/Charged'
]

# relations = [
#     TeslaTruthUtils.getRelLoc(''),
#     # Location of the truth tables for PersistReco objects
#     '/Event/Turbo/Relations/Hlt2/Protos/Charged'
#     ]

TeslaTruthUtils.makeTruth(Omegaccp_REC_WS, relations, mc_tools)

applyMVAvalue( Omegaccp_REC_WS.Xicc,
                    "BDTXicc",
                    MVAVars     = XiccVarsDiff,
                    MVAxmlFile  = XiccXmlDiff
                    )

tuple_sel_Omegaccp_WS = Selection("tuple_sel_Xiccp_WS",
                      Algorithm = Omegaccp_REC_WS,
                      RequiredSelections = [OmegaccpselWS])
#%% Configure DaVinci

from Configurables import DaVinci

from PhysConf.Selections import SelectionSequence
seq0 = SelectionSequence('SEQ0', tuple_sel_Lc )
seq1 = SelectionSequence('SEQ1', tuple_sel_Xicc )
seq2 = SelectionSequence('SEQ2', tuple_sel )
seq3 = SelectionSequence('SEQ3', tuple_sel_Omegaccp )
seq4 = SelectionSequence('SEQ4', tuple_sel_Omegaccp_WS )
seq5 = SelectionSequence('SEQ5', mcTuple_sel )



# DaVinci().EventPreFilters = fltrs.filters('Filter')
# DaVinci().UserAlgorithms = [seq0.sequence(), seq1.sequence(), seq2.sequence(), seq3.sequence(), seq4.sequence()] 
DaVinci().UserAlgorithms = [seq3.sequence(), seq4.sequence(),seq5.sequence()] 
DaVinci().InputType = 'MDST' 
DaVinci().TupleFile = f'DV_Omegaccp_MC_{evt_id}_{the_year}_{polarity}.root' 
DaVinci().PrintFreq = 2500 
DaVinci().DataType = the_year
DaVinci().Simulation = True


rootInTES = '/Event/Turbo'
DaVinci().RootInTES = rootInTES
DaVinci().Turbo = True 



# Only ask for luminosity information when not using simulated data
DaVinci().Lumi = not DaVinci().Simulation 
if ganga:
    DaVinci().EvtMax = -1
else:
    DaVinci().EvtMax = 10000


tag = int(the_year)%10
if polarity == 'MD':
    DaVinci().CondDBtag = f'sim-20201113-{tag}-vc-md100-Sim10' 
else :
    DaVinci().CondDBtag = f'sim-20201113-{tag}-vc-mu100-Sim10' 
DaVinci().DDDBtag = f'dddb-20220927-{the_year}'

#%% Use the local input data
if not ganga :
    from Gaudi.Configuration import *
    from GaudiConf import IOHelper

    if evt_id == 26266050 :
        if polarity == 'MD':
            IOHelper().inputFiles(['/afs/cern.ch/work/p/pgaigne/DST/00071452_00000051_7.AllStreams.dst',
                                '/afs/cern.ch/work/p/pgaigne/DST/00071452_00000095_7.AllStreams.dst'], clear=True)
        else :
            IOHelper().inputFiles(['/afs/cern.ch/work/p/pgaigne/DST/00071450_00000822_7.AllStreams.dst'], clear=True)
        #IOHelper().inputFiles(['/afs/cern.ch/work/p/pgaigne/DST/00071452_00000051_7.AllStreams.dst'], clear=True)

    elif evt_id == 26167052 :
        if the_year == '2016' :
            if polarity == 'MD':
                IOHelper().inputFiles(['/afs/cern.ch/work/p/pgaigne/DST/00184074_00000002_1.allstreams.mdst'], clear=True)
            else :
                print('No DST file')

        elif the_year == '2017' :
            print('No DST file')

        elif the_year == '2018' :
            if polarity == 'MD':
                IOHelper().inputFiles(['/afs/cern.ch/work/p/pgaigne/DST/00183846_00000011_1.allstreams.mdst'], clear=True)
            else :
                print('No DST file')
            


