#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
os.environ['ZFIT_DISABLE_TF_WARNINGS'] = '1'
# numpy is used for generating, storing, and plotting data
import numpy as np
import pandas
import uproot

# in order to visualise the results of the computation, we use matplotlib
import matplotlib as mpl

import matplotlib.pyplot as plt
import mplhep
plt.style.use(mplhep.style.LHCb2)
plt.rcParams['text.usetex'] = True
#plt.rcParams['figure.dpi'] = 50
# for histograms boost has an easy api and is very fast
import hist
# for statistical distributions we can use a lot from scipy
from scipy import stats

import ROOT
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import mplhep as hep
plt.style.use(hep.style.LHCb2)

ROOT.gROOT.SetBatch(True)


# ## File import, data processing
#  

# In[2]:


#Data used for training
path = "/eos/lhcb/user/p/pgaigne/STEP3/Run2/Xiccpst-WS-Run2-Lc-Loose-clone-duplicate.root"
with uproot.open(path) as file:
    Xiccp_WS = file['DecayTree']
    branches_we_want = ["C_M","Xicc_M_DTF_Lc_PV","Pi_M","C_M_DTF_Xicc_PV","Xicc_TMVA_BDTXicc"] 
    Xiccp_WS_data = Xiccp_WS.arrays(expressions = branches_we_want, library='pd')
    

    
#Data used for training
path = "/eos/lhcb/user/p/pgaigne/STEP3/Run2/Omegaccpst-WS-Run2-Lc-Loose-clone-duplicate.root"
with uproot.open(path) as file:
    Omegaccp_WS = file['DecayTree']
    branches_we_want = ["C_M","Xicc_M_DTF_Lc_PV","C_KaonDTF_C_M","C_M_DTF_Xicc_PV","Xicc_TMVA_BDTXicc"] 
    Omegaccp_WS_data = Omegaccp_WS.arrays(expressions = branches_we_want, library='pd')  
    


    
# xicc_bkg_data = pandas.concat([xicc_bkg_data1, xicc_bkg_data2])


# ## Cut selection

# In[3]:


Omegaccp_WS_data_cut_10 = Omegaccp_WS_data.query("abs(Xicc_M_DTF_Lc_PV-3621)<15 & C_KaonDTF_C_M-4115.1<12 & C_KaonDTF_C_M-4115.1>8")
Omegaccp_WS_data_cut_50 = Omegaccp_WS_data.query("abs(Xicc_M_DTF_Lc_PV-3621)<15 & C_KaonDTF_C_M-4115.1<52 & C_KaonDTF_C_M-4115.1>48")
Xiccp_WS_data_cut_10 = Xiccp_WS_data.query("abs(Xicc_M_DTF_Lc_PV-3621)<15 & C_M_DTF_Xicc_PV-3761<12 & C_M_DTF_Xicc_PV-3761>8")
Xiccp_WS_data_cut_50 = Xiccp_WS_data.query("abs(Xicc_M_DTF_Lc_PV-3621)<15 & C_M_DTF_Xicc_PV-3761<52 & C_M_DTF_Xicc_PV-3761>48")


print(len(Xiccp_WS_data_cut_10),len(Xiccp_WS_data_cut_50),len(Omegaccp_WS_data_cut_10),len(Omegaccp_WS_data_cut_50))


# In[9]:


