FROM kunstmaan/base-multichain
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    build-essential \
    ca-certificates \
    gcc \
    libpq-dev \
    make \
    python-pip \
    python2.7 \
    python2.7-dev \
    ssh \
    && apt-get autoremove \
    && apt-get clean
RUN pip install -U "pip==9.0.1"
RUN pip install ipython
RUN pip install Flask
RUN pip install requests
COPY multichaind-cold /usr/local/bin/multichaind-cold
RUN mkdir -p /root/.multichain-cold/test1
