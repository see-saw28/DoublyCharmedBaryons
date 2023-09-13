#!/usr/bin/env python

# 
# This example is basically the same as $ROOTSYS/tmva/test/TMVAClassification.C
# 

import ROOT

# in order to start TMVA
ROOT.TMVA.Tools.Instance()

# note that it seems to be mandatory to have an
# output file, just passing None to TMVA::Factory(..)
# does not work. Make sure you don't overwrite an
# existing file.


XiccMVAcut = 'Loose'
# XiccMVAcut = 'Tight'

if XiccMVAcut == 'Loose':
    mva_cut = 0.07
else :
    mva_cut = 0.17

# baryon = "Xiccpst"
baryon = "Omegaccpst"

# open input file, get trees, create output file

# MCFile = ROOT.TFile(f"/eos/lhcb/user/p/pgaigne/STEP3/2016/MC/-MC-2016-MCMatch.root")
MCFile = ROOT.TFile(f"/eos/lhcb/user/p/pgaigne/STEP3/Run2/{baryon}-MC-Run2-MCMatch-clone-duplicate.root")


tree_s = MCFile.Get("DecayTree")


# dataFile = ROOT.TFile("/eos/lhcb/user/p/pgaigne/STEP3/2016/WS/Xiccpst-WS-2016.root")
# tree_b = dataFile.Get("tuple_sel_Xiccp_WS/DecayTree")

dataFileWS = ROOT.TFile(f"/eos/lhcb/user/p/pgaigne/STEP3/Run2/{baryon}-WS-Run2-Lc-Loose-clone-duplicate.root")
tree_ws_b = dataFileWS.Get("DecayTree")

dataFileRS = ROOT.TFile(f"/eos/lhcb/user/p/pgaigne/STEP3/Run2/{baryon}-RS-Run2-Lc-Loose-clone-duplicate.root")
tree_rs_b = dataFileRS.Get("DecayTree")

fout = ROOT.TFile(f"/afs/cern.ch/work/p/pgaigne/MVA/TMVAout-{baryon}-{XiccMVAcut}.root","RECREATE")

# define factory with options
factory = ROOT.TMVA.Factory("TMVAClassification", fout,
                            ":".join([    "!V",
                                          "!Silent",
                                          "Color",
                                          "DrawProgressBar",
                                          "Transformations=I;D;P;G,D",
                                          "AnalysisType=Classification"]
                                     ))

loader = ROOT.TMVA.DataLoader(f"dataset-{baryon}-{XiccMVAcut}")

# add discriminating variables for training

loader.AddVariable("log(TMath::Max(10e-10,C_IPCHI2_OWNPV))","log_C_IPCHI2_OWNPV","","F")
# loader.AddVariable("TMath::ACos(C_DIRA_OWNPV)","acos_C_DIRA_OWNPV","","F")
# loader.AddVariable("log(TMath::Max(10e-10,C_FDCHI2_OWNPV))","log_C_FDCHI2_OWNPV","","F")
# loader.AddVariable("C_ENDVERTEX_CHI2/C_ENDVERTEX_NDOF","C_ENDVERTEX_CHI2_NDOF","","F")
# loader.AddVariable("log(TMath::Max(10e-10,C_ENDVERTEX_CHI2/C_ENDVERTEX_NDOF))","log_C_ENDVERTEX_CHI2_NDOF","","F")
# loader.AddVariable("log(TMath::Max(10e-10,C_CHI2NDOF_DTF_PV))","log_C_CHI2NDOF_DTF_PV","","F")
loader.AddVariable("C_PT","F")

loader.AddVariable("log(Pi_IPCHI2_OWNPV)","F")  
if baryon == "Xiccpst":
    loader.AddVariable("Pi_ProbNNpi","F")
    loader.AddVariable("Pi_PT","F")  

elif baryon == "Omegaccpst":
    loader.AddVariable("Pi_ProbNNk","F")
    loader.AddVariable("C_KaonDTF_K_PT","F") 

