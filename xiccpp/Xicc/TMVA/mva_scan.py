# %% [markdown]
# ## Import modules

# %%
import os
os.environ['ZFIT_DISABLE_TF_WARNINGS'] = '1'
# numpy is used for generating, storing, and plotting data
import numpy as np
# zfit will be used for the parameter estimation in the following
import zfit
import uproot
import pandas

# in order to visualise the results of the computation, we use matplotlib
import matplotlib as mpl
if os.path.exists('lhcbStylerc'):
    mpl.rc_file('lhcbStylerc') # some plotting presets i usually use, you can find them in the git-repo
import socket
#if 'jupyter-schmitse-' in socket.gethostname():
#    mpl.rcParams['text.usetex'] = False # no latex on binder
    
import matplotlib.pyplot as plt
import mplhep
plt.style.use(mplhep.style.LHCb2)
#plt.rcParams['text.usetex'] = True
# for histograms boost has an easy api and is very fast
import hist
# for statistical distributions we can use a lot from scipy
from scipy import stats

# %% [markdown]
# ### Open ntuple



# %%
path = '/afs/cern.ch/user/p/pgaigne/xiccpp/Xicc/TMVA/job26-CombDVntuple-full-evts-TMVA.root'
path = "/eos/lhcb/user/p/pgaigne/job30-CombDVntuple-95%-evts-0-Xicc-TMVA.root"
path1 = "/eos/lhcb/user/p/pgaigne/job30-CombDVntuple-95%-evts-0-Xicc-TMVA.root"

path  = "/eos/lhcb/user/p/pgaigne/Collision-2016-MU-Xicc-job38-MVA.root"
path1 = "/eos/lhcb/user/p/pgaigne/Collision-2016-MD-Xicc-job30-MVA.root"

year = 2018
mva = 'rec-SB'


if mva == 'rec':
    if year == 2016 :
        paths=["/eos/lhcb/user/p/pgaigne/job74-DV-Xiccpp-Collision-2016-MD-0-MVA.root",
            "/eos/lhcb/user/p/pgaigne/job74-DV-Xiccpp-Collision-2016-MD-1-MVA.root",
            "/eos/lhcb/user/p/pgaigne/job75-DV-Xiccpp-Collision-2016-MU-0-MVA.root",
            "/eos/lhcb/user/p/pgaigne/job75-DV-Xiccpp-Collision-2016-MU-1-MVA.root"]

    # paths=["/eos/lhcb/user/p/pgaigne/job74-DV-Xiccpp-Collision-2016-MD-0-MVA-WS.root",
    #        "/eos/lhcb/user/p/pgaigne/job74-DV-Xiccpp-Collision-2016-MD-1-MVA-WS.root",
    #        "/eos/lhcb/user/p/pgaigne/job75-DV-Xiccpp-Collision-2016-MU-0-MVA-WS.root",
    #        "/eos/lhcb/user/p/pgaigne/job75-DV-Xiccpp-Collision-2016-MU-1-MVA-WS.root"]

    elif year == 2017 :
        paths=["/eos/lhcb/user/p/pgaigne/job78-DV-Xiccpp-Collision-2017-MD-0-MVA.root",
            "/eos/lhcb/user/p/pgaigne/job80-DV-Xiccpp-Collision-2017-MU-0-MVA.root"]
        
    elif year == 2018 :
        paths=["/eos/lhcb/user/p/pgaigne/job79-DV-Xiccpp-Collision-2018-MD-0-MVA.root",
            "/eos/lhcb/user/p/pgaigne/job81-DV-Xiccpp-Collision-2018-MU-0-MVA.root"]
        
elif mva == 'rec-WS':
    if year == 2016 :
        paths=["/eos/lhcb/user/p/pgaigne/Collision-2016-Xiccpp-job74-75-reduced-MVA-WS.root"]


    elif year == 2017 :
        paths=["/eos/lhcb/user/p/pgaigne/Collision-2017-Xiccpp-job78-80-reduced-MVA-WS.root"]
        
    elif year == 2018 :
        paths=["/eos/lhcb/user/p/pgaigne/Collision-2018-Xiccpp-job110-111-reduced-MVA-WS.root"]
        
    elif year == "2016+2018":
        paths = ["/eos/lhcb/user/p/pgaigne/Collision-2016-Xiccpp-job74-75-reduced-MVA-WS.root",
         "/eos/lhcb/user/p/pgaigne/Collision-2018-Xiccpp-job110-111-reduced-MVA-WS.root"]


