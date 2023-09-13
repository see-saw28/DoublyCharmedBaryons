from __future__ import print_function

from ROOT import TTree, TChain, TFile, TRandom3, kTRUE, TVector3, gROOT
from ROOT.TObject import kOverwrite


#print
"""
This script is used to remove multiple candidates.
Here, the multiple candidates we try to remove are those that have exactly the same final state tracks, but using them
differently. For example, the K- coming from Lc decay can be swapped with the K- produced directly from Xicc. We refer
to these candidates as track-exchange candidates.

[1]: If two Xicc candidates (strategy the same for more than two candidates) share exact the same final state tracks (checked
using unique track keys), and the tracks are assigned to have the same ID in the two candidates, only one candidate is kept, 
randomly selected among the candidates. 

[2]: If two Xicc candidates have at least one corresponding track (same ID) with different track keys, they are not affected
by multiple candidate removal in this procedure.

[3]: If two Xicc candidates have the same set of final state tracks but with different ID assignments, we also don't
reject any of the two candidates due to this reason. The misID background is expected to small for signal events due to
tight PID cuts and Lc mass window (only relevant for the case of misID involving Lc decay tracks); and the misID background 
is not peaking around signals in our case.

Note [1]: Since two candidate can have different probability to be selected by selections. The implementation of multiple candidate
removal should be done at the end of your selection process.

Note [2]: We should redefine our truth matching for simulation to mimic data, i.e. to let in track-exchange candidates,
by requiring C_TRUEID==C_ID. Previously the exchange-track candidates are removed by asking for correct mother ID for
each track.  In data the track-exchanges are anyhow able to be selected.
"""



rnd = TRandom3()
sameCandsameKey_Count=0
count60=0
count51=0
countAll=0
countAbnormalPID=0
checkCloneCount=0
rnd.SetSeed(0)





def get_pids_keys_trackvs(tree):

    #calculate track vetors
    trackv_LcP = TVector3( tree.LcP_PX, tree.LcP_PY, tree.LcP_PZ)
    trackv_LcK = TVector3( tree.LcK_PX, tree.LcK_PY, tree.LcK_PZ)
    trackv_LcPi = TVector3( tree.LcPi_PX, tree.LcPi_PY, tree.LcPi_PZ)

    trackv_XiccK = TVector3( tree.XiccK_PX, tree.XiccK_PY, tree.XiccK_PZ)
    trackv_XiccPi1 = TVector3( tree.XiccPi1_PX, tree.XiccPi1_PY, tree.XiccPi1_PZ)
    trackv_XiccPi2 = TVector3( tree.XiccPi2_PX, tree.XiccPi2_PY, tree.XiccPi2_PZ)

    #get track vetors
    trackvs =[ trackv_LcP, trackv_LcK, trackv_LcPi,
               trackv_XiccK, trackv_XiccPi1, trackv_XiccPi2 ]

    #get keys
    keys = [ tree.LcP_TRACK_Key, tree.LcK_TRACK_Key,tree.LcPi_TRACK_Key,
             tree.XiccK_TRACK_Key, tree.XiccPi1_TRACK_Key, tree.XiccPi2_TRACK_Key ]

    pids = [ tree.LcP_PIDK, tree.LcK_PIDK,tree.LcPi_PIDK,
             tree.XiccK_PIDK, tree.XiccPi1_PIDK, tree.XiccPi2_PIDK ]


    return pids, keys, trackvs


cloneType_1 = 0
cloneType_2 = 0
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

