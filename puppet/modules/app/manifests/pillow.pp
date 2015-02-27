class app::pillow {

    $packageList = [
    'gifsicle',
    'optipng',
    'libtiff4-dev',
    'libjpeg-dev',
    'libjpeg-progs',
    'zlib1g-dev',
    'libfreetype6-dev',
    'liblcms1-dev',
    'tcl8.5-dev',
    'tk8.5-dev'
    ]

    package { $packageList: }

   package { 'svgo':
      ensure => present,
      provider => 'npm'
   }
    
}

