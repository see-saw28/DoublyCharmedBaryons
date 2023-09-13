import ROOT

ROOT.gROOT.SetBatch(True)

def draw(fin,matrix,output):
    f1 = ROOT.TFile(fin)
    hs = f1.Get("dataset-Xicc/"+matrix)

    ROOT.gStyle.SetPalette(55)
    ROOT.gStyle.SetPadBottomMargin(0.18)
    ROOT.gStyle.SetPadLeftMargin(0.20)
    ROOT.gStyle.SetPadRightMargin(0.12)

    c1 = ROOT.TCanvas('c1','c1')
    c1.SetGrid()

    hs.Draw("COL TEXT Z")
    hs.SetTitle("")
    hs.GetXaxis().SetLabelSize(0.03)
    hs.GetYaxis().SetLabelSize(0.03)

    c1.SaveAs(output)

draw("TMVAout-Xicc.root","CorrelationMatrixS","CorrelationMatrixS.pdf")
draw("TMVAout-Xicc.root","CorrelationMatrixB","CorrelationMatrixB.pdf")
