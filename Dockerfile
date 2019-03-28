FROM debian:stretch
RUN apt update
RUN apt install -y firefox-esr
RUN apt install -y python3 python3-pip git wget
RUN git clone https://github.com/chrisjsimpson/obp-boostrap-user.git
WORKDIR obp-boostrap-user
RUN pip3 install -r requirements.txt
