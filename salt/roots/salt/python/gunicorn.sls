include:
  - python

gunicorn:
  pip:
    - installed
    - require:
      - pkg: python
