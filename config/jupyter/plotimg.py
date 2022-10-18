import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

#from astropy.visualization import astropy_mpl_style
#plt.style.use(astropy_mpl_style)

def plot_images(images):
    data = images[0].data
    mean, sigma, min, max = np.mean(data), np.std(data), np.min(data), np.max(data)
    lperc, uperc = np.percentile(data, 5), np.percentile(data, 99.95)

    fig, ax = plt.subplots(1, ncols=(len(images)), figsize=(16,20))

    is_single_image = len(images) > 1

    for idx, img in enumerate(images):
        ax_idx = ax[idx] if is_single_image else ax
        ax_idx.set_title(img.header["CAMNAME"])
        ax_im = ax_idx.imshow(images[idx].data, vmin=mean-sigma, vmax=uperc)
        fig.colorbar(ax_im, cax=make_axes_locatable(ax_idx).append_axes('right', size='3%', pad=0.05), orientation='vertical')

    plt.show()

