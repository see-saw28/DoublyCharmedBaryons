#include <iostream>
#include <vector>

#include "TList.h"
#include "TROOT.h"
#include "TKey.h"
#include "TString.h"
#include "TControlBar.h"
#include "TObjString.h"

#include "tmvaglob.C"

// some global lists
static TList*               TMVAGui_keyContent;
static std::vector<TString> TMVAGui_inactiveButtons;

TList* GetKeyList( const TString& pattern )
{
   TList* list = new TList();

   TIter next( TMVAGui_keyContent );
   TKey* key(0);
   while ((key = (TKey*)next())) {         
      if (TString(key->GetName()).Contains( pattern )) { list->Add( new TObjString( key->GetName() ) ); }
   }
   return list;
}

// utility function
void ActionButton( TControlBar* cbar, 
                   const TString& title, const TString& macro, const TString& comment, 
                   const TString& buttonType, TString requiredKey = "" ) 
{
   cbar->AddButton( title, macro, comment, buttonType );

   // search    
   if (requiredKey != "") {
      Bool_t found = kFALSE;
      TIter next( TMVAGui_keyContent );
      TKey* key(0);
      while ((key = (TKey*)next())) {         
         if (TString(key->GetName()).Contains( requiredKey )) { found = kTRUE; break; }
      }
      if (!found) TMVAGui_inactiveButtons.push_back( title );
   }
}

