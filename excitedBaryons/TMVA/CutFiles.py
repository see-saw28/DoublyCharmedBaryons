from ROOT import TFile, TTree, TList

years = [2016,2017,2018]
baryons = ["Xiccpst","Omegaccpst"]

for baryon in baryons :
    for year in years :
        
        path = f"/eos/lhcb/user/p/pgaigne/STEP3/{year}/MC/{baryon}-MC-{year}.root"

        print(f"Applying cut on file {path}")
        name = path.split('.')[0]
        outputDir = f"/eos/lhcb/user/p/pgaigne/STEP3/{year}/MC/"
        # outputFilename = outputDir + name + '-500MeV-Xicc-Lc-Loose.root'
        # outputFilename =outputDir+ f'{baryon}-RS-{year}-Lc-Loose.root'
        outputFilename = name + "-MCMatch.root"
        outputFile = TFile(outputFilename, 'recreate')   
        inputFile = TFile(path, 'read')
        inputTree = inputFile.Get('tuple_sel_Xiccp/DecayTree')
        # inputTree = inputFile.Get('tuple_sel_rec/DecayTree')
        # inputTree = inputFile.Get('DecayTree')
        
        outputFile.cd()
        # newtree = inputTree.CopyTree("BDT>0")
        XiccpCut = "(abs(C_TRUEID)==4412&abs(Pi_TRUEID)==211&abs(Pi_MC_MOTHER_ID)==4412&abs(Xicc_TRUEID)==4422&abs(Xicc_MC_MOTHER_ID)==4412&abs(Lc_TRUEID)==4122&abs(LcP_TRUEID)==2212&abs(LcPi_TRUEID)==211&abs(LcK_TRUEID)==321&(abs(LcP_MC_MOTHER_ID)==4122|abs(LcP_MC_GD_MOTHER_ID)==4122)&(abs(LcK_MC_MOTHER_ID)==4122|abs(LcK_MC_GD_MOTHER_ID)==4122)&(abs(LcPi_MC_MOTHER_ID)==4122|abs(LcPi_MC_GD_MOTHER_ID)==4122)&abs(XiccPi1_TRUEID)==211&abs(XiccPi1_MC_MOTHER_ID)==4422&abs(XiccPi1_MC_GD_MOTHER_ID)==4412&abs(XiccPi2_TRUEID)==211&abs(XiccPi2_MC_MOTHER_ID)==4422&abs(XiccPi2_MC_GD_MOTHER_ID)==4412&abs(XiccK_TRUEID)==321&abs(XiccK_MC_MOTHER_ID)==4422&abs(XiccK_MC_GD_MOTHER_ID)==4412) "
        OmegaccpCut = "(abs(C_TRUEID)==4432&abs(Pi_TRUEID)==321&abs(Pi_MC_MOTHER_ID)==4432&abs(Xicc_TRUEID)==4422&abs(Xicc_MC_MOTHER_ID)==4432&abs(Lc_TRUEID)==4122&abs(LcP_TRUEID)==2212&abs(LcPi_TRUEID)==211&abs(LcK_TRUEID)==321&(abs(LcP_MC_MOTHER_ID)==4122|abs(LcP_MC_GD_MOTHER_ID)==4122)&(abs(LcK_MC_MOTHER_ID)==4122|abs(LcK_MC_GD_MOTHER_ID)==4122)&(abs(LcPi_MC_MOTHER_ID)==4122|abs(LcPi_MC_GD_MOTHER_ID)==4122)&abs(XiccPi1_TRUEID)==211&abs(XiccPi1_MC_MOTHER_ID)==4422&abs(XiccPi1_MC_GD_MOTHER_ID)==4432&abs(XiccPi2_TRUEID)==211&abs(XiccPi2_MC_MOTHER_ID)==4422&abs(XiccPi2_MC_GD_MOTHER_ID)==4432&abs(XiccK_TRUEID)==321&abs(XiccK_MC_MOTHER_ID)==4422&abs(XiccK_MC_GD_MOTHER_ID)==4432)  "
        XiccCut = "abs(Lc_M-2288)<18&(abs(Xicc_TRUEID)==4422&abs(Lc_TRUEID)==4122&abs(LcP_TRUEID)==2212&abs(LcPi_TRUEID)==211&abs(LcK_TRUEID)==321&(abs(LcP_MC_MOTHER_ID)==4122|abs(LcP_MC_GD_MOTHER_ID)==4122)&(abs(LcK_MC_MOTHER_ID)==4122|abs(LcK_MC_GD_MOTHER_ID)==4122)&(abs(LcPi_MC_MOTHER_ID)==4122|abs(LcPi_MC_GD_MOTHER_ID)==4122)&abs(XiccPi1_TRUEID)==211&abs(XiccPi1_MC_MOTHER_ID)==4422&abs(XiccPi2_TRUEID)==211&abs(XiccPi2_MC_MOTHER_ID)==4422&abs(XiccK_TRUEID)==321&abs(XiccK_MC_MOTHER_ID)==4422)"
        if baryon == "Xiccpst":
            newtree = inputTree.CopyTree(XiccpCut + "&"+"abs(Xicc_M_DTF_Lc_PV-3621)<15 & abs(Lc_M-2288)<18  & Pi_ProbNNpi>0.1 & Pi_PT>200 & Xicc_TMVA_BDTXicc>0.07")
        elif baryon == "Omegaccpst":
            newtree = inputTree.CopyTree(OmegaccpCut + "&"+"abs(Xicc_M_DTF_Lc_PV-3621)<15 & abs(Lc_M-2288)<18 & Pi_ProbNNk>0.1 & C_KaonDTF_K_PT>200 & Xicc_TMVA_BDTXicc>0.07")
        # newtree = inputTree.CopyTree("abs(Xicc_M_DTF_Lc_PV-3621)<15 & abs(Lc_M-2288)<18  & Xicc_TMVA_BDTXicc>0.07")
        
        print(newtree.GetEntries(),'/', inputTree.GetEntries())
        outputFile.Write()
        outputFile.Close()