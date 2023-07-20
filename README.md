# PDS Analysis Display (PAD)
Pad is a commissioning tool designed for SBND's PDS system. It's main purpose is to verify the channel mapping of the PDS components by overlying the light the observe with low level reconstructed tracks. The two types of tracks we use in commissioning are [muon tracks](https://github.com/SBNSoftware/sbndcode/blob/develop/sbndcode/Commissioning/MuonTrackProducer_module.cc) and CRT tracks (*to-do*). When a particle passes through the TPC, the PDS components closest to the track are expected to see the most light in general. So PAD is able to view the cumulative light within a time window collected by each PDS. Additionally, clicking on a PDS when in the PAD window shows the raw waveform in the plot window below. PAD also supports both TPCs which are updated simultaneously. Lastly, PAD runs on [dask](https://www.dask.org/) which skips port forwarding on the browser which makes PAD much faster than using terminal port forwarding.

## Installing
To install clone this repo

`git clone https://github.com/bear-is-asleep/PAD2.git`

To initialize the python enviroment - only need to do this once

`source init.sh`

To set it up just requires setting up the enviroment again

`source setup.sh`


## Preparing data
The data requires optical detector information but the waveforms are optional. First set up `sbndcode`

`source /cvmfs/sbnd.opensciencegrid.org/products/sbnd/setup_sbnd.sh`

`setup sbndcode v09_73_00 -q e20:prof` *(earlier versions not supported by PAD)*

Now you run your fcl in the typical way up to detector simulation - 
```
lar -c <your-generation-fcl>.fcl
lar -c standard_g4_sbnd.fcl -s <artroot-ouput-of-gen>.root
lar -c standard_detsim_sbnd.fcl -s <artroot-ouput-of-g4>.root
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

#### Muon tracks
The commissioning muon tracks are not turned on by default, but are optional for pad. If you want them in hitdumper set this line to true `readMuonTracks: true` and this line to true `readMuonHits: true`.

## Running PAD
`Loader` drives PAD and sets up all of the products to include. Set the 
### Initialize
### Run

## To-do 
* Implement truth level information
* Implement CRT tracks