elif mva == 'rec-SB':
    if year == 2016 :
        paths=["/eos/lhcb/user/p/pgaigne/Collision-2016-Xiccpp-job74-75-reduced-MVA-SB.root"]

    elif year == 2018 :
        paths=["/eos/lhcb/user/p/pgaigne/Collision-2018-Xiccpp-job110-111-reduced-MVA-SB.root"]

    elif year == "2016+2018":
        paths = ["/eos/lhcb/user/p/pgaigne/Collision-2016-Xiccpp-job74-75-reduced-MVA-SB.root",
         "/eos/lhcb/user/p/pgaigne/Collision-2018-Xiccpp-job110-111-reduced-MVA-SB.root"]

data_df = pandas.DataFrame([])
for path in paths :
    print(f"Opening file {path}")
    file =  uproot.open(path)
    tree = file['DecayTree']

    branches_we_want = ["Xicc_M_DTF_Lc","Lc_M","BDT","BDTG","MLP"] 
    data_df0 = tree.arrays(expressions = branches_we_want, library='pd')

    file.close()
    
    data_df = pandas.concat([data_df0, data_df])


print("All files opened")
# file =  uproot.open(path1)
# tree = file['DecayTree']

# data_df1 = tree.arrays(expressions = branches_we_want, library='pd')

# file.close()

# data_df = pandas.concat([data_df0, data_df1])


# note, these are the maximum likelihood estimators for both the 
# mean of a distribution and the variance (std = sqrt(variance))
# create a sample with size 3000 that follow a normal distribution
zfit.settings.set_seed(1337)
gen = np.random.default_rng(seed=1337)

# %% [markdown]
# ## BDT response

# %% [markdown]
# ## Apply cut on data

# %%



# new observable and zfit data




obs_min = 3470
obs_max = 3770
obs_bin_width = 3
obs_bin = int((obs_max-obs_min)/obs_bin_width)

def plot_fit(dat: np.ndarray, basis: np.ndarray, model: np.ndarray, 
             obs: zfit.Space, nbins : int=obs_bin, smodel: np.ndarray=None,
             drawstyle: str='default', zmodel: zfit.pdf.BasePDF=None, title='LHCb 2016'):
    """
    quick plotting function to visualise data and model. 
    Takes:
     - dat: (array) the data that are fitted
     - basis: (array) the points at which the model is evaluated
     - model: (array) the model that describes the data
     - obs: (zfit Space) the space in which the model lives
     - nbins: (int) the number of bins for the data histogram
     - smodel: (array) uncertainty on model (not needed)
     - drawstyle: (str) the drawstyle of plt.plot
     - zmodel: (BasePDF) for drawing submodels
    Returns:
     - None
    """
    # for normalising the pdf, scaled pdf = pdf * yield * area / bins
    limits = obs.limits 
    area = obs.area().numpy()

    # data in histogram over the full observable space
    histo = hist.Hist(hist.axis.Regular(nbins, *limits))
    histo.fill(dat)

    # the figure with an errorbar for the data and a line for the model
    fig, ax = plt.subplots()
    art_data = ax.errorbar(histo.axes.centers[0], histo.values(), 
                           xerr=histo.axes.widths[0]/2,
                           yerr=np.sqrt(histo.values()), fmt='.', 
                           label='Data', color='black', zorder=10)
    art_model = ax.plot(basis, model * area/nbins, color='darkturquoise', 
                        label='Model', zorder=8, drawstyle=drawstyle)[0]
    
    # if we have the uncertainty on the model we draw it as contour
    # and update the artist for the legend to reflect on the new model
    if smodel is not None:
        _art = ax.fill_between(basis, (model+smodel)*area/nbins, 
                               (model-smodel)*area/nbins, color='darkturquoise', 
                               alpha=0.5, zorder=-2)
        art_model = (art_model, _art)

    # define artists and labels for the legend
    artists = [art_data, art_model]
    labels = ['Data', 'Model']
    # if we want to plot the submodels of our model, we can iterate through
    # all of them and evaluate them at our basis. We will not bootstrap
    # all of their shape uncertainties though, this is just an illustration
    if hasattr(zmodel, 'get_models'):
        nmodels = len(zmodel.get_models())
        cmap = plt.get_cmap('autumn') # you can choose whatever you like. 
        norm = mpl.colors.Normalize(0, nmodels) # create a norm for the cmap
        pdfs = [(m.pdf(basis)*m.get_yield()).numpy()*area/nbins
                for m in zmodel.get_models()]
        names = [m.name.replace('_extended','') for m in zmodel.get_models()]
        labels.extend(names)
        for mdex, pdf in enumerate(pdfs):
            artists.append(ax.plot(basis, pdf, color=cmap(norm(mdex)), 
                                   linestyle='--', zorder=-1)[0])
        
    
    #ax.set_xlabel('$m_{cand}(\Xi_{cc}^{++})[MeV/c^2]$')
    ax.set_xlabel('$M(\Lambda_c^+ K^- \pi^+ \pi^+)[MeV/c^2]$')
    ax.set_ylabel(f'Events/( {obs_bin_width} MeV/$c^2$ )');
    
    textstr = '\n'.join((
    r'$\mu_m=%.2f \pm %.2f $ MeV/$c^2$' % (mu, mu_err ),
    r'$\sigma_m=%.2f \pm %.2f $ MeV/$c^2$' % (sigma, sigma_err ),
    r'$N_{bkg}=%.0f \pm %.0f$' % (bkg, bkg_err),
    r'$N_{sig}=%.0f \pm %.0f$' % (Y, Y_err),
    r'$S=%.1f \sigma$' % (S, ),
    r'$SNR_{%.1f \sigma}=%.2f $' % (sigma_width,SNR )))
    ax.text(0.6, 0.95, textstr, transform=ax.transAxes, fontsize=24,
        verticalalignment='top')
    
    # legend and axis labels
    ax.legend(artists, labels, loc='upper left', 
              title=title, title_fontsize=20)