# loader.AddVariable("log(Xicc_IPCHI2_OWNPV)","F")  
# loader.AddVariable("Xicc_PT","F")
# loader.AddVariable("Xicc_ENDVERTEX_CHI2/Xicc_ENDVERTEX_NDOF","Xicc_ENDVERTEX_CHI2_NDOF","","F")
# loader.AddVariable("log(TMath::Max(10e-10,Xicc_ENDVERTEX_CHI2/Xicc_ENDVERTEX_NDOF))","log_Xicc_ENDVERTEX_CHI2_NDOF","","F")
# loader.AddVariable("log(TMath::Max(10e-10,Xicc_CHI2NDOF_DTF_PV))","log_Xicc_CHI2NDOF_DTF_PV","","F")
     
loader.AddSpectator("C_M", "F")      
loader.AddSpectator("Xicc_M_DTF_Lc_PV", "F") 
loader.AddSpectator("Lc_M", "F")


if baryon == "Xiccpst":
    cut = "(abs(C_TRUEID)==4412&abs(Pi_TRUEID)==211&abs(Pi_MC_MOTHER_ID)==4412&abs(Xicc_TRUEID)==4422&abs(Xicc_MC_MOTHER_ID)==4412&abs(Lc_TRUEID)==4122&abs(LcP_TRUEID)==2212&abs(LcPi_TRUEID)==211&abs(LcK_TRUEID)==321&(abs(LcP_MC_MOTHER_ID)==4122|abs(LcP_MC_GD_MOTHER_ID)==4122)&(abs(LcK_MC_MOTHER_ID)==4122|abs(LcK_MC_GD_MOTHER_ID)==4122)&(abs(LcPi_MC_MOTHER_ID)==4122|abs(LcPi_MC_GD_MOTHER_ID)==4122)&abs(XiccPi1_TRUEID)==211&abs(XiccPi1_MC_MOTHER_ID)==4422&abs(XiccPi1_MC_GD_MOTHER_ID)==4412&abs(XiccPi2_TRUEID)==211&abs(XiccPi2_MC_MOTHER_ID)==4422&abs(XiccPi2_MC_GD_MOTHER_ID)==4412&abs(XiccK_TRUEID)==321&abs(XiccK_MC_MOTHER_ID)==4422&abs(XiccK_MC_GD_MOTHER_ID)==4412)"
    tree_s_cut = tree_s.CopyTree(cut+f"&abs(Xicc_M_DTF_Lc_PV-3621)<15 & abs(Lc_M-2288)<18  & Pi_ProbNNpi>0.1 & Pi_PT>200 & Xicc_TMVA_BDTXicc>{mva_cut}")

elif baryon == "Omegaccpst" :
    cut = "(abs(C_TRUEID)==4432&abs(Pi_TRUEID)==321&abs(Pi_MC_MOTHER_ID)==4432&abs(Xicc_TRUEID)==4422&abs(Xicc_MC_MOTHER_ID)==4432&abs(Lc_TRUEID)==4122&abs(LcP_TRUEID)==2212&abs(LcPi_TRUEID)==211&abs(LcK_TRUEID)==321&(abs(LcP_MC_MOTHER_ID)==4122|abs(LcP_MC_GD_MOTHER_ID)==4122)&(abs(LcK_MC_MOTHER_ID)==4122|abs(LcK_MC_GD_MOTHER_ID)==4122)&(abs(LcPi_MC_MOTHER_ID)==4122|abs(LcPi_MC_GD_MOTHER_ID)==4122)&abs(XiccPi1_TRUEID)==211&abs(XiccPi1_MC_MOTHER_ID)==4422&abs(XiccPi1_MC_GD_MOTHER_ID)==4432&abs(XiccPi2_TRUEID)==211&abs(XiccPi2_MC_MOTHER_ID)==4422&abs(XiccPi2_MC_GD_MOTHER_ID)==4432&abs(XiccK_TRUEID)==321&abs(XiccK_MC_MOTHER_ID)==4422&abs(XiccK_MC_GD_MOTHER_ID)==4432)"
    tree_s_cut = tree_s.CopyTree(cut+f"&abs(Xicc_M_DTF_Lc_PV-3621)<15 & abs(Lc_M-2288)<18  & Pi_ProbNNk>0.1 & C_KaonDTF_K_PT>200 & Xicc_TMVA_BDTXicc>{mva_cut}")

