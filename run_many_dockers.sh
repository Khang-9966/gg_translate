docker run --name gg_trans_1 -p 0.0.0.0:3234:80 -p 0.0.0.0:3235:5900 -p 0.0.0.0:3236:8889 -e VNC_PASSWORD=123456 -e RESOLUTION=1280x720 --shm-size 16g  gg_translate_api & \
docker run --name gg_trans_3 -p 0.0.0.0:3334:80 -p 0.0.0.0:3335:5900 -p 0.0.0.0:3336:8889 -e VNC_PASSWORD=123456 -e RESOLUTION=1280x720 --shm-size 16g  gg_translate_api & \
docker run --name gg_trans_4 -p 0.0.0.0:3434:80 -p 0.0.0.0:3435:5900 -p 0.0.0.0:3436:8889 -e VNC_PASSWORD=123456 -e RESOLUTION=1280x720 --shm-size 16g  gg_translate_api & \
docker run --name gg_trans_5 -p 0.0.0.0:3534:80 -p 0.0.0.0:3535:5900 -p 0.0.0.0:3536:8889 -e VNC_PASSWORD=123456 -e RESOLUTION=1280x720 --shm-size 16g  gg_translate_api
