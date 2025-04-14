# Note: Need to have roughly current date and time set with
# `sudo date -s YYYY-MM-DD HH:MM:SS`
# or else you will run into issue with certificates

# set up ntpdate to keep the date current
sudo apt update
sudo apt install ntpdate
sudo ntpdate pool.ntp.org

# Install dependencies
# Pillow dependencies
sudo apt update
sudo apt install -y libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjpeg-dev libtiff-dev libwebp-dev tcl-dev tk-dev python3-dev python3-pip

# LiteRT (formerly TFLite ) wheel
curl -k -OL https://github.com/LeviTranstrum/yokogawa-ert3/raw/master/tflite_runtime-2.6.0-cp39-cp39-linux_armv7l.whl
pip install tflite_runtime-2.6.0-cp39-cp39-linux_armv7l.whl

# Other pip packages
pip install -r gesture/requirements.txt
