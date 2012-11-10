class app::postgresql{
    package{['postgresql','libpq-dev']:
        ensure => installed
    }

    service{ "postgresql":
        ensure     => running,
        enable     => true,
        hasrestart => true,
        require    => Package['postgresql']
    }

    exec{"create db":
    	require => Package['postgresql'],
    	command => "createdb django",
    	user => postgres

    }
    #TODO
    # execute 'createuser vagrant'

}
