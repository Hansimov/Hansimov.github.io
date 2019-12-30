echo Installing UHD ...
cd /home/loccs/usrp
git clone https://github.com/EttusResearch/uhd
cd uhd
# git checkout release_003_008_004
# git checkout release_003_009_005
# git checkout release_003_010_000_000
# git checkout v3.12.0.0
git checkout v3.13.1.0
cd host
mkdir build
cd build
cmake ../
make
make test
sudo make install
sudo ldconfig
sudo uhd_images_downloader

# # Verifying UHD operations
# cd /usr/local/lib/uhd/examples
# sudo ./rx_samples_to_file --freq 98e6 --rate 5e6 --gain 20 --duration 10 usrp_samples.dat
# sudo ./tx_samples_from_file --freq 915e6 --rate 5e6 --gain 10 usrp_samples.dat