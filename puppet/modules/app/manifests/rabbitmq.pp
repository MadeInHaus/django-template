class app::rabbitmq {
    package{'rabbitmq-server':
        ensure => installed
    }
}