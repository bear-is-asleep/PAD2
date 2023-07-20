# PDS Analysis Display (PAD)
Pad is a commissioning tool designed for SBND's PDS system. It's main purpose is to verify the channel mapping of the PDS components by overlying the light the observe with low level reconstructed tracks. The two types of tracks we use in commissioning are [muon tracks](https://github.com/SBNSoftware/sbndcode/blob/develop/sbndcode/Commissioning/MuonTrackProducer_module.cc) and CRT tracks (*to-do*). When a particle passes through the TPC, the PDS components closest to the track are expected to see the most light in general. So PAD is able to view the cumulative light within a time window collected by each PDS. Additionally, clicking on a PDS when in the PAD window shows the raw waveform in the plot window below. PAD also supports both TPCs which are updated simultaneously. Lastly, PAD runs on [dask](https://www.dask.org/) which skips port forwarding on the browser which makes PAD much faster than using terminal port forwarding.

## Installing

## Preparing data
### Waveforms
### Hitdumper

## Running PAD
### Initialize
### Run

## To-do 
* Implement truth level information
* Implement CRT tracks
