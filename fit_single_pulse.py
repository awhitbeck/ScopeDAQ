from scipy.optimize import curve_fit
from utils import *

channel_list=[4]

if __name__ == "__main__":
    #run_name=sys.argv[1]
    run_name=r'C:\Users\awhitbec\OneDrive - Texas Tech University\CSV Files\5-13\timtestbar3-5-13'
    dir_name=run_name.split('\\')[-1]

    df = load_data(run_name)

    event_i=104
    range_low=0
    range_high=10000

    vs=df['voltage'].values[event_i]
    ts=df['time'].values[event_i]*1e9
    plt.plot(ts[range_low:range_high],vs[range_low:range_high],linewidth=1)

    coeff1=[]
    var_matrix1=[]
    pInit = [0.01,0.04,-5.,0.01,12.]
    try:
        coeff1, var_matrix1 = curve_fit(pulse, ts[range_low:range_high], vs[range_low:range_high], p0=pInit,
                                        bounds=([-np.inf, 0., -np.inf, 0., -np.inf], np.inf),
                                        check_finite=False)
    except ValueError:
        print("Oops!  fit failed... skipping event")
        exit()

    print("fitted parameters:",coeff1)
    pred = pulse(ts, *coeff1)
    print('prediction:',pred[range_low:range_high])
    plt.plot(ts[range_low:range_high], pred[range_low:range_high], linewidth=1)

    plt.show()