import uproot
import root_pandas
import pandas as pd
import numpy as np

import sys
import argparse

parser = argparse.ArgumentParser(description="Input and output files for the script.")
parser.add_argument('fileOld', type=str)
parser.add_argument('fileNew', type=str)
args = parser.parse_args()

input_file = args.fileOld
output_file = args.fileNew

data_tree = uproot.open(input_file)["DecayTree"]
#df_data = root_pandas.read_root(input_file)
df_data = data_tree.pandas.df()

if ("control_channel_XicpPip" in input_file):
   df_data.eval('final_weight=trackingEff*GBR_weight*Event_PIDCalibEffWeight_combined*Xicc_TAU_256_weight',inplace=True)
   df_data.eval('final_weight_presel=trackingEff*GBR_weight*Event_PIDCalibEffWeight_presel*Xicc_TAU_256_weight',inplace=True)
else:
   df_data.eval('final_weight_noGBR=trackingEff*Event_PIDCalibEffWeight_combined',inplace=True)
   df_data.eval('final_weight=trackingEff*GBR_weight*Event_PIDCalibEffWeight_combined',inplace=True)
   df_data.eval('final_presel=trackingEff*GBR_weight*Event_PIDCalibEffWeight_presel',inplace=True)
   df_data.eval('final_weight_3471=trackingEff*GBR_weight*Event_PIDCalibEffWeight_combined*mass_weights_3471',inplace=True)
   df_data.eval('final_weight_3521=trackingEff*GBR_weight*Event_PIDCalibEffWeight_combined*mass_weights_3521',inplace=True)
   df_data.eval('final_weight_3571=trackingEff*GBR_weight*Event_PIDCalibEffWeight_combined*mass_weights_3571',inplace=True)
   df_data.eval('final_weight_3671=trackingEff*GBR_weight*Event_PIDCalibEffWeight_combined*mass_weights_3671',inplace=True)
   df_data.eval('final_weight_3771=trackingEff*GBR_weight*Event_PIDCalibEffWeight_combined*mass_weights_3771',inplace=True)
   df_data.eval('final_weight_40=trackingEff*GBR_weight*Event_PIDCalibEffWeight_combined*Xicc_TAU_40_weight',inplace=True)
   df_data.eval('final_weight_60=trackingEff*GBR_weight*Event_PIDCalibEffWeight_combined*Xicc_TAU_60_weight',inplace=True)
   df_data.eval('final_weight_100=trackingEff*GBR_weight*Event_PIDCalibEffWeight_combined*Xicc_TAU_100_weight',inplace=True)
   df_data.eval('final_weight_120=trackingEff*GBR_weight*Event_PIDCalibEffWeight_combined*Xicc_TAU_120_weight',inplace=True)
   df_data.eval('final_weight_140=trackingEff*GBR_weight*Event_PIDCalibEffWeight_combined*Xicc_TAU_140_weight',inplace=True)
   df_data.eval('final_weight_160=trackingEff*GBR_weight*Event_PIDCalibEffWeight_combined*Xicc_TAU_160_weight',inplace=True)
   df_data.eval('final_weight_200=trackingEff*GBR_weight*Event_PIDCalibEffWeight_combined*Xicc_TAU_200_weight',inplace=True)
   df_data.eval('final_weight_250=trackingEff*GBR_weight*Event_PIDCalibEffWeight_combined*Xicc_TAU_250_weight',inplace=True)
   df_data.eval('final_weight_300=trackingEff*GBR_weight*Event_PIDCalibEffWeight_combined*Xicc_TAU_300_weight',inplace=True)
   df_data.eval('final_weight_350=trackingEff*GBR_weight*Event_PIDCalibEffWeight_combined*Xicc_TAU_350_weight',inplace=True)

df_data.to_root(output_file,key="DecayTree")
