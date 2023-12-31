import ROOT
import numpy as np
import pickle

variables = ['Lc_PT','XiccPi1_PT','XiccPi2_PT', 'XiccK_PT']

def load_data(signal_filename, background_filename):
    # Read data from ROOT files
    data_sig = ROOT.RDataFrame("Events", signal_filename).AsNumpy()
    data_bkg = ROOT.RDataFrame("Events", background_filename).AsNumpy()
 
    # Convert inputs to format readable by machine learning tools
    x_sig = np.vstack([data_sig[var] for var in variables]).T
    x_bkg = np.vstack([data_bkg[var] for var in variables]).T
    x = np.vstack([x_sig, x_bkg])
 
    # Create labels
    num_sig = x_sig.shape[0]
    num_bkg = x_bkg.shape[0]
    y = np.hstack([np.ones(num_sig), np.zeros(num_bkg)])
 
    # Compute weights balancing both classes
    num_all = num_sig + num_bkg
    w = np.hstack([np.ones(num_sig) * num_all / num_sig, np.ones(num_bkg) * num_all / num_bkg])
 
    return x, y, w
 
if __name__ == "__main__":
    # Load data
    x, y, w = load_data("train_signal.root", "train_background.root")
 
    # Fit xgboost model
    from xgboost import XGBClassifier
    bdt = XGBClassifier(max_depth=3, n_estimators=500)
    bdt.fit(x, y, sample_weight=w)
 
    # Save model in TMVA format
    print("Training done on ",x.shape[0],"events. Saving model in tmva101.root")
    ROOT.TMVA.Experimental.SaveXGBoost(bdt, "myBDT", "tmva101.root", num_inputs=x.shape[1])