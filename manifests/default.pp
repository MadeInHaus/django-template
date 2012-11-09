# Basic Puppet Apache manifest

class apache {
    exec { 'apt-get update':
        command => '/usr/bin/apt-get update'
    }

    package { "apache2":
        ensure => present,
    }

    service { "apache2":
        ensure => running,
        require => Package["apache2"],
    }
}

include apache

class git {
    package { "git-core":
        ensure => present,
    }
}

include git

class python27 {
    build-install::install {"Python-2.7.3": download => "http://python.org/ftp/python/$version/Python-2.7.3.tgz", creates => "/usr/local/bin/python", }
}

include python27
