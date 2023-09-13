void Reduce_generic_ntuple_Ds2KKpi(TString year, TString MagnetPolarity, Int_t nevents){

  cout << "Processing " << year << " " << MagnetPolarity << endl;
  

  if(MagnetPolarity!= "MD" & MagnetPolarity != "MU")
  {
    cout << "Magnet Polarity should be MD or MU" << endl;    
    return;
  }

  //TString Ds_Cut0 = "(Ds_CHI2NDOF_DTF_PV>0) & (Ds_CHI2NDOF_DTF_PV<5) & (Ds_IPCHI2_OWNPV<9) & (Kp_PIDK>7 & Km_PIDK > 7 & pip_PIDK<3) & ((Kp_PT+Km_PT+pip_PT) > 3000) & (Ds_ENDVERTEX_CHI2/Ds_ENDVERTEX_NDOF < 6) & (Ds_DIRA_OWNPV>0.9999) & (Ds_FDCHI2_OWNPV>36) & (Ds_TAU>0.0002)";

  TString Ds_Cut0 = "(Ds_CHI2NDOF_DTF_PV>0) & (Ds_CHI2NDOF_DTF_PV<5)";

  TString eos_home = "/eos/lhcb/user/m/mpappaga/Ds1_Spectroscopy/Ds1_Dsmumu/"+year+"/";  
  TString filename = "Dsmumu_"+year+"_"+MagnetPolarity+".root";

  //TString eos_home = "/tmp/mpappaga/";
  //TString filename = "888_temp.root";
  
  TFile *file =  TFile::Open(eos_home+filename);

  if (nevents > 0)
  {
    filename = "Training_TMVA_"+filename;
  }
  
  TTree *Jpsitree = (TTree*) file->Get("Ds2KKpiTree/DecayTree");  
  Jpsitree->SetName("Ds2KKpiTree");
  

  TFile *newfile = new TFile("/tmp/mpappaga/Reduced_Ds2KKpi_"+filename,"recreate");
  TTree *Lumitree = (TTree*) file->Get("GetIntegratedLuminosity/LumiTuple");

  Jpsitree->SetBranchStatus("*",0);
  
  if(year != "2015"){
    Jpsitree->SetBranchStatus("Km_ProbNNk",1);
    Jpsitree->SetBranchStatus("Kp_ProbNNk",1);
    Jpsitree->SetBranchStatus("pip_ProbNNpi",1);
  }else{
    Jpsitree->SetBranchStatus("Km_MC15TuneV1_ProbNNk",1);
    Jpsitree->SetBranchStatus("Kp_MC15TuneV1_ProbNNk",1);
    Jpsitree->SetBranchStatus("pip_MC15TuneV1_ProbNNpi",1);
  }
  
  Jpsitree->SetBranchStatus("Kp_PT",1);
  Jpsitree->SetBranchStatus("Km_PT",1);
  Jpsitree->SetBranchStatus("pip_PT",1);
  Jpsitree->SetBranchStatus("Kp_PIDK",1);
  Jpsitree->SetBranchStatus("Km_PIDK",1);
  Jpsitree->SetBranchStatus("pip_PIDK",1);  
  Jpsitree->SetBranchStatus("Km_IPCHI2*",1);
  Jpsitree->SetBranchStatus("Kp_IPCHI2*",1);
  Jpsitree->SetBranchStatus("pip_IPCHI2*",1);
  Jpsitree->SetBranchStatus("Ds_PT",1);
  Jpsitree->SetBranchStatus("Ds_IPCHI2*",1);
  Jpsitree->SetBranchStatus("Ds_DIRA*",1);
  Jpsitree->SetBranchStatus("Ds_FD*",1);
  Jpsitree->SetBranchStatus("Ds_M*",1);
  Jpsitree->SetBranchStatus("Ds_CHI2*",1);
  Jpsitree->SetBranchStatus("Ds_TAU*",1);
  Jpsitree->SetBranchStatus("Ds_ENDVERTEX_CHI2",1);
  Jpsitree->SetBranchStatus("Ds_ENDVERTEX_NDOF",1);
  
  Jpsitree->SetBranchStatus("Kp_PX",1);
  Jpsitree->SetBranchStatus("Kp_PY",1);
  Jpsitree->SetBranchStatus("Kp_PZ",1);
  Jpsitree->SetBranchStatus("Kp_PE",1);
  
  Jpsitree->SetBranchStatus("Km_PX",1);
  Jpsitree->SetBranchStatus("Km_PY",1);
  Jpsitree->SetBranchStatus("Km_PZ",1);
  Jpsitree->SetBranchStatus("Km_PE",1);

  Jpsitree->SetBranchStatus("pip_PX",1);
  Jpsitree->SetBranchStatus("pip_PY",1);
  Jpsitree->SetBranchStatus("pip_PZ",1);
  Jpsitree->SetBranchStatus("pip_PE",1);

  //Create a new file + a clone of old tree in new file    
  //TTree *newtree = Jpsitree->CloneTree(2000000);
  //TTree *newtree = Jpsitree->CloneTree();

  TString Cut_TOT = Ds_Cut0 ;

  TTree *newtree = new TTree();

  if (nevents > 0){
    newtree = Jpsitree->CopyTree(Cut_TOT,"",nevents);
  }else{
    newtree = Jpsitree->CopyTree(Cut_TOT);
  }
  
  //newtree->SetName("Ds2KKpiTree");

  //==================== Double to Float for BDT trainings =====================

  Float_t Km_ProbNNk_F;      TBranch* Br_Km_ProbNNk_F = newtree->Branch("Km_ProbNNk_F",&Km_ProbNNk_F, "Km_ProbNNk_F/F");
  Float_t Kp_ProbNNk_F;      TBranch* Br_Kp_ProbNNk_F = newtree->Branch("Kp_ProbNNk_F",&Kp_ProbNNk_F, "Kp_ProbNNk_F/F");
  Float_t pip_ProbNNpi_F;    TBranch* Br_pip_ProbNNpi_F = newtree->Branch("pip_ProbNNpi_F",&pip_ProbNNpi_F, "pip_ProbNNpi_F/F");
  
  Float_t Km_IPCHI2_OWNPV_F;   TBranch* Br_Km_IPCHI2_OWNPV_F = newtree->Branch("Km_IPCHI2_OWNPV_F", &Km_IPCHI2_OWNPV_F, "Km_IPCHI2_OWNPV_F/F");
  Float_t Kp_IPCHI2_OWNPV_F;   TBranch* Br_Kp_IPCHI2_OWNPV_F = newtree->Branch("Kp_IPCHI2_OWNPV_F", &Kp_IPCHI2_OWNPV_F, "Kp_IPCHI2_OWNPV_F/F");
  Float_t pip_IPCHI2_OWNPV_F;  TBranch* Br_pip_IPCHI2_OWNPV_F = newtree->Branch("pip_IPCHI2_OWNPV_F", &pip_IPCHI2_OWNPV_F, "pip_IPCHI2_OWNPV_F/F");
  
  Float_t Km_PT_F;             TBranch* Br_Km_PT_F = newtree->Branch("Km_PT_F", &Km_PT_F, "Km_PT_F/F");
  Float_t Kp_PT_F;             TBranch* Br_Kp_PT_F = newtree->Branch("Kp_PT_F", &Kp_PT_F, "Kp_PT_F/F");
  Float_t pip_PT_F;            TBranch* Br_pip_PT_F = newtree->Branch("pip_PT_F", &pip_PT_F, "pip_PT_F/F");
  
  Float_t Ds_IPCHI2_OWNPV_F;   TBranch* Br_Ds_IPCHI2_OWNPV_F = newtree->Branch("Ds_IPCHI2_OWNPV_F", &Ds_IPCHI2_OWNPV_F, "Ds_IPCHI2_OWNPV_F/F");
  Float_t Ds_FDCHI2_OWNPV_F;   TBranch* Br_Ds_FDCHI2_OWNPV_F = newtree->Branch("Ds_FDCHI2_OWNPV_F", &Ds_FDCHI2_OWNPV_F, "Ds_FDCHI2_OWNPV_F/F");
  Float_t Ds_FD_OWNPV_F;       TBranch* Br_Ds_FD_OWNPV_F = newtree->Branch("Ds_FD_OWNPV_F", &Ds_FD_OWNPV_F, "Ds_FD_OWNPV_F/F");
  Float_t Ds_DIRA_OWNPV_F;     TBranch* Br_Ds_DIRA_OWNPV_F = newtree->Branch("Ds_DIRA_OWNPV_F", &Ds_DIRA_OWNPV_F, "Ds_DIRA_OWNPV_F/F");
  Float_t Ds_PT_F;             TBranch* Br_Ds_PT_F = newtree->Branch("Ds_PT_F", &Ds_PT_F, "Ds_PT_F/F");
  Float_t Ds_TAU_F;            TBranch* Br_Ds_TAU_F = newtree->Branch("Ds_TAU_F", &Ds_TAU_F, "Ds_TAU_F/F");
  Float_t Ds_CHI2NDOF_DTF_PV_F;TBranch* Br_Ds_CHI2NDOF_DTF_PV_F = newtree->Branch("Ds_CHI2NDOF_DTF_PV_F", &Ds_CHI2NDOF_DTF_PV_F, "Ds_CHI2NDOF_DTF_PV_F/F");

  Double_t Ds_M_check;  TBranch* Br_Ds_M_check = newtree->Branch("Ds_M_check", &Ds_M_check, "Ds_M_check/D");
  Double_t Ds_M_Kpipi;  TBranch* Br_Ds_M_Kpipi = newtree->Branch("Ds_M_Kpipi", &Ds_M_Kpipi, "Ds_M_Kpipi/D");
  Double_t Ds_M_pKpi;   TBranch* Br_Ds_M_pKpi = newtree->Branch("Ds_M_pKpi", &Ds_M_pKpi, "Ds_M_pKpi/D");
  Double_t Ds_M_KKK;    TBranch* Br_Ds_M_KKK = newtree->Branch("Ds_M_KKK", &Ds_M_KKK, "Ds_M_KKK/D");
  Double_t Ds_M_pKK;    TBranch* Br_Ds_M_pKK = newtree->Branch("Ds_M_pKK", &Ds_M_pKK, "Ds_M_pKK/D");
  Double_t Ds_M_pipipi; TBranch* Br_Ds_M_pipipi = newtree->Branch("Ds_M_pipipi", &Ds_M_pipipi, "Ds_M_pipipi/D");
    
  //Double_t D0_M; TBranch* Br_D0_M = newtree->Branch("D0_M", &D0_M, "D0_M/D");  

  Double_t Km_ProbNNk;
  Double_t Kp_ProbNNk;
  Double_t pip_ProbNNpi;
  Double_t Km_MC15TuneV1_ProbNNk;
  Double_t Kp_MC15TuneV1_ProbNNk;
  Double_t pip_MC15TuneV1_ProbNNpi;
  
  if(year != "2015"){
    newtree->SetBranchAddress("Km_ProbNNk",&Km_ProbNNk);
    newtree->SetBranchAddress("Kp_ProbNNk",&Kp_ProbNNk);
    newtree->SetBranchAddress("pip_ProbNNpi",&pip_ProbNNpi);
  }else{
    newtree->SetBranchAddress("Km_MC15TuneV1_ProbNNk",&Km_MC15TuneV1_ProbNNk);
    newtree->SetBranchAddress("Kp_MC15TuneV1_ProbNNk",&Kp_MC15TuneV1_ProbNNk);
    newtree->SetBranchAddress("pip_MC15TuneV1_ProbNNpi",&pip_MC15TuneV1_ProbNNpi);
  }
  
  Double_t Km_IPCHI2_OWNPV;    newtree->SetBranchAddress("Km_IPCHI2_OWNPV", &Km_IPCHI2_OWNPV);
  Double_t Kp_IPCHI2_OWNPV;    newtree->SetBranchAddress("Kp_IPCHI2_OWNPV", &Kp_IPCHI2_OWNPV);
  Double_t pip_IPCHI2_OWNPV;   newtree->SetBranchAddress("pip_IPCHI2_OWNPV", &pip_IPCHI2_OWNPV);
  
  Double_t Km_PT;              newtree->SetBranchAddress("Km_PT", &Km_PT);
  Double_t Kp_PT;              newtree->SetBranchAddress("Kp_PT", &Kp_PT);
  Double_t pip_PT;             newtree->SetBranchAddress("pip_PT", &pip_PT);

  Double_t Ds_IPCHI2_OWNPV;    newtree->SetBranchAddress("Ds_IPCHI2_OWNPV", &Ds_IPCHI2_OWNPV);
  Double_t Ds_FDCHI2_OWNPV;    newtree->SetBranchAddress("Ds_FDCHI2_OWNPV", &Ds_FDCHI2_OWNPV);
  Double_t Ds_FD_OWNPV;        newtree->SetBranchAddress("Ds_FD_OWNPV", &Ds_FD_OWNPV);
  Double_t Ds_DIRA_OWNPV;      newtree->SetBranchAddress("Ds_DIRA_OWNPV", &Ds_DIRA_OWNPV);
  Double_t Ds_PT;              newtree->SetBranchAddress("Ds_PT", &Ds_PT);
  Double_t Ds_TAU;             newtree->SetBranchAddress("Ds_TAU", &Ds_TAU);
  Double_t Ds_CHI2NDOF_DTF_PV; newtree->SetBranchAddress("Ds_CHI2NDOF_DTF_PV", &Ds_CHI2NDOF_DTF_PV);
  
  Double_t Kp_PX;              newtree->SetBranchAddress("Kp_PX", &Kp_PX);
  Double_t Kp_PY;              newtree->SetBranchAddress("Kp_PY", &Kp_PY);
  Double_t Kp_PZ;              newtree->SetBranchAddress("Kp_PZ", &Kp_PZ);
  Double_t Kp_PE;              newtree->SetBranchAddress("Kp_PE", &Kp_PE);
  
  Double_t Km_PX;              newtree->SetBranchAddress("Km_PX", &Km_PX);
  Double_t Km_PY;              newtree->SetBranchAddress("Km_PY", &Km_PY);
  Double_t Km_PZ;              newtree->SetBranchAddress("Km_PZ", &Km_PZ);
  Double_t Km_PE;              newtree->SetBranchAddress("Km_PE", &Km_PE);
  
  Double_t pip_PX;             newtree->SetBranchAddress("pip_PX", &pip_PX);
  Double_t pip_PY;             newtree->SetBranchAddress("pip_PY", &pip_PY);
  Double_t pip_PZ;             newtree->SetBranchAddress("pip_PZ", &pip_PZ);
  Double_t pip_PE;             newtree->SetBranchAddress("pip_PE", &pip_PE);  

  TLorentzVector Kplus, Kminus, piplus, Kplus_piplus, Kplus_pplus, piplus_Kplus, piplus_pplus, Kminus_piminus;
  TLorentzVector T_Ds_M_check, T_Ds_M_Kpipi, T_Ds_M_pKpi, T_Ds_M_KKK, T_Ds_M_pKK, T_Ds_M_pipipi;

  Double_t pi_mass = 139.57;
  Double_t K_mass = 493.677;
  Double_t p_mass = 938.27;

  for ( Int_t i = 0;  i < newtree->GetEntries(); i++) {
    newtree->GetEntry(i);
    
    Kplus.SetXYZT(Kp_PX, Kp_PY,Kp_PZ,Kp_PE);
    Kminus.SetXYZT(Km_PX, Km_PY,Km_PZ,Km_PE);
    piplus.SetXYZT(pip_PX, pip_PY,pip_PZ,pip_PE);
    
    Kplus_piplus.SetXYZM(Kp_PX, Kp_PY,Kp_PZ,pi_mass);
    Kplus_pplus.SetXYZM(Kp_PX, Kp_PY,Kp_PZ,p_mass);
    piplus_Kplus.SetXYZM(pip_PX, pip_PY,pip_PZ,K_mass);
    piplus_pplus.SetXYZM(pip_PX, pip_PY,pip_PZ,p_mass);
    Kminus_piminus.SetXYZM(Km_PX, Km_PY,Km_PZ,pi_mass);
    
    T_Ds_M_check  = Kplus + Kminus + piplus;
    T_Ds_M_Kpipi  = Kminus + Kplus_piplus + piplus;
    T_Ds_M_pKpi   = Kplus_pplus + Kminus + piplus;
    T_Ds_M_KKK    = Kplus + Kminus + piplus_Kplus;
    T_Ds_M_pKK    = Kplus + Kminus + piplus_pplus;
    T_Ds_M_pipipi = piplus + Kplus_piplus + Kminus_piminus;

    Ds_M_check  = T_Ds_M_check.M();
    Ds_M_Kpipi  = T_Ds_M_Kpipi.M();
    Ds_M_pKpi   = T_Ds_M_pKpi.M();
    Ds_M_KKK    = T_Ds_M_KKK.M();
    Ds_M_pKK    = T_Ds_M_pKK.M();
    Ds_M_pipipi = T_Ds_M_pipipi.M();

    //D0 = Kplus + Kminus;
    //D0_M = D0.M();
    
    if(year != "2015")
    {
      Km_ProbNNk_F   = Km_ProbNNk;
      Kp_ProbNNk_F   = Kp_ProbNNk;
      pip_ProbNNpi_F = pip_ProbNNpi;
    }else{
      Km_ProbNNk_F   = Km_MC15TuneV1_ProbNNk;
      Kp_ProbNNk_F   = Kp_MC15TuneV1_ProbNNk;
      pip_ProbNNpi_F = pip_MC15TuneV1_ProbNNpi;
    }
    
    Km_IPCHI2_OWNPV_F  = Km_IPCHI2_OWNPV;
    Kp_IPCHI2_OWNPV_F  = Kp_IPCHI2_OWNPV;
    pip_IPCHI2_OWNPV_F = pip_IPCHI2_OWNPV;
    
    Km_PT_F  = Km_PT;
    Kp_PT_F  = Kp_PT;
    pip_PT_F = pip_PT;
    
    Ds_IPCHI2_OWNPV_F = Ds_IPCHI2_OWNPV;
    Ds_FDCHI2_OWNPV_F = Ds_FDCHI2_OWNPV;
    Ds_FD_OWNPV_F = Ds_FD_OWNPV;
    Ds_DIRA_OWNPV_F = Ds_DIRA_OWNPV;
    Ds_PT_F  = Ds_PT;
    Ds_TAU_F  = Ds_TAU;
    Ds_CHI2NDOF_DTF_PV_F = Ds_CHI2NDOF_DTF_PV;

    Br_Ds_M_check->Fill();
    Br_Ds_M_Kpipi->Fill();
    Br_Ds_M_pKpi->Fill();
    Br_Ds_M_KKK->Fill();
    Br_Ds_M_pKK->Fill();
    Br_Ds_M_pipipi->Fill();
    
    Br_Km_ProbNNk_F->Fill();
    Br_Kp_ProbNNk_F->Fill();
    Br_pip_ProbNNpi_F->Fill();
    
    Br_Km_IPCHI2_OWNPV_F->Fill();
    Br_Kp_IPCHI2_OWNPV_F->Fill();
    Br_pip_IPCHI2_OWNPV_F->Fill();

    Br_Km_PT_F->Fill();
    Br_Kp_PT_F->Fill();
    Br_pip_PT_F->Fill();

    Br_Ds_IPCHI2_OWNPV_F->Fill();
    Br_Ds_FDCHI2_OWNPV_F->Fill();
    Br_Ds_FD_OWNPV_F->Fill();
    Br_Ds_DIRA_OWNPV_F->Fill();
    Br_Ds_PT_F->Fill();
    Br_Ds_TAU_F->Fill();
    Br_Ds_CHI2NDOF_DTF_PV_F->Fill();

    //Br_D0_M->Fill();
    

  }
  

  //=====================================================================


  
  TTree *newtreelumi = Lumitree->CloneTree();
  
  newfile->Write();

  //newtree->SetAlias("lab5_ProbNNk", "lab5_MC12TuneV2_ProbNNk");
  //newfile->Write();
  
  newtree->Print();
  newtreelumi->Print();

  //newfile->Close();
  //file->Close();
    
  delete file;
  delete newfile;

}
