// Class: ReadMLP
// Automatically generated by MethodBase::MakeClass
//

/* configuration options =====================================================

#GEN -*-*-*-*-*-*-*-*-*-*-*- general info -*-*-*-*-*-*-*-*-*-*-*-

Method         : MLP::MLP
TMVA Release   : 4.2.1         [262657]
ROOT Release   : 6.26/08       [399880]
Creator        : pgaigne
Date           : Thu Jun 22 15:14:19 2023
Host           : Linux 28693209b56e 5.15.0-1022-azure #27~20.04.1-Ubuntu SMP Mon Oct 17 02:03:50 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux
Dir            : /afs/cern.ch/user/p/pgaigne/excitedBaryons/TMVA
Training events: 7283
Analysis type  : [Classification]


#OPT -*-*-*-*-*-*-*-*-*-*-*-*- options -*-*-*-*-*-*-*-*-*-*-*-*-

# Set by User:
NCycles: "600" [Number of training cycles]
HiddenLayers: "N+5" [Specification of hidden layer architecture]
NeuronType: "tanh" [Neuron activation function type]
V: "False" [Verbose output (short form of "VerbosityLevel" below - overrides the latter one)]
VarTransform: "N" [List of variable transformations performed before training, e.g., "D_Background,P_Signal,G,N_AllClasses" for: "Decorrelation, PCA-transformation, Gaussianisation, Normalisation, each for the given class of events ('AllClasses' denotes all events of all classes, if no class indication is given, 'All' is assumed)"]
H: "True" [Print method-specific help message]
TestRate: "5" [Test for overtraining performed at each #th epochs]
UseRegulator: "False" [Use regulator to avoid over-training]
# Default:
RandomSeed: "1" [Random seed for initial synapse weights (0 means unique seed for each run; default value '1')]
EstimatorType: "CE" [MSE (Mean Square Estimator) for Gaussian Likelihood or CE(Cross-Entropy) for Bernoulli Likelihood]
NeuronInputType: "sum" [Neuron input function type]
VerbosityLevel: "Default" [Verbosity level]
CreateMVAPdfs: "False" [Create PDFs for classifier outputs (signal and background)]
IgnoreNegWeightsInTraining: "False" [Events with negative weights are ignored in the training (but are included for testing and performance evaluation)]
TrainingMethod: "BP" [Train with Back-Propagation (BP), BFGS Algorithm (BFGS), or Genetic Algorithm (GA - slower and worse)]
LearningRate: "2.000000e-02" [ANN learning rate parameter]
DecayRate: "1.000000e-02" [Decay rate for learning parameter]
EpochMonitoring: "False" [Provide epoch-wise monitoring plots according to TestRate (caution: causes big ROOT output file!)]
Sampling: "1.000000e+00" [Only 'Sampling' (randomly selected) events are trained each epoch]
SamplingEpoch: "1.000000e+00" [Sampling is used for the first 'SamplingEpoch' epochs, afterwards, all events are taken for training]
SamplingImportance: "1.000000e+00" [ The sampling weights of events in epochs which successful (worse estimator than before) are multiplied with SamplingImportance, else they are divided.]
SamplingTraining: "True" [The training sample is sampled]
SamplingTesting: "False" [The testing sample is sampled]
ResetStep: "50" [How often BFGS should reset history]
Tau: "3.000000e+00" [LineSearch "size step"]
BPMode: "sequential" [Back-propagation learning mode: sequential or batch]
BatchSize: "-1" [Batch size: number of events/batch, only set if in Batch Mode, -1 for BatchSize=number_of_events]
ConvergenceImprove: "1.000000e-30" [Minimum improvement which counts as improvement (<0 means automatic convergence check is turned off)]
ConvergenceTests: "-1" [Number of steps (without improvement) required for convergence (<0 means automatic convergence check is turned off)]
UpdateLimit: "10000" [Maximum times of regulator update]
CalculateErrors: "False" [Calculates inverse Hessian matrix at the end of the training to be able to calculate the uncertainties of an MVA value]
WeightRange: "1.000000e+00" [Take the events for the estimator calculations from small deviations from the desired value to large deviations only over the weight range]
##


#VAR -*-*-*-*-*-*-*-*-*-*-*-* variables *-*-*-*-*-*-*-*-*-*-*-*-

NVar 5
log(TMath::Max(10e-10,C_ENDVERTEX_CHI2/C_ENDVERTEX_NDOF))    log_TMath_Max_10e_M_10,C_ENDVERTEX_CHI2_D_C_ENDVERTEX_NDOF__ log(TMath::Max(10e-10,C_ENDVERTEX_CHI2/C_ENDVERTEX_NDOF))    log_C_ENDVERTEX_CHI2_NDOF                                                                                                     'F'    [-18.805103302,3.21725702286]
C_PT                          C_PT                          C_PT                          C_PT                                                            'F'    [2822.02880859,36407.390625]
log(Pi_IPCHI2_OWNPV)          log_Pi_IPCHI2_OWNPV_          log(Pi_IPCHI2_OWNPV)          log(Pi_IPCHI2_OWNPV)                                            'F'    [-11.8929748535,2.77253508568]
Pi_ProbNNk                    Pi_ProbNNk                    Pi_ProbNNk                    Pi_ProbNNk                                                      'F'    [0.500148236752,0.999738037586]
C_KaonDTF_K_PT                C_KaonDTF_K_PT                C_KaonDTF_K_PT                C_KaonDTF_K_PT                                                  'F'    [200.605499268,9953.72753906]
NSpec 3
C_M                           C_M                           C_M                           F                                                               'F'    [3682.02172852,4613.16162109]
Xicc_M_DTF_Lc_PV              Xicc_M_DTF_Lc_PV              Xicc_M_DTF_Lc_PV              F                                                               'F'    [3541.01269531,3700.95117188]
Lc_M                          Lc_M                          Lc_M                          F                                                               'F'    [2270.01342773,2305.98876953]


============================================================================ */

