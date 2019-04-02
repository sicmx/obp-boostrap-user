FROM debian:stretch
RUN apt update
RUN apt install -y firefox-esr
RUN apt install -y python3 python3-pip git wget

# Get obp-python obp cli utilities (getauth, etc)
RUN pip3 install obp-python
RUN groupadd -r obp && useradd -rm -g obp obp
RUN git clone https://github.com/chrisjsimpson/obp-boostrap-user.git
WORKDIR obp-boostrap-user
RUN pip3 install -r requirements.txt
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.21.0/geckodriver-v0.21.0-linux64.tar.gz
RUN tar xvf ./geckodriver-v0.21.0-linux64.tar.gz
RUN chown -R obp:obp /obp-boostrap-user
# Switch to obp user
USER 999 
ENTRYPOINT ["top", "-b"]
