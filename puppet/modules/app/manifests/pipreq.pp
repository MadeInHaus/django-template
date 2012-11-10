class app::pipreq {

    exec{'pip-install':
    	require => Package['python-pip','postgresql','libpq-dev','rabbitmq-server'],
        command => "sudo pip install -r /var/www/requirements.txt",
    	timeout => 0,
        user => root,
    }
}