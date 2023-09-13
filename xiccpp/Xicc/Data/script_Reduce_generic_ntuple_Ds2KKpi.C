{

  gROOT->LoadMacro("Reduce_generic_ntuple_Ds2KKpi.C");
  
  TString years[4] = {"2015","2016", "2018" ,"2017"};
  
  for (Int_t i=1; i<2; i++) 
  {
    //Reduce_generic_ntuple_Ds2KKpi(years[i], "MU",0);
    Reduce_generic_ntuple_Ds2KKpi(years[i], "MD",0);
    
  }
  

}

