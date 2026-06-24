cmake_minimum_required(VERSION 3.16)
project(cpp_widgets_app VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOUIC_SEARCH_PATHS ${CMAKE_CURRENT_SOURCE_DIR}/views)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets)

add_executable(cpp_widgets_app
    src/main.cpp
    src/mainwindow.h
    src/mainwindow.cpp
    views/mainwindow.ui
)

target_link_libraries(cpp_widgets_app PRIVATE
    Qt6::Core
    Qt6::Gui
    Qt6::Widgets
)
