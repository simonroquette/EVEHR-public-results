import warnings
warnings.filterwarnings('ignore')

from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import matplotlib

import pandas as pd
import numpy as np
import itertools


def plot_noise_effect(noise_compositions = [["Dr"], ["Ar"], ["SRr"], ["SPr"]], 
                      metric="accuracy", task="LOS",
                       savepath="", plot_minmax=True,):

    matplotlib.rcParams.update({'font.size': 15})

    all_noises = ['Dr', 'Ar', 'SRr', 'SPr']

    fig = plt.figure(figsize=(10, 8))

    colors=cm.rainbow(np.linspace(0,1,len(noise_compositions)))

    for color, noise_composition in zip(colors, noise_compositions):
    #noise_composition = ["Dr", "SRr"] # ['Dr', 'Ar', 'SRr', 'SPr']
        other_noises = [noise for noise in all_noises if not noise in noise_composition]

        results_noise = results[(results.Model.str.contains("noise")) & (results.Task == task)]
        noise_values = np.unique(results_noise[noise_composition].values)

        split_results = [results_noise[((results_noise[noise_composition] == value).all(axis = 1)) &
                                      ((results_noise[other_noises] == 0).all(axis = 1))] 
                         for value in noise_values]
        split_results = [result[metric].values for result in split_results]

        #plt.boxplot(split_results, positions = noise_values)
        mins = [min(x) for x in split_results]
        maxs = [max(x) for x in split_results]
        means = [np.mean(x) for x in split_results]
        
        label = "+".join(noise_composition)
        plt.plot(noise_values, means, lw=2, color=color, label=label if not plot_minmax else "")
        if plot_minmax:
            plt.fill_between(noise_values, mins, maxs, facecolor=color, alpha=0.2, 
                             label=label)  

    for i, noise_value in enumerate(noise_values):
        plt.axvline(x=noise_value, linestyle="--", color= "grey", label="sample" if i==0 else "")
    #plt.title("Extraction Error's Impact on %s for %s prediction" % (metric, task))
    plt.ylabel("Score: " + metric)
    plt.xlabel("Error rate")
    plt.legend(loc="center left")
    fig.patch.set_facecolor('white')
    #if savepath:
    #    plt.savefig(savepath, format='png', dpi=300)
    plt.show()
    
all_noises = [['Dr', 'Ar', 'SRr', 'SPr']]*4
all_noises = [list(np.unique(comb)) for comb in itertools.product(*all_noises)]
all_noises = sorted(np.unique(all_noises), key=lambda x: len(x))
noise_compositions = widgets.SelectMultiple(
                                        options=all_noises,
                                        value=[["Ar"], ["Dr"]],
                                        #rows=10,
                                        description='Noise Composition'
                                    )

filepath = "shareable_noise_results.csv"
results = pd.read_csv(filepath)