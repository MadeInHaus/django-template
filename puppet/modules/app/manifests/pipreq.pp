class app::pipreq {

    package{['libevent-dev']:
            ensure => installed
    }
    
    exec{'pip-install':
    	require => Package['python-pip','postgresql','libpq-dev','rabbitmq-server','redis-server','memcached','libevent-dev'],
        command => "sudo pip install -r /var/www/requirements.txt",
    	timeout => 0,
        user => root,
    }
}
