FROM ess-repos01.wisers.com:8889/imgrec/pytorch:1.12.1-cuda11.6.2-cudnn8-devel
#RUN gpg --keyserver keyserver.ubuntu.com --recv-key 1A127079A92F09ED
#RUN apt-get update -y
#RUN apt-get install -y vim

COPY ailab/ /ailab/
COPY ailab/requirements.txt ./
COPY ailab/requirements/ ./requirements/
RUN pip install --ignore-installed --no-cache-dir -r requirements.txt
#RUN pip install --upgrade pip --ignore-installed && pip install --no-cache-dir -r requirements.txt
#RUN pip install --upgrade pip --ignore-installed

WORKDIR /ailab

EXPOSE 8080
ENTRYPOINT ["/bin/bash", "start.sh"]
