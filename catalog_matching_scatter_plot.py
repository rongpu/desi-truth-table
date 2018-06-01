import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

def scatter_plot(d_ra, d_dec, markersize=1, alpha=1):
    '''
    INPUTS:

     d_ra, d_dec: array of RA and Dec difference in arcsec
    
    OUTPUTS:

     axScatter: scatter-histogram plot
    '''

    nullfmt = NullFormatter()         # no labels

    # definitions for the axes
    left, width = 0.1, 0.85
    bottom, height = 0.1, 0.85

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom, width, 0.3]
    rect_histy = [left, bottom, 0.3, height]

    # start with a rectangular Figure
    plt.figure(figsize=(8,8))

    axScatter = plt.axes(rect_scatter)
    axHistx = plt.axes(rect_histx)
    axHisty = plt.axes(rect_histy)

    axScatter.plot(d_ra, d_dec, 'k.', markersize=markersize, alpha=alpha)

    axHistx.hist(d_ra, bins=100, histtype='step', color='r', linewidth=2)
    axHisty.hist(d_dec, bins=100, histtype='step', color='r', linewidth=2, orientation='horizontal')

    axHistx.set_xlim(axScatter.get_xlim())
    axHisty.set_ylim(axScatter.get_ylim())

    axHistx.axis('off')
    axHisty.axis('off')

    axScatter.axhline(0, color='r', linestyle='--', linewidth=1.2)
    axScatter.axvline(0, color='r', linestyle='--', linewidth=1.2)
    axScatter.set_xlabel('RA2 - RA1 (arcsec)}')
    axScatter.set_ylabel('DEC2 - DEC1 (arcsec)}')

    return(axScatter)
