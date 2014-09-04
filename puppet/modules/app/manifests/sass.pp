class app::sass{
    package { 'ruby1.9.3': }

    exec { 'install-gems':
      require => Package['ruby1.9.3'],
      command => 'sudo gem1.9.3 install sass rb-inotify listen compass oily_png'
    }
}