#include <array>
#include <vector>
#include <cmath>
#include <string>
#include <iostream>

#ifndef IClassifierReader__def
#define IClassifierReader__def

class IClassifierReader {

 public:

   // constructor
   IClassifierReader() : fStatusIsClean( true ) {}
   virtual ~IClassifierReader() {}

   // return classifier response
   virtual double GetMvaValue( const std::vector<double>& inputValues ) const = 0;

   // returns classifier status
   bool IsStatusClean() const { return fStatusIsClean; }

 protected:

   bool fStatusIsClean;
};

#endif

class ReadMLP : public IClassifierReader {

 public:

   // constructor
   ReadMLP( std::vector<std::string>& theInputVars )
      : IClassifierReader(),
        fClassName( "ReadMLP" ),
        fNvars( 5 )
   {
      // the training input variables
      const char* inputVars[] = { "log(TMath::Max(10e-10,C_ENDVERTEX_CHI2/C_ENDVERTEX_NDOF))", "C_PT", "log(Pi_IPCHI2_OWNPV)", "Pi_ProbNNk", "C_KaonDTF_K_PT" };

      // sanity checks
      if (theInputVars.size() <= 0) {
         std::cout << "Problem in class \"" << fClassName << "\": empty input vector" << std::endl;
         fStatusIsClean = false;
      }

      if (theInputVars.size() != fNvars) {
         std::cout << "Problem in class \"" << fClassName << "\": mismatch in number of input values: "
                   << theInputVars.size() << " != " << fNvars << std::endl;
         fStatusIsClean = false;
      }

      // validate input variables
      for (size_t ivar = 0; ivar < theInputVars.size(); ivar++) {
         if (theInputVars[ivar] != inputVars[ivar]) {
            std::cout << "Problem in class \"" << fClassName << "\": mismatch in input variable names" << std::endl
                      << " for variable [" << ivar << "]: " << theInputVars[ivar].c_str() << " != " << inputVars[ivar] << std::endl;
            fStatusIsClean = false;
         }
      }

      // initialize min and max vectors (for normalisation)
      fVmin[0] = -1;
      fVmax[0] = 1;
      fVmin[1] = -1;
      fVmax[1] = 1;
      fVmin[2] = -1;
      fVmax[2] = 0.99999988079071;
      fVmin[3] = -1;
      fVmax[3] = 1;
      fVmin[4] = -1;
      fVmax[4] = 1;

      // initialize input variable types
      fType[0] = 'F';
      fType[1] = 'F';
      fType[2] = 'F';
      fType[3] = 'F';
      fType[4] = 'F';

      // initialize constants
      Initialize();

      // initialize transformation
      InitTransform();
   }

