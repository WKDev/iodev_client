sudo usermod -l sid tr


sudo pkill -u tr pid

sudo pkill -9 -u tr

# 홈 디렉토리 이름 변경 (선택사항)
sudo usermod -d /home/sid -m sid

# 그룹 이름 변경 (유저네임과 그룹 이름이 동일한 경우)
sudo groupmod -n sid tr


/etc/ssh/sshd_config

sudo nano /etc/hostname
sudo nano /etc/hosts
