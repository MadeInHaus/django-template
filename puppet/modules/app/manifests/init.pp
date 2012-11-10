class app {
    class{'app::apt-get-update': stage => first }
    #class{'app::pip-requirements': stage => last }
    class{'app::configuration-actions': stage => last }
}

file { "/var/www":
    ensure => "directory",
}