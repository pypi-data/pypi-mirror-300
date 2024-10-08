.. _instruments:

Producing Realistic Observations Using External Packages
========================================================

If you want to produce a realistic simulation of a particular instrumental
configuration, pyXSIM provides options for exporting its event lists to
external packages. The supported software packages are:

* `MARX <https://space.mit.edu/ASC/MARX/>`_
* `SIMX <https://hea-www.cfa.harvard.edu/simx/>`_
* `SIXTE <https://https://www.sternwarte.uni-erlangen.de/research/sixte/>`_
* `SOXS <https://hea-www.cfa.harvard.edu/soxs>`_

MARX
----

The MARX version needs to be at least 5.3.1. To use SIMPUT with MARX, one only
needs to change the following lines in the ``marx.par`` file:

.. code-block:: bash

    # Change the source RA, Dec to match the center of the observation
    SourceRA,r,a,45.0,0,360,"Source RA (degrees)"
    SourceDEC,r,a,30.0,-90,90,"source DEC (degrees)"

    # The source type should be "SIMPUT"
    SourceType,s,a,"SIMPUT","POINT|GAUSS|IMAGE|LINE|BETA|RAYFILE|DISK|USER|SAOSAC|SIMPUT",,"source"

    # Pointers to your SIMPUT file and the location of the SIMPUT library
    S-SIMPUT-Source,f,a,"sloshing_events_simput.fits",,,"Filename of SIMPUT Catalog"
    S-SIMPUT-Library,f,a,"/usr/local/simput-2.1.2/lib/libsimput.dylib",,,"Path to dynamically linked file libsimput.so"

    # Pointing RA and Dec is up to you, but should be near the source
    RA_Nom,r,a,45.,,,"RA_NOM for dither (degrees)"
    Dec_Nom,r,a,30.,,,"DEC_NOM for dither (degrees)"
    Roll_Nom,r,a,0.,,,"ROLL_NOM for dither (degrees)"

SIMX
----

Here is an example set of SIMX commands that uses a SIMPUT catalog made with
pyXSIM:

.. code-block:: bash

    #!/bin/bash
    heainit
    simxinit

    punlearn simx
    pset simx mode=hl
    pset simx Exposure=1.0e4
    pset simx UseSimput=yes
    pset simx MissionName=XraySurveyor InstrumentName=HDXI
    pset simx ScaleBkgnd=0.0
    pset simx RandomSeed=24

    pset simx SimputFile=spiral_242959_noshift_xrs_simput.fits
    pset simx PointingRA=30.0 PointingDec=45.0
    pset simx OutputFileName=spiral_242959_noshift_xrs
    simx

SIXTE
-----

Here is an example set of SIXTE commands that uses a SIMPUT catalog made with
pyXSIM:

.. code-block:: bash

    #!/bin/bash

    export HEADASNOQUERY=
    export HEADASPROMPT=/dev/null

    . $HEADAS/headas-init.sh

    base=sloshing_simput
    xmldir=$SIXTE/share/sixte/instruments/athena-wfi/wfi_wo_filter_15row
    xml0=${xmldir}/ld_wfi_ff_chip0.xml
    xml1=${xmldir}/ld_wfi_ff_chip1.xml
    xml2=${xmldir}/ld_wfi_ff_chip2.xml
    xml3=${xmldir}/ld_wfi_ff_chip3.xml

    $SIXTE/bin/athenawfisim \
        XMLFile0=${xml0} XMLFile1=${xml1} XMLFile2=${xml2} XMLFile3=${xml3} \
        RA=30.05 Dec=45.04 \
        Prefix=sim_ \
        Simput=${base}.fits \
        EvtFile=evt.fits \
        Exposure=6000.0 \
        clobber=yes

    ftmerge \
        sim_chip0_evt.fits,sim_chip1_evt.fits,sim_chip2_evt.fits,sim_chip3_evt.fits \
        sim_combined_evt.fits clobber=yes

    $SIXTE/bin/imgev \
        EvtFile=sim_combined_evt.fits \
        Image=img_sloshing.fits \
        CoordinateSystem=0 Projection=TAN \
        NAXIS1=1078 NAXIS2=1078 CUNIT1=deg CUNIT2=deg \
        CRVAL1=30.05 CRVAL2=45.04 CRPIX1=593.192308 CRPIX2=485.807692 \
        CDELT1=-6.207043e-04 CDELT2=6.207043e-04 history=true \
        clobber=yes

.. _instr-soxs:

SOXS
----

As of pyXSIM 4.3.0 and SOXS 4.6.0, the SOXS :func:`~soxs.instrument.instrument_simulator`
can accept pyXSIM event list files in the HDF5 format as input, bypassing the need
for a SIMPUT catalog, although you can still use one if you wish.

Here is an example set of SOXS commands which uses an event list created by pyXSIM,
using either the HDF5 event file or the SIMPUT catalog:

.. code-block:: python

    import soxs
    input_file = "snr_events.h5" # pyXSIM event list file to be read
    #input_file = "snr_simput.fits" # SIMPUT file to be read
    out_file = "evt_mucal.fits" # event file to be written
    exp_time = 30000. # The exposure time in seconds
    instrument = "lem_2.3eV" # short name for instrument to be used
    sky_center = [30., 45.] # RA, Dec of pointing in degrees
    soxs.instrument_simulator(input_file, out_file, exp_time, instrument,
                              sky_center, overwrite=True)

Refer to the relevant documentation for all of those packages for more details,
as well as the :ref:`simput` section of the :class:`~pyxsim.event_list.EventList`
documentation.
