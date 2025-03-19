FROM jritsema/opencv-tensorflow-lite-arm32v7

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    zlib1g-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    tcl-dev \
    tk-dev \
    python3-tk && \
    rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

# Clone the repository and install Python requirements
RUN git clone https://github.com/LeviTranstrum/gesture.git && \
    cd gesture && \
    pip install --no-cache-dir -r requirements.txt

# Correct the CMD syntax
CMD ["bash"]
