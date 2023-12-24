FROM dorowu/ubuntu-desktop-lxde-vnc:bionic
WORKDIR /
COPY . .
RUN bash install.sh
RUN chmod +x /entrypoint.sh
RUN chmod +x /start_flask.sh
ENTRYPOINT ["/entrypoint.sh"]
