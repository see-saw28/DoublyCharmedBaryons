void Lumi(TString filename )
{
  
  //chain_lumi.SetBranchAddress("IntegratedLuminosity",&IntegratedLuminosity);


  TChain chain_lumi("GetIntegratedLuminosity/LumiTuple");
  //TString root = "/eos/lhcb/user/m/mpappaga/Omegab_XicKpi/Omegacpi/Data/2011/" ;

  chain_lumi.Add(filename);
  Double_t  IntegratedLuminosity;
  chain_lumi.SetBranchAddress("IntegratedLuminosity",&IntegratedLuminosity);
  Double_t TotintegLumi = 0.;

  Int_t nevent = chain_lumi.GetEntries();
  for (Int_t i=0;i<nevent;i++) 
  {
    chain_lumi.GetEvent(i);
    //read complete accepted event in memory
    TotintegLumi = TotintegLumi+IntegratedLuminosity;
  }
  
  cout<<"Integrated Luminosity = "<<TotintegLumi<<endl;
  
}
