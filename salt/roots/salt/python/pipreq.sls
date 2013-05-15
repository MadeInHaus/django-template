include:
  - python

python.pil.requirements:
    pkg.installed:
        - pkgs:
            - libjpeg8
            - libpng12-0
            - libfreetype6
            - zlib1g
    

python.create.virtualenv:
  cmd.run:
    - name: virtualenv --no-site-packages /home/vagrant/.venv
    - unless: test -d /home/vagrant/.venv
    - require: 
      - pkg: python

python.setup.virtualenv:
  cmd.run:
    - name: echo 'source /home/vagrant/.venv/bin/activate' >> /home/vagrant/.bashrc
    - unless: grep -c 'source /home/vagrant/.venv/bin/activate' /home/vagrant/.bashrc
    - require: 
      - pkg: python
      - cmd: python.create.virtualenv

python.setup.virtualenvfabric:
  cmd.run:
    - name: echo 'source /home/vagrant/.venv/bin/activate' >> /home/vagrant/.profile
    - unless: grep -c 'source /home/vagrant/.venv/bin/activate' /home/vagrant/.profile
    - require: 
      - pkg: python
      - cmd: python.setup.virtualenv

python.update.distribute:
  cmd.run:
    - name: /home/vagrant/.venv/bin/pip install --use-mirrors -U distribute
    - require: 
      - pkg: python
      - cmd: python.setup.virtualenvfabric

python.pip.install:
  cmd.run:
    - name: /home/vagrant/.venv/bin/pip install --use-mirrors -r /var/www/requirements.txt
    - require: 
      - cmd: python.update.distribute
