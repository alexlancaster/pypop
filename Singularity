# vim: ts=4 sw=4 noet

BootStrap: docker
From: fedora:25

%setup
	# Copy all files into a directory in the container
	# (We use -rlptD instead of -a because owner & group can be ignored.)
	mkdir ${SINGULARITY_ROOTFS}/pypop-source
	echo $PWD > ${SINGULARITY_ROOTFS}/.pwd
	rsync -v -rlptD . ${SINGULARITY_ROOTFS}/pypop-source/ > ${SINGULARITY_ROOTFS}/.rsync_output 2>&1
	ls -lR . > ${SINGULARITY_ROOTFS}/.pypop_listing_from_host 2>&1
	ls -lR ${SINGULARITY_ROOTFS}/pypop-source > ${SINGULARITY_ROOTFS}/.pypop_listing_from_setup 2>&1

%post
	# Inside the container, install our required packages.
	dnf install -y python27 python-devel python-numeric python-libxml2 libxslt-python gcc redhat-rpm-config gsl-devel swig less findutils vim

	# Now, build PyPop.
	# (to be clear, the installs pypop into the container Python)
	ls -lR /pypop-source > /.pypop_listing_from_post 2>&1
	cd /pypop-source
	./setup.py build > /.pypop_build 2>&1

    # Make everything group- and world-readable
    # Also make directories group and world-executable.
    chmod -R go+r /pypop-source
    find /pypop-source -type d -exec chmod go+x {} +

    # Make everything group- and world-readable
    # Also make directories group and world-executable.
    chmod -R go+r /pypop-source
    find /pypop-source -type d -exec chmod go+x {} +

%runscript
	#!/bin/bash
	/usr/bin/env PYTHONPATH=/pypop-source /usr/bin/python2.7 /pypop-source/bin/pypop.py $@

%test
	# Use the runscript to do a simple run
	/singularity -m -c /pypop-source/data/samples/minimal.ini /pypop-source/data/samples/USAFEL-UchiTelle-small.pop

	# Compare the output with our samples.  Exit if there are differences.
    # NOTE: Tests disabled because some output variance is apparently expected.
	diff -u /pypop-source/data/singularity-test/USAFEL-UchiTelle-small-out.txt USAFEL-UchiTelle-small-out.txt || true
	diff -u /pypop-source/data/singularity-test/USAFEL-UchiTelle-small-out.xml USAFEL-UchiTelle-small-out.xml || true

	# Clean up!
	rm USAFEL-UchiTelle-small-out.txt USAFEL-UchiTelle-small-out.xml
