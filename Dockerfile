FROM ubuntu:focal

ARG DEBIAN_FRONTEND=noninteractive

USER root

SHELL [ "/bin/bash", "-c" ]

RUN apt clean && \
    rm -rf /var/lib/apt/lists/* && \
    apt update && \
    apt upgrade -y

RUN apt install -y wget git ranger neofetch vim htop apt-utils \
    software-properties-common python3 python3-pip libopengl0 unzip ffmpeg \
    libsm6 libxext6 libgl1-mesa-glx libnss3 xvfb libxcomposite1 libxdamage1 \
    libxtst6 build-essential libgl1-mesa-dev libqt5webenginewidgets5 \
    libboost-all-dev python3.8-dev libpng-dev libjpeg-dev libtiff-dev \
    libglew-dev zlib1g-dev libqt5charts5 libxcb-cursor0

RUN pip install numpy scipy

RUN apt install sudo && groupadd noroot && \
    useradd -s /bin/bash -m -g noroot noroot && \
    usermod -aG sudo noroot && \
    echo "noroot ALL=(ALL) NOPASSWD ALL" >> /etc/sudoers

RUN wget "https://github.com/sofa-framework/sofa/releases/download/v22.12.00/SOFA_v22.12.00_Linux.zip" \
    -P /home/noroot/ && \
    cd /home/noroot && \
    unzip /home/noroot/SOFA_v22.12.00_Linux.zip && \
    echo "SofaPython3 NO_VERSION" >> \
    /home/noroot/SOFA_v22.12.00_Linux/lib/plugin_list.conf

USER noroot

WORKDIR /home/noroot/
