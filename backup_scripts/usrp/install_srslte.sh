echo Installing srsLTE ...
# sudo apt-get update
# sudo apt-get install cmake libfftw3-dev libmbedtls-dev libboost-program-options-dev libconfig++-dev libsctp-dev
cd /home/loccs/usrp
git clone https://github.com/srsLTE/srsLTE.git
cd srsLTE
mkdir build
cd build
cmake ../
make
make test
sudo make install
sudo ldconfig
sudo srslte_install_configs.sh user


# # Verifying srsLTE operations
# # change epc.conf, enb.conf, user_db.csv
# sudo srsepc
# sudo srsenb