from fabric.api import env
import vagrant, prod, dev, staging
from vagrant import runall, killall, resetdb, resetall

env.roledefs       = {
                      'vagrant'                : ['vagrant@127.0.0.1:2222']
                     }
env.passwords      = {
                      'vagrant@127.0.0.1:2222'      :'vagrant',
                     }
