import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.patches import Ellipse, Rectangle

from mpl_toolkits.axes_grid1 import make_axes_locatable

#from astropy.visualization import astropy_mpl_style
#plt.style.use(astropy_mpl_style)

def plot_catalog(ax, catalog, color="red", cat_max=8):
     for c in catalog[:cat_max]:
         e = Ellipse(xy=(c['x'], c['y']),
             width=8*c['a'],
             height=8*c['b'],
             angle=c['theta'] * -180. / np.pi)
         e.set_facecolor('none')
         e.set_edgecolor(color)
         ax.add_artist(e)


def plot_images(images, vmin=None, vmax=None, cat_max = 8, cat_extra=None):
    data = images[0].data
    mean, sigma, min, max = np.mean(data), np.std(data), np.min(data), np.max(data)
    lperc, uperc = np.percentile(data, 5), np.percentile(data, 99.95)
    
#    fig, ax = plt.subplots(1, ncols=(len(images)))
#    fig, ax = plt.subplots(1, ncols=(len(images)), dpi=100)
    fig, ax = plt.subplots(1, ncols=(len(images)), figsize=(8, 5/len(images)))
    
    fig.canvas.toolbar_visible = 'fade-in-fade-out'
#    fig.canvas.footer_visible = False
    fig.canvas.header_visible = False
    fig.canvas.toolbar_position = 'left'
    is_single_image = len(images) > 1

    for idx, img in enumerate(images):
        ax_idx = ax[idx] if is_single_image else ax
        ax_idx.set_title(img.header["CAMNAME"])
        ax_im = ax_idx.imshow(images[idx].data, vmin=vmin if vmin else mean-sigma, vmax=vmax if vmax else uperc)
        ax_idx.invert_yaxis()
        fig.colorbar(ax_im, cax=make_axes_locatable(ax_idx).append_axes('right', size='3%', pad=0.05), orientation='vertical')
      
        if cat_extra:
            plot_catalog(ax_idx, cat_extra, "blue", cat_max)

        if img.catalog:
            plot_catalog(ax_idx, img.catalog, "red", cat_max)


    fig.tight_layout()
    plt.show()