def generateSavedList(pids, keys, vectors):
    global sameCandsameKey_Count,count60, count51, countAll, countAbnormalPID
    if(len(keys)!=len(vectors)):
        raise Exception("the keys and vectors don't have the same length")
    totCan = len(keys)

    indices =[0]*totCan  #will store the tags of candidates to be removed or not
    cate = 0 #used to discriminant multiple candidates catagories
    for ii in range(totCan-1):
        if indices[ii] !=0:continue #already tested
        cate +=1
        for jj in range(ii+1,totCan):
            if indices[jj] !=0:continue #already tested
            pid1 = pids[ii]
            pid2 = pids[jj]
            key1 = keys[ii]
            key2 = keys[jj]
            vector1 = vectors[ii]
            vector2 = vectors[jj]
            flags1 = [False]*6
            flags2 = [False]*6
            
            # 2016 data is different from 2017 and 2018
            # so they have to be dealed in different ways
            # the difference is that tracks from Lc(P, K, pi) and Xicc(K, pi1, pi2) are from 2 different containers (Turbo and PersisReco)
            # this condition can have the following consequence
            # Result[1]: the track key in 2016 data can't gaurantee two tracks are the identical one, but 2017 and 2018 data can
            #            so the only to check clone track in 2016 is to check the open angle and momentun magnitude between 2 particles.
            # Result[2]: in 2016 data, particles in a candidates can share same track keys, but 2017 and 2018 datda can't
            
            if (SAMPLE==2016):        
                for i in range(6):
                    for j in range(6):
                        if (not flags1[i] and not flags2[j]
                            and checkClone(vector1[i], vector2[j])):
                                flags1[i]=True
                                flags2[j]=True

                                if {i,j} == {1,3} :
                                    print("K swap")
                                elif {i,j} == {4,5} :
                                    print("Xicc Pi swap")
                                
                                elif {i,j} in [{4,2},{2,5}] :
                                    print("Pi swap")

                        elif(not flags1[i] and not flags2[j]
                            and abs(pid1[i]-pid2[j])<1e-6 ):
                            countAbnormalPID+=1
                            # print('PID Abnoraml angle and particle:',vector1[i].Angle(vector2[j]), i,ii,j,jj)


            elif (SAMPLE==2017 or SAMPLE==2018):
                if len(set(key1)) !=6 or len(set(key1)) !=6: 
                    sameCandsameKey_Count+=1
                    raise Exception( "Tracks in the same candidate have the same key, do check!!!")

                # Number of particles have different keys
                # The following code can be simpler, but here the redundant code is to have some statistical inforation about  duplication
                # Case[1]: 2 candidates have exactly the same 6 track keys
                # Case[2]: 2 candidates have 5 same track keys but the remained tracks can be clone tracks
                # Case[3]:  2 candidates have less than 5 same track keys but the remained tracks can be clone tracks
                # the result is that: case[1] is the majority, and case[2][3] are the minority
                SetDifferenceNum = len(set(key1).difference(set(key2)))
                if (SetDifferenceNum==0): 
                    flags1 = [True]*6
                    flags2 = [True]*6
                    count60+=1         

                elif (SetDifferenceNum==1):
                    for i in range(6):
                        for j in range(6):
                            if (not flags1[i] and not flags2[j]
                                and key1[i]== key2[j]):
                                flags1[i]=True
                                flags2[j]=True
                    
                    for i in range(6):
                        for j in range(6):
                            if (not flags1[i] and not flags2[j]
                                and checkClone(vector1[i], vector2[j])):
                                flags1[i]=True
                                flags2[j]=True
                                count51+=1
                            elif(not flags1[i] and not flags2[j]
                                and abs(pid1[i]-pid2[j])<1e-6 ):
                                countAbnormalPID+=1

                else:
                    for i in range(6):
                        for j in range(6):
                            if (not flags1[i] and not flags2[j]
                                and key1[i]== key2[j]):
                                flags1[i]=True
                                flags2[j]=True
                    
                    for i in range(6):
                        for j in range(6):
                            if (not flags1[i] and not flags2[j]
                                and checkClone(vector1[i], vector2[j])):
                                    flags1[i]=True
                                    flags2[j]=True
                            elif(not flags1[i] and not flags2[j]
                                and abs(pid1[i]-pid2[j])<1e-6 ):
                                countAbnormalPID+=1
                                continue


            if(flags1.count(True)!=flags2.count(True)):
                raise Exception("The flags are not same")
            elif(flags1.count(True)==6):
                indices[ii] = cate
                indices[jj] = cate
                countAll+=1      
    # print(flags1,flags2)
    # print(key1,key2)
    print(indices)
    #print indices              
    result = {}
    for ii in range(totCan):
        cat = indices[ii]
        if not cat in result.keys():
            result[cat] = [ii]  #need the index for this candidate
        else:
            result[cat].append(ii)
    for key,val in result.items():
        if key ==0:continue #no duplicate candidate
        else:
            total_dup = len(val)
            selected = rnd.Integer(total_dup)
            #print selected,total_dup
            indices[val[selected]]  = 0  #force it zero, i.e. no duplicate cadidate
    #print indices
    return [ii for ii in range(totCan) if indices[ii]==0]


years = [2016]#,2017,2018]
baryons = ["Xiccp"]#,"Omegaccp"]

