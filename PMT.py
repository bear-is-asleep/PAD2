from utils.plotters import map_value_to_color
from utils.maps import COATING_MAP
import pandas as pd
import plotly.graph_objects as go
from variables import *
import numpy as np
from time import time

class PMT:
    def __init__(self, pmtid, coating, tpc, location, waveform=None, op_pe=None, t1=t1, t0=t0, dt=dt):
        self.id = pmtid
        self.coating = coating
        self.location = location
        self.waveform = waveform
        self.dt = dt
        self.tpc = tpc

        if op_pe is not None:
            self.op_pe = pd.DataFrame(op_pe)
            self.bins=np.arange(t0, t1+dt, dt)
            self.op_pe['time_bin'] = pd.cut(self.op_pe['op_time'], bins=self.bins,right=True,include_lowest=True)
            self.op_pe = self.op_pe.groupby('time_bin')['op_pe'].sum().reset_index()
        else:
            self.op_pe = None
            self.bins = None

    def get_pe_start_stop(self,start,end):
        """
        Get pe within start and stop times for bins

        Args:
            op_pe (pandas dataframe): contains two columns, 'time_bin' which are pd intervals, and op_pe which contain the pe for that time bin.
            bins (numpy array): time bins aranged in even intervals
            start (number): start time
            end (number): end time

        Returns:
            cum_pe (number): cumulative pe within start and stop times
        """
        start_ind = np.searchsorted(self.bins,start) 
        end_ind = np.searchsorted(self.bins,end)
        if start_ind < end_ind:
            mask = np.full(len(self.op_pe),False)
            inds = list(range(start_ind,end_ind))
            mask[inds] = True
            cum_pe = self.op_pe.loc[mask, 'op_pe'].sum()
        else:
            cum_pe = 0
        if np.isnan(cum_pe):
            cum_pe = 0
        return cum_pe

    def get_t0_threshold(self, t0_threshold=0.):
        #Find first bin where pe is above threshold
        mask = self.op_pe['op_pe'] > t0_threshold
        if mask.any():
            first_bin = self.op_pe.loc[mask, 'time_bin'].iloc[0]
            tind = self.op_pe.loc[self.op_pe['time_bin'] == first_bin].index[0]
        else:
            return np.nan
        return self.bins[tind] 
        
        

    def plot_coordinates(self, start, end, pds_ids,cmap='plasma', cmin=0, cmax=None, msize_max=1., msize_min=1.,t0_threshold=0.):
        """ 
        Plots PMTs onto PAD grid

        Args:
            start (_type_): start time window
            end (_type_): end time window
            pds_ids (_type_): list of pds ids that are plotted
            cmap (str, optional): Defaults to 'magma'.
            cmin (int, optional): Defaults to 0.
            cmax (int, optional): Defaults to None.
            msize_max (float, optional): Defaults to 1..
            msize_min (float, optional): Defaults to 1..
            t0_threshold (float, optional): Min pe to denote t0.
                Defaults to 0..

        Returns:
            go.Scatter: scatter point to be plotted on dash canvas
        """
        #if VERBOSE: print('pds id : ',self.id)
        z = [self.location[2]]
        y = [self.location[1]]
        if self.id in pds_ids[:2]: #only set colorbar for first two pds ids to avoid duplication 
            showscale = True
        else:
            showscale = False
        cum_pe = self.get_pe_start_stop(start, end)
        t0 = self.get_t0_threshold(t0_threshold)
        s1 = time()
        #if VERBOSE: print(f'-- time to bin {s1-s0:.3f} s')
        msize = cum_pe/msize_max  # marker size normalized to other pmts
        msize = msize if msize > 5 else 5
        hex_color = map_value_to_color(t0,cmin,cmax,cmap=cmap)
        text = f'ID : {self.id:.0f}'
        text += '<br>'
        text += f'Coating : {COATING_MAP[self.coating]}'
        text += '<br>'
        text += f'Cum. PE : {cum_pe:.2f}'
        text += '<br>'
        text += f't0 : {t0:.2f}'
        # print('color : ',color)
        # print('hex : ',hex_color)
        sc = go.Scatter(
            x=z,
            y=y,
            mode='markers',
            marker=dict(
                size=msize,
                color=hex_color,
                colorscale=cmap,
                showscale=showscale,
                cmin=cmin,
                cmax=cmax,
            ),
            name=f'PDS {self.id}',
            customdata=[self.id],
            text=text,  # display the color value on hover
            hoverinfo='text+name',  # show the custom text and trace name on hover
        )
        s2 = time()
        #if VERBOSE: print(f'-- time to make scatter {s2-s1:.3f} s')
        return sc

    def plot_waveform(self):
        """
        Plots PMT waveform

        Returns:
            go.Scatter: scatter point to be plotted on dash canvas
        """
        if self.waveform is not None:
            if VERBOSE: print(f'Plotting waveform for PDS {self.id}')
            return go.Scatter(
                x=self.waveform['time'],
                y=self.waveform['voltage'],
                mode='lines',
                name=f'Waveform for PDS {self.id}'
            )
        else:
            if VERBOSE: print(f'No waveform for PDS {self.id}')
            return None