obs_bkg = zfit.Space('Observable with Background', limits=(obs_min, obs_max))

# parameters for signal and background shapes
mu_signal = zfit.Parameter("mu_signal", 3621, obs_min, obs_max)
sigma_signal = zfit.Parameter("sigma_signal", 3., 1., 50.)

# be careful and check the documentation. numpy and in zfit there are
# different definitions of the slope parameter in use! 
# numpy: exp(-x/slope) zfit: exp(slope*x)
slope_bkg = zfit.Parameter('slope_bkg', 0.0021 , -1, 1)

# yields for an extended fit
n_signal = zfit.Parameter('n_signal', 100, 0, 10000)
n_bkg = zfit.Parameter('n_bkg', 10000, -200, 500000)

# create the pdfs with the extended term for the yields
gaussian = zfit.pdf.Gauss(obs=obs_bkg, mu=mu_signal, sigma=sigma_signal, name='Signal')
gaussian_ext = gaussian.create_extended(n_signal)

exponential = zfit.pdf.Exponential(obs=obs_bkg, lam=slope_bkg, name='Background')
exponential_ext = exponential.create_extended(n_bkg)

# build the model as the sum of the gaussian and the exponential functions
model = zfit.pdf.SumPDF([gaussian_ext, exponential_ext])

mva_methods={
             'BDT' :{'min_cut':0.0,'max_cut':0.25,'nb_step':26},
             'BDTG':{'min_cut':0.8,'max_cut':0.99,'nb_step':20},
             'MLP' :{'min_cut':0.7,'max_cut':0.99,'nb_step':30}
             }



significances_all = []
maxS=np.zeros(len(mva_methods))
opt_cut=np.zeros(len(mva_methods))
opt_Y=np.zeros(len(mva_methods))

mva_cuts_list = []

