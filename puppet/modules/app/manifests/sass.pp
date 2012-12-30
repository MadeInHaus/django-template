class app::sass{
    package {['sass','rb-inotify', 'listen']:
        provider => 'gem',  
        ensure => installed
    }
}