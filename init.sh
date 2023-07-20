source /cvmfs/sbnd.opensciencegrid.org/products/sbnd/setup_sbnd.sh
setup python v3_9_2

python -m venv env
source env/bin/activate
which python
pip install --upgrade pip
pip install wheel setuptools
pip install -r requirements.txt