   // destructor
   virtual ~ReadMLP() {
      Clear(); // method-specific
   }

   // the classifier response
   // "inputValues" is a vector of input values in the same order as the
   // variables given to the constructor
   double GetMvaValue( const std::vector<double>& inputValues ) const override;

 private:

   // method-specific destructor
   void Clear();

   // input variable transformation

   double fOff_1[3][5];
   double fScal_1[3][5];
   void InitTransform_1();
   void Transform_1( std::vector<double> & iv, int sigOrBgd ) const;
   void InitTransform();
   void Transform( std::vector<double> & iv, int sigOrBgd ) const;

   // common member variables
   const char* fClassName;

   const size_t fNvars;
   size_t GetNvar()           const { return fNvars; }
   char   GetType( int ivar ) const { return fType[ivar]; }

   // normalisation of input variables
   double fVmin[5];
   double fVmax[5];
   double NormVariable( double x, double xmin, double xmax ) const {
      // normalise to output range: [-1, 1]
      return 2*(x - xmin)/(xmax - xmin) - 1.0;
   }

   // type of input variable: 'F' or 'I'
   char   fType[5];

   // initialize internal variables
   void Initialize();
   double GetMvaValue__( const std::vector<double>& inputValues ) const;

   // private members (method specific)

   double ActivationFnc(double x) const;
   double OutputActivationFnc(double x) const;

   double fWeightMatrix0to1[11][6];   // weight matrix from layer 0 to 1
   double fWeightMatrix1to2[1][11];   // weight matrix from layer 1 to 2

};

