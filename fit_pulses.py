from scipy.optimize import curve_fit
from utils import *

channel_list=[4]

if __name__ == "__main__":
    #run_name=sys.argv[1]
    run_name=r'C:\Users\awhitbec\OneDrive - Texas Tech University\CSV Files\5-11\timtestbar1'
    dir_name=run_name.split('\\')[-1]

    df = load_data(run_name)

    fall_times=[]
    peak_times=[]
    Qs=[]
    ped=[]
    offsets=[]
    for i in range(200):
        event_i=i
        if i%100 == 0 :
            print('i:',i)
        range_low=2700
        range_high=10000

        vs=df['voltage'].values[event_i]
        ts=df['time'].values[event_i]*1e9
        #plt.plot(ts[range_low:range_high],vs[range_low:range_high],linewidth=1)

        coeff1=[]
        var_matrix1=[]
        pInit = [0.001,0.04,-5.,0.1,12.]
        try:
            coeff1, var_matrix1 = curve_fit(pulse, ts[range_low:range_high], vs[range_low:range_high], p0=pInit,
                                            bounds=([-np.inf, 0., -np.inf, 0., -np.inf], np.inf),
                                            check_finite=False)
        except ValueError:
            print("Oops!  fit failed... skipping event")
            continue

        #coeff1=pInit
        #print("fitted parameters:",coeff1)
        #pred = pulse(ts, *coeff1)
        #print('prediction:',pred[range_low:range_high])
        #plt.plot(ts[range_low:range_high], pred[range_low:range_high], linewidth=1)

        #plt.show()
        fall_times.append(coeff1[-2])
        peak_times.append(coeff1[-1])
        Qs.append(coeff1[1])
        ped.append(coeff1[0])
        offsets.append(coeff1[2])

    plt.style.use('fivethirtyeight')
    plt.hist(list(map(lambda x : 1./x,fall_times)),bins=np.arange(0,60,1),histtype='step',linewidth=1)
    plt.xlabel('Fall Time [ns]')
    plt.ylabel('Rate (A.U.)')
    plt.savefig(dir_name + '_pulse_fall_time.png')
    plt.show()

    plt.style.use('fivethirtyeight')
    plt.hist(peak_times,bins=np.arange(0,20,0.5),histtype='step',linewidth=1)
    plt.xlabel('Peak Time [ns]')
    plt.ylabel('Rate (A.U.)')
    plt.savefig(dir_name + '_pulse_peak_time.png')
    plt.show()

    plt.style.use('fivethirtyeight')
    #bins=np.arange(0,500,2),
    plt.hist(list(map(lambda x: x/0.4,Qs)),histtype='step',linewidth=1)
    plt.xlabel('Amplitude [PE]')
    plt.ylabel('Rate (A.U.)')
    plt.savefig(dir_name + '_pulse_amplitude.png')
    plt.show()

    plt.style.use('fivethirtyeight')
    plt.hist(ped,bins=np.arange(-0.01,0.03,0.0005),histtype='step',linewidth=1)
    plt.xlabel('Pedestal [V-ns]')
    plt.ylabel('Rate (A.U.)')
    plt.savefig(dir_name + '_pulse_pedestal.png')
    plt.show()

    plt.style.use('fivethirtyeight')
    plt.hist(offsets,bins=np.arange(-20,20,1),histtype='step',linewidth=1)
    plt.xlabel('Offset [ns]')
    plt.ylabel('Rate (A.U.)')
    plt.savefig(dir_name + '_pulse_offset.png')
    plt.show()