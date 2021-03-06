# Inherit from base node
FROM node:6.7.0-wheezy
ARG NPM_REGISTRY=http://registry.npmjs.org/
ARG PACKAGE_INSTALLER=npm


# Set our env vars
ENV PYTHONUNBUFFERED 1
ENV PATH=/app/user/node_modules/.bin:$PATH

RUN apt-get update && apt-get install -y \
        python-pip python-dev build-essential \
		gcc \
		gettext \
		mysql-client libmysqlclient-dev \
		postgresql-client libpq-dev \
		sqlite3 \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

# Create some needed directories
RUN mkdir -p /app/user && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* &&\
    if [ "$PACKAGE_INSTALLER" = "yarn" ]; then \
        npm install -g yarn; \
        ${PACKAGE_INSTALLER} config set ignore-optional false; \
    fi &&\
    ${PACKAGE_INSTALLER} config set registry "$NPM_REGISTRY"

WORKDIR /app/user
COPY package.json yarn.lock requirements.txt /app/user/
RUN $PACKAGE_INSTALLER install && \
    $PACKAGE_INSTALLER cache clean
RUN pip install -r requirements.txt
COPY . /app/user
# RUN gulp production
