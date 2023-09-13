#!/usr/bin/env python

# 
# This example is basically the same as $ROOTSYS/tmva/test/TMVAClassification.C
# 

import ROOT
import numpy as np
# from tqdm import tqdm
import array

# in order to start TMVA
ROOT.TMVA.Tools.Instance()

# note that it seems to be mandatory to have an
# output file, just passing None to TMVA::Factory(..)
# does not work. Make sure you don't overwrite an
# existing file.

tree = 'rec-SB'

#path = "/afs/cern.ch/user/p/pgaigne/xiccpp/Xicc/MC/job26-CombDVntuple-full-evts.root"


paths = [   "/eos/lhcb/user/p/pgaigne/job117-DV-Xiccpst-Collision-2018-MU-0.root",
            "/eos/lhcb/user/p/pgaigne/job117-DV-Xiccpst-Collision-2018-MU-1.root",
            "/eos/lhcb/user/p/pgaigne/job117-DV-Xiccpst-Collision-2018-MU-2.root",
"/eos/lhcb/user/p/pgaigne/job117-DV-Xiccpst-Collision-2018-MU-3.root",
"/eos/lhcb/user/p/pgaigne/job117-DV-Xiccpst-Collision-2018-MU-4.root"]

paths = ["/eos/lhcb/user/p/pgaigne/job126-DV-Xiccpst-Collision-2018-MD-0.root"]

paths = ["/afs/cern.ch/user/p/pgaigne/excitedBaryons/Data/DV_Xiccpst_Collision_2016_MD.root "]

outputDir = './'
outputDir ="/eos/lhcb/user/p/pgaigne/"

