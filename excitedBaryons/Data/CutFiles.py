from ROOT import TFile, TTree, TList

pathList = ["/eos/lhcb/user/p/pgaigne/Xiccpst-MC-2016-XiccMVA-cut.root"]


baryons = ["Xiccp","Omegaccp"]
# baryon = "Omegaccp"

year = 2017

# pathList = [f"/eos/lhcb/user/p/pgaigne/MC/26266050/MC-2016-26266050.root"]

# pathList = [f"/eos/lhcb/user/p/pgaigne/STEP3/{year}/MC/Omegaccpst-MC-{year}.root"] 

pathList = [f"/eos/lhcb/user/p/pgaigne/STEP3/{year}/Excited-RS-WS-Xiccpp-Data-{year}.root"] 

for path in pathList:
    print(f"Applying cut on file {path}")
    outputDir =f"/eos/lhcb/user/p/pgaigne/STEP3/{year}/RS/"
    # outputDir =f"/eos/lhcb/user/p/pgaigne/MC/26266050/"
    name = path.split('/')[-1].split('.')[0]

    for baryon in baryons :
        print("Generating",baryon,"file")
        outputFilename = outputDir + f'{baryon}st-RS-{year}-Xicc-Lc-Loose.root'
        
        # outputFilename = outputDir + name+ '-MCMatch.root'
        outputFile = TFile(outputFilename, 'recreate')   
        inputFile = TFile(path, 'read')
        inputTree = inputFile.Get('tuple_sel_Xiccp/DecayTree')
        # inputTree = inputFile.Get('tuple_sel_rec/DecayTree')
        # inputTree = inputFile.Get('DecayTree')
        
        outputFile.cd()
        # newtree = inputTree.CopyTree("BDT>0")
        
        if baryon == "Xiccp" :
            #Xiccpst
            newtree = inputTree.CopyTree("abs(Xicc_M_DTF_Lc_PV-3621)<15 & abs(Lc_M-2288)<18  & Pi_ProbNNpi>0.1 & Pi_PT>200 & Xicc_TMVA_BDTXicc>0.07")

        elif baryon == "Omegaccp" :
            #Omegaccpst
            newtree = inputTree.CopyTree("abs(Xicc_M_DTF_Lc_PV-3621)<15 & abs(Lc_M-2288)<18 & Pi_ProbNNk>0.1 & C_KaonDTF_K_PT>200 & Xicc_TMVA_BDTXicc>0.07")
        
        print(newtree.GetEntries(),'/', inputTree.GetEntries())
        outputFile.Write()
        outputFile.Close()