inline void ReadMLP::Initialize()
{
   // build network structure
   // weight matrix from layer 0 to 1
   fWeightMatrix0to1[0][0] = 0.487607296768114;
   fWeightMatrix0to1[1][0] = 0.984580823895199;
   fWeightMatrix0to1[2][0] = -0.555194136898494;
   fWeightMatrix0to1[3][0] = 1.61321937461184;
   fWeightMatrix0to1[4][0] = -2.49536143293028;
   fWeightMatrix0to1[5][0] = 0.0526511889017591;
   fWeightMatrix0to1[6][0] = -1.36831760885833;
   fWeightMatrix0to1[7][0] = 3.98748492656596;
   fWeightMatrix0to1[8][0] = -1.50610337808593;
   fWeightMatrix0to1[9][0] = -1.00211694476547;
   fWeightMatrix0to1[0][1] = -2.53940166863772;
   fWeightMatrix0to1[1][1] = -0.111648128480746;
   fWeightMatrix0to1[2][1] = -2.66502168923549;
   fWeightMatrix0to1[3][1] = -0.705496323853402;
   fWeightMatrix0to1[4][1] = -0.30520167393844;
   fWeightMatrix0to1[5][1] = 1.15262412371528;
   fWeightMatrix0to1[6][1] = 0.256958160959019;
   fWeightMatrix0to1[7][1] = 0.631621714810026;
   fWeightMatrix0to1[8][1] = -1.66202549120832;
   fWeightMatrix0to1[9][1] = 2.38959111347373;
   fWeightMatrix0to1[0][2] = -0.0784502141958563;
   fWeightMatrix0to1[1][2] = -1.72383143413469;
   fWeightMatrix0to1[2][2] = 3.87857176519136;
   fWeightMatrix0to1[3][2] = -0.655838839310931;
   fWeightMatrix0to1[4][2] = 1.08661685734236;
   fWeightMatrix0to1[5][2] = 0.301677512751647;
   fWeightMatrix0to1[6][2] = 4.75746717441209;
   fWeightMatrix0to1[7][2] = -2.49298015779695;
   fWeightMatrix0to1[8][2] = -2.14770599674277;
   fWeightMatrix0to1[9][2] = 0.881129227357861;
   fWeightMatrix0to1[0][3] = -1.67127005929744;
   fWeightMatrix0to1[1][3] = 3.26403632429213;
   fWeightMatrix0to1[2][3] = 0.999201484507621;
   fWeightMatrix0to1[3][3] = 0.367029920571449;
   fWeightMatrix0to1[4][3] = 0.661159032707443;
   fWeightMatrix0to1[5][3] = -0.32986733677235;
   fWeightMatrix0to1[6][3] = -0.103015216366528;
   fWeightMatrix0to1[7][3] = -0.24444515612007;
   fWeightMatrix0to1[8][3] = -0.324047738667641;
   fWeightMatrix0to1[9][3] = 1.16880673591875;
   fWeightMatrix0to1[0][4] = -1.45950178789098;
   fWeightMatrix0to1[1][4] = 3.14990929987187;
   fWeightMatrix0to1[2][4] = 4.06417127186234;
   fWeightMatrix0to1[3][4] = 3.02912336310623;
   fWeightMatrix0to1[4][4] = 0.435017391817935;
   fWeightMatrix0to1[5][4] = -6.10054640518836;
   fWeightMatrix0to1[6][4] = -0.416992286159999;
   fWeightMatrix0to1[7][4] = 0.330945565792638;
   fWeightMatrix0to1[8][4] = 2.27271613361153;
   fWeightMatrix0to1[9][4] = 1.37668323407931;
   fWeightMatrix0to1[0][5] = 2.45947641381024;
   fWeightMatrix0to1[1][5] = -0.204345147779611;
   fWeightMatrix0to1[2][5] = -3.84602510959052;
   fWeightMatrix0to1[3][5] = 2.34047258606707;
   fWeightMatrix0to1[4][5] = -1.41621343590713;
   fWeightMatrix0to1[5][5] = -5.75195361057529;
   fWeightMatrix0to1[6][5] = -3.88734748319559;
   fWeightMatrix0to1[7][5] = -1.83334437393881;
   fWeightMatrix0to1[8][5] = 1.83232905610811;
   fWeightMatrix0to1[9][5] = 1.63549111212728;
   // weight matrix from layer 1 to 2
   fWeightMatrix1to2[0][0] = -3.59917344849972;
   fWeightMatrix1to2[0][1] = 0.676978295798755;
   fWeightMatrix1to2[0][2] = -2.86328824579795;
   fWeightMatrix1to2[0][3] = 0.577831745665267;
   fWeightMatrix1to2[0][4] = 1.87779806754477;
   fWeightMatrix1to2[0][5] = -2.24506796055079;
   fWeightMatrix1to2[0][6] = -1.23229880483556;
   fWeightMatrix1to2[0][7] = -1.09997580358202;
   fWeightMatrix1to2[0][8] = -0.913317603164729;
   fWeightMatrix1to2[0][9] = 0.421799530202294;
   fWeightMatrix1to2[0][10] = -2.62722126578826;
}

inline double ReadMLP::GetMvaValue__( const std::vector<double>& inputValues ) const
{
   if (inputValues.size() != (unsigned int)5) {
      std::cout << "Input vector needs to be of size " << 5 << std::endl;
      return 0;
   }

   std::array<double, 11> fWeights1 {{}};
   std::array<double, 1> fWeights2 {{}};
   fWeights1.back() = 1.;

   // layer 0 to 1
   for (int o=0; o<10; o++) {
      std::array<double, 6> buffer; // no need to initialise
      for (int i = 0; i<6 - 1; i++) {
         buffer[i] = fWeightMatrix0to1[o][i] * inputValues[i];
      } // loop over i
      buffer.back() = fWeightMatrix0to1[o][5];
      for (int i=0; i<6; i++) {
         fWeights1[o] += buffer[i];
      } // loop over i
    } // loop over o
   for (int o=0; o<10; o++) {
      fWeights1[o] = ActivationFnc(fWeights1[o]);
   } // loop over o
   // layer 1 to 2
   for (int o=0; o<1; o++) {
      std::array<double, 11> buffer; // no need to initialise
      for (int i=0; i<11; i++) {
         buffer[i] = fWeightMatrix1to2[o][i] * fWeights1[i];
      } // loop over i
      for (int i=0; i<11; i++) {
         fWeights2[o] += buffer[i];
      } // loop over i
    } // loop over o
   for (int o=0; o<1; o++) {
      fWeights2[o] = OutputActivationFnc(fWeights2[o]);
   } // loop over o

   return fWeights2[0];
}

