import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
from astropy import log

from plotutils import *

def sci_plots(etable, gtitable, args):
    #GRID SET UP
    figure2 = plt.figure(figsize = (11, 8.5), facecolor = 'white')
    sci_grid = gridspec.GridSpec(5,7)

    # Build PHA Fast/Slow ratio plot before filtering by ratio
    # Only do this if powerspectrum not requested
    
    if not args.powspec:
        log.info('Building fast/slow subplot')
        plt.subplot(sci_grid[1:3,2:5])
        plot_slowfast(etable,args)

    # Now, filter out the points above the ratio cut, if requested
    if args.filtratio > 0:
        log.info('Applying ratio filter at {0}'.format(args.filtratio))
        etable = filt_ratio(etable, ratiocut = args.filtratio)

    #Light Curve
    log.info('Building light curve')
    plt.subplot(sci_grid[3:5,:7])
    meanrate, lc, a = plot_light_curve(etable, args.lclog, gtitable, binsize=args.lcbinsize)
    del a
    plot.title('Light Curve')
    plot.xlabel('Time Elapsed (s)')

    #Energy Spectrum
    log.info('Building energy spectrum')
    plt.subplot(sci_grid[1:3,:2])
    plot_energy_spec(etable)

    #Power Spectrum
    if args.powspec:
        log.info('Looking at power spectrum')
        plt.subplot(sci_grid[1:3,2:5])
        # plot_fft_of_power(etable, args.nyquist, args.pslog, args.writeps)

    # PULSE PROFILE
    log.info('Building pulse profile')
    axprofile = plt.subplot(sci_grid[1:3,5:7])
    if (args.orb is not None) and (args.par is not None):
        log.info('Calling pulse profile using PINT')
        pulse_profile(axprofile, etable, args)
    elif args.foldfreq > 0.0:
        log.info('Calling pulse profile with fixed frequency')
        pulse_profile_fixed(etable, args.foldfreq)
    else:
        pass

    #Making the plot all nice and stuff
    plt.subplots_adjust(left = .07, right = .99, bottom = .05, top = .9, wspace = .8, hspace = .8)

    figure2.suptitle('ObsID {0}: {1} on {2}'.format(etable.meta['OBS_ID'],
            etable.meta['OBJECT'],etable.meta['DATE-OBS'].replace('T',' at ')),
            fontsize=14)

    #tstart, tstop, exposure
    exposure = float(etable.meta['EXPOSURE'])
    tstart = etable.meta['DATE-OBS'].replace('T',' at ')
    tend = etable.meta['DATE-END'].replace('T', ' at ')
    fraction = exposure/(float(etable.meta['TSTOP'])-float(etable.meta['TSTART']))

    # Add text info here:
    plt.figtext(.07, .93, 'Start time is {0}, End time is {1}'.format(tstart,tend), fontsize = 10)
    plt.figtext(.07, .90, 'Exposure is {0:.1f} s, Good time fraction is {1:.3f}'.format(exposure, fraction),
        fontsize = 10)
    plt.figtext(.07, .87, 'Mean count rate {0:.3f} c/s'.format(meanrate), fontsize = 10)
   # plt.figtext(.07, .84, etable.meta['FILT_STR'], fontsize=10)
    if args.mask:
        plt.figtext(.07, .81, 'IDS {0} are masked'.format(args.mask), fontsize=10)
    plt.figtext(.5, .77, str(gtitable['START'][:]), fontsize =9)
    plt.figtext(.58, .77, str(gtitable['STOP'][:]), fontsize =9)
    plt.figtext(.66, .77, str(gtitable['DURATION'][:]), fontsize =9)

    return figure2
