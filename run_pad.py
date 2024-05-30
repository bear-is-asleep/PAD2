#Your config - you can also pass arguments
#from config.xa_test_rodrigo import *
#from config.pds_particles import *
#from config.intime import *
#from config.intime_crt import *
#from config.intime_notracks import *
from config.pmt_data import *

#Boilerplate imports
import dash
from dash import dcc
from dash import html
import numpy as np
from Loader import Loader
import plotly.graph_objects as go
from time import time
import argparse
import os
from utils.maps import get_random_map

#globals - passed between various update functions
global coatings #pds coatings
global mmax #max pe corresponding to max size anything above mmax will show as max size
global mmax_global #max pe integrated over entire window
global mmax_dynamic #max pe integrated over current window
global t0s #t0s for each pds

#tpc0 globals
global muons_tpc0
global pds_tpc0
global pds_coordinates_tpc0
global muon_lines_tpc0
global mcparts_lines_tpc0
global crt_lines_tpc0

#tpc 1 globals
global muons_tpc1
global pds_tpc1
global pds_coordinates_tpc1
global muon_lines_tpc1
global mcparts_lines_tpc1
global crt_lines_tpc1

# Create the parser
parser = argparse.ArgumentParser(description="Load data - default values are stored in the config selected")

# Add the arguments
parser.add_argument('--data', type=str, default=DATA_DIR, required=False, help='Path to the data')
parser.add_argument('--hdump_name', default=HDUMP_NAME, required=False, help='hitdumper file name')
parser.add_argument('--sm_name', default=SM_NAME, required=False, help='pmt software metrics file name')
parser.add_argument('--wfm_name', default=WFM_NAME, required=False, help='waveform file name')
parser.add_argument('--load_muon',type=bool, default=LOAD_MUON, required=False, help='load muon info')
parser.add_argument('--load_crt',type=bool, default=LOAD_CRT, required=False, help='load crt info')
parser.add_argument('--load_mcpart',type=bool, default=LOAD_MCPART, required=False, help='load mcpart info')
parser.add_argument('--mode',type=str, default=MODE, help='Optical detector mode')
parser.add_argument('--filter_primaries',type=bool, default=MCPART_FILTER_TIME, help='Filter mcpart to +- 10us around beam window')
parser.add_argument('--crt_filter_tpc',type=bool, default=CRT_FILTER_TPC, help='Filter CRT tracks to TPC')
parser.add_argument('--mcpart_filter_tpc',type=bool, default=MCPART_FILTER_TIME, help='Filter MCPart to TPC')
parser.add_argument('--max_entries',type=int, default=MAX_ENTRIES, help='Max number of entries to load')
parser.add_argument('--map',type=str, default=PMT_ARA_NAME, help='PMT map')

# Parse the arguments
args = parser.parse_args()

#Print the arguments
if VERBOSE:
    print(50*'*')
    print('Config : ')
    [print(f'-{key} : {value}') for key,value in vars(args).items()]
    print(f'-hdrkeys : {HDRKEYS}')
    print(f'-coatings : {COATINGS}')
    print(f'-t0 : {t0}')
    print(f'-t1 : {t1}')
    print(f'-dt : {dt}')
    print(f'-mmax : {MMAX}')
    print(f'-t0_thresholds : {T0_THRESHOLDS}')
    print(f'-max_spread : {MAX_SPREAD}')
    print(f'-set_to_thresholds : {SET_TO_THRESHOLDS}')
    print(f'-wfm_range : {WFM_RANGE}')

#Get a random map if specified
if args.map == 'random':
    if VERBOSE: print('**Getting random channel mapping**')
    args.map = get_random_map()

# Use the arguments
l = Loader(
    data_dir=args.data,
    hdump_name=args.hdump_name, 
    software_name=args.sm_name, 
    wfm_name=args.wfm_name, 
    load_muon=args.load_muon,
    load_crt=args.load_crt,
    load_mcpart=args.load_mcpart,
    mode=args.mode,
    hdrkeys=HDRKEYS, 
    pmt_ara_name=args.map, 
    filter_primaries=args.filter_primaries,
    max_entries=args.max_entries,
    wfm_range=WFM_RANGE
)

#Initialize display
run_list = l.run_list #Get list of run,subrun,evt
run,subrun,event = run_list[0] #get first run for initialization
start_bin = t0+dt
end_bin = t1
dt_window = t1-t0
l.get_event(run,subrun,event)
coatings = COATINGS #Select initial PDs to show
max_marker_size = 30 
min_marker_size = 5 

