#!/usr/bin/env bash -e

function download {
    filename=${1}
    url=https://esslab.jp/~kotaro/files/web_layout/${filename}
    wget ${url} -O data/${filename} -q || wget ${url} -O data/${filename}
}

download trainval.hdf5
download test.hdf5

echo "Successfully downloaded the WebForest dataset"