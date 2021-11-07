# INSTALL, UPGRADE AND UNINSTALL data_utils

sudo python3 -m pip install --upgrade pip setuptools wheel

mkdir -pv python/projects && cd python/projects

git clone https://github.com/rds1979/data_utils

cd data_utils

pip3 install . 

pip install --upgrade .

pip3 uninstall data_utils
