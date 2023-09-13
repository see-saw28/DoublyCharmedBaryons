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

pathList = ["/eos/lhcb/user/p/pgaigne/STEP3/2016/WS/Xiccpst-WS-2016-Xicc-Lc-Loose-clone-duplicate.root",
            "/eos/lhcb/user/p/pgaigne/STEP3/2016/WS/Omegaccpst-WS-2016-Xicc-Lc-Loose-clone-duplicate.root"]


#pathList = ["/eos/lhcb/user/p/pgaigne/job66-CombDVntuple-full-evts-4.root"]
 
for path in pathList:
    print(f"Reducing file {path}")
    outputDir ="/eos/lhcb/user/p/pgaigne/STEP3/2016/WS/"
    name = path.split('/')[-1].split('.')[0]
    outputFilename = outputDir + name + '-reduced.root'
    outputFile = TFile(outputFilename, 'recreate')   
    inputFile = TFile(path, 'read')
    inputTree = inputFile.Get('DecayTree')
    # inputTree.SetName("tuple_sel_rec")
    # Lumitree = inputFile.Get("GetIntegratedLuminosity/LumiTuple")

    inputTree.SetBranchStatus("C_KaonDTF_K_ID",0)
    
    # inputTree = inputFile.Get('DecayTree')
    outputFile.cd()
    newtree = inputTree.CloneTree()
    # newtreelumi = Lumitree.CloneTree()
    outputFile.Write()
    outputFile.Close()