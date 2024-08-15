sudo apt update -y
sudo apt install build-essential git dkms bc -y
git clone https://github.com/morrownr/rtl8852bu
cd rtl8852bu
chmod +x install-driver.sh
sudo sh install-driver.sh

sudo usb_modeswitch -KW -v 0bda -p 1a2b