double ReadMLP::ActivationFnc(double x) const {
   // fast hyperbolic tan approximation
   if (x > 4.97) return 1;
   if (x < -4.97) return -1;
   float x2 = x * x;
   float a = x * (135135.0f + x2 * (17325.0f + x2 * (378.0f + x2)));
   float b = 135135.0f + x2 * (62370.0f + x2 * (3150.0f + x2 * 28.0f));
   return a / b;
}
double ReadMLP::OutputActivationFnc(double x) const {
   // sigmoid
   return 1.0/(1.0+exp(-x));
}

// Clean up
inline void ReadMLP::Clear()
{
}
inline double ReadMLP::GetMvaValue( const std::vector<double>& inputValues ) const
{
   // classifier response value
   double retval = 0;

   // classifier response, sanity check first
   if (!IsStatusClean()) {
      std::cout << "Problem in class \"" << fClassName << "\": cannot return classifier response"
                << " because status is dirty" << std::endl;
   }
   else {
         std::vector<double> iV(inputValues);
         Transform( iV, -1 );
         retval = GetMvaValue__( iV );
   }

   return retval;
}

//_______________________________________________________________________
inline void ReadMLP::InitTransform_1()
{
   double fMin_1[3][5];
   double fMax_1[3][5];
   // Normalization transformation, initialisation
   fMin_1[0][0] = -16.4959335327;
   fMax_1[0][0] = 3.00290846825;
   fScal_1[0][0] = 2.0/(fMax_1[0][0]-fMin_1[0][0]);
   fOff_1[0][0] = fMin_1[0][0]*fScal_1[0][0]+1.;
   fMin_1[1][0] = -18.805103302;
   fMax_1[1][0] = 3.21725702286;
   fScal_1[1][0] = 2.0/(fMax_1[1][0]-fMin_1[1][0]);
   fOff_1[1][0] = fMin_1[1][0]*fScal_1[1][0]+1.;
   fMin_1[2][0] = -18.805103302;
   fMax_1[2][0] = 3.21725702286;
   fScal_1[2][0] = 2.0/(fMax_1[2][0]-fMin_1[2][0]);
   fOff_1[2][0] = fMin_1[2][0]*fScal_1[2][0]+1.;
   fMin_1[0][1] = 4080.97241211;
   fMax_1[0][1] = 36407.390625;
   fScal_1[0][1] = 2.0/(fMax_1[0][1]-fMin_1[0][1]);
   fOff_1[0][1] = fMin_1[0][1]*fScal_1[0][1]+1.;
   fMin_1[1][1] = 2822.02880859;
   fMax_1[1][1] = 30501.7265625;
   fScal_1[1][1] = 2.0/(fMax_1[1][1]-fMin_1[1][1]);
   fOff_1[1][1] = fMin_1[1][1]*fScal_1[1][1]+1.;
   fMin_1[2][1] = 2822.02880859;
   fMax_1[2][1] = 36407.390625;
   fScal_1[2][1] = 2.0/(fMax_1[2][1]-fMin_1[2][1]);
   fOff_1[2][1] = fMin_1[2][1]*fScal_1[2][1]+1.;
   fMin_1[0][2] = -9.33639526367;
   fMax_1[0][2] = 2.76286363602;
   fScal_1[0][2] = 2.0/(fMax_1[0][2]-fMin_1[0][2]);
   fOff_1[0][2] = fMin_1[0][2]*fScal_1[0][2]+1.;
   fMin_1[1][2] = -11.8929748535;
   fMax_1[1][2] = 2.77253508568;
   fScal_1[1][2] = 2.0/(fMax_1[1][2]-fMin_1[1][2]);
   fOff_1[1][2] = fMin_1[1][2]*fScal_1[1][2]+1.;
   fMin_1[2][2] = -11.8929748535;
   fMax_1[2][2] = 2.77253508568;
   fScal_1[2][2] = 2.0/(fMax_1[2][2]-fMin_1[2][2]);
   fOff_1[2][2] = fMin_1[2][2]*fScal_1[2][2]+1.;
   fMin_1[0][3] = 0.500277757645;
   fMax_1[0][3] = 0.999738037586;
   fScal_1[0][3] = 2.0/(fMax_1[0][3]-fMin_1[0][3]);
   fOff_1[0][3] = fMin_1[0][3]*fScal_1[0][3]+1.;
   fMin_1[1][3] = 0.500148236752;
   fMax_1[1][3] = 0.999481976032;
   fScal_1[1][3] = 2.0/(fMax_1[1][3]-fMin_1[1][3]);
   fOff_1[1][3] = fMin_1[1][3]*fScal_1[1][3]+1.;
   fMin_1[2][3] = 0.500148236752;
   fMax_1[2][3] = 0.999738037586;
   fScal_1[2][3] = 2.0/(fMax_1[2][3]-fMin_1[2][3]);
   fOff_1[2][3] = fMin_1[2][3]*fScal_1[2][3]+1.;
   fMin_1[0][4] = 236.892456055;
   fMax_1[0][4] = 7539.71289062;
   fScal_1[0][4] = 2.0/(fMax_1[0][4]-fMin_1[0][4]);
   fOff_1[0][4] = fMin_1[0][4]*fScal_1[0][4]+1.;
   fMin_1[1][4] = 200.605499268;
   fMax_1[1][4] = 9953.72753906;
   fScal_1[1][4] = 2.0/(fMax_1[1][4]-fMin_1[1][4]);
   fOff_1[1][4] = fMin_1[1][4]*fScal_1[1][4]+1.;
   fMin_1[2][4] = 200.605499268;
   fMax_1[2][4] = 9953.72753906;
   fScal_1[2][4] = 2.0/(fMax_1[2][4]-fMin_1[2][4]);
   fOff_1[2][4] = fMin_1[2][4]*fScal_1[2][4]+1.;
}

