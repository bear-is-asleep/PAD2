import dash
from dash import dcc
from dash import html
import numpy as np
from variables import *
from PMT import PMT
from Loader import Loader
import plotly.graph_objects as go
from config.test2 import *
from time import time

global muons_tpc0
global pds_tpc0
global muons_tpc1
global pds_tpc1

#Initialize
#l = Loader(DATA_DIR,PAD_DIR,HDUMP_NAME,WFM_NAME) #Loader class with PMT, muon, CRT info
l = Loader(DATA_DIR,PAD_DIR,HDUMP_NAME,WFM_NAME,load_muon=True) #Loader class with PMT, muon, CRT info

#Initialize display
run_list = l.run_list #Get list of run,subrun,evt
run,subrun,event = run_list[0]
start_bin = t0+dt
end_bin = t1
l.get_event(run,subrun,event)

#PDS init
pds_tpc0 = l.get_pmt_list(tpc=0) #Get list of pmts
pds_tpc1 = l.get_pmt_list(tpc=1) #Get list of pmts
cmax = np.max([pds.op_pe.op_pe.sum() for pds in pds_tpc0+pds_tpc1])
cmin = 0
pds_coordinates_tpc0 = [pds.plot_coordinates(start_bin,end_bin,cmin=cmin,cmax=cmax) for pds in pds_tpc0]
pds_coordinates_tpc1 = [pds.plot_coordinates(start_bin,end_bin,cmin=cmin,cmax=cmax) for pds in pds_tpc1]

#Muon init
muons_tpc0 = l.get_muon_list(tpc=0)
muons_tpc1 = l.get_muon_list(tpc=1)
muon_lines_tpc0 = [muons_tpc0[i].plot_line(i,0) for i in range(len(muons_tpc0))]
muon_lines_tpc1 = [muons_tpc1[i].plot_line(i,1) for i in range(len(muons_tpc1))]

#Start dash
app = dash.Dash(__name__)

# Layout for the Dash app
app.layout = html.Div(style={'display':'flex'},children=[
    html.Div(style={'width': '80%'},children=[
        html.H1('PAD'),
        html.Label('Run: '),
        dcc.Input(id='run-input', type='number', value=run),  # initialize with run from l.run_list

        html.Label('Subrun: '),
        dcc.Input(id='subrun-input', type='number', value=subrun),  # initialize with subrun from l.run_list

        html.Label('Event: '),
        dcc.Input(id='event-input', type='number', value=event),  # initialize with event from l.run_list
        html.Button('Submit', id='submit-button', n_clicks=0),
        html.Br(),
        html.Label('t0 [ns]: '),
        dcc.Slider(
            id='t0',
            min=t0,  # minimum value
            max=t1,  # maximum value
            step=dt,  # step size
            value=t0,  # current value at t0
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True}
        ),
        html.Label('t1 [ns]: '),
        dcc.Slider(
            id='t1',
            min=t0,  # minimum value
            max=t1,  # maximum value
            step=dt,  # step size
            value=t1,  # current value at t0
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True}
        ),
        html.H2('TPC0'),
        html.Div(children=[
            dcc.Graph(
                id='tpc0',
                figure=go.Figure(
                    data=pds_coordinates_tpc0+muon_lines_tpc0,
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
                id='waveform-graph-tpc0',
                style={'height': '400px', 'width': '1000px'}
                ),  # This will initialize an empty graph with correct size)
            ]),
        html.H2('TPC1'),
        html.Div(children=[
            dcc.Graph(
                id='tpc1',
                figure=go.Figure(
                    data=pds_coordinates_tpc1+muon_lines_tpc1,
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
                id='waveform-graph-tpc1',
                style={'height': '400px', 'width': '1000px'}
                ),  # This will initialize an empty graph with correct size)
            ])
    ]),
    # Right-hand side
    html.Div(style={'width': '20%'},children=[
        html.H2('Available Runs'),
        html.Ul(children=[
            html.Li(f'Run: {run}, Subrun: {subrun}, Event: {event}') for run, subrun, event in run_list
        ])
    ])
])

#Update PE
@app.callback(
    dash.dependencies.Output('tpc0', 'figure'),  
    dash.dependencies.Output('tpc1', 'figure'),
    [dash.dependencies.Input('t0', 'value'),      
     dash.dependencies.Input('t1', 'value'),
     dash.dependencies.Input('submit-button', 'n_clicks')],  
    [dash.dependencies.State('run-input', 'value'),  
     dash.dependencies.State('subrun-input', 'value'),  
     dash.dependencies.State('event-input', 'value')]  
)

