class app::node{
	class { 'nodejs':
		version => 'v12.0.0',
	}

    package { 'grunt-cli':
       ensure => present,
       provider => 'npm'
   }
}