// main GUI
void TMVAGui( const char* fName = "TMVAout.root" ) 
{   
   // Use this script in order to run the various individual macros
   // that plot the output of TMVA (e.g. running TMVAClassification.C),
   // stored in the file "TMVA.root"

   TString curMacroPath(gROOT->GetMacroPath());
   // uncomment next line for macros submitted to next root version
   // gROOT->SetMacroPath(curMacroPath+":$ROOTSYS/tmva/test/:");
   
   // for the sourceforge version, including $ROOTSYS/tmva/test in the
   // macro path is a mistake, especially if "./" was not part of path
   // add ../macros to the path (comment out next line for the ROOT version of TMVA)
   gROOT->SetMacroPath(curMacroPath+":../macros:");
   
   cout << "--- Launch TMVA GUI to view input file: " << fName << endl;

   // init
   TMVAGui_inactiveButtons.clear();

   // check if file exist
   TFile* file = TFile::Open( fName );
   if (!file) {
      cout << "==> Abort TMVAGui, please verify filename" << endl;
      return;
   }
   // find all references   
   cout << "--- Reading keys ..." << endl;
   TMVAGui_keyContent = (TList*)file->GetListOfKeys()->Clone();

   // close file
   file->Close();

   TString defaultRequiredClassifier = "";

   //   gROOT->Reset();
   //   gStyle->SetScreenFactor(2); // if you have a large screen, select 1,2 or 1.4

   // create the control bar
   TControlBar* cbar = new TControlBar( "vertical", "TMVA Plotting Macros for Classification", 0, 0 );

   const TString buttonType( "button" );

   // configure buttons   
   Int_t ic = 1;

   // find all input variables types
   TList* keylist = GetKeyList( "InputVariables" );
   TListIter it( keylist );
   TObjString* str = 0;
   char ch = 'a';
   while ((str = (TObjString*)it())) {
      TString tmp   = str->GetString();
      TString title = Form( "Input variables '%s'-transformed (training sample)", 
                            tmp.ReplaceAll("InputVariables_","").Data() );
      if (tmp.Contains( "Id" )) title = "Input variables (training sample)";
      ActionButton( cbar, 
                    Form( "(%i%c) %s", ic, ch++, title.Data() ),
                    Form( ".x variables.C(\"%s\",\"%s\",\"%s\")", fName, str->GetString().Data(), title.Data() ),
                    Form( "Plots all '%s'-transformed input variables (macro variables.C(...))", str->GetString().Data() ),
                    buttonType, str->GetString() );
   }      
   ic++;

   // correlation scatter plots 
   it.Reset(); ch = 'a';
   while ((str = (TObjString*)it())) {
      TString tmp   = str->GetString();
      TString title = Form( "Input variable correlations '%s'-transformed (scatter profiles)", 
                            tmp.ReplaceAll("InputVariables_","").Data() );
      if (tmp.Contains( "Id" )) title = "Input variable correlations (scatter profiles)";
      ActionButton( cbar, 
                    Form( "(%i%c) %s", ic, ch++, title.Data() ),
                    Form( ".x CorrGui.C(\"%s\",\"%s\",\"%s\")", fName, str->GetString().Data(), title.Data() ),
                    Form( "Plots all correlation profiles between '%s'-transformed input variables (macro CorrGui.C(...))", 
                          str->GetString().Data() ),
                    buttonType, str->GetString() );
   }      
   
   // coefficients
   ActionButton( cbar,  
                 Form( "(%i) Input Variable Linear Correlation Coefficients", ++ic ),
                 Form( ".x correlations.C(\"%s\")", fName ),
                 "Plots signal and background correlation summaries for all input variables (macro correlations.C)", 
                 buttonType );

   ActionButton( cbar,  
                 Form( "(%ia) Classifier Output Distributions (test sample)", ++ic ),
                 Form( ".x mvas.C(\"%s\",0)", fName ),
                 "Plots the output of each classifier for the test data (macro mvas.C(...,0))",
                 buttonType, defaultRequiredClassifier );

   ActionButton( cbar,  
                 Form( "   (%ib) Classifier Output Distributions (test and training samples superimposed)   ", ic ),
                 Form( ".x mvas.C(\"%s\",3)", fName ),
                 "Plots the output of each classifier for the test (histograms) and training (dots) data (macro mvas.C(...,3))",
                 buttonType, defaultRequiredClassifier );

   ActionButton( cbar,  
                 Form( "(%ic) Classifier Probability Distributions (test sample)", ic ),
                 Form( ".x mvas.C(\"%s\",1)", fName ),
                 "Plots the probability of each classifier for the test data (macro mvas.C(...,1))",
                 buttonType, defaultRequiredClassifier );

   ActionButton( cbar,  
                 Form( "(%id) Classifier Rarity Distributions (test sample)", ic ),
                 Form( ".x mvas.C(\"%s\",2)", fName ),
                 "Plots the Rarity of each classifier for the test data (macro mvas.C(...,2)) - background distribution should be uniform",
                 buttonType, defaultRequiredClassifier );

   ActionButton( cbar,  
                 Form( "(%ia) Classifier Cut Efficiencies", ++ic ),
                 Form( ".x mvaeffs.C+(\"%s\")", fName ),
                 "Plots signal and background efficiencies versus cut on classifier output (macro mvaeffs.C)",
                 buttonType, defaultRequiredClassifier );

   ActionButton( cbar,  
                 Form( "(%ib) Classifier Background Rejection vs Signal Efficiency (ROC curve)", ic ),
                 Form( ".x efficiencies.C(\"%s\")", fName ),
                 "Plots background rejection vs signal efficiencies (macro efficiencies.C) [\"ROC\" stands for \"Receiver Operation Characteristics\"]",
                 buttonType, defaultRequiredClassifier );

   TString title = Form( "(%i) Parallel Coordinates (requires ROOT-version >= 5.17)", ++ic );
   ActionButton( cbar,  
                 title,
                 Form( ".x paracoor.C(\"%s\")", fName ),
                 "Plots parallel coordinates for classifiers and input variables (macro paracoor.C, requires ROOT >= 5.17)",
                 buttonType, defaultRequiredClassifier );

   // parallel coordinates only exist since ROOT 5.17
   #if ROOT_VERSION_CODE < ROOT_VERSION(5,17,0)
   TMVAGui_inactiveButtons.push_back( title );
   #endif

   ActionButton( cbar,  
                 Form( "(%i) PDFs of Classifiers (requires \"CreateMVAPdfs\" option set)", ++ic ),
                 Form( ".x probas.C(\"%s\")", fName ),
                 "Plots the PDFs of the classifier output distributions for signal and background - if requested (macro probas.C)",
                 buttonType, defaultRequiredClassifier );

   ActionButton( cbar,  
                 Form( "(%i) Likelihood Reference Distributiuons", ++ic),
                 Form( ".x likelihoodrefs.C(\"%s\")", fName ), 
                 "Plots to verify the likelihood reference distributions (macro likelihoodrefs.C)",
                 buttonType, "Likelihood" );

   ActionButton( cbar,  
                 Form( "(%ia) Network Architecture (MLP)", ++ic ),
                 Form( ".x network.C(\"%s\")", fName ), 
                 "Plots the MLP weights (macro network.C)",
                 buttonType, "MLP" );

   ActionButton( cbar,  
                 Form( "(%ib) Network Convergence Test (MLP)", ic ),
                 Form( ".x annconvergencetest.C(\"%s\")", fName ), 
                 "Plots error estimator versus training epoch for training and test samples (macro annconvergencetest.C)",
                 buttonType, "MLP" );

   ActionButton( cbar,  
                 Form( "(%i) Decision Trees (BDT)", ++ic ),
                 Form( ".x BDT.C+(\"%s\")", fName ),
                 "Plots the Decision Trees trained by BDT algorithms (macro BDT.C(itree,...))",
                 buttonType, "BDT" );

   ActionButton( cbar,  
                 Form( "(%i) Decision Tree Control Plots (BDT)", ++ic ),
                 Form( ".x BDTControlPlots.C(\"%s\")", fName ),
                 "Plots to monitor boosting and pruning of decision trees (macro BDTControlPlots.C)",
                 buttonType, "BDT" );
   //    ActionButton( cbar,  
   //                  Form( "(%i) Monitor Decision Tree Boosting", ++ic ),
   //                  Form( ".x BDTBoostWatch.C+(\"%s\")", fName ),
   //                  "Plots separation obtained by BDT method as function of boosting steps (macro BDTBoostWatch.C(itree,...))",
   //                  buttonType, "BDT" );

   //    ActionButton( cbar,  
   //                  Form( "(%i) Rule Ensemble Importance Plots (RuleFit)", ++ic ),
   //                  Form( ".x rulevis.C(\"%s\",0)", fName ),
   //                  "Plots all input variables with rule ensemble weights, including linear terms (macro rulevis.C)",
   //                  buttonType, "RuleFit" );

   ActionButton( cbar,  
                 Form( "(%i) Plot Foams (PDEFoam)", ++ic ),
                 Form( ".x PlotFoams.C", fName ),
                 "Plot Foams (macro PlotFoams.C)",
                 buttonType, "PDEFoam" );

   ActionButton( cbar,  
                 Form( "(%i) General Boost Control Plots", ++ic ),
                 Form( ".x BoostControlPlots.C(\"%s\")", fName ),
                 "Plots to monitor boosting of general classifiers (macro BoostControlPlots.C)",
                 buttonType, "Boost" );

   cbar->AddSeparator();

   cbar->AddButton( Form( "(%i) Quit", ++ic ),   ".q", "Quit", buttonType );

   // set the style 
   cbar->SetTextColor("black");

   // there seems to be a bug in ROOT: font jumps back to default after pressing on >2 different buttons
   // cbar->SetFont("-adobe-helvetica-bold-r-*-*-12-*-*-*-*-*-iso8859-1");
   
   // draw
   cbar->Show();

   // indicate inactive buttons
   for (UInt_t i=0; i<TMVAGui_inactiveButtons.size(); i++) cbar->SetButtonState( TMVAGui_inactiveButtons[i], 3 );
   if (TMVAGui_inactiveButtons.size() > 0) {
      cout << "=== Note: inactive buttons indicate that the corresponding classifiers were not trained ===" << endl;
   }

   gROOT->SaveContext();
}
