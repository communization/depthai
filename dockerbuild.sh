#https://github.com/luxonis/depthai-ros
docker build -t depthai .

sudo docker run -it --network host --gpus all --ipc=host --privileged \
    -e DISPLAY=$DISPLAY -v $(pwd):/depthai -v /dev/:/dev/ -v /tmp/.X11-unix:/tmp/.X11-unix \
    --name depthai depthai

