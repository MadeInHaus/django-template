class app::pipreq {

    exec{'create-virtualenv':
        command => "virtualenv --no-site-packages /home/vagrant/.venv",
        unless  => "test -d /home/vagrant/.venv",
        timeout => 0,
        user    => vagrant,
    }

    exec{'setup-virtualenv':
        require => Exec['create-virtualenv'],
        command => "echo 'source /home/vagrant/.venv/bin/activate' >> /home/vagrant/.bashrc",
        unless  => "grep -c 'source /home/vagrant/.venv/bin/activate' /home/vagrant/.bashrc",
        user    => vagrant,
    }

    exec{'setup-virtualenv-fabric':
        require => Exec['setup-virtualenv'],
        command => "echo 'source /home/vagrant/.venv/bin/activate' >> /home/vagrant/.profile",
        unless  => "grep -c 'source /home/vagrant/.venv/bin/activate' /home/vagrant/.profile",
        user    => vagrant,
    }

    exec{'pip-install':
        require => Exec['setup-virtualenv-fabric'],
        command => "/home/vagrant/.venv/bin/pip install -r /var/www/requirements.txt",
        timeout => 0,
        user    => vagrant,
    }
}
