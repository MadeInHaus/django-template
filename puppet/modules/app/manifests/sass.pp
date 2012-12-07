class app::sass{
    package { 'sass':
        provider => 'gem',  
        ensure => installed
    }
}