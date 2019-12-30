echo Installing srsLTE ...
cd /home/loccs/usrp
git clone https://github.com/srsLTE/srsLTE.git
cd srsLTE
mkdir build
cd build
cmake ../
make -j8
make test
sudo make install
sudo ldconfig
sudo srslte_install_configs.sh user