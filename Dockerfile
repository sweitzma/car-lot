FROM python:3.7-buster

WORKDIR /build/

# pip
ADD requirements.txt /build/
RUN pip install -r requirements.txt
ENV PYTHONPATH=/mnt:${PYTHONPATH}

# install node for jupyter lab
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
      apt-get install -y nodejs && \
      jupyter labextension install \
        @jupyter-widgets/jupyterlab-manager \
        jupyter-matplotlib

WORKDIR /mnt/

ENTRYPOINT ["/bin/bash"]