for bkg in [10,50]:

    for tree in ['Xiccpst-Loose','Xiccpst-Tight','Omegaccpst-Loose','Omegaccpst-Tight'] :
        
        if 'Xicc' in tree :
            WS = Xiccp_WS_data.query(f"abs(Xicc_M_DTF_Lc_PV-3621)<15 & C_M_DTF_Xicc_PV-3761<{bkg+2} & C_M_DTF_Xicc_PV-3761>{bkg-2}")
        elif 'Omega' in tree :
            WS = Omegaccp_WS_data.query(f"abs(Xicc_M_DTF_Lc_PV-3621)<15 & C_KaonDTF_C_M-4115.1<{bkg+2} & C_KaonDTF_C_M-4115.1>{bkg-2}")
        
        if 'Loose' in tree :
            B0 = len(WS) 
        elif 'Tight' in tree :
            B0 = len(WS.query("Xicc_TMVA_BDTXicc>0.17"))

        
        f1 = ROOT.TFile(f"/afs/cern.ch/work/p/pgaigne/MVA/TMVAout-{tree}.root")

        mva_names = ['BDT', 'BDTG', 'MLP']

        histS = []
        histB = []
        minX = []
        maxX = []

        for mva in mva_names :
            histS.append(f1.Get(f"dataset-{tree}/Method_{mva[:3]}/{mva}/MVA_{mva}_effS"))
            histB.append(f1.Get(f"dataset-{tree}/Method_{mva[:3]}/{mva}/MVA_{mva}_effB"))

            minX.append(histS[-1].GetXaxis().GetXmin())
            maxX.append(histS[-1].GetXaxis().GetXmax())

        minCut = -1
        maxCut = 1
        nbBinPlot = 10000
        nbBin = 101
        stepBin = int(nbBinPlot/nbBin)


        maxSignificances = np.zeros(len(mva_names))
        optCuts = np.zeros(len(mva_names))
        optCutEffs = np.zeros(len(mva_names))

        cuts = np.linspace(minCut,maxCut,nbBin)

        significances = np.zeros((len(mva_names),nbBin))

        for i,cut in enumerate(cuts):
            for k in range(len(mva_names)):

                
                j = int((cut-minX[k])*nbBinPlot/(maxX[k]-minX[k]))

                if j<0 :
                    effB, effS = 1,1
                    binCenter = 0

                elif j<nbBinPlot:
                    effS = histS[k].GetBinContent(histS[k].GetXaxis().FindBin(cut))
                    effB = histB[k].GetBinContent(histB[k].GetXaxis().FindBin(cut))
                    

                else :
                    effB, effS = 1,0


                B = effB * B0

                punzi = effS/(3/2+np.sqrt(B))
                significances[k,i] = punzi

                if punzi > maxSignificances[k] :
                    maxSignificances[k] = punzi
                    optCuts[k] = cut
                    optCutEffs[k] = effS
            #fomcurve.SetBinContent(i*stepBin, significance)

        print(tree)
        print(f"Backround at {bkg}MeV :", B0)
        for i,mva in enumerate(mva_names):
            print(f'{mva} : Maximimum signal significance of {maxSignificances[i]:.4E} for a cut of {optCuts[i]:.3f} with a {optCutEffs[i]:.2f} signal efficiency')







        color=iter(cm.rainbow(np.linspace(0,1,len(mva_names))))
        for i,mva in enumerate(mva_names):
            c=next(color)
            #plt.errorbar(MVAcuts,fom[i],fom_err[i],[1/400.]*201,"o",c=c,label=mva_var[i][4:]+' (max {:0.2e})'.format(max(fom[i])))
            plt.errorbar(cuts,significances[i],np.zeros(nbBin),[1/(2*nbBin)]*nbBin,"o",c=c,label=mva,markersize=5.)

        bestCut = optCuts[np.argmax(maxSignificances)]
        plt.axvline(x=bestCut)
        plt.text(bestCut, -maxSignificances[0]/5, f"{mva_names[np.argmax(maxSignificances)]} $>$ {bestCut:.3f}")
        plt.legend(loc='best')
        plt.title(f'FoM ({tree})')
        plt.xlabel('MVA cut')
        plt.ylabel('F(t)')
        axes = plt.gca()
        axes.set_xlim([minCut,maxCut])

        plt.savefig(f"fom_punzi/fom-punzi-{tree}-{bkg}.png",bbox_inches="tight")
        plt.close()
    








# In[ ]:




