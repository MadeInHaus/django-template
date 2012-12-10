class app::pipreq {

    exec{'create-virtualenv':
        require => Package['python-pip','postgresql','libpq-dev','rabbitmq-server','redis-server','memcached','libevent-dev'],
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

    exec{'pip-install':
        require => Exec['setup-virtualenv'],
        command => "/home/vagrant/.venv/bin/pip install -r /var/www/requirements.txt",
        timeout => 0,
        user    => vagrant,
    }
}
