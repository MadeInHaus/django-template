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
}
