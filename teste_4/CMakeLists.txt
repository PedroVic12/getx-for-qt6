cmake_minimum_required(VERSION 3.16)
project(cpp_qml_app VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Qml Quick)

add_executable(cpp_qml_app
    src/main.cpp
    src/SampleController.h
    src/SampleController.cpp
)

target_link_libraries(cpp_qml_app PRIVATE
    Qt6::Core
    Qt6::Gui
    Qt6::Qml
    Qt6::Quick
)

file(COPY views/main.qml DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/views)
