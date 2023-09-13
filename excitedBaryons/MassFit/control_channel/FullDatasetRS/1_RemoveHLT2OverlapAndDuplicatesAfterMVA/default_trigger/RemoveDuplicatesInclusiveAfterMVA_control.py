import uproot
import root_pandas
import pandas as pd
import numpy as np

out_file = open("ClonesDuplicatesRemoval_controlRS_InclusiveLines.txt","w+")

############ Reading data ############
######################################
RS_2016 = ("/nfs/users/dbobulska/Xiccp_studies/2016/Data/control_channel_XicpPip/RS_full_dataset/hlt2_inclusive_line/"
                 "TMVAoutput/Data_2016_Xicc_inclusive_TMVAapplication_allMVAmethods_moreBranches_mvaCut.root")
RS_2017 = ("/nfs/users/dbobulska/Xiccp_studies/2017/Data/control_channel_XicpPip/RS_full_dataset/hlt2_inclusive_line/"
                 "TMVAoutput/Data_2017_Xicc_inclusive_TMVAapplication_allMVAmethods_moreBranches_mvaCut.root")
RS_2018 = ("/nfs/users/dbobulska/Xiccp_studies/2018/Data/control_channel_XicpPip/RS_full_dataset/hlt2_inclusive_line/"
                 "TMVAoutput/Data_2018_Xicc_inclusive_TMVAapplication_allMVAmethods_moreBranches_mvaCut.root")

cut = "Xic_M > 2450 & Xic_M < 2488 & DM > 3500 & DM < 3800 & PPi_angle > 0.0005 & PPi1_angle > 0.0005 & PiPi1_angle > 0.0005 & PK_angle > 0.0005 & KPi_angle > 0.0005 & KPi1_angle > 0.0005 & MVA_MLP > 0.6"

bkg_df_2016 = root_pandas.read_root(RS_2016,where=cut)
bkg_df_2017 = root_pandas.read_root(RS_2017,where=cut)
bkg_df_2018 = root_pandas.read_root(RS_2018,where=cut)

out_file.write("Entries in 2016 HLT2 inclusive data tree: {0}\n".format(bkg_df_2016.shape[0]))
out_file.write("Entries in 2017 HLT2 inclusive data tree: {0}\n".format(bkg_df_2017.shape[0]))
out_file.write("Entries in 2018 HLT2 inclusive data tree: {0}\n".format(bkg_df_2018.shape[0]))
out_file.write("----------------------------------------------\n")

########## Removing overlap ##########
##### removal based on the same ######
## eventNumber - runNumber matching ##
###### for the same Xicc+ mass #######
######################################

bkg_df_2016 = bkg_df_2016.drop_duplicates(subset=['DM','eventNumber','runNumber'])
bkg_df_2017 = bkg_df_2017.drop_duplicates(subset=['DM','eventNumber','runNumber'])
bkg_df_2018 = bkg_df_2018.drop_duplicates(subset=['DM','eventNumber','runNumber'])

bkg_df_2016.sort_values(["eventNumber","DM"], inplace = True)
bkg_df_2017.sort_values(["eventNumber","DM"], inplace = True)
bkg_df_2018.sort_values(["eventNumber","DM"], inplace = True)

mask_remove_16 = bkg_df_2016.groupby(['eventNumber']).DM.apply(lambda x: x.diff().abs() < 1.0)
mask_remove_17 = bkg_df_2017.groupby(['eventNumber']).DM.apply(lambda x: x.diff().abs() < 1.0)
mask_remove_18 = bkg_df_2018.groupby(['eventNumber']).DM.apply(lambda x: x.diff().abs() < 1.0)

bkg_df_2016 = bkg_df_2016[~mask_remove_16]
bkg_df_2017 = bkg_df_2017[~mask_remove_17]
bkg_df_2018 = bkg_df_2018[~mask_remove_18]

out_file.write("Entries in 2016 HLT2 inclusive data tree after duplicates removal: {0}\n".format(bkg_df_2016.shape[0]))
out_file.write("Entries in 2017 HLT2 inclusive data tree after duplicates removal: {0}\n".format(bkg_df_2017.shape[0]))
out_file.write("Entries in 2018 HLT2 inclusive data tree after duplicates removal: {0}\n".format(bkg_df_2018.shape[0]))
out_file.write("----------------------------------------------\n")

######### Saving Outputfile ##########
######################################
bkg_df_2016.to_root(("/nfs/users/dbobulska/Xiccp_studies/2016/Data/control_channel_XicpPip/RS_full_dataset/hlt2_inclusive_line/"
                  "TMVAoutput/Data_2016_Xicc_TMVAapplication_allMVAmethods_moreBranches_DuplicatesClonedRemoved_afterMVA.root"),
                  key="DecayTree")
bkg_df_2017.to_root(("/nfs/users/dbobulska/Xiccp_studies/2017/Data/control_channel_XicpPip/RS_full_dataset/hlt2_inclusive_line/"
                  "TMVAoutput/Data_2017_Xicc_TMVAapplication_allMVAmethods_moreBranches_DuplicatesClonedRemoved_afterMVA.root"),
                  key="DecayTree")
bkg_df_2018.to_root(("/nfs/users/dbobulska/Xiccp_studies/2018/Data/control_channel_XicpPip/RS_full_dataset/hlt2_inclusive_line/"
                  "TMVAoutput/Data_2018_Xicc_TMVAapplication_allMVAmethods_moreBranches_DuplicatesClonedRemoved_afterMVA.root"),
                  key="DecayTree")

out_file.close()
