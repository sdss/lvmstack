import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

#from astropy.visualization import astropy_mpl_style
#plt.style.use(astropy_mpl_style)

def plot_images(data_east, data_west):
    mean, sigma, min, max = np.mean(data_east), np.std(data_east), np.min(data_east), np.max(data_east)
    lperc, uperc = np.percentile(data_east, 5), np.percentile(data_east, 99.95)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,20))
    ax1.set_title("west")
    ax1_im = ax1.imshow(data_west, vmin=mean-sigma, vmax=uperc)
    fig.colorbar(ax1_im, cax=make_axes_locatable(ax1).append_axes('right', size='3%', pad=0.05), orientation='vertical')

    ax2.set_title("east")
    ax2_im = ax2.imshow(data_east, vmin=mean-sigma, vmax=uperc)
    fig.colorbar(ax2_im, cax=make_axes_locatable(ax2).append_axes('right', size='3%', pad=0.05), orientation='vertical')
    plt.show()
