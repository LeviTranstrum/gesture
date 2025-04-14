# Gesture Recognition on Yokogawa e-RT3
This is a machine vision demo showcasing the functionality of the Yokogawa e-RT3 as an industrial AI platform.

## Overview
In this demo, the e-RT3 acquires an image from a camera on the network via an HTTP GET request. The image is fed to a LiteRT (formerly TensorFlow Lite) model which detects the presence and location of hand keypoints. The number of fingertips which are far from the palm are counted. The digital output corresponding to the number of fingers held up (1-5) is then activated. 

## Usage
Hardware required:
- Yokogawa e-RT3 with RP70 CPU, digital input module, and digital output module
- PC with webcam, or other network camera
- Yokogawa input module switch unit, or other 24VDC signal to e-RT3 input module

### Setting up the e-RT3
#### Load the OS
1. Download the `debian_20240209` image from the [Yokogawa Customer Portal](https://myportal.yokogawa.com/).
2. Flash the image onto a 16 or 32 GB SD card using [Rawrite32, the NetBSD image writing tool](https://www.netbsd.org/~martin/rawrite32/index.html).
3. With the e-RT3 power off, and the mode switch in position 0, insert the SD card into the SD1 slot and turn the power on. The OS light should turn on within a few minutes.

#### Access the e-RT3 over SSH
1. Set your PC's IP address to `192.168.3.99`, or any other address on the `192.168.3.xxx` network. Using `192.168.3.99` will let you skip a configuration step later. The e-RT3's default IP address is 192.168.3.72.
2. Connect your PC to the e-RT3 using an ethernet cable.
3. Open a terminal window and SSH into the e-RT3 as `ert3`:
    ```bash
    ssh ert3@192.168.3.72
    ```
4. When prompted for the password, type `user_ert3`.

#### Download the Code and Install Dependencies
1. Connect the second ethernet port on the e-RT3 to a network with internet access.
2. Update the date and time on the e-RT3:
    ```bash
    sudo apt update
    sudo apt install ntpdate
    sudo ntpdate pool.ntp.org
    ```
    If the above doesn't work, your system clock may be too far off the current time. Set the date and time manually, then re-run the previous commands to keep the time current:

    ```bash
    # Replace YYYY-MM-DD with current year, month, and day, and HH:MM:SS with current hour, minute, and second
    sudo date -s "YYYY-MM-DD HH:MM:SS"
    ```
3. Clone this repository:
    ```bash
    git clone https://github.com/LeviTranstrum/gesture
    ```
4. Run the setup script to install dependencies and skip the next steps:
    ```bash
    gesture/setup.sh
    ```
    Or, if you're the paranoid type, continue with the following steps manually:
5. [Build a LiteRT wheel from source](https://dev.to/yokogawa-yts_india/running-a-basic-tensorflow-lite-model-on-e-rt3-plus-dgh), or download [my pre-built wheel](https://github.com/LeviTranstrum/yokogawa-ert3):
    ```bash
    curl -k -OL https://github.com/LeviTranstrum/yokogawa-ert3/raw/master/tflite_runtime-2.6.0-cp39-cp39-linux_armv7l.whl

    ```
6. Install the LiteRT wheel:
    ```bash
    pip install tflite_runtime-2.6.0-cp39-cp39-linux_armv7l.whl
    ```
7. Install other dependencies:
    ```bash
    # System requirements to build Pillow
    sudo apt install -y libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjpeg-dev libtiff-dev libwebp-dev tcl-dev tk-dev python3-dev python3-pip
    pip install -r gesture/requirements.txt
    ```
8. (Optional) Schedule the script to start automatically on bootup:
    ```bash
    sudo cat <<EOF > /etc/systemd/system/gesture.service
    [Unit]
    Description=Yokogawa Machine Vision Demo
    After=network.target

    [Service]
    Type=simple
    User=ert3
    ExecStart=/usr/bin/python3 /home/ert3/gesture/main.py
    Restart=always

    [Install]
    WantedBy=multi-user.target
    EOF

    sudo systemctl daemon-reload
    sudo systemctl enable gesture.service
    ```

#### Start the Program
Now that all dependencies have been installed, we can run the python script.
1. If you set your PC's IP address to something other than `192.168.3.99`, update the `config.yaml` file to match:
    ```
    sudo vim /home/ert3/gesture/config.yaml
    ```
2. Run the python script:
    ```bash
    python /home/ert3/gesture/main.py
    ```

#### Setting up the image server
Now that the e-RT3 is up and running, it will need a server to feed it images. To set this up on your PC:
1. Download and install [Python](https://www.python.org/downloads/windows/) and [git](https://git-scm.com/downloads/win).
2. Clone this repository:
    ```powershell
    git clone https://github.com/LeviTranstrum/gesture
    ```
3. Install requirements:
    ```powershell
    pip install -r ./gesture/image_service/
    image_server_requirements.txt
    ```
4. Start the image server:
    ```powershell
    python3 -m image_service.image_server
    ```

#### Detecting Gestures
Hold your hand up in front of the webcam, about 18-24 inches away. Activate digital input 1 on the e-RT3 input module to capture an image. The image will be processed by the LiteRT model, and the digital output corresponding to the number of fingers detected will be activated on the digital output module. 

For example, if you hold up 4 fingers, digital output 4 will be activated, and the number 4 will be lit up on the digital output card display. If there is an error receiving the image, or no hand is confidently detected in the image, the alarm (`ALM`) light will turn on.

If `visualize_data` is set to `True` in the `config.yaml`, detection data will be sent back to the image server to be displayed. You can use this to see where each fingertip was detected, as well as the confidence score. Having a white background and bright lighting seems to produce the best results. If fingertips are being accurately detected, but not counted, you may need to adjust the finger length setting in the `config.yaml`. Each fingertip must be detected at least this far from the center of the palm in order to be counted.