{

  gROOT->LoadMacro("TMVAClassificationApplication.C");
  
  TString years[4] = {"2015","2016", "2018" ,"2017"};
  
  for (Int_t i=1; i<2; i++) 
  {
    //TMVAClassificationApplication(years[i], "MU");
    TMVAClassificationApplication(years[i], "MD");
    
  }
  

}

