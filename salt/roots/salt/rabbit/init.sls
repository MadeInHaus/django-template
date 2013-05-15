rabbitmq-server:
  pkg.installed:
    - name: rabbitmq-server
  service:
    - name: rabbitmq-server
    - running