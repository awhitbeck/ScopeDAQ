from utils import *
from scipy.optimize import curve_fit

channel_list=[4]

if __name__ == "__main__":
    #run_name=sys.argv[1]
    run_name=r'C:\Users\awhitbec\OneDrive - Texas Tech University\CSV Files\5-11\timtestbar1-5-11'
    #run_name=r'D:\andrewMay4'
    dir_name=run_name.split('\\')[-1]

    df = load_data(run_name)

    #########################
    ## average pulse shape
    #########################

    range_low=2000
    for i in channel_list:
        ch_filter=(df['channel']==i)
        ts=df[ch_filter]['time'].values[0]*1e9
        #print(ts)
        vs=np.sum(df[ch_filter]['voltage'].values)
        vs = list(map(lambda x:  0. if np.isnan(x) or np.isinf(x) else x,vs))
        plt.plot(ts[range_low:],vs[range_low:])

    pInit = [5.,1000.,5.,0.1,10.]
    coeff1, var_matrix1 = curve_fit(pulse, ts[range_low:], vs[range_low:], p0=pInit)
    print("fitted coefficients:",coeff1)
    pred = pulse(ts[range_low:], *coeff1)
    plt.plot(ts[range_low:], pred, linewidth=1.5)

    plt.legend(['Channel 4'])
    plt.xlabel('Time [ns]')
    plt.ylabel('Amplitude (A.U.)')
    print('saving:',dir_name+'_average_pulses.png')
    plt.savefig(dir_name+'_average_pulses.png')
    plt.clf()
    plt.cla()

    #########################
    ## get charge for channels 1
    #########################
    events = np.unique(df['event_number'])
    charge_pairs=[]
    for event in events : 
        event_filter = df['event_number']==event
        ch4_filter=df['channel']==4

    #########################
    ### plot integrated charges
    #########################
    low_bin=20
    high_bin=200
    bin_width=10
    ch4_bins=plt.hist((df['charge']-df['baseline']*73./27.)/28.6,bins=np.arange(low_bin,high_bin,bin_width),histtype='step')
    #    ch4_bins = plt.hist(df['charge']*1.25e-3/0.0286,
    #                    bins=np.arange(low_bin, high_bin, bin_width), histtype='step')
    plt.legend(['Channel 4'])
    plt.xlabel('Charge [PEs]')
    plt.ylabel('Events')
    #plt.yscale('log')
    plt.savefig(dir_name+'_response.png')
    #plt.show()
    plt.clf()
    plt.cla()

    print('channel 4 mean',np.mean(df['charge']))
    print('channel 4 MPV',ch4_bins[1][np.argmax(ch4_bins[0])]+bin_width/2.)
    
