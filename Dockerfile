FROM ros:melodic

# install ros packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-melodic-desktop-full=1.4.1-0* \
    && rm -rf /var/lib/apt/lists/*

# install my own packages
RUN apt-get update && apt-get install -y \
    ros-melodic-teleop-twist-keyboard \
    ros-melodic-teleop-twist-joy

