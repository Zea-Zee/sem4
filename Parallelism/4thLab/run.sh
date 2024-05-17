CAMERA=$(ls /dev/video* | head -n 1)

if [ -z "$CAMERA" ]; then
    echo "No camera found"
    exit 1
fi

RESOLUTION="1280x720"
DISPLAY_FREQUENCY=30

python3 main.py --cam_name $CAMERA --resolution $RESOLUTION --display_frequency $DISPLAY_FREQUENCY
