curl -fsSL https://get.docker.com -o get-docker.sh
echo "installing docker.."
sudo sh get-docker.sh

echo "add docker to user group.."
sudo usermod -aG docker $USER
groups ${USER}

echo "installing docker-compose.."
sudo apt install -y docker-compose


sudo apt install python3-pip

read -p "Would you like to reboot now? (y/n) " answer
# 사용자의 응답에 따라 스크립트 실행 여부 결정
if [[ "$answer" == "y" || "$answer" == "Y" ]]; then
    echo "Running the script..."
    # 여기에 실행할 스크립트를 추가합니다.
    sudo reboot -h now
else
    echo "Script execution canceled."
fi