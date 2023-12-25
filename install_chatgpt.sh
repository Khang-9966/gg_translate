apt update
apt install -y python3-pip
pip3 install -U setuptools
pip3 install -U jupyter
pip3 install pandas
apt install -y libu2f-udev fonts-liberation libvulkan1
apt install wget
dpkg -i chrome_114_amd64.deb
# wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zipwget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zipwget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zipwget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zipwget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
apt install unzip
unzip -o chromedriver_linux64.zip
mv chromedriver /usr/bin/chromedriver
chown root:root /usr/bin/chromedriver
chmod +x /usr/bin/chromedriver
apt install -y libjpeg8-dev zlib1g-dev
#python3 -m pip install pip==19.3.1
pip3 install tqdm
pip3 install Cython
pip3 install beautifulsoup4
pip3 install python-xlib
apt-get install -y python3-tk python3-dev
pip3 install pandas
pip3 install flask
pip3 install selenium
pip3 install -U python-xlib
apt-get install -y python3-tk
apt-get -y install scrot
apt-get install python3-dev
pip3 install python3-xlib
pip3 install PyAutoGUI==0.9.54
