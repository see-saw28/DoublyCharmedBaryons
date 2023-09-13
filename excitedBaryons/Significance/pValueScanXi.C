#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "TMath.h"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "RooPolynomial.h"
#include "RooAbsReal.h"
#include "TCanvas.h"
#include "RooPlot.h"
#include "RooExponential.h"
#include "RooCBShape.h"
#include "RooChebychev.h"
#include "RooAddPdf.h"
#include "RooGenericPdf.h"
#include "TCanvas.h"
#include "TTree.h"
#include "TCut.h"
#include "TFile.h"
#include "TAxis.h"
#include  "RooHist.h"
#include "TLatex.h"
//#include <string>
#include <sstream>
#include <fstream>
#include <utility>
#include "TStyle.h"
#include "TROOT.h"

#include <TH1D.h>
#include <TFile.h>
#include "../MassFit/RooCustomPdfs/RooDSCBShape.cxx"
#include "../MassFit/RooCustomPdfs/lhcbStyle.C"

using namespace RooFit ;

void pValueScanXi(){

  lhcbStyle();

  TString filepath_Run2 = "/eos/lhcb/user/p/pgaigne/STEP3/Run2/Xiccpst-RS-Run2-Lc-Loose-clone-duplicate-Tight-MVA-delta.root";
//   TString filepath_2017 = "/nfs/users/dbobulska/Xiccp_studies/2017/Data/signal_channel/RS/hlt2_inclusive_line/TMVAoutput/Data_2017_Xicc_RS_TMVAapplication_allMVAmethods_moreBranches_OverlapRemoved_afterMVA_MLP.root";
//   TString filepath_2018 = "/nfs/users/dbobulska/Xiccp_studies/2018/Data/signal_channel/RS/hlt2_inclusive_line/TMVAoutput/Data_2018_Xicc_RS_TMVAapplication_allMVAmethods_moreBranches_OverlapRemoved_afterMVA_MLP.root";

  TFile *myfileRun2= new TFile(filepath_Run2,"READ");
//   TFile *myfile2017= new TFile(filepath_2017,"READ");
//   TFile *myfile2018= new TFile(filepath_2018,"READ");
  TTree *mytreeRun2= (TTree*)myfileRun2->Get("DecayTree");
//   TTree *mytree2017= (TTree*)myfile2017->Get("DecayTree");
//   TTree *mytree2018= (TTree*)myfile2018->Get("DecayTree");

  TCut selection = "abs(Xicc_M_DTF_Lc_PV-3621)<15 & MLP>0.24"; //MLP>0.18


  TFile *newfile = new TFile("temp.root","RECREATE");

  TTree *newtreeRun2 = mytreeRun2->CopyTree(selection);
//   TTree *newtree2017 = mytree2017->CopyTree(selection);
//   TTree *newtree2018 = mytree2018->CopyTree(selection);

  TList *list = new TList;
  list->Add(newtreeRun2);
//   list->Add(newtree2017);
//   list->Add(newtree2018);
  TTree *newtree = TTree::MergeTrees(list);

  RooRealVar x("DeltaM_Xicc","m_{inv} (MeV/c^{2})",0,500);
  RooDataSet data("data","m_{inv} (MeV/c^{2})",x,Import(*newtree));

  RooRealVar mu("mu","mu",0.,500.);
  RooRealVar sig1("sig1","sig1",6.,5.5,6.5);
  RooRealVar sig2("sig2","sig2",1.5,1.0,5.0);
  RooRealVar a1("alpha","alpha",1.5,0.,10.);
  RooRealVar n1("n","n",1.5,0.,5.);
  RooRealVar a2("alpha2","alpha2",6.5,0.,10.);
  RooRealVar n2("n2","n2",6.5,0.,10.);
  RooRealVar frac("frac","fraction of component 1 in signal",0.3,0.,1.) ;

  Double_t Gen_sigma1 = 5.95; 
  Double_t Gen_sigma2 = 7.5; //1.51
  Double_t Gen_alpha1 = 1.21;
  Double_t Gen_alpha2 = 1.04;
  Double_t Gen_n1 = 3.76;
  Double_t Gen_n2 = 6.66;
  Double_t Gen_frac = 0.138;
  Int_t bkg_expected = newtree->GetEntries("DeltaM_Xicc > 0. & DeltaM_Xicc < 500.");

  sig1.setVal(Gen_sigma1);
  sig1.setConstant(kTRUE);
  sig2.setVal(Gen_sigma2);
  sig2.setConstant(kTRUE);
  a1.setVal(Gen_alpha1);
  a1.setConstant(kTRUE);
  a2.setVal(Gen_alpha2);
  a2.setConstant(kTRUE);  
  n1.setVal(Gen_n1);
  n1.setConstant(kTRUE);
  n2.setVal(Gen_n2);
  n2.setConstant(kTRUE);
  frac.setVal(Gen_frac);
  frac.setConstant(kTRUE);

  // --- Build DSCB PDF ---
  RooDSCBShape signal("crystalBall", "crystalBall", x, mu, sig2, a1, n1, a2, n2);
  RooGaussian gausian("gausian", "gausian", x, mu, sig1);
  // RooAddPdf signal("signal","signal",RooArgList(gausian,crystalBall),frac);

  // background PDFs
 // --- Build User background PDF ---
 RooRealVar slope("slope","SLO",0.002,-0.01,0.01);
 RooRealVar power("power","EXP",0.415,0.,1.);
 RooGenericPdf bkg("bkg","BKG", "TMath::Power(x,power)*exp(-x*slope)",RooArgSet(x, slope, power)) ;


  RooRealVar nsig("nsig","#signal events",0.,-1000.,1000.);
  RooRealVar nbkg("nbkg","#background events",bkg_expected,bkg_expected*0.5,bkg_expected*1.5);

  RooExtendPdf esig("esig", "esig", signal, nsig);
  RooExtendPdf ebkg("esbkg", "esbkg", bkg, nbkg);
  RooAddPdf model("model","sig+bkg", RooArgSet(esig, ebkg));
  RooAddPdf bkgmodel("bmodel","bkgonly", RooArgSet(ebkg));

  Double_t mMin = 5.;
  Double_t mMax = 495.;
  Double_t mStep = 1.;

  Int_t nBins = (mMax-mMin)/mStep;
  Double_t fixedMass[nBins], qValues[nBins], pValues[nBins];
  RooFitResult* resultBkg;
  RooFitResult* resultSigBkg;

  Double_t pMin = 1.;
  Double_t massMin;
  Double_t SLOPE;
  Double_t POWER;

  for(Int_t iBin = 0; iBin<nBins; iBin++) {
    fixedMass[iBin] = mMin+iBin*mStep;
    mu.setVal(fixedMass[iBin]);
    mu.setConstant(kTRUE);
    resultBkg = bkgmodel.fitTo(data,Extended(),Save());
    resultSigBkg = model.fitTo(data,Extended(),Save());
    if (nsig.getVal() >= 0.) {
      qValues[iBin] = 2.*(resultBkg->minNll() - resultSigBkg->minNll());
    }
    else {
      qValues[iBin] = -2.*(resultBkg->minNll() - resultSigBkg->minNll());
    }
    if (qValues[iBin] >= 0.) {
      pValues[iBin] = 0.5*(1. - TMath::Erf(sqrt(qValues[iBin]/2.)));
    }
    else {
      pValues[iBin] = 0.5*(1. + TMath::Erf(sqrt(-1.*qValues[iBin]/2.)));
    }

    if (pValues[iBin] < pMin){
      pMin = pValues[iBin];
      massMin = fixedMass[iBin];
      SLOPE = slope.getValV();
      POWER = power.getValV();
    }
  }
  
  TCanvas *c1 = new TCanvas("c1", "Local p-value", 600, 400);
  c1->SetLogy();
  TGraph *graphPvalues = new TGraph(nBins, fixedMass, pValues);
  graphPvalues->SetLineColor(kBlue);
  graphPvalues->Draw("AC");
  graphPvalues->GetHistogram()->SetTitle("");
  graphPvalues->GetHistogram()->GetXaxis()->SetTitle("#it{m} (#it{#Xi_{cc}^{++}#pi^{-}}) (MeV/#it{c}^{2})");
  graphPvalues->GetHistogram()->GetYaxis()->SetTitle("local #it{p}-value");
  graphPvalues->GetHistogram()->GetXaxis()->SetRangeUser(mMin,mMax-1.);
  graphPvalues->GetHistogram()->GetYaxis()->SetRangeUser(5e-4,1.2);

  Double_t valXAxisSigma[] = {mMin, mMax-1.};
  Double_t val1Sigma[] = {RooStats::SignificanceToPValue(1.), RooStats::SignificanceToPValue(1.)}; //0.15866
  Double_t val2Sigma[] = {RooStats::SignificanceToPValue(2.), RooStats::SignificanceToPValue(2.)};   //0.02275
  Double_t val3Sigma[] = {RooStats::SignificanceToPValue(3.), RooStats::SignificanceToPValue(3.)}; //0.00135
  Double_t val4Sigma[] = {RooStats::SignificanceToPValue(4.), RooStats::SignificanceToPValue(4.)}; //3.167e-05
  Double_t val5Sigma[] = {RooStats::SignificanceToPValue(5.), RooStats::SignificanceToPValue(5.)}; //2.8665e-07

  TGraph *gr1Sigma = new TGraph(2, valXAxisSigma, val1Sigma);
  gr1Sigma->SetLineColor(kRed);
  gr1Sigma->SetLineStyle(2);
  TGraph *gr2Sigma = new TGraph(2, valXAxisSigma, val2Sigma);
  gr2Sigma->SetLineColor(kRed);
  gr2Sigma->SetLineStyle(2);
  TGraph *gr3Sigma = new TGraph(2, valXAxisSigma, val3Sigma);
  gr3Sigma->SetLineColor(kRed);
  gr3Sigma->SetLineStyle(2);
  TGraph *gr4Sigma = new TGraph(2, valXAxisSigma, val4Sigma);
  gr4Sigma->SetLineColor(kRed);
  gr4Sigma->SetLineStyle(2);
  TGraph *gr5Sigma = new TGraph(2, valXAxisSigma, val5Sigma);
  gr5Sigma->SetLineColor(kRed);
  gr5Sigma->SetLineStyle(2);

  gr1Sigma->Draw("same");
  gr2Sigma->Draw("same");
  gr3Sigma->Draw("same");
  // gr4Sigma->Draw("same");
  // gr5Sigma->Draw("same");

  gPad->Update();
  Double_t s1 = (log10(RooStats::SignificanceToPValue(1.)) - gPad->GetY1())/(gPad->GetY2()-gPad->GetY1());
  Double_t s2 = (log10(RooStats::SignificanceToPValue(2.)) - gPad->GetY1())/(gPad->GetY2()-gPad->GetY1());
  Double_t s3 = (log10(RooStats::SignificanceToPValue(3.)) - gPad->GetY1())/(gPad->GetY2()-gPad->GetY1());
  Double_t s4 = (log10(RooStats::SignificanceToPValue(4.)) - gPad->GetY1())/(gPad->GetY2()-gPad->GetY1());
  Double_t s5 = (log10(RooStats::SignificanceToPValue(5.)) - gPad->GetY1())/(gPad->GetY2()-gPad->GetY1());

  TLatex ltxLines;
  ltxLines.SetTextColor(kRed);
  ltxLines.DrawLatexNDC(0.955, s1-0.02,  "1#sigma");
  ltxLines.DrawLatexNDC(0.955, s2-0.02,  "2#sigma");
  ltxLines.DrawLatexNDC(0.955, s3-0.02,  "3#sigma");
  // ltxLines.DrawLatexNDC(0.955, s4-0.02,  "4#sigma");
  // ltxLines.DrawLatexNDC(0.955, s5-0.02,  "5#sigma");

  c1->SaveAs("pValuePlotRS_Xi_Tight.pdf");
  ofstream textfilePvalues;
  textfilePvalues.open("PvaluesXi_Tight.txt"); 
 
 
  for (Int_t iBin = 0; iBin<nBins; iBin++) {
    textfilePvalues << fixedMass[iBin] << " " << pValues[iBin]<< "\n";
    
  }

  textfilePvalues.close();
  printf("(default trigger set, L0 TIS TOS) min p-value %f for mass %f\n",pMin,massMin);
  
  ofstream textfileMass;
  textfileMass.open("massXi_Tight.txt");
  textfileMass << massMin;
  textfileMass.close();


// plot minimal value fit

  Int_t binWidth = 5;

  // slope.setVal(SLOPE);
  // power.setVal(POWER);
  mu.setVal(massMin);
  mu.setConstant(kTRUE);
  resultSigBkg = model.fitTo(data,Extended(),Save());

  printf("N signal %f for mass %f\n",nsig.getValV(),massMin);

  RooPlot * mframe = x.frame();
  RooPlot *frame2 = x.frame();
  data.plotOn(mframe,Name("dataset"),Binning(trunc(round(500/binWidth))));
  model.plotOn(mframe,Name("bkgmodel"),Components("bkg"),LineStyle(kDashed),LineColor(kGreen));
  model.plotOn(mframe,Name("signalmodel"),Components("crystalBall"),LineStyle(kDashed),LineColor(kRed));
  model.plotOn(mframe,Name("combinedmodel"));


  TCanvas *c1_Data = new TCanvas("c1_Data", "", 800, 600);
  c1_Data->Divide(1, 2, 0, 0, 0);
  c1_Data->cd(2);
  gPad->Update();
  //gPad-> SetLogy();
  gPad->SetTopMargin(0);
  gPad->SetLeftMargin(0.15);
  gPad->SetRightMargin(0.05);
  gPad->SetPad(0.02, 0.02, 0.95, 0.77);
  //mframe->SetTitle("");
  //mframe->SetMaximum(mframe->GetMaximum()*1.4);
  mframe->Draw();

  //TLatex *myLatex = new TLatex(0.5,0.5,"");
  //myLatex->SetTextFont(132);
  //myLatex->SetTextColor(1);
  //myLatex->SetTextSize(0.06);
  //myLatex->SetNDC(kTRUE);
  //myLatex->SetTextAlign(11);
  //myLatex->SetTextSize(0.055);

  //myLatex->DrawLatex(0.65, 0.8,"LHCb Preliminary");
  mframe->GetXaxis()->SetTitle("#Delta M [MeV/c^{2}]");
  char str[100];
  sprintf(str, "Candidates / %d (MeV/c^{2})", binWidth);
  mframe->GetYaxis()->SetTitle(str);

  data.plotOn(frame2, Name("dataHist"),MarkerSize(0.8), DataError(RooAbsData::SumW2));
  // signal.plotOn(frame2, LineColor(kRed));
  model.plotOn(frame2, LineColor(kBlue));

  c1_Data->cd(1);
  gPad->SetTopMargin(0);
  gPad->SetLeftMargin(0.15);
  gPad->SetRightMargin(0.05);
  gPad->SetPad(0.02, 0.76, 0.95, 0.97);
  RooHist* hpull1   = frame2->pullHist();
  RooPlot* mframeh1 = x.frame(Title(" "));
  //RooPlot* mframeh1 = m.frame();
  hpull1->SetFillColor(15);
  hpull1->SetFillStyle(3144);
  mframeh1->addPlotable(hpull1, "L3");
  mframeh1->GetYaxis()->SetNdivisions(505);
  //mframeh1->GetYaxis()->SetLabelSize(0.15);
  mframeh1->SetMinimum(-5.0);
  mframeh1->SetMaximum(5.0);
  mframeh1->Draw();


  c1_Data->SaveAs("pScan_XiccPi_fit_RS_Tight.pdf");


}
