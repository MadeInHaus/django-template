#!/bin/sh
BASEDIR=$(dirname $0)

install_requirements()
{
    installed=1
    for var in b.pypi c.pypi d.pypi pypi; do
        "$BASEDIR/../env/bin/pip" install -i "http://$var.python.org/simple" -r "$BASEDIR/../deploy/requirements/$1.txt"
        installed=$?
        if [ $installed -eq 0 ]; then
            echo "$1 require success"
            break
        fi
    done
    if [ $installed -eq 1 ]; then
            echo "Could not install all $1 requirements"
    fi
}

virtualenv --system-site-packages "$BASEDIR/../env"
if [ $? -ne 0 ]; then
    echo "Trying without system-site-packages"
    virtualenv "$BASEDIR/../env"
fi

if [ $? -eq 0 ]; then
    install_requirements "base"
    for var in "$@"
    do
        v="$BASEDIR/../deploy/requirements/$var.txt"
        if [ -f $v ]; then
            install_requirements $var
        fi
    done
fi
