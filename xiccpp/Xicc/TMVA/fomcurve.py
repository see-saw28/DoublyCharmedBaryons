#!/usr/bin/env python
import ROOT
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import mplhep as hep
plt.style.use(hep.style.LHCb2)

ROOT.gROOT.SetBatch(True)

tree='rec-SB-diff'

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

#fomcurve = ROOT.TH1F("fomcurve","FoM optimisation", nbBinPlot, minCut, maxCut )



Cwindow = 100/30

#Background coef in sidebands 3800 < Xicc_M < 3900 and 2270 < Lc_M < 2306
#2016 data
numB_data = 3960864 
# 2016+2018 data
numB_data = 6793280
#run2 data
numB_data = 8890038

#nb bkg in SB after selection and BDT = 0.0
numB_0 = 49047
effB = 0.0041971527
numB_data = numB_0/effB

# 26266050 rec tree
numS_MC = 7048
# 26266050 rec tree
numS_MC = 3051 

# #BDTcut = 0.16 2016+2018 WS
# numS_data = 1351
# eff_MC = 0.48

#BDTcut = 0.2 2016+2018 SB
numS_data = 1251
eff_MC = 0.456

#BDTcut = 0.2 Run2 SB-diff
numS_data = 1499
eff_MC = 0.45217144

#BDTcut = 0.07 Run2 SB-diff
numS_data = 2488
eff_MC = 0.76181102

Cmcdata = numS_MC*eff_MC/numS_data

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
            binCenter = histS[k].GetBinCenter(j)
            effS = histS[k].GetBinContent(j)
            effB = histB[k].GetBinContent(j)

        else :
            effB, effS = 1,0

        newS = effS * numS_data / eff_MC
        newB = effB * numB_data / Cwindow

        significance = newS/np.sqrt(newS + newB)
        significances[k,i] = significance

        if significance > maxSignificances[k] :
            maxSignificances[k] = significance
            optCuts[k] = binCenter
            optCutEffs[k] = effS
    #fomcurve.SetBinContent(i*stepBin, significance)

    
for i,mva in enumerate(mva_names):
    print(f'{mva} : Maximimum signal significance of {maxSignificances[i]:.2f} for a cut of {optCuts[i]:.3f} with a {optCutEffs[i]:.2f} signal efficiency')

print(f'Effective number of bkg events : {numB_data / Cwindow} and signal events : {numS_MC / Cmcdata}')





color=iter(cm.rainbow(np.linspace(0,1,len(mva_names))))
for i,mva in enumerate(mva_names):
  c=next(color)
  #plt.errorbar(MVAcuts,fom[i],fom_err[i],[1/400.]*201,"o",c=c,label=mva_var[i][4:]+' (max {:0.2e})'.format(max(fom[i])))
  plt.errorbar(cuts,significances[i],np.zeros(nbBin),[1/(2*nbBin)]*nbBin,"o",c=c,label=mva,markersize=5.)

bestCut = optCuts[np.argmax(maxSignificances)]
plt.axvline(x=bestCut)
# plt.text(bestCut, -5, f"{bestCut:.2f}")
plt.legend(loc='best')
plt.title('FoM')
plt.xlabel('MVA cut')
plt.ylabel('Significance $S/\sqrt{S+B}$')
axes = plt.gca()
axes.set_xlim([minCut,maxCut])
plt.savefig(f"fom-{tree}.png",bbox_inches="tight")
plt.close()

# ROOT.gStyle.SetPalette(55)
# ROOT.gStyle.SetPadBottomMargin(0.18)
# ROOT.gStyle.SetPadLeftMargin(0.20)
# ROOT.gStyle.SetPadRightMargin(0.12)

# c1 = ROOT.TCanvas('c1','c1')
# c1.SetGrid()

# fomcurve.Draw("COL TEXT Z")
# fomcurve.SetTitle("")
# fomcurve.GetXaxis().SetLabelSize(0.03)
# fomcurve.GetYaxis().SetLabelSize(0.03)

# c1.Print("fomcurve.png")