#Muon init
if l.load_muon:
    muons_tpc0 = l.get_muon_list(tpc=0)
    muons_tpc1 = l.get_muon_list(tpc=1)
    muon_lines_tpc0 = [muons_tpc0[i].plot_line(i,0) for i in range(len(muons_tpc0))]
    muon_lines_tpc1 = [muons_tpc1[i].plot_line(i,1) for i in range(len(muons_tpc1))]
else:
    muon_lines_tpc0 = [go.Scatter()]
    muon_lines_tpc1 = [go.Scatter()]

#MCPart init
if l.load_mcpart:
    mcparts = l.get_mcpart_list()
    mcparts_lines_tpc0 = [mcparts[i].plot_line(i,0,max_color=len(mcparts),filter_tpc=MCPART_FILTER_TPC) for i in range(len(mcparts))]
    mcparts_lines_tpc1 = [mcparts[i].plot_line(i,1,max_color=len(mcparts),filter_tpc=MCPART_FILTER_TPC) for i in range(len(mcparts))]
else:
    mcparts_lines_tpc0 = [go.Scatter()]
    mcparts_lines_tpc1 = [go.Scatter()]
    
#CRT track init
if l.load_crt:
    crt_trks = l.get_crt_list()
    crt_lines_tpc0 = [crt_trks[i].plot_line(i,0,max_color=len(crt_trks),filter_tpc=CRT_FILTER_TPC) for i in range(len(crt_trks))]
    crt_lines_tpc1 = [crt_trks[i].plot_line(i,1,max_color=len(crt_trks),filter_tpc=CRT_FILTER_TPC) for i in range(len(crt_trks))]
else:
    crt_lines_tpc0 = [go.Scatter()]
    crt_lines_tpc1 = [go.Scatter()]

#Display figures
WIDTH = 700
TPC_HEIGHT = WIDTH * 4/5
WAVEFORM_HEIGHT = WIDTH * 2/5
def set_t0_minmax(max_spread=MAX_SPREAD,t0_threshold=t0,t1_threshold=t1,set_to_thresholds=SET_TO_THRESHOLDS):
    global t0s,tmax,tmin
    if set_to_thresholds:
        tmax,tmin = t1_threshold,t0_threshold
        return 
    tmax,tmin = 1e10,-1e10
    #filter out dummy pds with nan values
    t0s = [t0 for t0 in t0s if not np.isnan(t0)]
    if len(t0s) == 0:
        tmax,tmin = 1,0
    else:
        iterations = 0
        while (tmax - tmin) > max_spread:
            #get rid of outliers
            if len(t0s) == 0:
                print(f'WARNING: No t0s found in range {tmin} to {tmax} ns with max spread {max_spread} ns')
                break
            if iterations > 50:
                print(f'WARNING: Iteration timeout with max spread {max_spread} ns')
                break
            tmax = np.percentile(t0s,99.5) # 3 sigma
            tmin = np.percentile(t0s,0.5) # 3 sigma
            t0s = [t0 for t0 in t0s if t0 <= tmax and t0 >= tmin]
            iterations += 1
        if len(t0s) == 0:
            tmax,tmin = 1,0
        else:
            tmin = np.min(t0s)
            tmax = np.max(t0s)
    
def get_tpc0():
    global pds_coordinates_tpc0,muon_lines_tpc0,mcparts_lines,mmax,crt_lines,t0s
    set_t0_minmax()
    return go.Figure(
        data=pds_coordinates_tpc0+muon_lines_tpc0+mcparts_lines_tpc0+crt_lines_tpc0,
        layout=go.Layout(
            autosize=False,
            width=WIDTH,
            height=TPC_HEIGHT,
            showlegend=False,
            xaxis=dict(range=[0, 500]),  # Set x-axis limits
            yaxis=dict(range=[-200, 200]),   # Set y-axis limits
            coloraxis=dict(cmin=tmin,cmax=tmax),
            margin=dict(l=50, r=50, b=50, t=50, pad=0),
            xaxis_title='z [cm]',
            yaxis_title='y [cm]',
        )
    )    
def get_tpc1():
    global pds_coordinates_tpc1,muon_lines_tpc1,mcparts_lines,mmax,crt_lines,t0s
    set_t0_minmax()
    return go.Figure(
        data=pds_coordinates_tpc1+muon_lines_tpc1+mcparts_lines_tpc1+crt_lines_tpc1,
        layout=go.Layout(
            autosize=False,
            width=WIDTH,
            height=TPC_HEIGHT,
            showlegend=False,
            xaxis=dict(range=[0, 500]),  # Set x-axis limits
            yaxis=dict(range=[-200, 200]),   # Set y-axis limits
            coloraxis=dict(cmin=tmin,cmax=tmax),
            margin=dict(l=50, r=50, b=50, t=50, pad=0),
            xaxis_title='z [cm]',
            yaxis_title='y [cm]',
        )
    )
