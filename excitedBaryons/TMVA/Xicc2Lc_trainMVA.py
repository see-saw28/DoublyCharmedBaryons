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

tree = 'rec'

# open input file, get trees, create output file
MCFile = ROOT.TFile("/eos/lhcb/user/p/pgaigne/MC/26266052/MC-Run2-26266052-MCMatch-Lc-clone-duplicate.root")
# MCFile = ROOT.TFile("/eos/lhcb/user/p/pgaigne/MC/26266050/MC-2016-26266050.root") #old

dataFile = ROOT.TFile("/eos/lhcb/user/p/pgaigne/STEP2/2016/job74-CombDVntuple-Lc_Cuts-SB-3800-3900-Lc-clone-duplicate.root")
# dataFile = ROOT.TFile("/eos/lhcb/user/p/pgaigne/STEP2/2016/job74-DV-Xiccpp-Collision-2016-MD-0-reduced.root") #old
tree_s = MCFile.Get(f"DecayTree")
if tree == 'rec':
     # tree_b = dataFile.Get("tuple_sel_rec_WS/DecayTree")
     # tree_b = dataFile.Get("tuple_sel_rec/DecayTree")
     tree_b = dataFile.Get("DecayTree")
else :
     tree_b = dataFile.Get("tuple_sel_Xicc/DecayTree")

fout = ROOT.TFile(f"/afs/cern.ch/work/p/pgaigne/MVA/TMVAout-{tree}-SB-diff.root","RECREATE")

# define factory with options
factory = ROOT.TMVA.Factory("TMVAClassification", fout,
                            ":".join([    "!V",
                                          "!Silent",
                                          "Color",
                                          "DrawProgressBar",
                                          "Transformations=I;D;P;G,D",
                                          "AnalysisType=Classification"]
                                     ))

loader = ROOT.TMVA.DataLoader(f"dataset-{tree}-SB-diff")

# add discriminating variables for training
if tree == 'rec' :
     loader.AddVariable("log(TMath::Max(10e-10,Xicc_IPCHI2_OWNPV))","log_Xicc_IPCHI2_OWNPV","","F")
     loader.AddVariable("TMath::ACos(Xicc_DIRA_OWNPV)","acos_Xicc_DIRA_OWNPV","","F")
     loader.AddVariable("log(TMath::Max(10e-10,Xicc_FDCHI2_OWNPV))","log_Xicc_FDCHI2_OWNPV","","F")
     loader.AddVariable("Lc_ENDVERTEX_CHI2/Lc_ENDVERTEX_NDOF","Lc_ENDVERTEX_CHI2_NDOF","","F")
     loader.AddVariable("log(TMath::Max(10e-10,Xicc_ENDVERTEX_CHI2/Xicc_ENDVERTEX_NDOF))","log_Xicc_ENDVERTEX_CHI2_NDOF","","F")
     loader.AddVariable("log(TMath::Max(10e-10,Xicc_CHI2NDOF_DTF_PV))","log_Xicc_CHI2NDOF_DTF_PV","","F")
     loader.AddVariable("LcP_PIDp","F")
     loader.AddVariable("LcK_PIDK","F")
     loader.AddVariable("LcPi_PIDK","F")
     loader.AddVariable("XiccK_PIDK","F")
     loader.AddVariable("XiccPi1_PIDK+XiccPi2_PIDK","XiccPi_PIDK_sum","","F")
     loader.AddVariable("abs(XiccPi1_PIDK-XiccPi2_PIDK)","XiccPi_PIDK_diff","","F")
     loader.AddVariable("TMath::Min(TMath::Min(XiccK_PT,Lc_PT),TMath::Min(XiccPi1_PT,XiccPi2_PT))","min_Xicc_Daughters_PT","","F")
     loader.AddVariable("Lc_PT","F")
     loader.AddVariable("XiccPi1_PT+XiccPi2_PT","XiccPi_PT_sum","","F")
     loader.AddVariable("abs(XiccPi1_PT-XiccPi2_PT)","XiccPi_PT_diff","","F")
     loader.AddVariable("XiccK_PT","F")
     loader.AddVariable("log(TMath::Max(10e-10,Lc_IPCHI2_OWNPV))","log_Lc_IPCHI2_OWNPV","","F")
     loader.AddVariable("log(TMath::Max(10e-10,XiccK_IPCHI2_OWNPV))","log_XiccK_IPCHI2_OWNPV","","F")
     loader.AddVariable("log(XiccPi1_IPCHI2_OWNPV+XiccPi2_IPCHI2_OWNPV)","log_XiccPi_IPCHI2_OWNPV_sum","","F")
     loader.AddVariable("log(abs(XiccPi1_IPCHI2_OWNPV-XiccPi2_IPCHI2_OWNPV))","log_XiccPi_IPCHI2_OWNPV_diff","","F")
          