for baryon in baryons :
    for SAMPLE in years :

        mychain = TChain("DecayTree")



        path = f"/eos/lhcb/user/p/pgaigne/MC/26266050/MC-{SAMPLE}-26266050-MCMatch-Lc-clone.root"
        path = "/eos/lhcb/user/p/pgaigne/job388-Xiccp3800-MC-2017-MD-AllOptions-0-clone.root "
        
        # path = f"/eos/lhcb/user/p/pgaigne/job428-Xicc-MC-2016-MU-0-clone.root"
        # path = f"/eos/lhcb/user/p/pgaigne/STEP3/{SAMPLE}/MC/{baryon}st-MC-{SAMPLE}-MCMatch-clone.root"
        # path = f"/eos/lhcb/user/p/pgaigne/STEP3/{SAMPLE}/WS/{baryon}st-WS-{SAMPLE}-Xicc-Lc-Loose-clone.root"
        path = f"/eos/lhcb/user/p/pgaigne/STEP2/RetrainedNtuples/Xiccpp-Data-{SAMPLE}-Lc-clone.root "

        mychain.Add(path)

        tree_temp = mychain

        tree_temp.SetName("temp")

        name = path.split('.')[0]
        outputFilename = name+ '-duplicate1.root'
        fn=TFile(outputFilename,"recreate")
        newtree = tree_temp.CloneTree(0)
        newtree.SetName("DecayTree")

        total_entries = tree_temp.GetEntries()
        print(total_entries)

        from array import array
        sumCandidates = array("i",[1])
        newtree.Branch("sumCandidates",sumCandidates,"sumCandidates/I")



        preRun, preEvt = -1, -1
        processed = 0
        NewEvent = -1                  # starting entry for each event
        category = [0,0,0]
        selected_candidate_list = []  # for each event
        totalCandidates = 1           # for each event
        for jentry in range(total_entries):
            processed +=1

            if not(processed%10000):
                    print(f'Event {processed} of {total_entries}')

            tree_temp.GetEntry(jentry) #tree_temp.LoadTree(jentry)



            selected_indices = [NewEvent+ii for ii in selected_candidate_list]
            if jentry in selected_indices:
                newtree.Fill()


            if jentry <= NewEvent+totalCandidates-1: # if still within the same event, skip the following processes
                continue

            # If we are here, it means we are at the first candidate of each event, so let's reset the tags
            selected_candidate_list=[]
            totalCandidates = 1
            NewEvent = -1


            preRun, preEvt = tree_temp.runNumber, tree_temp.eventNumber

            trk_pid_temp, trk_key_temp, trk_vector_temp = get_pids_keys_trackvs(tree_temp)

            trk_pids = [trk_pid_temp]
            trk_keys = [trk_key_temp] #separate ID types to avoid testing misID backgrounds
            trk_vectors = [trk_vector_temp]

            tree_temp.GetEntry(jentry+1)
            if preRun!=tree_temp.runNumber or preEvt != tree_temp.eventNumber or jentry+1 == total_entries: #already the next/last event (and another candidate)
                tree_temp.GetEntry(jentry)
                sumCandidates[0] = 1
                newtree.Fill()
                continue
            else: #the same event but another candidate
                NewEvent = jentry
                trk_pid_temp, trk_key_temp, trk_vector_temp = get_pids_keys_trackvs(tree_temp)

                trk_pids.append(trk_pid_temp)
                trk_keys.append(trk_key_temp)
                trk_vectors.append(trk_vector_temp)
                
                for nCan in range(2,10000): #large enough to include all candidates in the same event
                    if jentry+nCan>=total_entries:break
                    tree_temp.GetEntry(jentry+nCan)
                    if preRun!=tree_temp.runNumber or preEvt != tree_temp.eventNumber: #stop if next event
                        break
                    else:
                        trk_pid_temp, trk_key_temp, trk_vector_temp = get_pids_keys_trackvs(tree_temp)

                        trk_pids.append(trk_pid_temp)
                        trk_keys.append(trk_key_temp)
                        trk_vectors.append(trk_vector_temp)
            #Now we get a new list of keys for each candidate in the same event, test them to throw duplicate candidates
            #and we get the indices of candidates selected
            print(preEvt,len(trk_keys))
            selected_candidate_list = generateSavedList(trk_pids, trk_keys, trk_vectors)
            totalCandidates = len(trk_keys)
            sumCandidates[0] = len(selected_candidate_list)
            #print jentry,len(trk_keys), len(selected_candidate_list), trk_keys, selected_candidate_list,"\n"
            category[0] += len(trk_keys)
            category[1] += len(selected_candidate_list)
            category[2] += 1.
            # print(trk_keys)
            # print(preEvt,len(selected_candidate_list))
            if 0 in selected_candidate_list:
                tree_temp.GetEntry(jentry)
                newtree.Fill()


        newtree.Write("",kOverwrite)
        print(path)
        print( "total candidates in the tree: ",tree_temp.GetEntries(),processed,newtree.GetEntries())
        print( "total events with multiple candidates", category[2])
        print( "total multiple candidates", category[0])
        print( "removed candidates", category[0]-category[1])
        print("countAll: %d, countAbnormalPID: %d"%(countAll, countAbnormalPID))
        print("magFrac:%f\nclone tracks have close mag: %d \nclone tracks have different mag: %d"%(magFrac, cloneType_2, cloneType_1) )