for path in paths :
     # open input file, get trees, create output file
     file1 = ROOT.TFile(path)


     theTree = file1.Get("tuple_sel_Xiccp/DecayTree")
          # tree_s = tree_b.CopyTree("Lc_M>2280 && Lc_M<2306")

     name = path.split('/')[-1].split('.')[0]
     
     outputFilename = outputDir + name + '-XiccMVA-cut1.root'
     
     
     ofile   = ROOT.TFile(outputFilename, 'RECREATE')
     outTree = theTree.CloneTree(0)


     reader = ROOT.TMVA.Reader("!Color:!Silent")
     
     #reader variables 
     rlog_Xicc_IPCHI2_OWNPV = array.array('f',[0])
     racos_Xicc_DIRA_OWNPV = array.array('f',[0])
     rlog_Xicc_FDCHI2_OWNPV = array.array('f',[0])
     rLc_ENDVERTEX_CHI2_NDOF = array.array('f',[0])
     rlog_Xicc_ENDVERTEX_CHI2_NDOF = array.array('f',[0])
     rXicc_ENDVERTEX_CHI2_NDOF = array.array('f',[0])
     rlog_Xicc_CHI2NDOF_DTF_PV = array.array('f',[0])
     rXicc_CHI2NDOF_DTF_PV = array.array('f',[0])
     rLcP_PIDp = array.array('f',[0])
     rLcK_PIDK = array.array('f',[0])
     rLcPi_PIDK = array.array('f',[0])
     rXiccK_PIDK = array.array('f',[0])
     rXiccPi1_PIDK = array.array('f',[0])
     rXiccPi2_PIDK = array.array('f',[0])
     rsumPT = array.array('f',[0])
     rminPT = array.array('f',[0])
     rminPT_Lc = array.array('f',[0])
     rminlog_IPCHI2 = array.array('f',[0])
     rLc_PT = array.array('f',[0])
     rXiccPi1_PT = array.array('f',[0])
     rXiccPi2_PT = array.array('f',[0])
     rXiccK_PT = array.array('f',[0])
     rlog_Lc_IPCHI2_OWNPV = array.array('f',[0])
     rlog_XiccK_IPCHI2_OWNPV = array.array('f',[0])
     rlog_XiccPi1_IPCHI2_OWNPV = array.array('f',[0])
     rlog_XiccPi2_IPCHI2_OWNPV = array.array('f',[0])

     # add discriminating variables for training
     reader.AddVariable("log(TMath::Max(10e-10,Xicc_IPCHI2_OWNPV))", rlog_Xicc_IPCHI2_OWNPV)
     reader.AddVariable("TMath::ACos(Xicc_DIRA_OWNPV)",racos_Xicc_DIRA_OWNPV)
     reader.AddVariable("log(TMath::Max(10e-10,Xicc_FDCHI2_OWNPV))",rlog_Xicc_FDCHI2_OWNPV)
     reader.AddVariable("Lc_ENDVERTEX_CHI2/Lc_ENDVERTEX_NDOF",rLc_ENDVERTEX_CHI2_NDOF)
     reader.AddVariable("log(TMath::Max(10e-10,Xicc_ENDVERTEX_CHI2/Xicc_ENDVERTEX_NDOF))",rlog_Xicc_ENDVERTEX_CHI2_NDOF)
     reader.AddVariable("log(TMath::Max(10e-10,Xicc_CHI2NDOF_DTF_PV))",rlog_Xicc_CHI2NDOF_DTF_PV)
     reader.AddVariable("LcP_PIDp",rLcP_PIDp)
     reader.AddVariable("LcK_PIDK",rLcK_PIDK)
     reader.AddVariable("LcPi_PIDK",rLcPi_PIDK)
     reader.AddVariable("XiccK_PIDK",rXiccK_PIDK)
     reader.AddVariable("XiccPi1_PIDK",rXiccPi1_PIDK)
     reader.AddVariable("XiccPi2_PIDK",rXiccPi2_PIDK)
     reader.AddVariable("TMath::Min(TMath::Min(XiccK_PT,Lc_PT),TMath::Min(XiccPi1_PT,XiccPi2_PT))",rminPT)
     reader.AddVariable("Lc_PT",rLc_PT)
     reader.AddVariable("XiccPi1_PT",rXiccPi1_PT)
     reader.AddVariable("XiccPi2_PT",rXiccPi2_PT)
     reader.AddVariable("XiccK_PT",rXiccK_PT)
     reader.AddVariable("log(TMath::Max(10e-10,Lc_IPCHI2_OWNPV))",rlog_Lc_IPCHI2_OWNPV)
     reader.AddVariable("log(TMath::Max(10e-10,XiccK_IPCHI2_OWNPV))", rlog_XiccK_IPCHI2_OWNPV)
     reader.AddVariable("log(TMath::Max(10e-10,XiccPi1_IPCHI2_OWNPV))",rlog_XiccPi1_IPCHI2_OWNPV)
     reader.AddVariable("log(TMath::Max(10e-10,XiccPi2_IPCHI2_OWNPV))",rlog_XiccPi2_IPCHI2_OWNPV)
    
          

     rXicc_M = array.array('f',[0])
     rLc_M = array.array('f',[0])

     reader.AddSpectator("Xicc_M", rXicc_M)
     reader.AddSpectator("Lc_M", rLc_M)

     #variables for branches
     Xicc_IPCHI2_OWNPV = array.array('d',[0])
     Xicc_DIRA_OWNPV = array.array('d',[0])
     Xicc_FDCHI2_OWNPV = array.array('d',[0])
     Lc_ENDVERTEX_CHI2 = array.array('d',[0])
     Xicc_ENDVERTEX_CHI2 = array.array('d',[0])
     Xicc_CHI2NDOF_DTF_PV = array.array('d',[0])
     LcP_PIDp = array.array('d',[0])
     LcK_PIDK = array.array('d',[0])
     LcPi_PIDK = array.array('d',[0])
     XiccK_PIDK = array.array('d',[0])
     XiccPi1_PIDK = array.array('d',[0])
     XiccPi2_PIDK = array.array('d',[0])
     minPT = array.array('d',[0])
     Lc_PT = array.array('d',[0])
     XiccPi1_PT = array.array('d',[0])
     XiccPi2_PT = array.array('d',[0])
     XiccK_PT = array.array('d',[0])
     LcPi_PT = array.array('d',[0])
     LcP_PT = array.array('d',[0])
     LcK_PT = array.array('d',[0])
     Lc_IPCHI2_OWNPV = array.array('d',[0])
     XiccK_IPCHI2_OWNPV = array.array('d',[0])
     XiccPi1_IPCHI2_OWNPV = array.array('d',[0])
     XiccPi2_IPCHI2_OWNPV = array.array('d',[0])
     Lc_ENDVERTEX_NDOF = array.array('l',[0])
     Xicc_ENDVERTEX_NDOF = array.array('l',[0])
     Xicc_M = array.array('d',[0])

     # add discriminating variables for training
     theTree.SetBranchAddress("Xicc_IPCHI2_OWNPV", Xicc_IPCHI2_OWNPV)
     theTree.SetBranchAddress("Xicc_DIRA_OWNPV",Xicc_DIRA_OWNPV)
     theTree.SetBranchAddress("Xicc_FDCHI2_OWNPV",Xicc_FDCHI2_OWNPV)
     theTree.SetBranchAddress("Lc_ENDVERTEX_CHI2",Lc_ENDVERTEX_CHI2)
     theTree.SetBranchAddress("Lc_ENDVERTEX_NDOF",Lc_ENDVERTEX_NDOF)
     theTree.SetBranchAddress("Xicc_ENDVERTEX_CHI2",Xicc_ENDVERTEX_CHI2)
     theTree.SetBranchAddress("Xicc_ENDVERTEX_NDOF",Xicc_ENDVERTEX_NDOF)
     theTree.SetBranchAddress("Xicc_CHI2NDOF_DTF_PV",Xicc_CHI2NDOF_DTF_PV)
     theTree.SetBranchAddress("LcP_PIDp",LcP_PIDp)
     theTree.SetBranchAddress("LcK_PIDK",LcK_PIDK)
     theTree.SetBranchAddress("LcPi_PIDK",LcPi_PIDK)
     theTree.SetBranchAddress("XiccK_PIDK",XiccK_PIDK)
     theTree.SetBranchAddress("XiccPi1_PIDK",XiccPi1_PIDK)
     theTree.SetBranchAddress("XiccPi2_PIDK",XiccPi2_PIDK)
     theTree.SetBranchAddress("Lc_PT",Lc_PT)
     theTree.SetBranchAddress("XiccPi1_PT",XiccPi1_PT)
     theTree.SetBranchAddress("XiccPi2_PT",XiccPi2_PT)
     theTree.SetBranchAddress("XiccK_PT",XiccK_PT)
     theTree.SetBranchAddress("LcPi_PT",LcPi_PT)
     theTree.SetBranchAddress("LcP_PT",LcP_PT)
     theTree.SetBranchAddress("LcK_PT",LcK_PT)
     theTree.SetBranchAddress("Lc_IPCHI2_OWNPV",Lc_IPCHI2_OWNPV)
     theTree.SetBranchAddress("XiccK_IPCHI2_OWNPV", XiccK_IPCHI2_OWNPV)
     theTree.SetBranchAddress("XiccPi1_IPCHI2_OWNPV",XiccPi1_IPCHI2_OWNPV)
     theTree.SetBranchAddress("XiccPi2_IPCHI2_OWNPV",XiccPi2_IPCHI2_OWNPV)
     theTree.SetBranchAddress("Xicc_M",Xicc_M)

     # define signal and background trees
     reader.BookMVA("BDT", f"/afs/cern.ch/user/p/pgaigne/xiccpp/Xicc/TMVA/dataset-{tree}/weights/TMVAClassification_BDT.weights.xml")
     # reader.BookMVA("BDTG", f"dataset-{tree}/weights/TMVAClassification_BDTG.weights.xml")
     # reader.BookMVA("MLP", f"dataset-{tree}/weights/TMVAClassification_MLP.weights.xml")

     # canvas = ROOT.TCanvas("c1","c1", 800, 800)
     # canvas.SetTickx()
     # canvas.SetTicky()
     # canvas.Divide(2,2)
     # histBDT = ROOT.TH1F("MVA_BDT", "MVA_BDT", 100, -0.8, 0.8)

     # mass_before_BDT = ROOT.TH1F("M distribution before cut", "MVA_BDT", 100, 3400, 3800)
     # mass_after_BDT = ROOT.TH1F("M distribution after cut", "MVA_BDT", 100, 3400, 3800)

     nbEvents = theTree.GetEntries()
     print(nbEvents)

     if '2016' in path :
          YEAR = 2016
     elif '2017' in path :
          YEAR = 2017
     elif '2018' in path :
          YEAR = 2018

     bdt = array.array('f',[0])
     # bdtg = array.array('f',[0])
     # mlp = array.array('f',[0])
     year = array.array('l',[0])

     outTree.Branch("BDT_Xicc", bdt, "BDT_Xicc/F")
     # outTree.Branch("BDTG", bdtg, "BDTG/F")
     # outTree.Branch("MLP", mlp, "MLP/F")
     outTree.Branch("year", year, "year/L")

     outTree.Branch("log_Xicc_IPCHI2_OWNPV", rlog_Xicc_IPCHI2_OWNPV, "log_Xicc_IPCHI2_OWNPV/F")
     outTree.Branch("acos_Xicc_DIRA_OWNPV", racos_Xicc_DIRA_OWNPV, "acos_Xicc_DIRA_OWNPV/F")
     outTree.Branch("log_Xicc_FDCHI2_OWNPV", rlog_Xicc_FDCHI2_OWNPV, "log_Xicc_FDCHI2_OWNPV_/F")
     outTree.Branch("Lc_ENDVERTEX_CHI2_NDOF", rLc_ENDVERTEX_CHI2_NDOF, "Lc_ENDVERTEX_CHI2_NDOF/F")
     outTree.Branch("log_Xicc_ENDVERTEX_CHI2_NDOF", rlog_Xicc_ENDVERTEX_CHI2_NDOF, "log_Xicc_ENDVERTEX_CHI2_NDOF/F")
     outTree.Branch("log_Xicc_CHI2NDOF_DTF_PV", rlog_Xicc_CHI2NDOF_DTF_PV, "log_Xicc_CHI2NDOF_DTF_PV/F")
     outTree.Branch("min_Xicc_Daughters_PT", rminPT, "min_Xicc_Daughters_PT/F")
     outTree.Branch("log_Lc_IPCHI2_OWNPV", rlog_Lc_IPCHI2_OWNPV, "log_Lc_IPCHI2_OWNPV/F")
     outTree.Branch("log_XiccK_IPCHI2_OWNPV", rlog_XiccK_IPCHI2_OWNPV, "log_XiccK_IPCHI2_OWNPV/F")
     outTree.Branch("log_XiccPi1_IPCHI2_OWNPV", rlog_XiccPi1_IPCHI2_OWNPV, "log_XiccPi1_IPCHI2_OWNPV/F")
     outTree.Branch("log_XiccPi2_IPCHI2_OWNPV", rlog_XiccPi2_IPCHI2_OWNPV, "log_XiccPi2_IPCHI2_OWNPV/F")

     #extra branches
     outTree.Branch("sum_Xicc_Daughters_PT", rsumPT, "sum_Xicc_Daughters_PT/F")
     outTree.Branch("Xicc_ENDVERTEX_CHI2_NDOF", rXicc_ENDVERTEX_CHI2_NDOF, "Xicc_ENDVERTEX_CHI2_NDOF/F")
          


     for i in range(0, nbEvents):
          theTree.GetEntry(i)
          
          rlog_Xicc_IPCHI2_OWNPV[0] = np.log(max(10e-10,Xicc_IPCHI2_OWNPV[0]))
          racos_Xicc_DIRA_OWNPV[0] = np.arccos(Xicc_DIRA_OWNPV)
          rlog_Xicc_FDCHI2_OWNPV[0] = np.log(max(10e-10,Xicc_FDCHI2_OWNPV[0]))
          rLc_ENDVERTEX_CHI2_NDOF[0] = Lc_ENDVERTEX_CHI2[0]/Lc_ENDVERTEX_NDOF[0]
          # rLc_ENDVERTEX_CHI2_NDOF[0] = 0
          rXicc_ENDVERTEX_CHI2_NDOF[0] = Xicc_ENDVERTEX_CHI2[0]/Xicc_ENDVERTEX_NDOF[0]
          rlog_Xicc_ENDVERTEX_CHI2_NDOF[0] = np.log(max(10e-10,Xicc_ENDVERTEX_CHI2[0]/Xicc_ENDVERTEX_NDOF[0]))
          # rlog_Xicc_ENDVERTEX_CHI2_NDOF[0] = 0

          rXicc_CHI2NDOF_DTF_PV[0] = Xicc_CHI2NDOF_DTF_PV[0]
          rlog_Xicc_CHI2NDOF_DTF_PV[0] = np.log(max(10e-10,Xicc_CHI2NDOF_DTF_PV[0]))
          # rlog_Xicc_CHI2NDOF_DTF_PV[0] = np.log(max(10e-10,Xicc_ENDVERTEX_CHI2[0]/Xicc_ENDVERTEX_NDOF[0]))
          rLcP_PIDp[0] = LcP_PIDp[0]
          rLcK_PIDK[0] = LcK_PIDK[0]
          rLcPi_PIDK[0] = LcPi_PIDK[0]
          rXiccK_PIDK[0] = XiccK_PIDK[0]
          rXiccPi1_PIDK[0] = XiccPi1_PIDK[0]
          rXiccPi2_PIDK[0] = XiccPi2_PIDK[0]
          rminlog_IPCHI2[0] = np.log(max(10e-10,min(min(Lc_IPCHI2_OWNPV,XiccK_IPCHI2_OWNPV),min(XiccPi1_IPCHI2_OWNPV,XiccPi2_IPCHI2_OWNPV))[0]))
          rsumPT[0] = XiccK_PT[0]+Lc_PT[0]+XiccPi1_PT[0]+XiccPi2_PT[0]
          rminPT[0] = min(min(XiccK_PT,Lc_PT),min(XiccPi1_PT,XiccPi2_PT))[0]
          rminPT_Lc[0] = min(min(LcPi_PT,LcP_PT),LcK_PT)[0]
          rLc_PT[0] = Lc_PT[0]
          rXiccPi1_PT[0] = XiccPi1_PT[0]
          rXiccPi2_PT[0] = XiccPi2_PT[0]
          rXiccK_PT[0] = XiccK_PT[0]
          rlog_Lc_IPCHI2_OWNPV[0] = np.log(max(10e-10,Lc_IPCHI2_OWNPV[0]))
          rlog_XiccK_IPCHI2_OWNPV[0] = np.log(max(10e-10,XiccK_IPCHI2_OWNPV[0]))
          rlog_XiccPi1_IPCHI2_OWNPV[0] = np.log(max(10e-10,XiccPi1_IPCHI2_OWNPV[0]))
          rlog_XiccPi2_IPCHI2_OWNPV[0] = np.log(max(10e-10,XiccPi2_IPCHI2_OWNPV[0]))

          
          # print(rLc_ENDVERTEX_CHI2_NDOF,rXicc_ENDVERTEX_CHI2_NDOF,Lc_ENDVERTEX_NDOF,Xicc_ENDVERTEX_NDOF)

          BDT = reader.EvaluateMVA("BDT")
          # BDTG = reader.EvaluateMVA("BDTG")
          # MLP = reader.EvaluateMVA("MLP")

          # print(BDT)

          bdt[0] = BDT
          # bdtg[0] = BDTG
          # mlp[0] = MLP
          year[0] = YEAR

          if BDT>-0.5:
               outTree.Fill()

          # outTree.Fill()


          # if BDT > -0.0 :
          #      mass_after_BDT.Fill(Xicc_M[0])
          # histBDT.Fill(BDT)
          # mass_before_BDT.Fill(Xicc_M[0])

          if not(i%100000):
               print(f'Event {i} of {nbEvents}')


     outTree.AutoSave()
     ofile.Close()

# canvas.cd(1)
# histBDT.Draw()
# canvas.cd(3)
# mass_before_BDT.Draw()
# canvas.cd(4)
# mass_after_BDT.Draw()
# canvas.Print("apply.png")

