include:
  - python

libevent-dev:
  pkg:
    - installed

gevent:
  pip:
    - installed
    - require:
      - pkg: python
      - pkg: libevent-dev
