FROM ubuntu:latest
EXPOSE 8888
RUN apt-get update \
  && apt-get install -y \
  curl \
  python3 \
  python3-pip \
  && pip3 install --upgrade pip \
  && pip3 install -U pandas \
  && pip3 install -U jupyter \
  && pip3 install -U pyparsing \
  && pip3 install -U seaborn \
  && pip3 install -U numpy \
  && pip3 install -U matplotlib \
  && curl -LO https://maboss.curie.fr/pub/MaBoSS-2.0.tgz \
  && tar xvfz MaBoSS-2.0.tgz \
  && ln -s /MaBoSS-2.0/binaries/linux-x86/MaBoSS /usr/bin/MaBoSS

COPY maboss /maboss
COPY test /test
COPY Tutorial.ipynb /Tutorial.ipynb

RUN echo '#!/bin/bash ' > /usr/bin/tuto-nb \
  && echo 'jupyter notebook --allow-root --no-browser --ip=* --port=8888' >> /usr/bin/tuto-nb \
  && chmod +x /usr/bin/tuto-nb

CMD tuto-nb
