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

void massFitOmega(){

  lhcbStyle();

  TString filepath_Run2 = "/eos/lhcb/user/p/pgaigne/STEP3/Run2/Omegaccpst-RS-Run2-Lc-Loose-clone-duplicate-Loose-MVA-delta.root";
//   TString filepath_2017 = "/nfs/users/dbobulska/Xiccp_studies/2017/Data/signal_channel/RS/hlt2_inclusive_line/TMVAoutput/Data_2017_Xicc_RS_TMVAapplication_allMVAmethods_moreBranches_OverlapRemoved_afterMVA_MLP.root";
//   TString filepath_2018 = "/nfs/users/dbobulska/Xiccp_studies/2018/Data/signal_channel/RS/hlt2_inclusive_line/TMVAoutput/Data_2018_Xicc_RS_TMVAapplication_allMVAmethods_moreBranches_OverlapRemoved_afterMVA_MLP.root";

  TFile *myfileRun2= new TFile(filepath_Run2,"READ");
//   TFile *myfile2017= new TFile(filepath_2017,"READ");
//   TFile *myfile2018= new TFile(filepath_2018,"READ");
  TTree *mytreeRun2= (TTree*)myfileRun2->Get("DecayTree");
//   TTree *mytree2017= (TTree*)myfile2017->Get("DecayTree");
//   TTree *mytree2018= (TTree*)myfile2018->Get("DecayTree");

  TCut selection = "abs(Xicc_M_DTF_Lc_PV-3621)<15 & MLP>0.22";


  TFile *newfile = new TFile("temp.root","RECREATE");

  TTree *newtreeRun2 = mytreeRun2->CopyTree(selection);
//   TTree *newtree2017 = mytree2017->CopyTree(selection);
//   TTree *newtree2018 = mytree2018->CopyTree(selection);

  TList *list = new TList;
  list->Add(newtreeRun2);
//   list->Add(newtree2017);
//   list->Add(newtree2018);
  TTree *newtree = TTree::MergeTrees(list);

  RooRealVar x("DeltaM_Omega","m_{inv} (MeV/c^{2})",0,500);

  
  RooDataSet data("data","m_{inv} (MeV/c^{2})",x,Import(*newtree));

  RooRealVar mu("mu","mu",0.,500.);
  RooRealVar sig1("sig1","sig1",6.,1.,10.);
  RooRealVar sig2("sig2","sig2",1.5,1.,10.);
  RooRealVar a1("alpha","alpha",1.5,0.,10.);
  RooRealVar n1("n","n",1.5,0.,5.);
  RooRealVar a2("alpha2","alpha2",6.5,0.,10.);
  RooRealVar n2("n2","n2",6.5,0.,10.);
  RooRealVar frac("frac","fraction of component 1 in signal",0.3,0.,1.) ;

  Double_t Gen_sigma1 = 5.95; 
  Double_t Gen_sigma2 = 5.27; //1.27
  Double_t Gen_alpha1 = 1.561;
  Double_t Gen_alpha2 = 1.254;
  Double_t Gen_n1 = 2.253;
  Double_t Gen_n2 = 3.332;
  Double_t Gen_frac = 0.138;
  Int_t bkg_expected = newtree->GetEntries("DeltaM_Omega > 0. & DeltaM_Omega < 500.");

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
 RooRealVar power("power","EXP",0.27,0.,1.);
 RooGenericPdf bkg("bkg","BKG", "TMath::Power(x,power)*exp(-x*slope)",RooArgSet(x, slope, power)) ;


  RooRealVar nsig("nsig","#signal events",0.,-1000.,1000.);
  RooRealVar nbkg("nbkg","#background events",bkg_expected,bkg_expected*0.5,bkg_expected*1.5);

  RooExtendPdf esig("esig", "esig", signal, nsig);
  RooExtendPdf ebkg("esbkg", "esbkg", bkg, nbkg);
  RooAddPdf model("model","sig+bkg", RooArgSet(esig, ebkg));
  RooAddPdf bkgmodel("bmodel","bkgonly", RooArgSet(ebkg));


  RooFitResult* resultBkg;
  RooFitResult* resultSigBkg;

  Int_t binWidth = 4;
  Double_t massMin = 90;

// plot minimal value fit
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
  // mframe->GetXaxis()->SetTitle("m(#Xi_{cc}^{++} K^{-}) [MeV/c^{2}]");
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


  c1_Data->SaveAs("XiccKfit_RS.pdf");


}
