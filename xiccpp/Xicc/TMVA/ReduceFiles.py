from ROOT import TFile, TTree, TList

pathList = ["/eos/lhcb/user/p/pgaigne/job38-CombDVntuple-full-evts-0.root",
            "/eos/lhcb/user/p/pgaigne/job38-CombDVntuple-full-evts-1.root",
			"/eos/lhcb/user/p/pgaigne/job38-CombDVntuple-full-evts-2.root"]

pathList = ["/eos/lhcb/user/p/pgaigne/Collision-2016-MU-Xicc-job38-MVA.root ",
            "/eos/lhcb/user/p/pgaigne/Collision-2016-MD-Xicc-job30-MVA.root "]

pathList = ["/eos/lhcb/user/p/pgaigne/MC/26266050/job63-CombDVntuple-Xicc-MC-2016-MD.root",
            "/eos/lhcb/user/p/pgaigne/MC/26266050/job64-CombDVntuple-Xicc-MC-2016-MU.root"]

pathList = ["/eos/lhcb/user/p/pgaigne/job67-CombDVntuple-full-evts-0.root",
            "/eos/lhcb/user/p/pgaigne/job67-CombDVntuple-full-evts-1.root",
            "/eos/lhcb/user/p/pgaigne/job67-CombDVntuple-full-evts-2.root",
            "/eos/lhcb/user/p/pgaigne/job67-CombDVntuple-full-evts-3.root",
            "/eos/lhcb/user/p/pgaigne/job67-CombDVntuple-full-evts-4.root"]


pathList = ["/eos/lhcb/user/p/pgaigne/job74-DV-Xiccpp-Collision-2016-MD-0.root",
            "/eos/lhcb/user/p/pgaigne/job74-DV-Xiccpp-Collision-2016-MD-1.root",
            "/eos/lhcb/user/p/pgaigne/job75-DV-Xiccpp-Collision-2016-MU-0.root",
            "/eos/lhcb/user/p/pgaigne/job75-DV-Xiccpp-Collision-2016-MU-1.root",
            "/eos/lhcb/user/p/pgaigne/job110-DV-Xiccpp-Collision-2018-MD-0.root",
            "/eos/lhcb/user/p/pgaigne/job111-DV-Xiccpp-Collision-2018-MU-0.root",]

pathList = ["/eos/lhcb/user/p/pgaigne/job78-DV-Xiccpp-Collision-2017-MD-0.root",
            "/eos/lhcb/user/p/pgaigne/job80-DV-Xiccpp-Collision-2017-MU-0.root"]


#pathList = ["/eos/lhcb/user/p/pgaigne/job66-CombDVntuple-full-evts-4.root"]
 
for path in pathList:
    print(f"Reducing file {path}")
    outputDir ="/eos/lhcb/user/p/pgaigne/"
    name = path.split('/')[-1].split('.')[0]
    outputFilename = outputDir + name + '-reduced.root'
    outputFile = TFile(outputFilename, 'recreate')   
    inputFile = TFile(path, 'read')
    inputTree = inputFile.Get('tuple_sel_rec/DecayTree')
    # inputTree.SetName("tuple_sel_rec")
    Lumitree = inputFile.Get("GetIntegratedLuminosity/LumiTuple")

    inputTree.SetBranchStatus("*",0)
    inputTree.SetBranchStatus("Xicc_IPCHI2_OWNPV", 1)
    inputTree.SetBranchStatus("Xicc_DIRA_OWNPV",1)
    inputTree.SetBranchStatus("Xicc_FDCHI2_OWNPV",1)
    inputTree.SetBranchStatus("Lc_ENDVERTEX_CHI2",1)
    inputTree.SetBranchStatus("Lc_ENDVERTEX_NDOF",1)
    inputTree.SetBranchStatus("Xicc_ENDVERTEX_CHI2",1)
    inputTree.SetBranchStatus("Xicc_ENDVERTEX_NDOF",1)
    inputTree.SetBranchStatus("Xicc_CHI2NDOF_DTF_PV",1)
    inputTree.SetBranchStatus("LcP_PIDp",1)
    inputTree.SetBranchStatus("LcK_PIDK",1)
    inputTree.SetBranchStatus("LcPi_PIDK",1)
    inputTree.SetBranchStatus("XiccK_PIDK",1)
    inputTree.SetBranchStatus("XiccPi1_PIDK",1)
    inputTree.SetBranchStatus("XiccPi2_PIDK",1)
    inputTree.SetBranchStatus("Lc_PT",1)
    inputTree.SetBranchStatus("XiccPi1_PT",1)
    inputTree.SetBranchStatus("XiccPi2_PT",1)
    inputTree.SetBranchStatus("XiccK_PT",1)
    inputTree.SetBranchStatus("LcPi_PT",1)
    inputTree.SetBranchStatus("LcP_PT",1)
    inputTree.SetBranchStatus("LcK_PT",1)
    inputTree.SetBranchStatus("Lc_P",1)
    inputTree.SetBranchStatus("XiccPi1_P",1)
    inputTree.SetBranchStatus("XiccPi2_P",1)
    inputTree.SetBranchStatus("XiccK_P",1)
    inputTree.SetBranchStatus("LcPi_P",1)
    inputTree.SetBranchStatus("LcP_P",1)
    inputTree.SetBranchStatus("LcK_P",1)
    inputTree.SetBranchStatus("Lc_IPCHI2_OWNPV",1)
    inputTree.SetBranchStatus("XiccK_IPCHI2_OWNPV", 1)
    inputTree.SetBranchStatus("XiccPi1_IPCHI2_OWNPV",1)
    inputTree.SetBranchStatus("XiccPi2_IPCHI2_OWNPV",1)
    inputTree.SetBranchStatus("Xicc_M",1)
    inputTree.SetBranchStatus("Xicc_M_DTF",1)
    inputTree.SetBranchStatus("Xicc_M_DTF_Lc",1)
    inputTree.SetBranchStatus("Xicc_M_DTF_PV",1)
    inputTree.SetBranchStatus("Xicc_M_DTF_Lc_PV",1)
    inputTree.SetBranchStatus("Lc_M",1)
    inputTree.SetBranchStatus("Polarity",1)
    # inputTree = inputFile.Get('DecayTree')
    outputFile.cd()
    newtree = inputTree.CloneTree()
    newtreelumi = Lumitree.CloneTree()
    outputFile.Write()
    outputFile.Close()