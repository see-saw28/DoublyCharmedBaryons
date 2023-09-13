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

void FitSigDSCBGaussAllYears(){

  lhcbStyle();

  TFile *myfile2017 = new TFile("/nfs/users/dbobulska/Xiccp_studies/2017/MC/control_channel_XicpPip/TMVAoutput/MCmatch_2017_TMVAapplication_allMVAmethods_HLT2selNoPID_moreBranches_finalWeight.root","READ");
  TFile *myfile2018 = new TFile("/nfs/users/dbobulska/Xiccp_studies/2018/MC/control_channel_XicpPip/TMVAoutput/MCmatch_2018_TMVAapplication_allMVAmethods_HLT2selNoPID_moreBranches_finalWeight.root","READ");
  TTree *mytree2017 = (TTree*)myfile2017->Get("DecayTree");
  TTree *mytree2018 = (TTree*)myfile2018->Get("DecayTree");

  // L0 TIS
  TCut selection = "Xic_M > 2450. && Xic_M < 2488. && MVA_MLP > 0.97 && PPi_angle > 0.0005 & PPi1_angle > 0.0005 & PiPi1_angle > 0.0005 & PK_angle > 0.0005 & KPi_angle > 0.0005 & KPi1_angle > 0.0005 && "
                   "(KKpi < 2025 || KKpi > 2060) && (Kpipi < 1850 || Kpipi > 1890) && "
                   "Xicc_Y > 2.0 && Xicc_Y < 4.5 && Xicc_PT > 2500. && Xicc_PT < 25000. && "
                   "(Xicc_L0HadronDecision_TIS || Xicc_L0MuonDecision_TIS || Xicc_L0DiMuonDecision_TIS || Xicc_L0ElectronDecision_TIS || Xicc_L0PhotonDecision_TIS)";
  TFile *newfile = new TFile("temp.root","RECREATE");

  Double_t initial_mass = 3621.;

  mytree2017->SetBranchStatus("*",0);
  mytree2017->SetBranchStatus("MVA_MLP",1);
  mytree2017->SetBranchStatus("DM",1);
  mytree2017->SetBranchStatus("Xic_M",1);
  mytree2017->SetBranchStatus("PK_angle",1);
  mytree2017->SetBranchStatus("KPi_angle",1);
  mytree2017->SetBranchStatus("KPi1_angle",1);
  mytree2017->SetBranchStatus("PPi_angle",1);
  mytree2017->SetBranchStatus("PPi1_angle",1);
  mytree2017->SetBranchStatus("PiPi1_angle",1);
  mytree2017->SetBranchStatus("Xic_Hlt2CharmHadXicpToPpKmPipTurboDecision_Dec",1);
  mytree2017->SetBranchStatus("XicP_ProbNNghost",1);
  mytree2017->SetBranchStatus("XicK_ProbNNghost",1);
  mytree2017->SetBranchStatus("XicPi_ProbNNghost",1);
  mytree2017->SetBranchStatus("XiccPi1_PIDK_corr",1);
  mytree2017->SetBranchStatus("XiccPi1_ProbNNghost",1);
  mytree2017->SetBranchStatus("XiccPi1_ProbNNpi",1);
  mytree2017->SetBranchStatus("KKpi",1);
  mytree2017->SetBranchStatus("Kpipi",1);
  mytree2017->SetBranchStatus("Xicc_PT",1);
  mytree2017->SetBranchStatus("Xicc_Y",1);
  mytree2017->SetBranchStatus("Xic_L0HadronDecision_TOS",1);
  mytree2017->SetBranchStatus("Xicc_L0HadronDecision_TIS",1);
  mytree2017->SetBranchStatus("Xicc_L0MuonDecision_TIS",1);
  mytree2017->SetBranchStatus("Xicc_L0DiMuonDecision_TIS",1);
  mytree2017->SetBranchStatus("Xicc_L0ElectronDecision_TIS",1);
  mytree2017->SetBranchStatus("Xicc_L0PhotonDecision_TIS",1);
  mytree2017->SetBranchStatus("final_weight",1);

  mytree2018->SetBranchStatus("*",0);
  mytree2018->SetBranchStatus("MVA_MLP",1);
  mytree2018->SetBranchStatus("DM",1);
  mytree2018->SetBranchStatus("Xic_M",1);
  mytree2018->SetBranchStatus("PK_angle",1);
  mytree2018->SetBranchStatus("KPi_angle",1);
  mytree2018->SetBranchStatus("KPi1_angle",1);
  mytree2018->SetBranchStatus("PPi_angle",1);
  mytree2018->SetBranchStatus("PPi1_angle",1);
  mytree2018->SetBranchStatus("PiPi1_angle",1);
  mytree2018->SetBranchStatus("Xic_Hlt2CharmHadXicpToPpKmPipTurboDecision_Dec",1);
  mytree2018->SetBranchStatus("XicP_ProbNNghost",1);
  mytree2018->SetBranchStatus("XicK_ProbNNghost",1);
  mytree2018->SetBranchStatus("XicPi_ProbNNghost",1);
  mytree2018->SetBranchStatus("XiccPi1_PIDK_corr",1);
  mytree2018->SetBranchStatus("XiccPi1_ProbNNghost",1);
  mytree2018->SetBranchStatus("XiccPi1_ProbNNpi",1);
  mytree2018->SetBranchStatus("KKpi",1);
  mytree2018->SetBranchStatus("Kpipi",1);
  mytree2018->SetBranchStatus("Xicc_PT",1);
  mytree2018->SetBranchStatus("Xicc_Y",1);
  mytree2018->SetBranchStatus("Xic_L0HadronDecision_TOS",1);
  mytree2018->SetBranchStatus("Xicc_L0HadronDecision_TIS",1);
  mytree2018->SetBranchStatus("Xicc_L0MuonDecision_TIS",1);
  mytree2018->SetBranchStatus("Xicc_L0DiMuonDecision_TIS",1);
  mytree2018->SetBranchStatus("Xicc_L0ElectronDecision_TIS",1);
  mytree2018->SetBranchStatus("Xicc_L0PhotonDecision_TIS",1);
  mytree2018->SetBranchStatus("final_weight",1);

  TTree *newtree2017 = mytree2017->CopyTree(selection);
  TTree *newtree2018 = mytree2018->CopyTree(selection);

  TList *list = new TList;
  list->Add(newtree2017);
  list->Add(newtree2018);
  TTree *newtree = TTree::MergeTrees(list);

  TCanvas *c1= new TCanvas ("c1","c1");

  RooRealVar x("DM","m_{inv} (MeV/c^{2})",3560,3680);
  RooRealVar final_weight("final_weight","final_weight",-100.,100.);
  RooArgSet variables;
  variables.add(x);
  variables.add(final_weight);
  RooDataSet data("data","m_{inv} (MeV/c^{2})",variables,WeightVar(final_weight),Import(*newtree));

  RooPlot* xframe = x.frame(Title(""));
  data.plotOn(xframe,Name("data"),Binning(40));

  // signal PDF - DSCB
  RooRealVar mean("#mu","mean of gaussians",initial_mass,initial_mass-2.,initial_mass+2.);
  RooRealVar sigma1("#sigma (Gaussian)","width of gaussian",8.,3.,14.) ;
  RooRealVar sigma2("#sigma (DSCB)","width of gaussian",8.,3.,14.) ;
  RooRealVar alpha1("alpha","alpha",1.5,0.,10.);
  RooRealVar n1("n","n",1.5,0.0,15.);
  RooRealVar alpha2("alpha2","alpha2",6.5,0.,10.);
  RooRealVar n2("n2","n2",1.5,0.0,15.);
  RooDSCBShape crystalBall("crystalBall", "crystalBall", x, mean, sigma2, alpha1, n1, alpha2, n2);
  RooGaussian gausian("gausian", "gausian", x, mean, sigma1);
  RooRealVar frac("frac","fraction of component 1 in signal",0.3,0.,1.) ;

  //frac.setVal(0.6);
  //frac.setConstant(kTRUE);

  // Combine signal and background
  RooAddPdf model("model","model",RooArgList(gausian,crystalBall),frac);

  model.fitTo(data,RooFit::PrintLevel(-1));
  model.plotOn(xframe,Name("gausian"),Components(gausian),LineStyle(kDashed),LineWidth(2),LineColor(kGreen)) ;
  model.plotOn(xframe,Name("crystalBall"),Components(crystalBall),LineStyle(kDashed),LineWidth(2),LineColor(kRed)) ;
  model.plotOn(xframe,Name("fit"),LineWidth(2));

  RooRealVar sigma("#sigma","width of gaussian",5.5,0.,10.) ;
  sigma.setVal(sqrt( (frac.getVal() * sigma1.getVal() * sigma1.getVal()) + ( (1-frac.getVal()) * sigma2.getVal() * sigma2.getVal() ) ));
  //sigma.setError(sqrt( pow((frac.getVal() * (1/sigma.getVal()) * sigma1.getVal() * sigma1.getError()),2) + pow( ((1-frac.getVal())) * (1/sigma.getVal()) * sigma2.getVal() * sigma2.getError(),2) ) );
  sigma.setError(0.32);
  sigma.setConstant(kTRUE);
/*
  TPaveText *param = new TPaveText(0.12,0.80,0.7,0.65,"blNDC");
  xframe->addObject(param);
  param->AddText(Form("#mu = %.2f #pm %.2f", mean.getVal(), mean.getError()));
  param->AddText(Form("#sigma = %.2f #pm %.2f", sigma.getVal(), sigma.getError()));
  param->AddText(Form("#chi^{2}/ndf = %.2f", xframe->chiSquare(8)));
  param->SetBorderSize(0);
  param->SetFillStyle(0);
  param->SetLineColor(0);
  param->SetTextSize(0.04);
  param->SetTextAlign(11);
*/

  TLegend *leg = new TLegend(0.68,0.88,0.95,0.6);
  leg->SetBorderSize(0);
  leg->AddEntry(xframe->findObject("data"),"MC data","lep");
  leg->AddEntry(xframe->findObject("fit"),"Fit","L");
  leg->AddEntry(xframe->findObject("crystalBall"),"DSCB","L");
  leg->AddEntry(xframe->findObject("gausian"),"Gausian","L");
  leg->SetTextSize(gROOT->GetStyle("lhcbStyle")->GetTextSize());
  leg->SetTextFont(gROOT->GetStyle("lhcbStyle")->GetTextFont());
  xframe->addObject(leg);
  xframe->SetTitle("");
  xframe->GetXaxis()->SetTitle("");
  xframe->GetYaxis()->SetTitle("Candidates / (3 MeV/#it{c}^{2})");
  //xframe->GetYaxis()->SetTitleOffset(1.3);

  printf("alpha1 is %.2f ± %.2f\n",alpha1.getVal(), alpha1.getError());
  printf("n1 is %.2f ± %.2f\n",n1.getVal(), n1.getError());
  printf("alpha2 is %.2f ± %.2f\n",alpha2.getVal(), alpha2.getError());
  printf("n2 is %.2f ± %.2f\n",n2.getVal(), n2.getError());
  printf("chi2/ndof is %.2f\n",xframe->chiSquare("fit","data",8));
  printf("mean is %.2f ± %.2f\n",mean.getVal(), mean.getError());
  printf("sigma 1 is %.4f ± %.4f\n",sigma1.getVal(),sigma1.getError());
  printf("sigma 2 is %.4f ± %.4f\n",sigma2.getVal(),sigma2.getError());
  printf("sigma is %.4f ± %.4f\n",sigma.getVal(),sigma.getError());
  printf("frac is %.4f ± %.4f\n",frac.getVal(),frac.getError());

  RooHist* hresid = xframe->pullHist() ;
  RooPlot* frame2 = x.frame(Title("")) ;
  frame2->addPlotable(hresid) ;

  TCanvas* c = new TCanvas("c","c",1000,1000) ;

  TPad *pad1 = new TPad("pad1", "pad1", 0, 0.3, 1, 1.0);
  pad1->SetBottomMargin(0.1); // Upper and lower plot are joined
  pad1->Draw();             // Draw the upper pad: pad1
  pad1->cd();               // pad1 becomes the current pad
  xframe->Draw();               // Draw h1

  TLatex lat;
  lat.SetNDC();
  lat.SetTextFont(132);
  lat.SetTextSize(0.06);
  lat.DrawLatex(0.18,0.83,Form("#mu = %.2f #pm %.2f",mean.getVal(),mean.getError()));
  lat.DrawLatex(0.18,0.76,Form("#sigma = %.2f #pm %.2f",sigma.getVal(), sigma.getError() ));
  lat.DrawLatex(0.18,0.69,Form("#chi^{2}/ndf = %.2f", xframe->chiSquare("fit","data",8)));

  xframe->SetTitle("");

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

  frame2->GetXaxis()->SetTitle("#it{m} (#it{#Xi_{c}^{+}#pi^{+}}) (MeV/#it{c}^{2})");
  frame2->GetXaxis()->SetLabelSize(0);
  frame2->GetXaxis()->SetTitleSize(0.23);
  frame2->GetXaxis()->SetTitleOffset(0.4);
  frame2->SetFillColor(15) ;
  //xframe->Draw();

  c->SaveAs("Xiccpp_GaussDSCB_MC_combined.pdf");
  RooMsgService::instance().Print();

  newfile->Close();

}
