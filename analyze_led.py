from scipy.optimize import curve_fit
from utils import *
channel_list=[4]

if __name__ == "__main__":
    run_name=r'C:\Users\awhitbec\OneDrive - Texas Tech University\CSV Files\5-13\timtestnoisebegin5-13'
    dir_name=run_name.split('\\')[-1]

    df = load_data(run_name)
    print(df.head())
    binning=np.arange(0,150,0.5)

    def gauss(x, *p):
        A, mu, sigma = p
        return A * np.exp(-(x - mu) ** 2 / (2. * sigma ** 2))/sigma/np.sqrt(2*np.pi)


    p0 = [400.,10, 2]
    p1 = [400.,30, 2]
    p2 = [400.,60, 2]

    norm_charge=df['charge'].values  ## difference in time is 1.25e-12 second.  Then convert to ns
    hist, bin_edges = np.histogram(norm_charge, density=True, bins=binning)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    coeff1, var_matrix1 = curve_fit(gauss, bin_centers, hist, p0=p0)
    hist_fit1 = gauss(bin_centers, *coeff1)
    coeff2, var_matrix2 = curve_fit(gauss, bin_centers, hist, p0=p1)
    hist_fit2 = gauss(bin_centers, *coeff2)
    coeff3, var_matrix3 = curve_fit(gauss, bin_centers, hist, p0=p2)
    hist_fit3 = gauss(bin_centers, *coeff3)

    #plt.hist(df['charge'])
    #plt.show()
    plt.plot(bin_centers, hist, label='Test data',linewidth=0.8)
    plt.plot(bin_centers, hist_fit1, label='Fitted data',linewidth=1.4)
    plt.plot(bin_centers, hist_fit2, label='Fitted data',linewidth=1.4)
    plt.plot(bin_centers, hist_fit3, label='Fitted data',linewidth=1.4)

    plt.legend(['Channel 4','1 PE fit','2 PE fit','3 PE fit'])
    plt.xlabel('V-ns')
    plt.ylabel('Rate [A.U]')
    plt.savefig(dir_name + '_average_pulses.png')
    plt.show()
    plt.clf()
    plt.cla()

    print('coeff1:',coeff1)
    print('coeff2:',coeff2)
    print('coeff3:',coeff3)
    print('gain (2-1):',coeff2[1]-coeff1[1])
    print('gain (3-2):',coeff3[1]-coeff2[1])
