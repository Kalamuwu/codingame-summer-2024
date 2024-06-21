CC             = /usr/bin/g++
BUILD_DIR     ?= build

EXECUTABLE     = cg-summer-2024
#LIBRARIES      = -lSDL2 -lSDL2_image
LIBRARIES      =
INCLUDES       = -Iinclude

# select one of these for Debug vs. Release
CC_DBG         = -g -DINPUT_TUNABLES=true
#CC_DBG         =

CCFLAGS        = $(CC_DBG) $(INCLUDES) -std=c++11 -m64 -O2 -march=native -ffast-math -Wall -Wextra -Wpedantic
LDFLAGS        = $(CC_DBG) $(LIBRARIES)

#SOURCES = test.cpp
SOURCES = Answer.cpp actors/hurdles.cpp actors/archery.cpp actors/skating.cpp actors/diving.cpp
OBJECTS_C = $(SOURCES:.c=.o)
OBJECTS_C_CPP = $(OBJECTS_C:.cpp=.o)
OBJECTS = $(addprefix ${BUILD_DIR}/,$(OBJECTS_C_CPP))

.PHONY: all
.DEFAULT: all

all: $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(LDFLAGS) -o $(BUILD_DIR)/$(EXECUTABLE) $(OBJECTS)

$(BUILD_DIR)/%.o: %.c
	$(CC) $(CCFLAGS) -c $< -o $@
$(BUILD_DIR)/%.o: %.cpp
	$(CC) $(CCFLAGS) -c $< -o $@

clean:
	rm -rf $(BUILD_DIR)/*
	mkdir -p $(BUILD_DIR)/actors
