# PDS Analysis Display (PAD)

## Authors
Bear Carlson - bcarlson1@ufl.edu

## Quick setup
`git clone https://github.com/bear-is-asleep/PAD2.git`
`cd PAD2`
`source init.sh` (or `source setup.sh` if `env` is already setup)
`python run_pad.py`

## Introduction
Pad is a commissioning tool designed for SBND's PDS system. It's main purpose is to verify the channel mapping of the PDS components by overlying the light the observe with low level reconstructed tracks. The two types of tracks we use in commissioning are [muon tracks](https://github.com/SBNSoftware/sbndcode/blob/develop/sbndcode/Commissioning/MuonTrackProducer_module.cc) and CRT tracks (*to-do*). When a particle passes through the TPC, the PDS components closest to the track are expected to see the most light in general. So PAD is able to view the cumulative light within a time window collected by each PDS. Additionally, clicking on a PDS when in the PAD window shows the raw waveform in the plot window below. PAD also supports both TPCs which are updated simultaneously. Lastly, PAD runs on [dask](https://www.dask.org/) which skips port forwarding on the browser which makes PAD much faster than using terminal port forwarding.

## Installing
To install clone this repo wherever you want - I'd recommend your `app` directory

`git clone https://github.com/bear-is-asleep/PAD2.git`


## Preparing data
The data requires optical detector information but the waveforms are optional. First set up `sbndcode`

`source /cvmfs/sbnd.opensciencegrid.org/products/sbnd/setup_sbnd.sh`

`setup sbndcode v09_73_00 -q e20:prof` *(earlier versions not supported by PAD)*

Now you run your fcl in the typical way up to detector simulation - 
```
lar -c <your-generation-fcl>.fcl
lar -c standard_g4_sbnd.fcl -s [Gen root file].root
lar -c standard_detsim_sbnd.fcl -s [G4 root file]
```

### Waveforms - optional
Waveforms come from the software trigger producer, so we need to run the pmt trigger chain

Then run the pmt trigger chain
```
lar -c run_pmttriggerproducer.fcl -s [DetSim root file]
lar -c run_pmtArtdaqFragmentProducer.fcl -s [PMT hardware trigger root file]
```

Next make sure you set `SaveHists: true` in the [pmt software trigger producer fcl](https://github.com/SBNSoftware/sbndcode/blob/b93d59d593f94e7f91c903fda60c3edbb2e3fb1c/sbndcode/Trigger/PMT/pmtsoftwaretriggerproducer.fcl) to produce `test_hist.root` which contains the waveforms. Now you can get the waveforms by running 

`lar -c run_pmtsoftwaretriggerproducer.fcl -s [PMT fragment simulation root file]`

### Hitdumper
[Hitdumper](https://github.com/SBNSoftware/sbndcode/blob/develop/sbndcode/Commissioning/HitDumper_module.cc) is the commissioning tree that contains all of the available commissioning data. It also contains truth neutrino energy from GENIE. You can run this directly on a detsim file or on the software trigger producer output file. If you want software metrics make sure this line in the [hitdumper fcl](https://github.com/SBNSoftware/sbndcode/blob/develop/sbndcode/Commissioning/fcls/hitdumpermodule.fcl) is set to true `readpmtSoftTrigger: true`. If you want PAD to show the full reconstructed PE (deconvolution, noise filtering, etc.) set this line to true `readOpHits: true`.

#### Muon tracks - optional
The commissioning muon tracks are not turned on by default, but are optional for pad. If you want them in hitdumper set this line to true `readMuonTracks: true` and this line to true `readMuonHits: true`.

Now that the fcl is prepared you can run 

`lar -c run_hitdumper.fcl -s [DetSim or PMT software trigger root file]`

## Running PAD

### Initialize
To initialize the python enviroment - only need to do this once

`source init.sh`

### Setup
To set it up just requires setting up the enviroment again

`source setup.sh`

### Run
`Loader` drives PAD and sets up all of the products to include. You can find out more about the parameters of the loader by running `python run_pad.py --help`

```
usage: run_pad.py [-h] [--data DATA] [--pad PAD] [--hdump_name HDUMP_NAME] [--sm_name SM_NAME] [--wfm_name WFM_NAME] [--load_muon LOAD_MUON] [--load_crt LOAD_CRT] [--mode MODE]

Load data

optional arguments:
  -h, --help            show this help message and exit
  --data DATA           Path to the data
  --pad PAD             PAD directory
  --hdump_name HDUMP_NAME
                        hitdumper file name
  --sm_name SM_NAME     pmt software metrics file name
  --wfm_name WFM_NAME   waveform file name
  --load_muon LOAD_MUON
                        load muon info
  --load_crt LOAD_CRT   load crt info
  --mode MODE           Optical detector mode
```


Alternatively you can set the filenames using a config. Set this line `from config.default import *` to point to you configuration file, which should be formatted like this

```
#default.py example

#Setup for PMT timing
t0 = -1600 #Start time for PE range [ns]
t1 = 1600 #End time for PE range [ns]
dt = 2 #Step size [ns]

#Get directories
DATA_DIR = '/sbnd/data/users/brindenc/PAD/test_fcl/v1' #Waveforms and hitdumper location
SAVE_DIR = '/sbnd/data/users/brindenc/PAD/figures' 
PAD_DIR  = '/sbnd/app/users/brindenc/PAD' #Your local PAD dir

#Get fnames
HDUMP_NAME = 'hitdumper_tree.root'
WFM_NAME = 'test_hist.root' #WFM_NAME = None if you did not make waveforms
SM_NAME = None

#Settings
VERBOSE = True

#Hdr keys
HDRKEYS = ['run','subrun','event']

#Coatings
COATINGS = [0,1,2,3,4] #All PDS components
```

In the terminal at the base of your PAD directory type `python run_pad.py <--options>`. Dask will show a link to the event display like this

```
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'run_pad'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8050
Press CTRL+C to quit
127.0.0.1 - - [21/Jul/2023 13:03:04] "GET / HTTP/1.1" 200 -
```

Opening `http://127.0.0.1:8050` in a browser will take you to the PAD display.

![PAD](https://github.com/bear-is-asleep/PAD2/blob/master/Images/PAD2.png)

### Actions
Time sliders change the range to integrate the PE for each PDS component
* Moving the t0 slider will change the initial time for both TPCs
* Moving the t1 slider will change the final time for both TPCs
* Takes about 100 ms to update

A list of available runs are on the right
* Entering the run, subrun, event of an event from the list on the right and clicking submit will update PAD to that readout
* Takes about 10 s to update

⚠️ **Repeatedly clicking submit will overload the update command and cause the update to take a lot longer**

The waveforms for each TPC are shown just below in ADC vs. time [us] (*X-ARAPUCA waveforms are not included*)
* Clicking on a PDS shows its waveform
* Takes about 50 ms to update


## To-do 
* Display run, subrun, event after it's loaded/include loading bar
* Add option to filter out PDS by coating - supported but not an option in dash window
* Get official channel mapping (current one stored in `PMT_ARAPUCA_info.pkl`)
* Get X-ARAPUCA waveform information
* Implement truth level information - new class
* Implement CRT tracks - new class
* Make PAD prettier - include logo
