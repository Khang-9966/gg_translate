docker run --name gg_trans_1 -p 0.0.0.0:1234:80 -p 0.0.0.0:1235:5900 -p 0.0.0.0:1236:8889 -e VNC_PASSWORD=123456 -e RESOLUTION=1280x720 --shm-size 16g  gg_translate_api & \
docker run --name gg_trans_3 -p 0.0.0.0:1334:80 -p 0.0.0.0:1335:5900 -p 0.0.0.0:1336:8889 -e VNC_PASSWORD=123456 -e RESOLUTION=1280x720 --shm-size 16g  gg_translate_api & \
docker run --name gg_trans_4 -p 0.0.0.0:1434:80 -p 0.0.0.0:1435:5900 -p 0.0.0.0:1436:8889 -e VNC_PASSWORD=123456 -e RESOLUTION=1280x720 --shm-size 16g  gg_translate_api & \
docker run --name gg_trans_5 -p 0.0.0.0:1534:80 -p 0.0.0.0:1535:5900 -p 0.0.0.0:1536:8889 -e VNC_PASSWORD=123456 -e RESOLUTION=1280x720 --shm-size 16g  gg_translate_api