def get_waveform(waveform_data,pmt_id=None):
    return go.Figure(data=waveform_data,
                             layout=go.Layout(
                                autosize=False,
                                width=WIDTH,
                                height=WAVEFORM_HEIGHT,
                                title=dict(
                                    text=f'PDS ID : {pmt_id}'
                                ),
                                xaxis_title='t [us]',
                                yaxis_title='ADC',
                                margin=dict(l=50, r=50, b=50, t=50, pad=0),
                            )
                        )
#Get t0s for each pds and set t0 (different thresholds for pmt and xa)
def set_t0s():
    global t0s
    
    t0s = []
    for pds in pds_tpc0+pds_tpc1:
        if 'pmt' in pds.pd_type:
            t0s.append(pds.get_t0_threshold(T0_THRESHOLDS[0])) #also sets t0
        else: #assume xa
            t0s.append(pds.get_t0_threshold(T0_THRESHOLDS[1])) #also sets t0
    
def set_mmax(start,end):
    global mmax
    global mmax_global
    global mmax_dynamic
    global pds_tpc0
    global pds_tpc1
    
    mmax_global = np.max([pds.op_pe.op_pe.sum() for pds in pds_tpc0+pds_tpc1])
    mmax_dynamic = np.max([pds.get_pe_start_stop(start,end) for pds in pds_tpc0+pds_tpc1])
    if MMAX == 'global':
        mmax = mmax_global
    elif MMAX == 'dynamic':
        mmax = mmax_dynamic
    elif isinstance(MMAX,(int,float)):
        mmax = MMAX
    else:
        if VERBOSE: print(f'{MMAX} is not a valid setting for setting pe size')
        mmax = None

def set_pds_coordinates(start,end):
    global pds_coordinates_tpc0,pds_coordinates_tpc1,pds_tpc0,pds_tpc1
    global mmax,t0s,tmin,tmax
    
    pds_ids = [pds.id for pds in pds_tpc0+pds_tpc1]
    pds_coordinates_tpc0 = [pds.plot_coordinates(start,end,pds_ids,cmin=tmin,cmax=tmax
                                                 ,msize_max=max_marker_size,msize_min=min_marker_size,mmax=mmax)\
        for pds in pds_tpc0]
    pds_coordinates_tpc1 = [pds.plot_coordinates(start,end,pds_ids,cmin=tmin,cmax=tmax
                                                 ,msize_max=max_marker_size,msize_min=min_marker_size,mmax=mmax)\
        for pds in pds_tpc1]

#PDS init
def init_pds_dash():
    global pds_coordinates_tpc0
    global pds_tpc0
    
    global pds_coordinates_tpc1
    global pds_tpc1
    
    global mmax
    global coatings
    
    global t0s,tmin,tmax
    
    pds_tpc0 = l.get_pmt_list(t0,t1,dt,tpc=0,coatings=coatings) #Get list of pmts
    pds_tpc1 = l.get_pmt_list(t0,t1,dt,tpc=1,coatings=coatings) #Get list of pmts
    #Get t0s for each pds
    set_t0s() #sets t0s
    set_t0_minmax() #get t0 min and max
    set_mmax(start_bin,end_bin) #sets mmax
    set_pds_coordinates(start_bin,end_bin) #sets pds coordinates

init_pds_dash()

#Start dash
app = dash.Dash(__name__)

