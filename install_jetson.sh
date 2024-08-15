# change sshd config to allow password login
echo "Changing sshd config"
echo "------------------------"
sudo sed -i 's/# PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
# uncomment the listen address in sshd_config
sudo sed -i 's/# ListenAddress 0.0.0.0/ListenAddress 0.0.0.0/g' /etc/ssh/sshd_config
sudo systemctl restart sshd


# install prerequisites
echo "Installing prerequisites"
echo "------------------------"
sudo apt-get update -y
sudo apt install -y nano
sudo apt install -y curl
sudo apt install build-essential git dkms bc -y
sudo apt install -y cmake
sudo apt install -y python3-pip


# update docker and install docker-compose
echo "Updating Docker"
echo "------------------------"
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
# sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo add-apt-repository "deb [arch=arm64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker $USER
sudo systemctl enable docker
sudo systemctl start docker
sudo apt-get install -y docker-compose

# install jetson-stats
echo "Installing jetson-stats"
echo "------------------------"
sudo -H pip3 install -U jetson-stats


# install wifi driver
echo "Installing wifi driver"
echo "------------------------"
git clone https://github.com/morrownr/rtl8852bu
cd rtl8852bu
chmod +x install-driver.sh
sudo sh install-driver.sh

sudo usb_modeswitch -KW -v 0bda -p 1a2b

