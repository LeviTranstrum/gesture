# Builds an image based on the factory Yokogawa ubuntu image, with TFLite installed according to
# https://dev.to/yokogawa-yts_india/running-a-basic-tensorflow-lite-model-on-e-rt3-plus-dgh

FROM yokogawa-ubuntu-image

# Prepare to install CMake
RUN sudo apt update && \
    sudo apt upgrade -y && \
    sudo apt install -y libssl-dev wget build-essential && \
    cd /home/ert3 && \
    wget --no-check-certificate https://github.com/Kitware/CMake/releases/download/v3.17.1/cmake-3.17.1.tar.gz && \
    tar zxvf cmake-3.17.1.tar.gz

# Install CMake
RUN cd /home/ert3/cmake-3.17.1 && \
    mkdir -p /home/ert3/cmake-3.17.1/Testing/JacocoCoverage/Coverage/target/site && \
    touch /home/ert3/cmake-3.17.1/Testing/JacocoCoverage/Coverage/target/site/jacoco.xml.in && \
    ./bootstrap --prefix=/usr/local -- -DCMAKE_USE_OPENSSL=OFF && \
    make && \
    sudo make install

# Install pybind11
RUN sudo pip3 install pybind11

# Clone tflite
RUN cd /home/ert3 && \
    git clone --branch v2.6.0 --depth 1 https://github.com/tensorflow/tensorflow.git tensorflow_src

# Build tflite wheel
RUN cd /home/ert3/tensorflow_src/tensorflow/lite/tools/pip_package && \
    sed -i '1 a BUILD_NUM_JOBS=1' build_pip_package_with_cmake.sh && \
    sed -i '/-DCMAKE_CXX_FLAGS="${BUILD_FLAGS}" \\/a\      -DTFLITE_ENABLE_XNNPACK=OFF \\' build_pip_package_with_cmake.sh && \
    cd /home/ert3/tensorflow_src && \
    export CMAKE_ROOT=/usr/local/share/cmake-3.17 && \
    PYTHON=python3 tensorflow/lite/tools/pip_package/build_pip_package_with_cmake.sh native

# Install tflite wheel
RUN cd /home/ert3 && \
    sudo apt update && \
    sudo apt install python3-venv libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk libharfbuzz-dev libfribidi-dev libxcb1-dev && \
    python3 -m venv tf-env --system-site-packages && \
    source tf-env/bin/activate && \
    pip install wheel cython numpy tensorflow_src/tensorflow/lite/tools/pip_package/gen/tflite_pip/python3/dist/*.whl --no-cache-dir

RUN cd /home/ert3 && \
    source tf-env/bin/activate && \ 
    git clone https://github.com/LeviTranstrum/gesture.git

CMD ["bash"]