loader.AddSignalTree(tree_s_cut)
# define signal and background trees



if baryon == "Xiccpst":
    SB_start = 25
    SB_end = 40 

    tree_ws_b_cut = tree_ws_b.CopyTree(f"abs(Xicc_M_DTF_Lc_PV-3621)<{SB_end} & abs(Lc_M-2288)<18 & C_M_DTF_Xicc_PV-3761<500 & Xicc_TMVA_BDTXicc>{mva_cut}")
    loader.AddBackgroundTree(tree_ws_b_cut)

    tree_rs_b_cut = tree_rs_b.CopyTree(f"(((Xicc_M_DTF_Lc_PV<3621-{SB_start})&(Xicc_M_DTF_Lc_PV>3621-{SB_end}))|((Xicc_M_DTF_Lc_PV>3621+{SB_start})&(Xicc_M_DTF_Lc_PV<3621+{SB_end}))) & abs(Lc_M-2288)<18 & C_M_DTF_Xicc_PV-3761<500 & Xicc_TMVA_BDTXicc>{mva_cut}")
    loader.AddBackgroundTree(tree_rs_b_cut)

elif baryon == "Omegaccpst":
    SB_start = 25
    SB_end = 80 
    
    tree_ws_b_cut = tree_ws_b.CopyTree(f"abs(Xicc_M_DTF_Lc_PV-3621)<{SB_end} & abs(Lc_M-2288)<18 & C_KaonDTF_C_M-4115.1<500 & Xicc_TMVA_BDTXicc>{mva_cut}")
    loader.AddBackgroundTree(tree_ws_b_cut)    

    tree_rs_b_cut = tree_rs_b.CopyTree(f"(((Xicc_M_DTF_Lc_PV<3621-{SB_start})&(Xicc_M_DTF_Lc_PV>3621-{SB_end}))|((Xicc_M_DTF_Lc_PV>3621+{SB_start})&(Xicc_M_DTF_Lc_PV<3621+{SB_end}))) & abs(Lc_M-2288)<18 & C_KaonDTF_C_M-4115.1<500 & Xicc_TMVA_BDTXicc>{mva_cut}")
    loader.AddBackgroundTree(tree_rs_b_cut)


# define additional cuts 

sigCut = ROOT.TCut(f"abs(Xicc_M_DTF_Lc_PV-3621)<15 & abs(Lc_M-2288)<18") #mass window for Xicc and Lc
bkgCut = ROOT.TCut(f"") #mass window for Xicc and Lc and Xicc BDT cut 


# set options for trainings
loader.PrepareTrainingAndTestTree(sigCut, 
                                   bkgCut, 
                                   ":".join(["nTrain_Signal=0",
                                             "nTrain_Background=0",
                                             "SplitMode=Random",
                                             "NormMode=NumEvents",
                                             "!V"
                                             ]))

# book and define methods that should be trained

method = factory.BookMethod(loader,
                            ROOT.TMVA.Types.kBDT, 
                            "BDT",
                            "!H:!V:NTrees=850:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20" )

method = factory.BookMethod(loader,
                            ROOT.TMVA.Types.kBDT, 
                            "BDTG",
                            "!H:!V:NTrees=1000:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=2" )

method = factory.BookMethod(loader,
                            ROOT.TMVA.Types.kMLP, 
                            "MLP", 
                            "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:!UseRegulator" )




# self-explaining
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

c1 = factory.GetROCCurve(loader)
c1.Draw()
#c1.SaveAs("ROC.pdf")
c1.Print(f"ROC-{baryon}-{XiccMVAcut}-test-1.png")
