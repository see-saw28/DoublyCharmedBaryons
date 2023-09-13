import uproot
import root_pandas
import pandas as pd
import numpy as np

out_file = open("OverlapDuplicatesRemoval_controlRS_2016.txt","w+")

############ Reading data ############
######################################
RS_2016_incl = ("/nfs/users/dbobulska/Xiccp_studies/2016/Data/control_channel_XicpPip/RS_full_dataset/hlt2_inclusive_line/"
                 "TMVAoutput/Data_2016_Xicc_inclusive_TMVAapplication_allMVAmethods_moreBranches_mvaCut.root")

cut = "Xic_M > 2450 & Xic_M < 2488 & DM > 3500 & DM < 3800 & PPi_angle > 0.0005 & PPi1_angle > 0.0005 & PiPi1_angle > 0.0005 & PK_angle > 0.0005 & KPi_angle > 0.0005 & KPi1_angle > 0.0005 & MVA_MLP > 0.6"

bkg_df_2016_incl = root_pandas.read_root(RS_2016_incl,where=cut)
bkg_df_2016_incl.reset_index(inplace=True)

out_file.write("Entries in 2016 HLT2 inclusive data tree: {0}\n".format(bkg_df_2016_incl.shape[0]))
out_file.write("----------------------------------------------\n")

bkg_df_2016_incl = bkg_df_2016_incl.drop_duplicates(subset=['DM','eventNumber','runNumber'])
bkg_df_2016_incl.sort_values(['eventNumber','DM'], inplace = True)
mask_remove = bkg_df_2016_incl.groupby(['eventNumber']).DM.apply(lambda x: x.diff().abs() < 1.0)
bkg_df_2016_incl = bkg_df_2016_incl[~mask_remove]

out_file.write("Final number of events: {0}\n".format(bkg_df_2016_incl.shape[0]))
out_file.write("----------------------------------------------\n")

######### Saving outputfile ##########
######################################
bkg_df_2016_incl.to_root("/nfs/users/dbobulska/Xiccp_studies/2016/Data/control_channel_XicpPip/RS_full_dataset/TMVAoutput/"
                         "Data_2016_Xicc_TMVAapplication_allMVAmethods_moreBranches_OverlapRemoved_afterMVA_MLP096.root",
                         key="DecayTree")

out_file.close()
