memcached:
  pkg.installed:
    - name: memcached
  service:
    - name: memcached
    - running
