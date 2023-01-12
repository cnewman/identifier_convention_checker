file(GLOB DISPATCHER_SOURCE dispatcher/*.cpp)
file(GLOB DISPATCHER_HEADER dispatcher/*.hpp)

file(GLOB SOURCE *.cpp)
file(GLOB HEADER *.hpp)

add_executable(checkidentifiers ${DISPATCHER_SOURCE} ${DISPATCHER_HEADER} ${HEADER} ${SOURCE})
target_link_libraries(checkidentifiers srcsaxeventdispatch srcsax_static ${LIBXML2_LIBRARIES})
install(TARGETS checkidentifiers DESTINATION bin)