else :
     loader.AddVariable("log(TMath::Max(10e-10,Xicc_IPCHI2_OWNPV))","log_Xicc_IPCHI2_OWNPV","","F")
     loader.AddVariable("TMath::ACos(Xicc_DIRA_OWNPV)","acos_Xicc_DIRA_OWNPV","","F")
     loader.AddVariable("log(TMath::Max(10e-10,Xicc_FDCHI2_OWNPV))","log_Xicc_FDCHI2_OWNPV","","F")
     loader.AddVariable("Lc_ENDVERTEX_CHI2/Lc_ENDVERTEX_NDOF","Lc_ENDVERTEX_CHI2_NDOF","","F")
     loader.AddVariable("Xicc_ENDVERTEX_CHI2/Xicc_ENDVERTEX_NDOF","Xicc_ENDVERTEX_CHI2_NDOF","","F")
     loader.AddVariable("Xicc_CHI2NDOF_DTF_PV","Xicc_CHI2NDOF_DTF_PV","","F")
     loader.AddVariable("log(TMath::Max(10e-10,TMath::Min(TMath::Min(Lc_IPCHI2_OWNPV,XiccK_IPCHI2_OWNPV),TMath::Min(XiccPi1_IPCHI2_OWNPV,XiccPi2_IPCHI2_OWNPV))))","log_min_Xicc_Daughters_IPCHI2_OWNPV","","F")
     loader.AddVariable("XiccK_PT + Lc_PT + XiccPi1_PT + XiccPi2_PT","sum_Xicc_Daughters_PT","","F")
     loader.AddVariable("TMath::Min(TMath::Min(XiccK_PT,Lc_PT),TMath::Min(XiccPi1_PT,XiccPi2_PT))","min_Xicc_Daughters_PT","","F")
     loader.AddVariable("TMath::Min(TMath::Min(LcK_PT,LcPi_PT),LcP_PT)","min_Lc_Daughters_PT","","F")

     
     
loader.AddSpectator("Xicc_M", "F") 
loader.AddSpectator("Lc_M", "F")

cut = "(abs(Xicc_TRUEID)==4422&&abs(Lc_TRUEID)==4122&&abs(LcP_TRUEID)==2212&&abs(LcPi_TRUEID)==211&&abs(LcK_TRUEID)==321&&(abs(LcP_MC_MOTHER_ID)==4122||abs(LcP_MC_GD_MOTHER_ID)==4122)&&(abs(LcK_MC_MOTHER_ID)==4122||abs(LcK_MC_GD_MOTHER_ID)==4122)&&(abs(LcPi_MC_MOTHER_ID)==4122||abs(LcPi_MC_GD_MOTHER_ID)==4122)&&abs(XiccPi1_TRUEID)==211&&abs(XiccPi1_MC_MOTHER_ID)==4422&&abs(XiccPi2_TRUEID)==211&&abs(XiccPi2_MC_MOTHER_ID)==4422&&abs(XiccK_TRUEID)==321&&abs(XiccK_MC_MOTHER_ID)==4422)"

# define signal and background trees
tree_s_cut = tree_s.CopyTree(cut)
loader.AddSignalTree(tree_s_cut)
if tree=='rec':
     tree_b_cut = tree_b.CopyTree("","",1000000,0)
     # print(len(tree_b_cut))
     loader.AddBackgroundTree(tree_b_cut)
else :
     loader.AddBackgroundTree(tree_b)



# define additional cuts 

## 2017 cuts
# sigCut = ROOT.TCut("abs(Xicc_M-3621)<15&(Lc_M>2270)&(Lc_M<2306)&XiccK_PIDK>-40 & XiccK_IPCHI2_OWNPV<15&XiccPi1_IPCHI2_OWNPV<15&XiccPi2_IPCHI2_OWNPV<15&Lc_IPCHI2_OWNPV<15&Lc_P>30000&Lc_PT>2000") #mass window for Xicc
# bgCut = ROOT.TCut("(Xicc_M>3800)&(Xicc_M<3900)&(Lc_M>2270)&(Lc_M<2306)& XiccK_PIDK>-40& XiccK_IPCHI2_OWNPV<15&XiccPi1_IPCHI2_OWNPV<15&XiccPi2_IPCHI2_OWNPV<15&Lc_IPCHI2_OWNPV<15&Lc_P>30000&Lc_PT>2000") #100MeV sideband and mass window for Lc

# 2016 cuts
sigCut = ROOT.TCut("abs(Xicc_M_DTF_Lc_PV-3621)<15&(Lc_M>2270)&(Lc_M<2306)&XiccK_PIDK>-40") #mass window for Xicc
bgCut = ROOT.TCut("(Xicc_M>3800)&(Xicc_M<3900)&(Lc_M>2270)&(Lc_M<2306)& XiccK_PIDK>-40") #100MeV sideband and mass window for Lc


# set options for trainings
loader.PrepareTrainingAndTestTree(sigCut, 
                                   bgCut, 
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
c1.Print(f"ROC-{tree}.png")
