import os
from datetime import date
import matplotlib.pyplot as plt
import utils
import matplotlib.colors as mcolors

day = date.today().strftime("%Y_%m_%d")


def save_plot(fname, fig=None, ftype='.png', dpi=300, folder_name=None, overwrite=True):
  if folder_name is None:
    folder_name = f'Plots/Plots_{day}'

  # Save the plot
  if fig == None:
    plt.savefig(f'{fname}{ftype}', bbox_inches="tight", dpi=dpi)
  else:
    fig.savefig(f'{fname}{ftype}', bbox_inches="tight", dpi=dpi)
  utils.move_file(f'{fname}{ftype}',folder_name,overwrite=overwrite)
    
def set_style(ax,legend_size=16,legend_loc='best',axis_size=16,title_size=20,tick_size=16,
              bbox_to_anchor=None):
  #plt.style.use('science')
  ax.tick_params(axis='x', labelsize=tick_size)
  ax.tick_params(axis='y', labelsize=tick_size)
  ax.xaxis.label.set_size(axis_size)
  ax.yaxis.label.set_size(axis_size)
  ax.title.set_size(title_size)
  if ax.get_legend() is not None:
    if bbox_to_anchor is not None:
      ax.legend(bbox_to_anchor=bbox_to_anchor,fontsize=legend_size)
    else:
      ax.legend(loc=legend_loc,fontsize=legend_size)

def map_value_to_color(value, min_val, max_val, cmap='viridis',return_hex=True):
    # Create a colormap
    cmap = plt.get_cmap(cmap)  # replace 'viridis' with your colormap
    norm = mcolors.Normalize(vmin=min_val, vmax=max_val)
    normalized_value = norm(value)
    rgb_color = cmap(normalized_value)
    if return_hex:
        return mcolors.rgb2hex(rgb_color[:3])
    return rgb_color
  
