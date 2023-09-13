

from ROOT import TVector3, TChain, TFile
from math import acos
from array import array

years = [2017,2018]#,2017,2018]
baryons = ["Xiccpst","Omegaccpst"]

# years = [2016]
# baryons = ["Xiccp"]#,"Omegaccp"]

for baryon in baryons :
    for year in years :
        path = f"/eos/lhcb/user/p/pgaigne/STEP3/{year}/RS/{baryon}-RS-{year}-Xicc-Lc-Loose.root"
        # path = f"/eos/lhcb/user/p/pgaigne/STEP3/{year}/MC/{baryon}st-MC-{year}-MCMatch.root"
        # path = f"/eos/lhcb/user/p/pgaigne/STEP3/{year}/MC/{baryon}st-MC-{year}.root"
        # path = f"/eos/lhcb/user/p/pgaigne/job388-Xiccp3800-MC-2017-MD-AllOptions-0.root"

        # path = f"/eos/lhcb/user/p/pgaigne/STEP2/RetrainedNtuples/Xiccpp-Data-{year}-Lc.root "
        
        # path = f"/eos/lhcb/user/p/pgaigne/MC/26266050/MC-{year}-26266050-MCMatch-Lc.root"
        # path = "/eos/lhcb/user/p/pgaigne/STEP2/2016/job74-CombDVntuple-Lc_Cuts-SB-3800-3900-Lc.root "
        # path = f"/eos/lhcb/user/p/pgaigne/job428-Xicc-MC-2016-MU-0.root"

        print("Remove clone :",path)

        tbkg1 = TChain("DecayTree")

        tbkg1.Add(path)
        total_entries = tbkg1.GetEntries()

        name = path.split('.')[0]
        outputFilename = name+ '-clone.root'
        nfile = TFile(outputFilename ,"recreate")
        newtree = tbkg1.CloneTree(0)

        # This two new branches are for checking purpose, and have no influnce on the result.
        # If two particles have little PID difference but have a big angle, then they will be denoted as "abnormal"
        # "pidAbnormalType": this branches record the 2 particles in a integer number.
        #  For example, 'pidAbnormalType==35' means LcPi and pi1 are the abnormal couple
        #       -----------------------------------------------------
        #       LcP | LcK  | LcPi  | XiccK  | XiccPi1 | XiccPi2 | Pi
        #       -----------------------------------------------------
        #       1   | 2    | 3     | 4      | 5       | 6       | 7
        #
        pidAbnormalType=array("i",[1]);newtree.Branch("pidAbnormalType",pidAbnormalType,"pidAbnormalType/I")
        pidAbnormalTheta=array("d",[1]);newtree.Branch("pidAbnormalTheta",pidAbnormalTheta,"pidAbnormalTheta/D")



        abnormalCount=0
        abnormalTypeList=[]
        abnormalThetaList=[]


        cloneType_1 = 0 # small angle difference but big amplitude difference
        cloneType_2 = 0 # small angle difference with small amplitude difference, real clone
        # If the angle between two particles are smaller than this angle "drad" (default is 0.5 mrad),
        # and the momentun magnitude have a relative difference smaller "magFrac" (default is 5%),
        # then  they will be denoted as clone
        drad = 0.5/1000. 
        magFrac = 0.05

        def checkClone(TV_A, TV_B, drad = 0.5/1000.):
            global cloneType_1, cloneType_2
            if (TV_A.Angle(TV_B) < drad):
                if(TV_A.Mag()/TV_B.Mag()>1+magFrac or TV_A.Mag()/TV_B.Mag()<1/(1+magFrac)):
                    cloneType_1+=1
                    return False
                else:
                    cloneType_2+=1
                    return True 
            else:
                return False



        for jentry in range(total_entries):

            if not(jentry%10000):
                    print(f'Event {jentry} of {total_entries}')
            tbkg1.GetEntry(jentry)


            vectors = [ TVector3(tbkg1.LcP_PX,tbkg1.LcP_PY,tbkg1.LcP_PZ),
                        TVector3(tbkg1.LcK_PX,tbkg1.LcK_PY,tbkg1.LcK_PZ),
                        TVector3(tbkg1.LcPi_PX,tbkg1.LcPi_PY,tbkg1.LcPi_PZ),
                        TVector3(tbkg1.XiccK_PX,tbkg1.XiccK_PY,tbkg1.XiccK_PZ),
                        TVector3(tbkg1.XiccPi1_PX,tbkg1.XiccPi1_PY,tbkg1.XiccPi1_PZ),
                        TVector3(tbkg1.XiccPi2_PX,tbkg1.XiccPi2_PY,tbkg1.XiccPi2_PZ),
                        TVector3(tbkg1.Pi_PX,tbkg1.Pi_PY,tbkg1.Pi_PZ) 
                        ]


            pidks = [tbkg1.LcP_PIDK,
                    tbkg1.LcK_PIDK,
                    tbkg1.LcPi_PIDK,
                    tbkg1.XiccK_PIDK,
                    tbkg1.XiccPi1_PIDK,
                    tbkg1.XiccPi2_PIDK,
                    tbkg1.Pi_PIDK]
            clone = 0
            pidAbnormalType[0] = 0
            pidAbnormalTheta[0] = 10.
            for i in range(6):
                for j in range(i+1, 7):
                    # clone check
                    if(checkClone(vectors[i], vectors[j])):
                        clone = 1
                        break
                    # abnormal check
                    elif(abs(pidks[i]-pidks[j])<1e-6):
                        pidAbnormalType[0] = (i+1)*10+(j+1)
                        pidAbnormalTheta[0] =vectors[i].Angle(vectors[j])
                        abnormalTypeList.append(pidAbnormalType[0])
                        abnormalThetaList.append(pidAbnormalTheta[0])
                        abnormalCount+=1

                if clone: break

            if not clone: newtree.Fill()

        newtree.Write()


        print("\n=== START printing statistic information about clone==")
        print( "Before : ",tbkg1.GetEntries() )
        print( "After  : ",newtree.GetEntries() )
        print( "Removed clone:", tbkg1.GetEntries()-newtree.GetEntries())
        print("magFrac:%f, clone tracks have close mag: %d \nclone tracks have different mag: %d"%(magFrac, cloneType_2, cloneType_1) )
        print("=== END printing statistic information about clone==")


        print( "\n=== START printing statistic information about the abnormal particles== ")
        if(len(abnormalThetaList)):
            abnormalThetaList.sort()
            print("abnormalCount", abnormalCount)
            print("abnormalTypeList statistic", [[x,abnormalTypeList.count(x)] for x in set(abnormalTypeList)])
            print("abnormal theta: min(%.8f), max(%.8f), mean(%.8f), middle(%.8f)"%( 
                    min(abnormalThetaList), max(abnormalThetaList), sum(abnormalThetaList)/len(abnormalThetaList), abnormalThetaList[int(len(abnormalThetaList)/2 )]) )
        else:
            print('No abnormal find')
        print( "=== END statistic information about the abnormal particles== ")
        print( "Clones are removed")

