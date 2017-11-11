FROM colomoto/colomoto-docker
EXPOSE 8888


RUN pip install -U pyparsing \
    && pip install -U pandas \
    && pip install -U matplotlib

    
COPY maboss /opt/conda/lib/python3.6/site-packages/maboss
RUN echo '#!/bin/bash ' > /usr/bin/tuto-nb \
  && echo 'jupyter notebook --allow-root --no-browser --ip=* --port=8888' >> /usr/bin/tuto-nb \
  && chmod +x /usr/bin/tuto-nb

CMD tuto-nb