def update_tpcs(start_time_bin, end_time_bin, n_clicks,run, subrun, event):
    #Make graph objects global
    global muons_tpc0
    global pds_tpc0  
    global muons_tpc1
    global pds_tpc1   
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'] == 'submit-button.n_clicks':  # Check if the button triggered the callback
        if [run,subrun,event] in l.run_list:
            if VERBOSE: print(f'Retrieving Run {run} Subrun {subrun} Event {event}')
            l.get_event(run, subrun, event)
            
            pds_tpc0 = l.get_pmt_list(tpc=0)
            muons_tpc0 = l.get_muon_list(tpc=0)
            
            pds_tpc1 = l.get_pmt_list(tpc=1)
            muons_tpc1 = l.get_muons_list(tpc=1)
        else:
            print(f'Run {run} Subrun {subrun} Event {event} not in file')
            if VERBOSE: 
                print('List of run,subrun,events - ')
                #print(l.run_list)
                return None
    
    #PDS
    #if VERBOSE: print('Update time window')
    s0 = time()
    cmax = np.max([pds.op_pe.op_pe.sum() for pds in pds_tpc0+pds_tpc1])
    cmin = 0
    pds_coordinates_tpc0 = [pds.plot_coordinates(start_time_bin,end_time_bin,cmin=cmin,cmax=cmax) for pds in pds_tpc0]
    pds_coordinates_tpc1 = [pds.plot_coordinates(start_time_bin,end_time_bin,cmin=cmin,cmax=cmax) for pds in pds_tpc1]
    s1 = time()
    if VERBOSE: print(f'Get new PE from {start_time_bin} to {end_time_bin} (ns): {s1-s0:.2f} s')
    
    #Muons
    #if VERBOSE: print('Get muon trajectories')
    s0 = time()
    muon_lines_tpc0 = [muons_tpc0[i].plot_line(i,0) for i in range(len(muons_tpc0))]
    muon_lines_tpc1 = [muons_tpc1[i].plot_line(i,1) for i in range(len(muons_tpc1))]
    s1 = time()
    if VERBOSE: print(f'Get new muon trajectories : {s1-s0:.2f} s')

    return [go.Figure(data=pds_coordinates_tpc0+muon_lines_tpc0,
                     layout=go.Layout(
                         autosize=False,
                         width=1000,
                         height=800,
                         showlegend=False,
                         xaxis=dict(range=[0, 500]),  # Set x-axis limits
                         yaxis=dict(range=[-200, 200])   # Set y-axis limits
                     )),
            go.Figure(data=pds_coordinates_tpc1+muon_lines_tpc1,
                     layout=go.Layout(
                         autosize=False,
                         width=1000,
                         height=800,
                         showlegend=False,
                         xaxis=dict(range=[0, 500]),  # Set x-axis limits
                         yaxis=dict(range=[-200, 200])   # Set y-axis limits
                     ))]


# Callback to update the waveform graph when the button is clicked
@app.callback(
    dash.dependencies.Output('waveform-graph-tpc0', 'figure'),
    [dash.dependencies.Input('tpc0', 'clickData')]
)

def update_waveform_graph(click_data):
    if click_data is not None:
        if VERBOSE: print('Drawing waveform')
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
                                width=1000,
                                height=400,
                                title=dict(
                                    text=f'PDS ID : {pmt_id}'
                                ),
                                xaxis_title='t [us]',
                                yaxis_title='ADC',
                            ))

    return go.Figure()

# Callback to update the waveform graph when the button is clicked
@app.callback(
    dash.dependencies.Output('waveform-graph-tpc1', 'figure'),
    [dash.dependencies.Input('tpc1', 'clickData')]
)

def update_waveform_graph(click_data):
    if click_data is not None:
        if VERBOSE: print('Drawing waveform')
        pmt_id = click_data['points'][0]['customdata']
        ind = l.pds_tpc1_ids.index(pmt_id) #find index of pmt
        s0 = time()
        waveform_data = pds_tpc1[ind].plot_waveform()
        s1 = time() 
        if VERBOSE: print(f'Get waveform for PDS {pmt_id} which is {ind}: {s1-s0:.2f} s')
            
        if waveform_data is not None:
            if VERBOSE: print('Done')
            return go.Figure(data=waveform_data,
                             layout=go.Layout(
                                autosize=False,
                                width=1000,
                                height=400,
                                title=dict(
                                    text=f'PDS ID : {pmt_id}'
                                ),
                                xaxis_title='t [us]',
                                yaxis_title='ADC',
                            ))

    return go.Figure()


if __name__ == '__main__':
    app.run_server(debug=True)