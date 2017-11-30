FROM colomoto/colomoto-docker

RUN conda install -c conda-forge ipywidgets --yes
RUN pip install -U pyparsing \
    && pip install -U pandas \
    && pip install -U matplotlib
RUN apt-get update && apt-get install git --yes
RUN pip install -U --user git+https://github.com/thenlevy/pyMaBoSS
COPY model /model
COPY notebook /notebook/
