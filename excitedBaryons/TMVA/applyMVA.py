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



#path = "/afs/cern.ch/user/p/pgaigne/xiccpp/Xicc/MC/job26-CombDVntuple-full-evts.root"

# baryon = "Xiccpst"
baryon = "Omegaccpst"

XiccMVAcut = 'Loose'
# XiccMVAcut = 'Tight'


paths = ["/eos/lhcb/user/p/pgaigne/STEP3/2017/RS/Xiccpst-RS-2017.root",
         "/eos/lhcb/user/p/pgaigne/STEP3/2018/RS/Xiccpst-RS-2018.root"]

paths = [f"/eos/lhcb/user/p/pgaigne/STEP3/Run2/{baryon}-RS-Run2-Lc-Loose-clone-duplicate.root"]

outputDir = './'
outputDir ="/eos/lhcb/user/p/pgaigne/"




for path in paths :
     # open input file, get trees, create output file
     file1 = ROOT.TFile(path)


     theTree = file1.Get("DecayTree")
          # tree_s = tree_b.CopyTree("Lc_M>2280 && Lc_M<2306")

     name = path.split('.')[0]
     
     outputFilename = name + f'-{XiccMVAcut}-MVA.root'
     
     
     ofile   = ROOT.TFile(outputFilename, 'RECREATE')
     outTree = theTree.CloneTree(0)


     reader = ROOT.TMVA.Reader("!Color:!Silent")
     
     #reader variables 
     # rlog_C_IPCHI2_OWNPV = array.array('f',[0])
     rlog_C_ENDVERTEX_CHI2_NDOF = array.array('f',[0])
     rC_PT = array.array('f',[0])
     rlog_Pi_IPCHI2_OWNPV = array.array('f',[0])
     rPi_ProbNNpi = array.array('f',[0])
     rPi_ProbNNk = array.array('f',[0])
     rPi_PT = array.array('f',[0])
     rK_PT = array.array('f',[0])
     # rXicc_IPCHI2_OWNPV = array.array('f',[0])
     # rXicc_PT = array.array('f',[0])

     # add discriminating variables for training
     # reader.AddVariable("log(TMath::Max(10e-10,C_IPCHI2_OWNPV))", rlog_C_IPCHI2_OWNPV)
     reader.AddVariable("log(TMath::Max(10e-10,C_ENDVERTEX_CHI2/C_ENDVERTEX_NDOF))",rlog_C_ENDVERTEX_CHI2_NDOF)
     reader.AddVariable("C_PT",rC_PT)
     reader.AddVariable("log(Pi_IPCHI2_OWNPV)",rlog_Pi_IPCHI2_OWNPV)  
     
     if baryon == "Xiccpst" :
          reader.AddVariable("Pi_ProbNNpi",rPi_ProbNNpi)
          reader.AddVariable("Pi_PT",rPi_PT)   

     elif baryon == "Omegaccpst" :
          reader.AddVariable("Pi_ProbNNk",rPi_ProbNNk)
          reader.AddVariable("C_KaonDTF_K_PT",rK_PT)

     # reader.AddVariable("Xicc_IPCHI2_OWNPV",rXicc_IPCHI2_OWNPV)  
     # reader.AddVariable("Xicc_PT",rXicc_PT)
          

     rC_M = array.array('f',[0])
     rXicc_M = array.array('f',[0])
     rLc_M = array.array('f',[0])

     reader.AddSpectator("C_M", rC_M)
     reader.AddSpectator("Xicc_M_DTF_Lc_PV", rXicc_M)
     reader.AddSpectator("Lc_M", rLc_M)

     #variables for branches
     
     C_ENDVERTEX_CHI2 = array.array('d',[0])
     C_ENDVERTEX_NDOF = array.array('l',[0])
     # C_IPCHI2_OWNPV = array.array('d',[0])
     C_PT = array.array('d',[0])
     Pi_IPCHI2_OWNPV = array.array('d',[0])
     Pi_ProbNNpi = array.array('d',[0])
     Pi_PT = array.array('d',[0])
     Pi_ProbNNk = array.array('d',[0])
     C_KaonDTF_K_PT = array.array('d',[0])
     # Xicc_IPCHI2_OWNPV = array.array('d',[0])
     # Xicc_PT = array.array('d',[0])

     # add discriminating variables for training
     theTree.SetBranchAddress("C_ENDVERTEX_CHI2", C_ENDVERTEX_CHI2)
     theTree.SetBranchAddress("C_ENDVERTEX_NDOF",C_ENDVERTEX_NDOF)
     # theTree.SetBranchAddress("C_IPCHI2_OWNPV",C_IPCHI2_OWNPV)
     theTree.SetBranchAddress("C_PT",C_PT)
     theTree.SetBranchAddress("Pi_IPCHI2_OWNPV",Pi_IPCHI2_OWNPV)
     theTree.SetBranchAddress("Pi_ProbNNpi",Pi_ProbNNpi)
     theTree.SetBranchAddress("Pi_ProbNNk",Pi_ProbNNk)
     theTree.SetBranchAddress("Pi_PT",Pi_PT)
     theTree.SetBranchAddress("C_KaonDTF_K_PT",C_KaonDTF_K_PT)
     # theTree.SetBranchAddress("Xicc_IPCHI2_OWNPV",Xicc_IPCHI2_OWNPV)
     # theTree.SetBranchAddress("Xicc_PT",Xicc_PT)
     

     # define signal and background trees
     reader.BookMVA("BDT", f"/afs/cern.ch/user/p/pgaigne/excitedBaryons/TMVA/dataset-{baryon}-{XiccMVAcut}/weights/TMVAClassification_BDT.weights.xml")
     reader.BookMVA("BDTG", f"/afs/cern.ch/user/p/pgaigne/excitedBaryons/TMVA/dataset-{baryon}-{XiccMVAcut}/weights/TMVAClassification_BDTG.weights.xml")
     reader.BookMVA("MLP", f"/afs/cern.ch/user/p/pgaigne/excitedBaryons/TMVA/dataset-{baryon}-{XiccMVAcut}/weights/TMVAClassification_MLP.weights.xml")
    
     nbEvents = theTree.GetEntries()

     # if '2016' in path :
     #      YEAR = 2016
     # elif '2017' in path :
     #      YEAR = 2017
     # elif '2018' in path :
     #      YEAR = 2018

     bdt = array.array('f',[0])
     bdtg = array.array('f',[0])
     mlp = array.array('f',[0])
     # year = array.array('l',[0])

     outTree.Branch("BDT", bdt, "BDT_Xicc/F")
     outTree.Branch("BDTG", bdtg, "BDTG/F")
     outTree.Branch("MLP", mlp, "MLP/F")
     # outTree.Branch("year", year, "year/L")

     outTree.Branch("C_ENDVERTEX_CHI2_NDOF", rlog_C_ENDVERTEX_CHI2_NDOF, "log_C_ENDVERTEX_CHI2_NDOF/F")
          


     for i in range(0, nbEvents):
          theTree.GetEntry(i)


          # rlog_C_IPCHI2_OWNPV[0] = np.log(C_IPCHI2_OWNPV[0])
          rlog_C_ENDVERTEX_CHI2_NDOF[0] = np.log(C_ENDVERTEX_CHI2[0]/C_ENDVERTEX_NDOF[0])
          rC_PT[0] = C_PT[0]
          rlog_Pi_IPCHI2_OWNPV[0] = np.log(Pi_IPCHI2_OWNPV[0])
          rPi_ProbNNpi[0] = Pi_ProbNNpi[0]
          rPi_ProbNNk[0] = Pi_ProbNNk[0]
          rPi_PT[0] = Pi_PT[0]
          rK_PT[0] = C_KaonDTF_K_PT[0]
          # rXicc_IPCHI2_OWNPV[0] = Xicc_IPCHI2_OWNPV[0]
          # rXicc_PT[0] =  Xicc_PT[0]
          
          # print(rLc_ENDVERTEX_CHI2_NDOF,rXicc_ENDVERTEX_CHI2_NDOF,Lc_ENDVERTEX_NDOF,Xicc_ENDVERTEX_NDOF)

          BDT = reader.EvaluateMVA("BDT")
          BDTG = reader.EvaluateMVA("BDTG")
          MLP = reader.EvaluateMVA("MLP")

          # print(BDT)

          bdt[0] = BDT
          bdtg[0] = BDTG
          mlp[0] = MLP
          # year[0] = YEAR

          # if BDT>-5:
          #      outTree.Fill()

          outTree.Fill()


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

