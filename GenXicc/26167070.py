# file /afs/cern.ch/user/p/pgaigne/GaussDev_v49r17/Gen/DecFiles/options/26167070.py generated: Wed, 07 Dec 2022 15:25:45
#
# Event Type: 26167070
#
# ASCII decay Descriptor: [Xi_cc+ -> (Xi_cc++ -> (Lambda_c+ -> p+ K- pi+) K- pi+ pi+) pi- ]cc
#
from Configurables import Generation
Generation().EventType = 26167070
Generation().SampleGenerationTool = "Special"
from Configurables import Special
Generation().addTool( Special )
Generation().Special.ProductionTool = "GenXiccProduction"
Generation().PileUpTool = "FixedLuminosityForRareProcess"
from Configurables import GenXiccProduction
Generation().Special.addTool( GenXiccProduction )
Generation().Special.GenXiccProduction.BaryonState = "Xi_cc+"
from Configurables import ToolSvc
from Configurables import EvtGenDecay
ToolSvc().addTool( EvtGenDecay )
ToolSvc().EvtGenDecay.UserDecayFile = "/afs/cern.ch/user/p/pgaigne/GaussDev_v49r17/Gen/DecFiles/dkfiles/Xiccst+_Xicc++pi,LcKmPipPip=GenXicc,DecProdCut,WithMinPTv1.dec"
Generation().Special.CutTool = "XiccDaughtersInLHCbAndWithMinPT"
from Configurables import XiccDaughtersInLHCbAndWithMinPT
Generation().Special.addTool( XiccDaughtersInLHCbAndWithMinPT )
Generation().Special.XiccDaughtersInLHCbAndWithMinPT.BaryonState = Generation().Special.GenXiccProduction.BaryonState
from GaudiKernel import SystemOfUnits
Generation().Special.XiccDaughtersInLHCbAndWithMinPT.MinXiccPT = 2500*SystemOfUnits.MeV
from GaudiKernel import SystemOfUnits
Generation().Special.XiccDaughtersInLHCbAndWithMinPT.MinDaughterPT = 200*SystemOfUnits.MeV
from Configurables import LHCb__ParticlePropertySvc
LHCb__ParticlePropertySvc().Particles = [ "Xi_cc+ 502 4412 1.0 4.0  6.58e-22 Xi_cc+ 4412 0.005", "Xi_cc~- 503 -4412 -1.0 4.0  6.58e-22 anti-Xi_cc- -4412 0.005" ]
