FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
# NOTE: python3-tk is used for matplotlib
RUN apt-get update && apt-get install -y \
    sudo wget curl vim \
    python3 python3-pip python3-venv python3-dev python3-tk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#RUN apt-get update && apt-get install -y libgl1-mesa-glx libegl1-mesa libxkbcommon-x11-dev \
#        libdbus-1-dev

# Arguments for user and group creation
ARG HOST_UID
ARG HOST_GID
ARG GIT_ARCH
ARG USERNAME=dockeruser

# Create or modify user and group with matching UID and GID
RUN if ! getent group ${HOST_GID} >/dev/null; then groupadd -g ${HOST_GID} ${USERNAME}; fi && \
    if ! id -u ${HOST_UID} >/dev/null 2>&1; then \
        useradd -m -u ${HOST_UID} -g ${HOST_GID} -s /bin/bash ${USERNAME}; \
    else \
        existing_user=$(getent passwd ${HOST_UID} | cut -d: -f1); \
        if [ "$existing_user" != "$USERNAME" ]; then \
            usermod -l ${USERNAME} -d /home/${USERNAME} -m $existing_user; \
            groupmod -n ${USERNAME} $(getent group ${HOST_GID} | cut -d: -f1); \
        fi; \
    fi && \
    usermod -aG sudo ${USERNAME} && \
    echo "${USERNAME}:ubuntu" | chpasswd && \
    echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} && \
    chmod 0440 /etc/sudoers.d/${USERNAME}

ARG PYPROJECT=pyml-regression-example1
ARG PROJECTDIR=/home/$USERNAME/$PYPROJECT
WORKDIR $PROJECTDIR

ADD ${GIT_ARCH} $PROJECTDIR
RUN chown -R $USERNAME:$USERNAME /home/$USERNAME

USER $USERNAME

# Install pipx and uv for the user
ENV PATH=/home/$USERNAME/.local/bin:$PATH
RUN python3 -m pip install --user pipx --break-system-packages && \
    /home/$USERNAME/.local/bin/pipx install uv

RUN cd $PROJECTDIR && uv venv && uv sync

# Command to run when starting the container
CMD [ "bash" ]
