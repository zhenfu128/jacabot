cmake_minimum_required(VERSION 3.0.2)
project(jacabot_simulation)


find_package(catkin REQUIRED COMPONENTS
rospy
urdf
xacro
)

catkin_package(
CATKIN_DEPENDS rospy urdf xacro 
)

include_directories(
${catkin_INCLUDE_DIRS}
)

install(DIRECTORY meshes urdf launch worlds
DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
