echo Installing UHD ...
# sudo apt-get update
# sudo apt-get -y install git swig cmake doxygen build-essential libboost-all-dev libtool libusb-1.0-0 libusb-1.0-0-dev libudev-dev libncurses5-dev libfftw3-bin libfftw3-dev libfftw3-doc libcppunit-1.14-0 libcppunit-dev libcppunit-doc ncurses-bin cpufrequtils python-numpy python-numpy-doc python-numpy-dbg python-scipy python-docutils qt4-bin-dbg qt4-default qt4-doc libqt4-dev libqt4-dev-bin python-qt4 python-qt4-dbg python-qt4-dev python-qt4-doc python-qt4-doc libqwt6abi1 libfftw3-bin libfftw3-dev libfftw3-doc ncurses-bin libncurses5 libncurses5-dev libncurses5-dbg libfontconfig1-dev libxrender-dev libpulse-dev swig g++ automake autoconf libtool python-dev libfftw3-dev libcppunit-dev libboost-all-dev libusb-dev libusb-1.0-0-dev fort77 libsdl1.2-dev python-wxgtk3.0 git libqt4-dev python-numpy ccache python-opengl libgsl-dev python-cheetah python-mako python-lxml doxygen qt4-default qt4-dev-tools libusb-1.0-0-dev libqwtplot3d-qt5-dev pyqt4-dev-tools python-qwt5-qt4 cmake git wget libxi-dev gtk2-engines-pixbuf r-base-dev python-tk liborc-0.4-0 liborc-0.4-dev libasound2-dev python-gtk2 libzmq3-dev libzmq5 python-requests python-sphinx libcomedi-dev python-zmq libqwt-dev libqwt6abi1 python-six libgps-dev libgps23 gpsd gpsd-clients python-gps python-setuptools

cd /home/loccs/usrp
git clone https://github.com/EttusResearch/uhd
cd uhd

# git checkout release_003_008_004
# git checkout release_003_009_005
# git checkout release_003_010_000_000
# git checkout v3.12.0.0
# git checkout v3.13.1.0
git checkout v3.15.0.0

cd host
mkdir build
cd build
cmake ../
make
make test
sudo make install
sudo ldconfig

# # Append to `.bashrc`
# export LD_LIBRARY_PATH=/usr/local/lib

sudo uhd_images_downloader

# # Configureing USB
cd /home/loccs/usrp/uhd/host/utils
sudo cp uhd-usrp.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger

# # Thread priority sheduling
sudo groupadd usrp
sudo usermod -aG usrp $USER

# # Append to `/etc/security/limits.conf`
# @usrp - rtprio  99

# # Verifying UHD operations
# cd /usr/local/lib/uhd/examples
# sudo ./rx_samples_to_file --freq 98e6 --rate 5e6 --gain 20 --duration 10 usrp_samples.dat
# sudo ./tx_samples_from_file --freq 915e6 --rate 5e6 --gain 10 usrp_samples.dat 
