node.dependancies:
  pkg.installed:
    - pkgs:
      - curl
      - libssl-dev
      - build-essential

node:
  cmd.run:
    - name: curl -s https://raw.github.com/isaacs/nave/master/nave.sh | bash -s usemain 0.8.15
    - unless: test "v0.8.15" = $(node -v)
    - require: 
      - pkg: node.dependancies
