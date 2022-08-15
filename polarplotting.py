#Import Libraries for Feature plot

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def feature_plot(features):
    

    labels= list(features)[:]
    stats= features.mean().tolist()

    angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False)

    # close the plot
    stats=np.concatenate((stats,[stats[0]]))
    angles=np.concatenate((angles,[angles[0]]))

    #Size of the figure
    fig=plt.figure(figsize = (5,5))

    ax = fig.add_subplot(221, polar=True)
    ax.plot(angles, stats, '.-', linewidth=0.5, label = "Features", color= 'green')
    ax.fill(angles, stats, alpha=0.25, facecolor='green')
    ax.set_thetagrids(angles[0:7] * 180/np.pi, labels , fontsize = 5)


    ax.set_rlabel_position(250)
    plt.yticks([0.2 , 0.4 , 0.6 , 0.8 ], ["0.2",'0.4', "0.6", "0.8"], color="grey", size=5)
    plt.ylim(0,1)

    plt.legend(loc='best', bbox_to_anchor=(0.1, 0.1))
    st.pyplot(plt)