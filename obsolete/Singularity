# vim: ts=4 sw=4 et

BootStrap: docker
From: ubuntu:17.04

%setup
    # Copy all files into a directory in the container
    # Make destination directories (code, and a place for logs)
    echo 'BOOTSTRAP[SETUP]: Creating directories'
    mkdir ${SINGULARITY_ROOTFS}/pypop-source
    mkdir ${SINGULARITY_ROOTFS}/.bootstrap_logs
    echo $PWD > ${SINGULARITY_ROOTFS}/.bootstrap_logs/setup_pwd

    # Use rsync to copy the files into the container
    # (We use -rlptD instead of -a because owner & group can be ignored.)
    echo 'BOOTSTRAP[SETUP]: Copying files'
    rsync -v -rlptD --exclude image . ${SINGULARITY_ROOTFS}/pypop-source/ 2>&1 | tee ${SINGULARITY_ROOTFS}/.bootstrap_logs/setup_rsync_output

    # Download swig
    curl -L -o ${SINGULARITY_ROOTFS}/swig-3.0.12.tar.gz http://prdownloads.sourceforge.net/swig/swig-3.0.12.tar.gz

    # Output some debug file listings
    echo 'BOOTSTRAP[SETUP]: Source listing (from host)'
    ls -lR . 2>&1 | tee ${SINGULARITY_ROOTFS}/.bootstrap_logs/setup_pypop_listing_from_host
    echo 'BOOTSTRAP[SETUP]: Source listing (from rootfs)'
    ls -lR ${SINGULARITY_ROOTFS}/pypop-source 2>&1 | tee ${SINGULARITY_ROOTFS}/.bootstrap_logs/setup_pypop_listing_in_rootfs

%post
    # Inside the container, install our required packages.
    apt update
    apt install --no-install-recommends -y build-essential libboost-dev libgsl2 libgsl-dev libpcre3 libpcre3-dev python2.7-dev python-numpy python-libxml2 python-libxslt1 python-pip python-pytest python-setuptools

    # Build and install SWIG 3.0.12
    tar -xzvf /swig-3.0.12.tar.gz
    cd /swig-3.0.12
    ./configure --without-alllang --with-python
    make
    make install

    # Now, build PyPop.
    # (to be clear, the installs pypop into the container Python)
    echo 'BOOTSTRAP[POST]: Source listing (inside container)'
    ls -lR /pypop-source 2>&1 | tee /.bootstrap_logs/pypop_listing_from_post
    echo 'BOOTSTRAP[POST]: Building PyPop'
    cd /pypop-source
    ./setup.py build 2>&1 | tee /.bootstrap_logs/pypop_build

    # Do some cleanup
    cd /
    rm -rf swig-3.0.12 swig-3.0.12.tar.gz
    apt purge -y build-essential libgsl-dev libpcre3-dev python2.7-dev
    apt autoremove -y
    apt clean

    # Make everything group- and world-readable
    # Also make directories group and world-executable.
    echo 'BOOTSTRAP[POST]: Fixing up permissions'
    chmod -R go+r /pypop-source
    find /pypop-source -type d -exec chmod go+x {} +

    # Make everything group- and world-readable
    # Also make directories group and world-executable.
    chmod -R go+r /pypop-source
    find /pypop-source -type d -exec chmod go+x {} +

%runscript
    #!/bin/bash
    if [ "$#" = '0' ]; then
        echo 'You did not choose a program to run!'
        echo 'Please re-run this command, but add the word...'
        echo '    "pypop"   (to run PyPop), or'
        echo '    "popmeta" (to run PopMeta).'
        echo 'Then add your normal command-line arguments.'
        echo 'Thanks!'
        exit 1
    fi
    case $1 in
    pypop)
        shift
        exec /usr/bin/env PYTHONPATH=/pypop-source /usr/bin/python2.7 /pypop-source/bin/pypop.py $@
        ;;
    popmeta)
        shift
        exec /usr/bin/env PYTHONPATH=/pypop-source /usr/bin/python2.7 /pypop-source/bin/popmeta.py $@
        ;;
    *)
        echo "I'm sorry, I did not recognize what program you wanted to run!"
        echo "Please place 'pypop' or 'popmeta' at the start of your argument list,"
        echo 'followed by the normal pypop or popmeta arguments.'
        echo 'Thanks!'
        exit 1
        ;;
    esac

%test
    # Use py.test
    cd /pypop-source
    /usr/bin/py.test -s -v
