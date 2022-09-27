
Vagrant.configure("2") do |config|
    config.vm.box = "centos/7"
    config.vm.network 'private_network', ip: "192.168.50.112",  virtualbox__intnet: true
    config.vm.network "forwarded_port", guest: 22, host: 2222, id: "ssh", disabled: true
    config.vm.network "forwarded_port", guest: 22, host: 2000 # Master Node SSH
    config.vm.network "forwarded_port", guest: 3000, host: 3000 # Port Grafana
    config.vm.network "forwarded_port", guest: 9090, host: 9090 # Port Prometheus
    config.vm.network "forwarded_port", guest: 9100, host: 9100 # Port Node Exporter
    config.vm.network "forwarded_port", guest: 9093, host: 9093 # Port Alerting
    config.vm.provider "virtualbox" do |v|
        v.memory = "4096"
        v.name = "prometheus-k3s"
    end
    config.vm.provision "shell", inline: <<-SHELL
      sudo bash
      sudo yum update -y
      sudo yum install yum-utils device-mapper-persistent-data lvm2 -y
      sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
      sudo yum install docker-ce docker-ce-cli containerd.io -y
      yum install wget -y 
      curl -sfL https://get.k3s.io | sh -
    SHELL
    config.vm.provision "shell", path: "setup.sh"
    
end