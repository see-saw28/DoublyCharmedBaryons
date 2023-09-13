from ROOT import TFile, TTree, TList

pathList = ["/eos/lhcb/user/p/pgaigne/Xiccpst-MC-2016-XiccMVA-cut.root"]

pathList = ["/eos/lhcb/user/p/pgaigne/STEP3/2016/WS/Xiccpst-WS-2016.root"]
 
for path in pathList:
    print(f"Applying cut on file {path}")
    outputDir ="/eos/lhcb/user/p/pgaigne/STEP3/2016/WS/"
    name = path.split('/')[-1].split('.')[0]
    outputFilename = outputDir + name + '-cut-Loose.root'
    outputFile = TFile(outputFilename, 'recreate')   
    inputFile = TFile(path, 'read')
    inputTree = inputFile.Get('tuple_sel_Xiccp_WS/DecayTree')
    # inputTree = inputFile.Get('DecayTree')
    
    outputFile.cd()
    # newtree = inputTree.CopyTree("BDT>0")
    cut = "(abs(Pi_TRUEID)==211&abs(Pi_MC_MOTHER_ID)==4412&abs(Xicc_TRUEID)==4422&abs(Xicc_MC_MOTHER_ID)==4412&abs(Lc_TRUEID)==4122&abs(LcP_TRUEID)==2212&abs(LcPi_TRUEID)==211&abs(LcK_TRUEID)==321&(abs(LcP_MC_MOTHER_ID)==4122|abs(LcP_MC_GD_MOTHER_ID)==4122)&(abs(LcK_MC_MOTHER_ID)==4122|abs(LcK_MC_GD_MOTHER_ID)==4122)&(abs(LcPi_MC_MOTHER_ID)==4122|abs(LcPi_MC_GD_MOTHER_ID)==4122)&abs(XiccPi1_TRUEID)==211&abs(XiccPi1_MC_MOTHER_ID)==4422&abs(XiccPi1_MC_GD_MOTHER_ID)==4412&abs(XiccPi2_TRUEID)==211&abs(XiccPi2_MC_MOTHER_ID)==4422&abs(XiccPi2_MC_GD_MOTHER_ID)==4412&abs(XiccK_TRUEID)==321&abs(XiccK_MC_MOTHER_ID)==4422&abs(XiccK_MC_GD_MOTHER_ID)==4412) "
    # newtree = inputTree.CopyTree(cut+"& BDT_Xicc>0.06")
    newtree = inputTree.CopyTree("abs(Xicc_M_DTF_Lc_PV-3621)<15 & abs(Lc_M-2288)<18  & Xicc_TMVA_BDTXicc>0.06")
    
    print(newtree.GetEntries(),'/', inputTree.GetEntries())
    outputFile.Write()
    outputFile.Close()