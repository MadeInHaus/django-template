# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "precise32"

  # The url from where the 'config.vm.box' box will be fetched if it
  # doesn't already exist on the user's system.
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"
  
  config.vm.network :forwarded_port, guest: 8000, host: 8080
  config.vm.synced_folder "./", "/var/www"
  config.vm.synced_folder "salt/roots/", "/srv/"
  
  

  ## Use all the defaults:
  config.vm.provision :salt do |salt|
    salt.run_highstate = true
    salt.minion_config = Dir.pwd + "/salt/minion"
    salt.verbose  = true
  end

end