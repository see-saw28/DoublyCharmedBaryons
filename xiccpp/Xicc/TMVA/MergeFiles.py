from ROOT import TFile, TTree, TList

pathList = ["/eos/lhcb/user/p/pgaigne/job38-CombDVntuple-full-evts-0.root",
            "/eos/lhcb/user/p/pgaigne/job38-CombDVntuple-full-evts-1.root",
			"/eos/lhcb/user/p/pgaigne/job38-CombDVntuple-full-evts-2.root"]

pathList = ["/eos/lhcb/user/p/pgaigne/Collision-2016-MU-Xicc-job38-MVA.root ",
            "/eos/lhcb/user/p/pgaigne/Collision-2016-MD-Xicc-job30-MVA.root "]

pathList = ["/eos/lhcb/user/p/pgaigne/MC/26266050/job63-CombDVntuple-Xicc-MC-2016-MD.root",
            "/eos/lhcb/user/p/pgaigne/MC/26266050/job64-CombDVntuple-Xicc-MC-2016-MU.root"]

pathList = ["/eos/lhcb/user/p/pgaigne/job67-CombDVntuple-full-evts-0-reduced.root",
            "/eos/lhcb/user/p/pgaigne/job67-CombDVntuple-full-evts-1-reduced.root",
            "/eos/lhcb/user/p/pgaigne/job67-CombDVntuple-full-evts-2-reduced.root",
            "/eos/lhcb/user/p/pgaigne/job67-CombDVntuple-full-evts-3-reduced.root",
            "/eos/lhcb/user/p/pgaigne/job67-CombDVntuple-full-evts-4-reduced.root"]

pathList = ["/eos/lhcb/user/p/pgaigne/job78-DV-Xiccpp-Collision-2017-MD-0-reduced.root",
            "/eos/lhcb/user/p/pgaigne/job80-DV-Xiccpp-Collision-2017-MU-0-reduced.root"]

treeList = TList()
outputDir ="/eos/lhcb/user/p/pgaigne/"
outputFile = TFile(outputDir+'Collision-2017-Xiccpp-job78-80-reduced.root', 'recreate')
pyFileList = list()
pyTreeList = list()
 
for path in pathList:
	print(f"Merging {path}")
	inputFile = TFile(path)
	pyFileList.append(inputFile)
	# inputTree = inputFile.Get('tuple_sel_rec')
	inputTree = inputFile.Get('DecayTree')
	outputFile.cd()
	outputTree = inputTree.CloneTree()
	pyTreeList.append(outputTree)
	treeList.Add(outputTree)

outputFile.cd()
outputTree = TTree.MergeTrees(treeList) 
# outputTree.SetName("tuple_sel_rec")
outputFile.Write()
outputFile.Close()