# ---------- base image ----------
FROM ubuntu:24.04

RUN apt-get update && apt-get install -y --no-install-recommends \
        git libc6 python3.12 python3.12-venv python3.12-dev python3-pip redis-tools \
        build-essential cmake wget curl ca-certificates gnupg \
    && rm -rf /var/lib/apt/lists/*

# ---------- Node.js 20 LTS ----------
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
&& apt-get update \
&& apt-get install -y --no-install-recommends nodejs \
&& rm -rf /var/lib/apt/lists/* \
&& node -v && npm -v   # sanity-check


# ---------- Python virtual-env & deps ----------
ENV VIRTUAL_ENV=/opt/venv
RUN python3.12 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt /tmp/
RUN $VIRTUAL_ENV/bin/pip install --upgrade pip && \
    $VIRTUAL_ENV/bin/pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

ENV PYTHONPATH="$VIRTUAL_ENV/lib/python3.12/site-packages:/cdvistapp/app/lib:/cdvistapp/app"

# ---------- install bioinformatics tools ----------
# Install HMMER
RUN wget http://eddylab.org/software/hmmer/hmmer.tar.gz -O /tmp/hmmer.tar.gz && \
    tar -xzf /tmp/hmmer.tar.gz -C /tmp && \
    cd /tmp/hmmer-* && \
    ./configure && make && make install && \
    rm -rf /tmp/hmmer*

# Install HHsearch (from HH-suite)
RUN git clone https://github.com/soedinglab/hh-suite.git && \
    mkdir -p hh-suite/build && cd hh-suite/build && \
    cmake -DCMAKE_INSTALL_PREFIX=. .. && \
    make -j 4 && make install && \
    cd /

ENV PATH="/hh-suite/build/bin:/hh-suite/build/scripts:$PATH"

# Install BLAST
RUN wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.16.0+-x64-linux.tar.gz -O /tmp/blast.tar.gz && \
    tar -xzf /tmp/blast.tar.gz -C /tmp && \
    mv /tmp/ncbi-blast*/bin/* /usr/local/bin/ && \
    rm -rf /tmp/blast*


# Install TMHMM
# ENV TMHMMKEY="63374a58-11ea-41bd-9d71-84acbc5cf611"
# RUN wget https://services.healthtech.dtu.dk/download/${TMHMMKEY}/tmhmm-2.0c.Linux.tar.gz -O /tmp/tmhmm.tar.gz && \
#     tar -xzf /tmp/tmhmm.tar.gz -C /tmp && \


# # ---------- Install Docker CLI manually ----------
# RUN curl -L https://download.docker.com/linux/static/stable/x86_64/docker-24.0.7.tgz -o docker.tgz && \
#     tar xzvf docker.tgz && \
#     mv docker/docker /usr/bin/docker && \
#     rm -rf docker docker.tgz

WORKDIR /cdvist

CMD ["flask", "run", "--host=0.0.0.0"]