# Layout for the Dash app
app.layout = html.Div(style={'display':'flex', 'font-family': 'Verdana'},children=[
    html.Div(style={'width': '85%'},children=[
        html.H1('PAD (PDS Analysis Display)'),
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
        html.Label('time window [ns]: '),
        dcc.Slider(
            id='dt_window',
            min=dt,  # minimum value
            max=t1-t0,  # maximum value
            step=dt,  # step size
            value=dt_window,  # dt window for summing
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True}
        ),
        # Put TPC0 and TPC1 side by side
        html.Div(style={'display': 'flex'}, children=[
            # TPC0 Div
            html.Div(children=[
                html.H2('TPC0 - East APA Back'),
                dcc.Graph(
                    id='tpc0',
                    figure=get_tpc0(),
                ),
                dcc.Graph(
                    id='waveform-graph-tpc0',
                    style={'height': f'{WAVEFORM_HEIGHT}px', 'width': f'{WIDTH}px'}
                ),  # This will initialize an empty graph with correct size)
            ]),
            # TPC1 Div
            html.Div(children=[
                html.H2('TPC1 - West APA Front'),
                dcc.Graph(
                    id='tpc1',
                    figure=get_tpc1()
                ),
                dcc.Graph(
                    id='waveform-graph-tpc1',
                    style={'height': f'{WAVEFORM_HEIGHT}px', 'width': f'{WIDTH}px'}
                ),  # This will initialize an empty graph with correct size)
            ]),
        ]),
    ]),
    # Right-hand side
    html.Div(style={'width': '15%'},children=[
        html.Img(src=dash.get_asset_url('sbnd_pretty.png'), style={'width': '100%', 'height': 'auto'}),
        html.H3(f'Mode : {l.mode}'),
        html.Img(src=dash.get_asset_url('muon_track.png'), style={'width': '100%', 'height': 'auto'}) if l.load_muon else html.H3('Muon Tracks : NA'),
        html.Img(src=dash.get_asset_url('crt_track.png'), style={'width': '100%', 'height': 'auto'}) if l.load_crt else html.H3('CRT Tracks : NA'),
        html.Img(src=dash.get_asset_url('g4.png'), style={'width': '100%', 'height': 'auto'}) if l.load_mcpart else html.H3('G4 Primaries : NA'),
        html.H4(id='mmax-global-display',children=f'Global Max PE : {mmax_global:.2f}'),
        html.H4(id='mmax-dynamic-display',children=f'Current Max PE : {mmax_dynamic:.2f}'),
        html.H4(id='mmax-display',children=f'Max Marker Size PE : {mmax:.2f}'),
        #Not supported yet
        #html.H3(f'Current event : '),
        #html.H5(f'    Run: {l.run}, Subrun {l.subrun}, Event {l.event}'),
        html.H3('Select PDS Coatings:'),
        dcc.Checklist(
            id='pds_coatings',
            options=[
                {'label': 'Undefined PDs', 'value': 0},
                {'label': 'Coated (VUV) PMTs', 'value': 1},
                {'label': 'Uncoated (VIS) PMTs', 'value': 2},
                {'label': 'Coated (VUV) XAs', 'value': 4},
                {'label': 'Uncoated (VIS) XAs', 'value': 3},
            ],
            value=coatings
        ),
        html.H2('Available Runs'),
        html.Ul(children=[
            html.Li(f'Run: {run}, Subrun: {subrun}, Event: {event}', style={'font-size': '12px'}) for run, subrun, event in run_list
        ])
    ])
])

#Update PE and/or coatings
@app.callback(
    dash.dependencies.Output('tpc0', 'figure'),  
    dash.dependencies.Output('tpc1', 'figure'),
    dash.dependencies.Output('mmax-display', 'children'),
    dash.dependencies.Output('mmax-global-display', 'children'),
    dash.dependencies.Output('mmax-dynamic-display', 'children'),
    [dash.dependencies.Input('t0', 'value'),      
     dash.dependencies.Input('dt_window', 'value'),
     dash.dependencies.Input('submit-button', 'n_clicks'),
     dash.dependencies.Input('pds_coatings', 'value')],  
    [dash.dependencies.State('run-input', 'value'),  
     dash.dependencies.State('subrun-input', 'value'),  
     dash.dependencies.State('event-input', 'value')]  
)

