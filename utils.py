#from pathlib import Path
import glob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import os

plt.style.use('fivethirtyeight')
plt.subplots_adjust(left=.14,bottom=.14,top=1.00)
plt.rcParams['patch.linewidth']=3.0
plt.rcParams['axes.facecolor']='#ffffff'
plt.rcParams['figure.facecolor']='#ffffff'
plt.rcParams['savefig.facecolor']='#ffffff'
plt.rcParams['axes.edgecolor']='#ffffff'
plt.rc('xtick', direction='out', color='#000000')
plt.rc('ytick', direction='out', color='#000000')

# following shape used by niramay: https://indico.fnal.gov/event/46521/contributions/202319/attachments/138355/173167/QIE_Multiple_Pulse_Input_and_noise.pdf
def pulse(x, *p):
    base, A, toff, k, tmax = p
    return base + ((x - toff) < 0) * 0. + ((x - toff) <= tmax) * ((x - toff) >= 0.) * (
                A/(tmax-toff) * (1 - np.exp(-k * (x - toff)))) + ((x - toff) > tmax) * ((x - toff) >= 0.) * (
                       A/(tmax-toff) * (1 - np.exp(-k * (tmax - toff))) * np.exp(-k * (x - toff))) / np.exp(-k * (tmax - toff))

def fit_pulse(xs, ys, *p):
    print('xs:',xs)
    print('ys:',ys)
    print('p:',p)
    try:
        coeff1, var_matrix1 = curve_fit(pulse, xs, ys, p0=p,
                                        bounds=([-np.inf, 0., -np.inf, 0., -np.inf], np.inf),
                                        check_finite=False)
        return coeff1
    except ValueError:
        print("Oops!  fit failed... return dummy values")
        return [0.,0.,0.,0.,0.]


def get_files(dir,ext='.csv'):
    file_list=[]
    for file in os.listdir(dir+'/'):
        if file.endswith(ext):
            file_list.append(os.path.join(dir+'/', file))
    return file_list

def get_pulse(timestamp,channel,debug=False):
    ch4_filter=df['channel']==4
    ch4_single_filter=df['event_timestamp']==(df[ch4_filter]['event_timestamp'].values[0])
    if debug : 
        print('ch4 times',df[ch4_single_filter]['time'].values[0])
        print('ch4 voltage',df[ch4_single_filter]['voltage'].values[0])
        print('ch4 timestamps',df[ch4_single_filter]['event_timestamp'].values[0])
    return df[ch4_single_filter]['time'].values[0],df[ch4_single_filter]['voltage'].values[0]

def match_channels(timestamps,debug=False):
    event_number=[-1]*len(timestamps)
    for i,t in enumerate(timestamps):
        if event_number[i]>=0 : continue
        diff = np.absolute(np.subtract(timestamps,t))
        diff[i]=99999999.
        if debug : 
            print('t',t,'i',i)
            print('min',min(diff))
            print('argmin',np.argmin(diff))
        event_number[np.argmin(diff)]=i
        event_number[i]=i
    return event_number
            
def load_data(dir_name,debug=False):

    file_name=''
    if dir_name[-1]=='/' : 
        file_name=dir_name[:-1]
    else :
        file_name=dir_name
        
    if dir_name[-1]=='/' : dir_name=dir_name[:-1]
    if len(glob.glob(dir_name+'*.pkl')) > 0 :
        df=None
        for f in glob.glob(dir_name+'*.pkl') :
            if df is None : 
                df = pd.read_pickle(f)
            else :
                df = df.append(pd.read_pickle(f),ignore_index=True)
        return df

    df=pd.DataFrame(columns=['time','voltage','event_timestamp','channel'])

    files=get_files(dir_name)
    for i,file in enumerate(files):
        if i % 100 == 0 : print('file',i,'/',len(files))
        fileonly = file.split('/')[-1]
        words=fileonly.split('_')
        channel=int(words[1][-1:])
        time=int(words[2][:-4])
        if debug:
            print('channel:',channel)
            print('time:',time)

        print('file name:',file)
        df_temp=pd.read_csv(file,header=8)  ### header is the number of rows in the header
        df=df.append({'time':df_temp['TIME'].values,
                      'voltage':df_temp['CH'+str(channel)].values,
                      'event_timestamp':time,
                      'channel':channel},
                     ignore_index=True)
        

    df['event_number']=match_channels(df['event_timestamp'].values)
    # baseline is meant to be the average value of charge measured before pulse
    df['baseline']=list(map(lambda x : np.sum(x[:2700]),df['voltage'].values))
    df['charge']=list(map(lambda x : np.sum(x[2700:]),df['voltage']))

    div=1000
    for i in range(int(len(df)/div)):
        if (i+1)*div > len(df) :
            df[i*div:].to_pickle(file_name+'_'+str(i)+'.pkl')
        else :
            df[i*div:(i+1)*div].to_pickle(file_name+'_'+str(i)+'.pkl')

    if debug:
        print(df.head(20))
    return df

