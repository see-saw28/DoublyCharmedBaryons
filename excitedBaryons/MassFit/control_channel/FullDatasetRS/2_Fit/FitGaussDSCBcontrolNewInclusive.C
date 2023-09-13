#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "RooPolynomial.h"
#include "RooExponential.h"
#include "RooAbsReal.h"
#include "RooAddPdf.h"
#include "TCanvas.h"
#include "RooPlot.h"
#include <TH1D.h>
#include "RooWorkspace.h"
#include <TFile.h>
#include "RooStats/AsymptoticCalculator.h"
#include "RooStats/HypoTestCalculatorGeneric.h"
#include "RooStats/ProfileLikelihoodCalculator.h"
#include "RooStats/LikelihoodInterval.h"
#include "../../../RooCustomPdfs/RooDSCBShape.cxx"
#include "../../../RooCustomPdfs/lhcbStyle.C"
using namespace RooFit;
using namespace RooStats;


void DoSPlot(RooWorkspace* ws){
  std::cout << "Calculate sWeights" << std::endl;
  /*
  Float_t s_sig;
  Float_t s_bkg;
  TFile *newfile = new TFile("sweights.root","RECREATE");
  auto newBranch = newtree->Branch("s_sig", &s_sig, "s_sig/F");
  auto newBranch = newtree->Branch("s_bkg", &s_bkg, "s_bkg/F");
  Long64_t nentries = t3->GetEntries(); // read the number of entries in the t3
  for (Long64_t i = 0; i < nentries; i++) {
        new_v = gRandom->Gaus(0, 1);
        newBranch->Fill();
  }
*/
  // get what we need out of the workspace to do the fit
  RooAbsPdf* model = ws->pdf("model");
  RooRealVar* nsig = ws->var("nsig");
  RooRealVar* nbkg = ws->var("nbkg");
  RooDataSet* data = (RooDataSet*) ws->data("data");

  // fit the model to the data.
  model->fitTo(*data, Extended() );

  // The sPlot technique requires that we fix the parameters
  // of the model that are not yields after doing the fit.
  RooRealVar* mu = ws->var("mu");
  RooRealVar* sig1 = ws->var("sig1");
  RooRealVar* sig2 = ws->var("sig2");
  mu->setConstant();
  sig1->setConstant();
  //sig2->setConstant();

  RooMsgService::instance().setSilentMode(true);

  // Now we use the SPlot class to add SWeights to our data set
  // based on our model and our yield variables
  RooStats::SPlot* sData = new RooStats::SPlot("sData","An SPlot",
                                               *data, model, RooArgList(*nsig,*nbkg) );


  // Check that our weights have the desired properties

  std::cout << "Check SWeights:" << std::endl;


  std::cout << std::endl <<  "Signal yield is "
            << nsig->getVal() << ".  From sWeights it is "
            << sData->GetYieldFromSWeight("nsig") << std::endl;


  std::cout << "Bkg yield is "
            << nbkg->getVal() << ".  From sWeights it is "
            << sData->GetYieldFromSWeight("nbkg") << std::endl
            << std::endl;

  for(Int_t i=0; i < 10; i++)
    {
      std::cout << "Sig Weight   " << sData->GetSWeight(i,"nsig")
                << "   Bkg Weight   " << sData->GetSWeight(i,"nbkg")
                << "  Total Weight   " << sData->GetSumOfEventSWeight(i)
                << std::endl;
    }

  std::cout << std::endl;

  // import this new dataset with sWeights
 std::cout << "import new dataset with sWeights" << std::endl;
 ws->import(*data, Rename("dataWithSWeights"));
 sData->GetSDataSet()->write("weights_inclusiveHLT2line.out");
 printf("!!! number of entries: %f \n", sData->GetSDataSet()->sumEntries() );
 //ws->writeToFile("ws.root");

}

