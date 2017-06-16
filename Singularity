Bootstrap: docker
From: continuumio/miniconda3

%setup

    # Copy all files into a directory in the container
    # (Make sure to exclude our Singularity image file)
    mkdir ${SINGULARITY_ROOTFS}/pypop-source
    rsync -rlptD --exclude '*.img' --exclude '.git' . ${SINGULARITY_ROOTFS}/pypop-source


%post

    apt-get update && apt-get install -y swig gcc wget build-essential vim
    /opt/conda/bin/conda install -y numpy
 
    cd /
    wget ftp://ftp.gnu.org/gnu/gsl/gsl-2.3.tar.gz
    tar -xzvf gsl-2.3.tar.gz
    cd gsl-2.3
    ./configure --prefix=/usr/local
    make
    make install

    # Install pypop with swig, etc.
    cd /pypop-source
    /opt/conda/bin/python setup.py install

%runscript

    exec /opt/conda/bin/python /pypop-source/pypop.py $@
