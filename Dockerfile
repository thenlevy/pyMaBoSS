FROM pauleve/pint
EXPOSE 8888

#RUN conda install -c conda-forge ipywidgets --yes
RUN apt-get update && apt-get install git wget -y 
RUN pip3 install -U --user git+https://github.com/GINsim/GINsim-python
RUN wget http://ginsim.org/sites/default/files/ginsim-dev/GINsim-2.9.6-SNAPSHOT-jar-with-dependencies.jar -O /bin/GINsim.jar \
    && echo '#!/bin/bash' > /bin/GINsim \
    && echo 'java -jar "/bin/GINsim.jar" "${@}"' >> /bin/GINsim \
    && chmod +x /bin/GINsim


RUN pip3 install -U pyparsing \
    && pip3 install -U pandas \
    && pip3 install -U matplotlib
RUN curl -LO https://maboss.curie.fr/pub/MaBoSS-2.0.tgz \
   && tar xvfz MaBoSS-2.0.tgz -C / \
   && ln -s /MaBoSS-2.0/binaries/linux-x86/MaBoSS /bin/MaBoSS
RUN pip3 install ipywidgets \
    && jupyter nbextension enable --py widgetsnbextension
RUN pip3 install -U --user git+https://github.com/thenlevy/pyMaBoSS
COPY model /model
COPY notebook /notebook/
