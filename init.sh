source /cvmfs/sbnd.opensciencegrid.org/products/sbnd/setup_sbnd.sh
setup python v3_9_13
setup root v6_26_06b -q e26:p3913:prof

python -m venv env
source env/bin/activate
which python
pip install --upgrade pip
pip install wheel setuptools
pip install -r requirements.txt

export PYTHONPATH=$PYTHONPATH:$PWD
export MPLCONFIGDIR=$PWD/.config/matplotlib