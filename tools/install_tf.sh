

sudo pip install setuptools==41.0.0



sudo pip3 install https://github.com/lhelontra/tensorflow-on-arm/releases/download/v1.14.0-buster/tensorflow-1.14.0-cp37-none-linux_armv7l.whl



sudo apt-get install libatlas-base-dev



sudo pip3 install pillow lxml jupyter matplotlib cython



sudo apt-get install python-tk



sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev



sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev



sudo apt-get install libxvidcore-dev libx264-dev



sudo apt-get install qt4-dev-tools



sudo pip3 install opencv-python



sudo apt-get install autoconf automake libtool curl



mkdir protobuff

cd protobuff



wget https://github.com/protocolbuffers/protobuf/releases/download/v3.9.2/protobuf-all-3.9.2.tar.gz



tar -zxvf protobuf-all-3.9.2.tar.gz



gunzip protobuf-all-3.9.2.tar.gz



cd protobuf-3.9.2



./configure



make



make check 



sudo make install



cd python



export LD_LIBRARY_PATH=../src/.libs



sudo python3 setup.py build --cpp_implementation 



sudo python3 setup.py test --cpp_implementation



sudo python3 setup.py install --cpp_implementation



export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp



export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION_VERSION=3



sudo ldconfig



protoc