for k,mva_method in enumerate(mva_methods) :


    min_cut = mva_methods[mva_method]['min_cut']
    max_cut = mva_methods[mva_method]['max_cut']
    nb_step = mva_methods[mva_method]['nb_step']

    significances = np.zeros(nb_step)

    mva_cuts = np.linspace(min_cut, max_cut, nb_step)
    mva_cuts_list.append(mva_cuts)

    for i,mva_cut in enumerate(mva_cuts):

        mva_cut = round(mva_cut,4)

        data_with_cuts_df = data_df.query(f"{mva_method}>{mva_cut} & abs(Lc_M-2288)<18")

        Xicc_M_after_cut = data_with_cuts_df.Xicc_M_DTF_Lc

        data = Xicc_M_after_cut
        data_all = data.to_numpy()

        data_zfit = zfit.Data.from_numpy(obs=obs_bkg, array=data_all)

        # loss function is now extended unbinned NLL
        nll_ext = zfit.loss.ExtendedUnbinnedNLL(model=model, data=data_zfit)

        # the minimiser
        minimiser = zfit.minimize.Minuit(mode=1)

        # %% [markdown]
        # ### Minimization

        # %%
        result_ext = minimiser.minimize(nll_ext)
        result_ext.hesse(name='minuit_hesse')
        result_ext.errors(method='minuit_minos', name='minuit_minos')
        #print(result_ext)

        Y = float(n_signal)
        Y_err = result_ext.hesse()[n_signal]['error']
        mu = float(mu_signal)
        mu_err = result_ext.hesse()[mu_signal]['error']
        sigma = float(sigma_signal)
        sigma_err = result_ext.hesse()[sigma_signal]['error']
        bkg = float(n_bkg)
        bkg_err = result_ext.hesse()[n_bkg]['error']

        sigma_width = 2.5

        integral_norm_gauss = gaussian.integrate(limits=(mu-sigma_width*sigma, mu+sigma_width*sigma))
        integral_norm_exp = exponential.integrate(limits=(mu-sigma_width*sigma, mu+sigma_width*sigma))

        B = float(integral_norm_exp*bkg)
        # print('Signal yield :',Y,'Background :',B)
        S = Y/np.sqrt(Y+B)
        print('Cut: ', mva_cut, 'Local significance :', round(S,2), 'Signal yield :', round(Y), 'Bkg yield :', round(B))
        SNR = Y/B
        significances[i] = S

        if S >= maxS[k]:
            maxS[k] = S
            opt_cut[k] = mva_cut
            opt_Y[k] = Y

        basis_pdf = np.linspace(obs_min, obs_max, 200)
        model_pdf_np = model.pdf(basis_pdf).numpy() * (n_signal.numpy()+n_bkg.numpy())
        plot_fit(data_all, basis_pdf, model_pdf_np, obs_bkg, zmodel=model, title=f'LHCb {year}')
        plt.savefig(f"mva_scan/{mva}/{mva_method}/{year}/fit-{mva_method}-{str(mva_cut).replace('.','-')}-{year}.png",bbox_inches="tight")
        plt.close()

    significances_all.append(significances)

    print(f'{mva_method} : Maximimum signal significance of {maxS[k]:.2f} for a cut of {opt_cut[k]:.3f} with a signal yield of {opt_Y[k]:.0f}')

    plt.errorbar(mva_cuts,significances,np.zeros(nb_step),[(max_cut-min_cut)/(2*nb_step)]*nb_step,"o",label=mva_method,markersize=5.)


    # plt.legend(loc='best')
    # plt.title('FoM')
    plt.xlabel(f'{mva_method} cut')
    plt.ylabel('Signifiance $S/\sqrt{S+B}$')
    axes = plt.gca()
    axes.set_xlim([min_cut,max_cut])
    plt.savefig(f"mva_scan/{mva}/{mva_method}/{year}/mva_scan-{mva_method}-{year}.png",bbox_inches="tight")   # the model as the sum of the individual pdfs
    


for k,mva_method in enumerate(mva_methods):
    min_cut = mva_methods[mva_method]['min_cut']
    max_cut = mva_methods[mva_method]['max_cut']
    nb_step = mva_methods[mva_method]['nb_step']

    plt.errorbar(mva_cuts_list[k],significances_all[k],np.zeros(nb_step),[(max_cut-min_cut)/(2*nb_step)]*nb_step,"o",label=mva_method,markersize=5.)


plt.legend(loc='best')
# plt.title('FoM')
plt.xlabel(f'{mva_method} cut')
plt.ylabel('Signifiance $S/\sqrt{S+B}$')
axes = plt.gca()
axes.set_xlim([0,1])
plt.savefig(f"mva_scan/{mva}/mva_scan-all-methods-{year}.png",bbox_inches="tight")   # the model as the sum of the individual pdfs
    










