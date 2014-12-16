Vagrant.configure("2") do |config|

  config.vm.box = "dummy"
  config.vm.network "forwarded_port", guest: 5000, host: 5000

  config.vm.define "h" do |machine|      

    machine.vm.synced_folder ".", "/h"

    machine.vm.provision :chef_solo do |chef|
      chef.cookbooks_path = ["cookbooks", "chef/applications"]
      chef.roles_path = "chef/roles"
      chef.add_role "h"      
    end

  end

  config.vm.provider :virtualbox do |vb, override|
    vb.customize ["modifyvm", :id, "--memory", "1024"]
    vb.customize ["modifyvm", :id, "--cpus", "1"]
    override.vm.box = "trusty64"
    override.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"
  end

  config.omnibus.chef_version = "11.16.4"

  config.vm.provider :digital_ocean do |provider, override|
    override.ssh.private_key_path = '~/.ssh/id_rsa'
    override.vm.box = 'digital_ocean'
    override.vm.box_url = "https://github.com/smdahlen/vagrant-digitalocean/raw/master/box/digital_ocean.box"

    provider.token = 'c842ecf096fdf1514dd3758d87dc0065d580a65eb285ac4a72f74ca40ad88b83'
    provider.image = 'ubuntu-14-04-x64'
    provider.region = 'nyc3'
    provider.size = '512mb'
  end

  config.vm.provider :aws do |aws, override|
    aws.access_key_id = "YOUR_ACCESS_KEY"      
    aws.secret_access_key = "YOUR_SECRET_KEY"
    aws.keypair_name = "YOUR_KEYPAIR_NAME"
    aws.ami = "ami-864d84ee"
    aws.instance_type = "t2.micro"      
    aws.region = "us-east-1"
    aws.availability_zone = "us-east-1a"
    override.ssh.private_key_path = "PATH_TO_KEY"
  end

end