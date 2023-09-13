#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "RooPolynomial.h"
#include "RooAbsReal.h"
#include "TCanvas.h"
#include "RooPlot.h"
#include <TH1D.h>
#include <TFile.h>
#include "../../RooCustomPdfs/RooDSCBShape.cxx"
#include "../../RooCustomPdfs/lhcbStyle.C"

using namespace RooFit ;

void ExpoFitCombined(){

  lhcbStyle();

  TString filepath_2016 = "/nfs/users/dbobulska/Xiccp_studies/2016/Data/signal_channel/WSM/hlt2_inclusive_line/TMVAoutput/Data_2016_Xicc_WSM_TMVAapplication_allMVAmethods_moreBranches_OverlapRemoved_afterMVA_MLP.root";
  TString filepath_2017 = "/nfs/users/dbobulska/Xiccp_studies/2017/Data/signal_channel/WSM/hlt2_inclusive_line/TMVAoutput/Data_2017_Xicc_WSM_TMVAapplication_allMVAmethods_moreBranches_OverlapRemoved_afterMVA_MLP.root";
  TString filepath_2018 = "/nfs/users/dbobulska/Xiccp_studies/2018/Data/signal_channel/WSM/hlt2_inclusive_line/TMVAoutput/Data_2018_Xicc_WSM_TMVAapplication_allMVAmethods_moreBranches_OverlapRemoved_afterMVA_MLP.root";

  TFile *myfile2016= new TFile(filepath_2016,"READ");
  TFile *myfile2017= new TFile(filepath_2017,"READ");
  TFile *myfile2018= new TFile(filepath_2018,"READ");
  TTree *mytree2016= (TTree*)myfile2016->Get("DecayTree");
  TTree *mytree2017= (TTree*)myfile2017->Get("DecayTree");
  TTree *mytree2018= (TTree*)myfile2018->Get("DecayTree");

  TCut selection = "Xic_M > 2450. && Xic_M < 2488. && MVA_MLP > 0.905 && PK_angle > 0.0005 && PPi_angle > 0.0005 && PPi1_angle > 0.0005 && "
                   "PPi2_angle > 0.0005 && KPi_angle > 0.0005 && KPi1_angle > 0.0005 && KPi2_angle > 0.0005 && PiPi1_angle > 0.0005 && "
                   "PiPi2_angle > 0.0005 && Pi1Pi2_angle > 0.0005 && "
                   "(Xicc_Y > 2.0 && Xicc_Y < 4.5 && Xicc_PT > 2500. && Xicc_PT < 25000.) && "
                   "(KKpi < 2025 || KKpi > 2060) && (Kpipi < 1850 || Kpipi > 1890) && "
                   "(Xicc_L0HadronDecision_TIS || Xicc_L0MuonDecision_TIS || Xicc_L0DiMuonDecision_TIS || Xicc_L0ElectronDecision_TIS || Xicc_L0PhotonDecision_TIS)";


  TFile *newfile = new TFile("temp.root","RECREATE");

  TTree *newtree2016 = mytree2016->CopyTree(selection);
  TTree *newtree2017 = mytree2017->CopyTree(selection);
  TTree *newtree2018 = mytree2018->CopyTree(selection);

  TList *list = new TList;
  list->Add(newtree2016);
  list->Add(newtree2017);
  list->Add(newtree2018);
  TTree *newtree = TTree::MergeTrees(list);
  TCanvas *c1= new TCanvas ("c1","c1");

  RooRealVar x("DM","m_{inv} (MeV/c^{2})",3400,3800);
  RooDataSet data("data","m_{inv} (MeV/c^{2})",x,Import(*newtree));

  //RooPlot* xframe = x.frame(Title("#Xi_{cc}^{++} -> #Xi_{c}^{+} #pi^{-} #pi^{-}"));
  RooPlot* xframe = x.frame(Title(""));
  data.plotOn(xframe,Name("data"),Binning(40));

  RooRealVar bkg_yield("N_{bkg}","bkg_yield",2000.,1000.,10000.);

  // background PDFs
  // ------- expon ------- //
  RooRealVar lambda("lambda", "slope", 0.001, 0., 0.01);
  RooExponential bkg("bkg", "exponential PDF", x, lambda);
  RooAddPdf model("model","model",RooArgList(bkg),RooArgList(bkg_yield)) ;

  model.fitTo(data,RooFit::PrintLevel(-1));
  model.plotOn(xframe,Name("bkg"),Components(bkg),LineWidth(2),LineColor(kBlue)) ;

/*
  TPaveText *param = new TPaveText(0.12,0.80,0.7,0.65,"blNDC");
  xframe->addObject(param);
  param->AddText(Form("#chi^{2}/ndf = %.2f", xframe->chiSquare(1)));
  param->SetBorderSize(0);
  param->SetFillStyle(0);
  param->SetLineColor(0);
  param->SetTextSize(0.04);
  param->SetTextAlign(11);
*/
  //TLegend *leg = new TLegend(0.58,0.88,0.77,0.65);
  TLegend *leg = new TLegend(0.58,0.93,0.85,0.64);
  leg->SetBorderSize(0);
  leg->AddEntry(xframe->findObject("data"),"WSM data (20\%)","lep");
  leg->AddEntry(xframe->findObject("bkg"),"Exponential fit","L");
  leg->SetTextSize(gROOT->GetStyle("lhcbStyle")->GetTextSize());
  leg->SetTextFont(gROOT->GetStyle("lhcbStyle")->GetTextFont());
  xframe->addObject(leg);
  xframe->GetYaxis()->SetRangeUser(0.,800);
  xframe->GetYaxis()->SetTitle("Candidates / (10 MeV/#it{c}^{2})");
  xframe->SetTitle("");
  xframe->GetXaxis()->SetTitle("");

  RooHist* hresid = xframe->pullHist() ;
  RooPlot* frame2 = x.frame(Title("")) ;
  frame2->addPlotable(hresid) ;

  TCanvas* c = new TCanvas("c","c",1000,1000) ;
  //c->Divide(2) ;

  TPad *pad1 = new TPad("pad1", "pad1", 0, 0.3, 1, 1.0);
  pad1->SetBottomMargin(0.1); // Upper and lower plot are joined
  pad1->Draw();             // Draw the upper pad: pad1
  pad1->cd();               // pad1 becomes the current pad
  xframe->Draw();               // Draw h1

  TLatex lat;
  lat.SetNDC();
  lat.SetTextFont(132);
  lat.SetTextSize(0.06);
  lat.DrawLatex(0.18,0.83,Form("#chi^{2}/ndf = %.2f", xframe->chiSquare("bkg","data",1)));

  c->cd();          // Go back to the main canvas before defining pad2
  TPad *pad2 = new TPad("pad2", "pad2", 0, 0.08, 1, 0.28);
  pad2->SetTopMargin(0.0);
  pad2->SetBottomMargin(0.32);
  pad2->Draw();
  pad2->cd();       // pad2 becomes the current pad

  frame2->Draw();
  frame2->SetTitle("");
  frame2->GetYaxis()->SetTitle("Pulls");
  frame2->GetYaxis()->SetLabelSize(0.17);
  frame2->GetYaxis()->SetTitleSize(0.23);
  frame2->GetYaxis()->SetRangeUser(-4.8,4.8);
  frame2->GetYaxis()->SetNdivisions(5);
  frame2->GetYaxis()->SetTitleOffset(0.28);

  frame2->GetXaxis()->SetTitle("#it{m} (#it{#Xi_{c}^{+}#pi^{-}#pi^{+}}) (MeV/#it{c}^{2})");
  frame2->GetXaxis()->SetLabelSize(0);
  frame2->GetXaxis()->SetTitleSize(0.23);
  frame2->GetXaxis()->SetTitleOffset(0.4);
  frame2->SetFillColor(15) ;
  //frame2->SetFillStyle(3001) ;
  
  printf("lambda is %f ± %f\n",lambda.getVal(),lambda.getError());

  c->SaveAs("Expo_bkg_WSM_combined_L0TIS.pdf");
  RooMsgService::instance().Print();

}