def update_tpcs(start_time_bin, dt_window_size, n_clicks,values,run, subrun, event):
    #Make graph objects global
    global muons_tpc0
    global pds_tpc0  
    global pds_coordinates_tpc0
    global muon_lines_tpc0
    global mcparts_lines_tpc0
    global crt_lines_tpc0
    
    global muons_tpc1
    global pds_tpc1 
    global pds_coordinates_tpc1
    global muon_lines_tpc1
    global mcparts_lines_tpc1
    global crt_lines_tpc1
    
    global coatings
    global mmax,mmax_global,mmax_dynamic
    global t0s
    
    ctx = dash.callback_context
    # Check if the button triggered the callback or if a coating was changed
    if ctx.triggered[0]['prop_id'] == 'submit-button.n_clicks' or (coatings != values and values != []):  
        coatings = values
        if [run,subrun,event] in l.run_list:
            if VERBOSE: print(f'Retrieving Run {run} Subrun {subrun} Event {event}')
            l.get_event(run, subrun, event)
            
            pds_tpc0 = l.get_pmt_list(t0,t1,dt,tpc=0,coatings=coatings)  
            pds_tpc1 = l.get_pmt_list(t0,t1,dt,tpc=1,coatings=coatings)
            
            if l.load_muon:
                muons_tpc0 = l.get_muon_list(tpc=0)
                muons_tpc1 = l.get_muon_list(tpc=1)
                muon_lines_tpc0 = [muons_tpc0[i].plot_line(i,0) for i in range(len(muons_tpc0))]
                muon_lines_tpc1 = [muons_tpc1[i].plot_line(i,1) for i in range(len(muons_tpc1))]
            else:
                muon_lines_tpc0 = [go.Scatter()]
                muon_lines_tpc1 = [go.Scatter()]
            if l.load_mcpart:
                mcparts = l.get_mcpart_list()
                mcparts_lines_tpc0 = [mcparts[i].plot_line(i,0,max_color=len(mcparts),filter_tpc=MCPART_FILTER_TPC) for i in range(len(mcparts))]
                mcparts_lines_tpc1 = [mcparts[i].plot_line(i,1,max_color=len(mcparts),filter_tpc=MCPART_FILTER_TPC) for i in range(len(mcparts))]
            else:
                mcparts_lines_tpc0 = [go.Scatter()]
                mcparts_lines_tpc1 = [go.Scatter()]
            if l.load_crt:
                crt_trks = l.get_crt_list()
                crt_lines_tpc0 = [crt_trks[i].plot_line(i,0,max_color=len(crt_trks),filter_tpc=CRT_FILTER_TPC) for i in range(len(crt_trks))]
                crt_lines_tpc1 = [crt_trks[i].plot_line(i,1,max_color=len(crt_trks),filter_tpc=CRT_FILTER_TPC) for i in range(len(crt_trks))]
            else:
                crt_lines_tpc0 = [go.Scatter()]
                crt_lines_tpc1 = [go.Scatter()]
        else:
            print(f'-Run {run} Subrun {subrun} Event {event} not in file')
            if VERBOSE: 
                return None
    
    #PDS
    #if VERBOSE: print('Update time window')
    s0 = time()
    #Get t0s for each pds
    set_t0s() #sets t0s
    set_t0_minmax()
    set_mmax(start_time_bin,start_time_bin+dt_window_size)
    set_pds_coordinates(start_time_bin,start_time_bin+dt_window_size)
    s1 = time()
    if VERBOSE: print(f'-Get PE from {start_time_bin} to {start_time_bin+dt_window_size} (ns): {s1-s0:.2f} s')
    return [get_tpc0(),get_tpc1(),f'Max PE : {mmax:.2f}',f'Global Max PE : {mmax_global:.2f}',f'Current Max PE : {mmax_dynamic:.2f}']


# Callback to update the waveform graph when the button is clicked
@app.callback(
    dash.dependencies.Output('waveform-graph-tpc0', 'figure'),
    [dash.dependencies.Input('tpc0', 'clickData')]
)

def update_waveform_graph(click_data):
    if click_data is not None:
        if VERBOSE: print('-Drawing waveform')
        pmt_id = click_data['points'][0]['customdata']
        #find index of pmt
        ind = [i for i,p in enumerate(pds_tpc0) if pmt_id == p.id] 
        assert len(ind) == 1, f'Error: More than one PDS with id {pmt_id}'
        ind = ind[0]
        s0 = time()
        waveform_data = pds_tpc0[ind].plot_waveform()
        s1 = time() 
        if VERBOSE: print(f'-Get waveform for PDS {pmt_id}: {s1-s0:.2f} s')
            
        if waveform_data is not None:
            if VERBOSE: print('-Done')
            return get_waveform(waveform_data,pmt_id=pmt_id)

    return go.Figure()

# Callback to update the waveform graph when the button is clicked
@app.callback(
    dash.dependencies.Output('waveform-graph-tpc1', 'figure'),
    [dash.dependencies.Input('tpc1', 'clickData')]
)

def update_waveform_graph(click_data):
    if click_data is not None:
        #if VERBOSE: print('-Drawing waveform')
        pmt_id = click_data['points'][0]['customdata']
        #find index of pmt
        ind = [i for i,p in enumerate(pds_tpc1) if pmt_id == p.id] 
        assert len(ind) == 1, f'Error: More than one PDS with id {pmt_id}'
        ind = ind[0]
        s0 = time()
        waveform_data = pds_tpc1[ind].plot_waveform()
        s1 = time() 
        if VERBOSE: print(f'-Get waveform for PDS {pmt_id}: {s1-s0:.2f} s')
        if waveform_data is not None:
            return get_waveform(waveform_data,pmt_id=pmt_id)
        else:
            if VERBOSE: print(f'-No waveform data for PDS {pmt_id}')

    return go.Figure()


if __name__ == '__main__':
    app.run_server(debug=True)