include:
 - config

/etc/redis/redis.conf:
  file.managed:
    - source: salt://config/redis/redis.conf
redis-server:
  pkg.installed:
    - name: redis-server
  service:
    - name: redis-server
    - running