void FitGaussDSCBcontrolNewInclusive(){

  lhcbStyle();

  TFile *myfile2016 = new TFile("/nfs/users/dbobulska/Xiccp_studies/2016/Data/control_channel_XicpPip/RS_full_dataset/hlt2_inclusive_line/TMVAoutput/Data_2016_Xicc_TMVAapplication_allMVAmethods_moreBranches_DuplicatesClonedRemoved_afterMVA.root","READ");
  TFile *myfile2017 = new TFile("/nfs/users/dbobulska/Xiccp_studies/2017/Data/control_channel_XicpPip/RS_full_dataset/hlt2_inclusive_line/TMVAoutput/Data_2017_Xicc_TMVAapplication_allMVAmethods_moreBranches_DuplicatesClonedRemoved_afterMVA.root","READ");
  TFile *myfile2018 = new TFile("/nfs/users/dbobulska/Xiccp_studies/2018/Data/control_channel_XicpPip/RS_full_dataset/hlt2_inclusive_line/TMVAoutput/Data_2018_Xicc_TMVAapplication_allMVAmethods_moreBranches_DuplicatesClonedRemoved_afterMVA.root","READ");
  TTree *mytree2016 = (TTree*)myfile2016->Get("DecayTree");
  TTree *mytree2017 = (TTree*)myfile2017->Get("DecayTree");
  TTree *mytree2018 = (TTree*)myfile2018->Get("DecayTree");

  TCut selection = "Xic_M > 2450. && Xic_M < 2488. && MVA_MLP > 0.97 && PPi_angle > 0.0005 & PPi1_angle > 0.0005 & PiPi1_angle > 0.0005 & PK_angle > 0.0005 & KPi_angle > 0.0005 & KPi1_angle > 0.0005 && "
                   "(KKpi < 2025 || KKpi > 2060) && (Kpipi < 1850 || Kpipi > 1890) && "
                   "Xicc_Y > 2.0 && Xicc_Y < 4.5 && Xicc_PT > 2500. && Xicc_PT < 25000. && "
                   "(Xicc_L0HadronDecision_TIS || Xicc_L0MuonDecision_TIS || Xicc_L0DiMuonDecision_TIS || Xicc_L0ElectronDecision_TIS || Xicc_L0PhotonDecision_TIS)";
  //"(Xic_L0HadronDecision_TOS || Xicc_L0HadronDecision_TIS || Xicc_L0MuonDecision_TIS || Xicc_L0DiMuonDecision_TIS || Xicc_L0ElectronDecision_TIS || Xicc_L0PhotonDecision_TIS)";
  //                 "(Xic_L0HadronDecision_TOS)";

  Double_t initial_mass = 3620.;

  TFile *newfile = new TFile("temp.root","RECREATE");

  mytree2016->SetBranchStatus("*",0);
  mytree2016->SetBranchStatus("MVA_MLP",1);
  mytree2016->SetBranchStatus("MVA_BDT",1);
  mytree2016->SetBranchStatus("DM",1);
  mytree2016->SetBranchStatus("Xic_M",1);
  mytree2016->SetBranchStatus("PK_angle",1);
  mytree2016->SetBranchStatus("KPi_angle",1);
  mytree2016->SetBranchStatus("KPi1_angle",1);
  mytree2016->SetBranchStatus("PPi_angle",1);
  mytree2016->SetBranchStatus("PPi1_angle",1);
  mytree2016->SetBranchStatus("PiPi1_angle",1);
  mytree2016->SetBranchStatus("Xic_L0HadronDecision_TOS",1);
  mytree2016->SetBranchStatus("Xicc_L0HadronDecision_TIS",1);
  mytree2016->SetBranchStatus("Xicc_L0MuonDecision_TIS",1);
  mytree2016->SetBranchStatus("Xicc_L0DiMuonDecision_TIS",1);
  mytree2016->SetBranchStatus("Xicc_L0ElectronDecision_TIS",1);
  mytree2016->SetBranchStatus("Xicc_L0PhotonDecision_TIS",1);
  mytree2016->SetBranchStatus("Xicc_PT",1);
  mytree2016->SetBranchStatus("Xicc_Y",1);
  mytree2016->SetBranchStatus("KKpi",1);
  mytree2016->SetBranchStatus("Kpipi",1);

  mytree2017->SetBranchStatus("*",0);
  mytree2017->SetBranchStatus("MVA_MLP",1);
  mytree2017->SetBranchStatus("MVA_BDT",1);
  mytree2017->SetBranchStatus("DM",1);
  mytree2017->SetBranchStatus("Xic_M",1);
  mytree2017->SetBranchStatus("PK_angle",1);
  mytree2017->SetBranchStatus("KPi_angle",1);
  mytree2017->SetBranchStatus("KPi1_angle",1);
  mytree2017->SetBranchStatus("PPi_angle",1);
  mytree2017->SetBranchStatus("PPi1_angle",1);
  mytree2017->SetBranchStatus("PiPi1_angle",1);
  mytree2017->SetBranchStatus("Xic_L0HadronDecision_TOS",1);
  mytree2017->SetBranchStatus("Xicc_L0HadronDecision_TIS",1);
  mytree2017->SetBranchStatus("Xicc_L0MuonDecision_TIS",1);
  mytree2017->SetBranchStatus("Xicc_L0DiMuonDecision_TIS",1);
  mytree2017->SetBranchStatus("Xicc_L0ElectronDecision_TIS",1);
  mytree2017->SetBranchStatus("Xicc_L0PhotonDecision_TIS",1);
  mytree2017->SetBranchStatus("Xicc_PT",1);
  mytree2017->SetBranchStatus("Xicc_Y",1);
  mytree2017->SetBranchStatus("KKpi",1);
  mytree2017->SetBranchStatus("Kpipi",1);

  mytree2018->SetBranchStatus("*",0);
  mytree2018->SetBranchStatus("MVA_MLP",1);
  mytree2018->SetBranchStatus("MVA_BDT",1);
  mytree2018->SetBranchStatus("DM",1);
  mytree2018->SetBranchStatus("Xic_M",1);
  mytree2018->SetBranchStatus("PK_angle",1);
  mytree2018->SetBranchStatus("KPi_angle",1);
  mytree2018->SetBranchStatus("KPi1_angle",1);
  mytree2018->SetBranchStatus("PPi_angle",1);
  mytree2018->SetBranchStatus("PPi1_angle",1);
  mytree2018->SetBranchStatus("PiPi1_angle",1);
  mytree2018->SetBranchStatus("Xic_L0HadronDecision_TOS",1);
  mytree2018->SetBranchStatus("Xicc_L0HadronDecision_TIS",1);
  mytree2018->SetBranchStatus("Xicc_L0MuonDecision_TIS",1);
  mytree2018->SetBranchStatus("Xicc_L0DiMuonDecision_TIS",1);
  mytree2018->SetBranchStatus("Xicc_L0ElectronDecision_TIS",1);
  mytree2018->SetBranchStatus("Xicc_L0PhotonDecision_TIS",1);
  mytree2018->SetBranchStatus("Xicc_PT",1);
  mytree2018->SetBranchStatus("Xicc_Y",1);
  mytree2018->SetBranchStatus("KKpi",1);
  mytree2018->SetBranchStatus("Kpipi",1);

  TTree *newtree2016 = mytree2016->CopyTree(selection);
  TTree *newtree2017 = mytree2017->CopyTree(selection);
  TTree *newtree2018 = mytree2018->CopyTree(selection);

  TList *list = new TList;
  list->Add(newtree2016);
  list->Add(newtree2017);
  list->Add(newtree2018);
  TTree *newtree = TTree::MergeTrees(list);
  TCanvas *c1= new TCanvas ("c1","c1");

  printf("!!! number of events: %lld \n", newtree->GetEntries("DM > 3565 && DM < 3745"));

  RooRealVar DM("DM","m_{inv} (MeV/c^{2})",3565,3745);
  RooDataSet data("data","m_{inv} (MeV/c^{2})",DM,Import(*newtree));

  RooPlot* xframe = DM.frame(Title("#Xi_{cc}^{++} -> #Xi_{c}^{+} #pi^{+}"));
  //data.plotOn(xframe,Name("data"),Binning(42));

  //----------------------------//
  //-------- Parameters --------//
  //----------------------------//
  RooRealVar mu("mu","mu",3621.,3618.0,3624.0);
  RooRealVar sig1("sig1","sig1",4.8,3.5,20.8);
  //RooRealVar sig2("sig2","sig2",8.2,3.2,20.8);
  RooRealVar a1("alpha","alpha",1.5,0.,10.);
  RooRealVar n1("n","n",1.5,1.0,5.);
  RooRealVar a2("alpha2","alpha2",6.5,0.,10.);
  RooRealVar n2("n2","n2",1.5,1.0,5.);
  RooRealVar frac("frac","fraction of component 1 in signal",0.3,0.,1.) ;
  RooRealVar ratiosigmas("ratiosigmas","ratiosigmas",1.0,0.0,10.0);
  //RooGaussian const_ratio(“const_ratio”,"",ratio,RooFit::RooConst(2.0),RooFit::RooConst(0.1));
  RooProduct sig2("sig2","sig2",RooArgSet(sig1,ratiosigmas));
  //RooProduct sigsigma2("#sigma_{B}2",“B sigma2”,RooArgSet(sigsigma,const_ratio));
  //RooGaussian BSig_RF2( “Bsig_RF2”, “Signal Gaussian B RF Mass”, Donly_CM_M, sigmean, sigsigma2 );

  frac.setVal(0.67);
  frac.setConstant(kTRUE);
  a1.setVal(2.12);
  a1.setConstant(kTRUE);
  n1.setVal(1.01);
  n1.setConstant(kTRUE);
  a2.setVal(2.09);
  a2.setConstant(kTRUE);
  n2.setVal(4.26);
  n2.setConstant(kTRUE);
  //sig1.setVal(6.29);
  //sig1.setConstant(kTRUE);
  //sig2.setVal(9.40);
  //sig2.setConstant(kTRUE);
  ratiosigmas.setVal(1.81);
  ratiosigmas.setConstant(kTRUE); 
 
  //----------------------------//
  //---- signal PDF - DSCB -----//
  //----------------------------//
  RooDSCBShape crystalBall("crystalBall", "crystalBall", DM, mu, sig2, a1, n1, a2, n2);
  RooGaussian gausian("gausian", "gausian", DM, mu, sig1);
  RooAddPdf signal("signal","signal",RooArgList(gausian,crystalBall),frac);

  //----------------------------//
  //------ bkg PDF - Expo ------//
  //----------------------------//
  RooRealVar lambda("lambda", "slope", 0.0016, -1, 1);
  RooExponential bkg("bkg", "exponential PDF", DM, lambda);

  //----------------------------//
  //------- signal + bkg -------//
  //----------------------------//
  RooRealVar nsig("nsig","#signal events",300.,0.,1200.);
  RooRealVar nbkg("nbkg","#background events",20000.,0.,30000.);

  RooExtendPdf esig("esig", "esig", signal, nsig);
  RooExtendPdf ebkg("esbkg", "esbkg", bkg, nbkg);

  RooAddPdf model("model","sig+bkg", RooArgSet(esig, ebkg));

  RooExponential bkg2("bkg2", "exponential PDF", DM, lambda);
  RooRealVar nbkg2("nbkg2","#background events",7500.,2000.,12000.);
  RooExtendPdf ebkg2("esbkg2", "esbkg2", bkg2, nbkg2);
  RooAddPdf bkgmod("bkgmod","bkgmod", RooArgSet(ebkg2));

  //----------------------------//
  //--------- Workspace --------//
  //----------------------------//
  RooWorkspace *w = new RooWorkspace("w","w");
  w->addClassDeclImportDir("../../../RooCustomPdfs/");
  w->addClassImplImportDir("../../../RooCustomPdfs/");
  w->import(model);
  w->import(bkgmod);
  w->import(data);
  w->importClassCode("RooDSCBShape",kTRUE);

  //----------------------------//
  //------ Fit data + plot -----//
  //----------------------------//
  model.fitTo(data);
  data.plotOn(xframe,Name("dataset"),Binning(36));
  model.plotOn(xframe,Name("bkgmodel"),Components("bkg"),LineStyle(kDotted),LineColor(kGreen+1));
  model.plotOn(xframe,Name("signalmodel"),Components("signal"),LineStyle(kDashed),LineColor(kRed));
  model.plotOn(xframe,Name("combinedmodel"));
  //new TCanvas("modelControlChannel","model for Control channel",600,600);

  RooRealVar sig("sig","width",4.5,0.,20.) ;
  sig.setVal(sig1.getVal() * sqrt( (frac.getVal()) + ( (1-frac.getVal()) * ratiosigmas.getVal() * ratiosigmas.getVal() ) ));
  sig.setError(sig1.getError() * sqrt( (frac.getVal()) + ( (1-frac.getVal()) * ratiosigmas.getVal() * ratiosigmas.getVal() ) ));

  sig.setConstant(kTRUE);

  //----------------------------//
  //---- Print fitted param ----//
  //----------------------------//
  printf("number of signal events: %f ± %f\n", nsig.getVal(), nsig.getError());
  printf("number of bkg events: %f ± %f\n", nbkg.getVal(), nbkg.getError());
  DM.setRange("sigreg",mu.getVal()-2*sig.getVal(),mu.getVal()+2*sig.getVal());
  RooAbsReal* fsigregion_model = model.createIntegral(DM,NormSet(DM),Range("sigreg"));
  RooAbsReal* fsigregion_bkg = bkg.createIntegral(DM,NormSet(DM),Range("sigreg"));
  Double_t nsigevents = fsigregion_model->getVal()*(nsig.getVal()+nbkg.getVal())-fsigregion_bkg->getVal()*nbkg.getVal();
  Double_t nbkgevents = fsigregion_bkg->getVal()*nbkg.getVal();
  Double_t signif = nsigevents/(sqrt(nsigevents+nbkgevents));
  printf("bkg yield in mass window is %f\n",nbkgevents);
  printf("sig yield in mass window is %f\n",nsigevents);
  printf("signif is %f\n",signif);
  printf("bkg lambda is %f ± %f\n",lambda.getVal(),lambda.getError());
  printf("sigma is %f ± %f\n",sig.getVal(),sig.getError());
  printf("sigma 1 is %f ± %f\n",sig1.getVal(),sig1.getError());
  printf("sigma 2 is %f\n",sig2.getVal());
  printf("fraction is %f\n",ratiosigmas.getVal());
  printf("chi2/ndof is %f\n",xframe->chiSquare("combinedmodel","dataset",4));
/*
  TPaveText *param = new TPaveText(0.12,0.80,0.7,0.65,"blNDC");
  xframe->addObject(param);
  param->AddText(Form("#mu = %.2f #pm %.2f", mu.getVal(), mu.getError()));
  param->AddText(Form("#chi^{2}/ndf = %.2f", xframe->chiSquare("combinedmodel","dataset",4)));
  param->SetBorderSize(0);
  param->SetFillStyle(0);
  param->SetLineColor(0);
  param->SetTextSize(0.04);
  param->SetTextAlign(11);
*/
  TLegend *leg = new TLegend(0.58,0.88,0.88,0.6);
  leg->SetBorderSize(0);
  leg->AddEntry(xframe->findObject("dataset"),"2016-2018 data","lep");
  leg->AddEntry(xframe->findObject("combinedmodel"),"Fit","L");
  leg->AddEntry(xframe->findObject("signalmodel"),"Signal","L");
  leg->AddEntry(xframe->findObject("bkgmodel"),"Background","L");
  leg->SetTextSize(gROOT->GetStyle("lhcbStyle")->GetTextSize());
  leg->SetTextFont(gROOT->GetStyle("lhcbStyle")->GetTextFont());
  xframe->addObject(leg);
  xframe->GetXaxis()->SetTitle("");
  xframe->GetYaxis()->SetRangeUser(0,400);
  //xframe->GetXaxis()->SetTitle("m (#Xi_{c}^{+}#pi^{+}) (MeV/c^{2})");
  xframe->GetYaxis()->SetTitle("Candidates / (5 MeV/#it{c}^{2})");
  //xframe->GetYaxis()->SetTitleOffset(1.3);

  //----------------------------//
  //------- Model config -------//
  //----------------------------//

  //-------- H0 - B only -------//
  ModelConfig h0("h0",w);
  h0.SetPdf(*w->pdf("model"));
  h0.SetParametersOfInterest("nsig");
  RooRealVar* poi0 = (RooRealVar*) h0.GetParametersOfInterest()->first();
  poi0->setVal(0.);
  h0.SetSnapshot(*poi0);
  h0.SetObservables(*w->var("DM"));
  h0.Print();

  //---- H1 - S+B hypothesis ---//
  ModelConfig* h1 = (ModelConfig*) h0.Clone("h1");
  RooRealVar* poi1 = (RooRealVar*) h1->GetParametersOfInterest()->first();
  poi1->setVal(nsig.getVal());
  h1->SetSnapshot(*poi1);
  h1->Print();

  w->Print();

  //----------------------------//
  //----- Asymptotic Calc ------//
  //----------------------------//
  AsymptoticCalculator ac(data,*h1,h0);
  ac.SetOneSidedDiscovery(kTRUE);
  HypoTestResult *acResult = ac.GetHypoTest();
  acResult->Print();
  cout << "Significance from Asymptotic Calculator is " << acResult->Significance() << "\n";

/*
  //----------------------------//
  //- Profile Likelihood Calc  -//
  //----------------------------//
  ProfileLikelihoodCalculator plCalc(data,*h1); 
  // alterative definition - ProfileLikelihoodCalculator plCalc(data,model,nsig);
  plCalc.SetConfidenceLevel(0.68);
  //---- LikelihoodInterval ----//
  LikelihoodInterval* interval = plCalc.GetInterval();
  const double MLE = poi1->getVal();
  const double lowerLimit = interval->LowerLimit(*poi1);
  const double upperLimit = interval->UpperLimit(*poi1);
  printf("%.0f%% interval (Profile Likelihood Calculator) on %s is [%.3f,%.3f] \n",
         plCalc.ConfidenceLevel()*100,poi1->GetName(),lowerLimit,upperLimit);
*/
  printf("bkg yield in mass window is %f\n",nbkgevents);
  printf("sig yield in mass window is %f\n",nsigevents);

  RooHist* hresid = xframe->pullHist() ;
  RooPlot* frame2 = DM.frame(Title("")) ;
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
  lat.DrawLatex(0.18,0.83,Form("#mu = %.2f #pm %.2f",mu.getVal(),mu.getError()));
  lat.DrawLatex(0.18,0.76,Form("#sigma = %.2f #pm %.2f",sig.getVal(), sig.getError() ));
  lat.DrawLatex(0.18,0.69,Form("#chi^{2}/ndf = %.2f", xframe->chiSquare("combinedmodel","dataset",4)));

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
  c->SaveAs("Xiccpp_GaussDSCB_RSdata_combined_InclusiveL0TIS.pdf");

  //DoSPlot(w);
}
