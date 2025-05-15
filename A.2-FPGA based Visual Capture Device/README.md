# Aliensense NetCam Demo

### Prepare for MacOS:

```
brew install cmake jpeg-turbo wolfssl wxwidgets
```

### Prepare for Linux:

```
sudo apt install cmake libwxgtk3.2-dev libturbojpeg0-dev libwolfssl-dev
```

### Build:

```
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make SecubloxViewerDemo
```

### Run:

```
./SecubloxViewerDemo/SecubloxViewerDemo
```

### That's it!