//_______________________________________________________________________
inline void ReadMLP::Transform_1( std::vector<double>& iv, int cls) const
{
   // Normalization transformation
   if (cls < 0 || cls > 2) {
   if (2 > 1 ) cls = 2;
      else cls = 2;
   }
   const int nVar = 5;

   // get indices of used variables

   // define the indices of the variables which are transformed by this transformation
   static std::vector<int> indicesGet;
   static std::vector<int> indicesPut;

   if ( indicesGet.empty() ) {
      indicesGet.reserve(fNvars);
      indicesGet.push_back( 0);
      indicesGet.push_back( 1);
      indicesGet.push_back( 2);
      indicesGet.push_back( 3);
      indicesGet.push_back( 4);
   }
   if ( indicesPut.empty() ) {
      indicesPut.reserve(fNvars);
      indicesPut.push_back( 0);
      indicesPut.push_back( 1);
      indicesPut.push_back( 2);
      indicesPut.push_back( 3);
      indicesPut.push_back( 4);
   }

   static std::vector<double> dv;
   dv.resize(nVar);
   for (int ivar=0; ivar<nVar; ivar++) dv[ivar] = iv[indicesGet.at(ivar)];
   for (int ivar=0;ivar<5;ivar++) {
      double offset = fOff_1[cls][ivar];
      double scale  = fScal_1[cls][ivar];
      iv[indicesPut.at(ivar)] = scale*dv[ivar]-offset;
   }
}

//_______________________________________________________________________
inline void ReadMLP::InitTransform()
{
   InitTransform_1();
}

//_______________________________________________________________________
inline void ReadMLP::Transform( std::vector<double>& iv, int sigOrBgd ) const
{
   Transform_1( iv, sigOrBgd );
}
