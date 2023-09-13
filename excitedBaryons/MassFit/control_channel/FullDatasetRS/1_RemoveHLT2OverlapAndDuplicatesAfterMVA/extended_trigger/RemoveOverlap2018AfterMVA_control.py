import uproot
import root_pandas
import pandas as pd
import numpy as np

out_file = open("OverlapDuplicatesRemoval_controlRS_2018.txt","w+")

############ Reading data ############
######################################
RS_2018_incl = ("/nfs/users/dbobulska/Xiccp_studies/2018/Data/control_channel_XicpPip/RS_full_dataset/hlt2_inclusive_line/"
                 "TMVAoutput/Data_2018_Xicc_inclusive_TMVAapplication_allMVAmethods_moreBranches_mvaCut.root")
RS_2018_excl = ("/nfs/users/dbobulska/Xiccp_studies/2018/Data/control_channel_XicpPip/RS_full_dataset/hlt2_exclusive_line/"
                 "TMVAoutput/Data_2018_Xicc_exclusive_TMVAapplication_allMVAmethods_moreBranches_mvaCut.root")
RS_2018_BDT = ("/nfs/users/dbobulska/Xiccp_studies/2018/Data/control_channel_XicpPip/RS_full_dataset/hlt2_inclusive_BDTline/"
                 "TMVAoutput/Data_2018_Xicc_inclusiveBDT_TMVAapplication_allMVAmethods_moreBranches_mvaCut.root")

cut = "Xic_M > 2450 & Xic_M < 2488 & DM > 3500 & DM < 3800 & PPi_angle > 0.0005 & PPi1_angle > 0.0005 & PiPi1_angle > 0.0005 & PK_angle > 0.0005 & KPi_angle > 0.0005 & KPi1_angle > 0.0005 & MVA_MLP > 0.6"

bkg_df_2018_incl = root_pandas.read_root(RS_2018_incl,where=cut)
bkg_df_2018_excl = root_pandas.read_root(RS_2018_excl,where=cut)
bkg_df_2018_BDT = root_pandas.read_root(RS_2018_BDT,where=cut)

out_file.write("Entries in 2018 HLT2 inclusive data tree: {0}\n".format(bkg_df_2018_incl.shape[0]))
out_file.write("Entries in 2018 HLT2 exclusive data tree: {0}\n".format(bkg_df_2018_excl.shape[0]))
out_file.write("Entries in 2018 HLT2 BDT inclusive data tree: {0}\n".format(bkg_df_2018_BDT.shape[0]))
out_file.write("----------------------------------------------\n")

bkg_df_2018_incl.reset_index(inplace=True)
bkg_df_2018_excl.reset_index(inplace=True)
bkg_df_2018_BDT.reset_index(inplace=True)

#### Flag for the HLT2 line type #####
######################################
bkg_df_2018_incl.eval("HLT2 = 0", inplace=True)
bkg_df_2018_excl.eval("HLT2 = 1", inplace=True)
bkg_df_2018_BDT.eval("HLT2 = 2", inplace=True)

########## Removing overlap ##########
##### removal based on the same ######
## eventNumber - runNumber matching ##
###### for the same Xicc+ mass #######
######################################

merged_df = pd.concat([bkg_df_2018_incl, bkg_df_2018_excl, bkg_df_2018_BDT], axis = 0, sort=True)
merged_df = merged_df.drop_duplicates(subset=['eventNumber','runNumber','DM'])
merged_df.sort_values(['eventNumber','DM'], inplace = True)
mask_remove = merged_df.groupby(['eventNumber']).DM.apply(lambda x: x.diff().abs() < 1.0)
merged_df = merged_df[~mask_remove]

out_file.write("Final number of events: {0}\n".format(merged_df.shape[0]))
out_file.write("----------------------------------------------\n")

######### Saving Outputfile ##########
######################################
merged_df.to_root(("/nfs/users/dbobulska/Xiccp_studies/2018/Data/control_channel_XicpPip/RS_full_dataset/TMVAoutput/"
                  "Data_2018_Xicc_TMVAapplication_allMVAmethods_moreBranches_OverlapRemoved_afterMVA_MLP096.root"),
                  key="DecayTree")

out_file.close()
