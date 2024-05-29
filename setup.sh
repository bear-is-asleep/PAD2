source /cvmfs/sbnd.opensciencegrid.org/products/sbnd/setup_sbnd.sh
setup python v3_9_13
setup root v6_26_06b -q e26:p3913:prof
source env/bin/activate

#export PYTHONPATH=$PYTHONPATH:$PWD
export PYTHONPATH=$PWD #only use current directory to ensure correct version(s) is used
export MPLCONFIGDIR=$PWD/.config/matplotlib