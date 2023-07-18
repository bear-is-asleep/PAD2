from utils.plotters import map_value_to_color
import pandas as pd
import plotly.graph_objects as go
from variables import *
import numpy as np

class PMT:
    def __init__(self, id, coating, tpc, location, waveform=None, op_pe=None, t1=t1, t0=t0, dt=dt):
        self.id = id
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

    def plot_coordinates(self, start, end, cmap='viridis', cmin=0, cmax=2000):
        """ 
        Plots PMTs onto PAD grid

        Args:
            start (_type_): start time window
            end (_type_): end time window
            cmap (str, optional): Defaults to 'viridis'.
            cmin (int, optional): Defaults to 0.
            cmax (int, optional): Defaults to 10000.

        Returns:
            go.Scatter: scatter point to be plotted on dash canvas
        """
        #print('pds id : ',self.id)
        z = [self.location[2]]
        y = [self.location[1]]
        if self.id in [6,7]: 
            showscale = True
        else:
            showscale = False
        if self.op_pe is not None:
            start_interval = pd.cut([start],self.bins,include_lowest=True)[0]
            end_interval = pd.cut([end],self.bins)[0]
            # print('-- start : ',start)
            # print('-- end : ',end)
            # print('-- start int : ',start_interval)
            # print('-- end int : ',end_interval)
            if start_interval < end_interval:
                if start == t0: #handle edge case since include lowest is true
                    selected_intervals = [bin for bin in self.bins if bin >= start_interval.left and bin <= end_interval.right]
                else:
                    selected_intervals = [bin for bin in self.bins if bin >= start_interval.left + self.dt/3 and bin <= end_interval.right]
                selected_intervals = pd.Interval(left=selected_intervals[0], right=selected_intervals[-1])
                mask = [selected_intervals.overlaps(i) for i in self.op_pe['time_bin']]
                color = self.op_pe.loc[mask, 'op_pe'].sum()
            else:
                color = 0
            if np.isnan(color):
                color = 0
        else:
            color = 0
        msize = 18
        hex_color = map_value_to_color(color,cmin,cmax,cmap=cmap)
        text = f'ID : {self.id:.0f}'
        text += '<br>'
        text += f'Coating : {self.coating:.2f}'
        text += '<br>'
        text += f'Cum. PE : {color:.2f}'
        # print('color : ',color)
        # print('hex : ',hex_color)
        return go.Scatter(
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
            name=f'PMT {self.id}',
            customdata=[self.id],
            text=text,  # display the color value on hover
            hoverinfo='text+name',  # show the custom text and trace name on hover
        )

    def plot_waveform(self):
        """
        Plots PMT waveform

        Returns:
            go.Scatter: scatter point to be plotted on dash canvas
        """
        if self.waveform is not None:
            return go.Scatter(
                x=self.waveform['time'],
                y=self.waveform['voltage'],
                mode='lines',
                name=f'Waveform for PMT {self.id}'
            )
        else:
            return None