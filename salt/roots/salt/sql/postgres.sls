postgresql-server:
  pkg.installed:
  {% if grains['os'] == 'RedHat' %}
    - name: postgresql-server
  {% elif grains['os'] == 'Ubuntu' %}
    - name: postgresql
  {% endif %}
  service:
    - name: postgresql
    - running
  libpq-dev:
    - installed
