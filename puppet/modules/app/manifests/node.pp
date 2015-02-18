class app::node{
	class { 'nodejs':
		version => 'v0.12.0',
	}

    package { 'grunt-cli':
       ensure => present,
       provider => 'npm'
   }
}
