sudo apt update -y
sudo apt install build-essential git dkms bc -y
git clone https://github.com/brektrou/rtl8821CU.git
cd rtl8821CU
chmod +x install-driver.sh
sudo sh install-driver.sh