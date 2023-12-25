sudo docker run --name gg_trans_1 -p 0.0.0.0:3234:80 -p 0.0.0.0:3235:5900 -p 0.0.0.0:3236:8889 -e VNC_PASSWORD=123456 -e RESOLUTION=1280x720 --shm-size 16g  gg_translate_api

