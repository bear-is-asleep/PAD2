import dash
from dash import dcc
from dash import html
import numpy as np
from variables import *
from PMT import PMT
from Loader import Loader
import plotly.graph_objects as go
from config.test import *
from time import time

app = dash.Dash(__name__)

l = Loader(DATA_DIR,PAD_DIR,HDUMP_NAME,WFM_NAME) #Loader class with PMT, muon, CRT info
run_list = l.run_list #Get list of run,subrun,evt
run,subrun,event = run_list[0]
l.get_event(run,subrun,event)


pds_tpc0 = l.get_pmt_list(tpc=0) #Get list of pmts
#pds_tpc1 = l.get_pmt_list(tpc=1) #Get list of pmts
# Plot coordinates
start_bin = t0+dt
end_bin = t1

pds_coordinates_tpc0 = [pds.plot_coordinates(start_bin,end_bin) for pds in pds_tpc0]

# Layout for the Dash app
app.layout = html.Div(children=[
    html.H1('TPC0'),
    # ]+[
    # html.Div(
    #     children=[
    #         dcc.Input(
    #             id='input-{}-{}'.format(index, i),
    #             type='number',  # Change the type to 'number' as inputs are integers
    #             value=value,
    #         )
    #         for i, value in enumerate(option)
    #     ]
    # )
    # for index, option in enumerate(run_list)
    # ]+[
    html.Label('t0 [ns]: '),
    dcc.Slider(
        id='t0-tpc0',
        min=t0,  # minimum value
        max=t1,  # maximum value
        step=dt,  # step size
        value=t0,  # current value at t0
        marks=None,
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    html.Label('t1 [ns]: '),
    dcc.Slider(
        id='t1-tpc1',
        min=t0,  # minimum value
        max=t1,  # maximum value
        step=dt,  # step size
        value=t1,  # current value at t0
        marks=None,
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    html.Div(children=[
        dcc.Graph(
            id='tpc0',
            figure=go.Figure(
                data=pds_coordinates_tpc0,
                layout=go.Layout(
                    autosize=False,
                    width=1000,
                    height=800,
                    showlegend=False,
                    xaxis=dict(range=[0, 500]),  # Set x-axis limits
                    yaxis=dict(range=[-200, 200])   # Set y-axis limits
                ))
        ),
        dcc.Graph(
            id='waveform-graph',
            style={'height': '300px', 'width': '1500px'}
            ),  # This will initialize an empty graph with correct size)
    ])
])

#Update PE
@app.callback(
    dash.dependencies.Output('tpc0', 'figure'),
    [dash.dependencies.Input('t0-tpc0', 'value'),
     dash.dependencies.Input('t1-tpc1', 'value')]
)
def update_tpc0(start_time_bin,end_time_bin):
    if VERBOSE: print('Update time window')
    s0 = time()
    pds_coordinates_tpc0 = [pds.plot_coordinates(start_time_bin,end_time_bin) for pds in pds_tpc0]
    s1 = time()
    if VERBOSE: print(f'Get new PE from {start_time_bin} to {end_time_bin} (ns): {s1-s0:.2f} s')
    return go.Figure(data=pds_coordinates_tpc0,
        layout=go.Layout(
            autosize=False,
            width=1000,
            height=800,
            showlegend=False,
            xaxis=dict(range=[0, 500]),  # Set x-axis limits
            yaxis=dict(range=[-200, 200])   # Set y-axis limits
    ))


# Callback to update the waveform graph when the button is clicked
@app.callback(
    dash.dependencies.Output('waveform-graph', 'figure'),
    [dash.dependencies.Input('tpc0', 'clickData')]
)

def update_waveform_graph(click_data):
    if VERBOSE: print('Drawing waveform')
    if click_data is not None:
        #print(click_data)
        pmt_id = click_data['points'][0]['customdata']
        ind = l.pds_tpc0_ids.index(pmt_id) #find index of pmt
        s0 = time()
        waveform_data = pds_tpc0[ind].plot_waveform()
        s1 = time() 
        if VERBOSE: print(f'Get waveform for PDS {pmt_id} which is {ind}: {s1-s0:.2f} s')
            
        if waveform_data is not None:
            if VERBOSE: print('Done')
            return go.Figure(data=waveform_data,
                             layout=go.Layout(
                                autosize=False,
                                width=1500,
                                height=300,
                                title=dict(
                                    text=f'PDS ID : {pmt_id}'
                                )
                            ))

    return go.Figure()


if __name__ == '__main__':
    app.run_server(debug=True)