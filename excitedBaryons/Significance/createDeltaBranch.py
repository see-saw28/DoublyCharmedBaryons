import ROOT
from array import array

def clone_and_shift_branch(file_name, tree_name, old_branch_name, new_branch_name, shift_value):
    file = ROOT.TFile(file_name, "UPDATE")
    tree = file.Get(tree_name)
    
    old_branch = tree.GetBranch(old_branch_name)
    old_value = array('d', [0.0])
    tree.SetBranchAddress(old_branch_name, old_value)
    
    new_value = array('d', [0.0])
    new_branch = tree.Branch(new_branch_name, new_value, new_branch_name + "/D")
    
    for i in range(tree.GetEntries()):
        tree.GetEntry(i)
        
        new_value[0] = old_value[0] - shift_value
        
        new_branch.Fill()
    
    tree.Write("", ROOT.TObject.kOverwrite)
    file.Close()


# excited = 'Omega'
excited = 'Xi'

file_name = f"/eos/lhcb/user/p/pgaigne/STEP3/Run2/{excited}ccpst-RS-Run2-Lc-Loose-clone-duplicate-Tight-MVA-delta.root"
tree_name = "DecayTree"
if excited == 'Omega':
    old_branch_name = "C_KaonDTF_C_M"
    new_branch_name = "DeltaM_Omega"
    shift_value = 4115.1
elif excited == 'Xi':
    old_branch_name = "C_M_DTF_Xicc_PV"
    new_branch_name = "DeltaM_Xicc"
    shift_value = 3761.0

clone_and_shift_branch(file_name, tree_name, old_branch_name, new_branch_name, shift_value)