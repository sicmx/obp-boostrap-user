FROM debian:stretch
RUN apt update
RUN apt install -y firefox-esr
RUN apt install -y python3 python3-pip git wget

# Get obp-python obp cli utilities (getauth, etc)
RUN pip3 install obp-python
WORKDIR /opt/obp-boostrap-user
COPY bootstrap/* ./
RUN pip3 install -r requirements.txt
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.21.0/geckodriver-v0.21.0-linux64.tar.gz
RUN tar xvf ./geckodriver-v0.21.0-linux64.tar.gz

# grant user execute permissions,
# change group to root group,
# copy user permissions to group
RUN chmod -R u+x /opt/obp-boostrap-user && \
    chgrp -R 0 /opt/obp-boostrap-user && \
    chmod -R g=u /opt/obp-boostrap-user /etc/passwd

# Add obpuser
RUN groupadd -r obpuser && useradd -r -g obpuser obpuser

# Change owner of /opt/obp-boostrap-user to obpuser (see ./uid_entrypoint)
RUN chown -R obpuser /opt/obp-boostrap-user/*

USER 10001
COPY uid_entrypoint ./
COPY run ./

ENV OBP_API_HOST=http://127.0.0.1:8080
ENV OBP_USERNAME=demo
ENV OBP_EMAIL=demo@example.com
ENV OBP_PASSWORD=Treedom#112
ENV OBP_FIRSTNAME=Fred
ENV OBP_LASTNAME=Smith
ENV MOZ_HEADLESS=1

ENTRYPOINT [ "/opt/obp-boostrap-user/uid_entrypoint" ] # patch /etc/passwd to contain obp user
CMD /opt/obp-boostrap-user/run
