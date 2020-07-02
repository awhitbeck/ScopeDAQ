import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ROOT as r
from array import array 
import os
from itertools import combinations

plt.style.use('fivethirtyeight')
plt.subplots_adjust(left=.14,bottom=.14,top=1.00)
plt.rcParams['patch.linewidth']=3.0
plt.rcParams['axes.facecolor']='#ffffff'
plt.rcParams['figure.facecolor']='#ffffff'
plt.rcParams['savefig.facecolor']='#ffffff'
plt.rcParams['axes.edgecolor']='#ffffff'
plt.rc('xtick', direction='out', color='#000000')
plt.rc('ytick', direction='out', color='#000000')

def get_files(dir):
    file_list=[]
    for file in os.listdir(dir):
        if file.endswith(".csv"):
            file_list.append(os.path.join(dir, file))
    return file_list

def get_pulse(timestamp,channel,debug=False):
    ch4_filter=df['channel']==4
    ch4_single_filter=df['event_timestamp']==(df[ch4_filter]['event_timestamp'].values[0])
    if debug : 
        print 'ch4 times',df[ch4_single_filter]['time'].values[0]
        print 'ch4 voltage',df[ch4_single_filter]['voltage'].values[0]
        print 'ch4 timestamps',df[ch4_single_filter]['event_timestamp'].values[0]
    return df[ch4_single_filter]['time'].values[0],df[ch4_single_filter]['voltage'].values[0]

def match_channels(timestamps,debug=False):
    event_number=[-1]*len(timestamps)
    for i,t in enumerate(timestamps):
        if event_number[i]>=0 : continue
        diff = np.absolute(np.subtract(timestamps,t))
        diff[i]=99999999.
        if debug : 
            print 't',t,'i',i
            print 'min',min(diff)
            print 'argmin',np.argmin(diff)
        event_number[np.argmin(diff)]=i
        event_number[i]=i
    return event_number
            
def load_data(dir_name,debug=False):

    file_name=''
    if dir_name[-1]=='/' : 
        file_name=dir_name[:-1]
    else :
        file_name=dir_name

    if os.path.exists(file_name+'.pkl') : 
        return pd.read_pickle(file_name+'.pkl')

    df=pd.DataFrame(columns=['time','voltage','event_timestamp','channel'])

    files=get_files(dir_name)
    for i,file in enumerate(files):
        if i % 10 == 0 : print 'file',i,'/',len(files)
        fileonly = file.split('/')[-1]
        words=fileonly.split('_')
        channel=int(words[1][-1:])
        time=int(words[2][:-4])
        if debug:
            print 'channel:',channel
            print 'time:',time

        df_temp=pd.read_csv(file,header=7)
        df=df.append({'time':df_temp['TIME'].values,
                      'voltage':df_temp['CH'+str(channel)].values,
                      'event_timestamp':time,
                      'channel':channel},
                     ignore_index=True)
        

    df['event_number']=match_channels(df['event_timestamp'].values)
    df['charge']=map(np.sum,df['voltage'])

    df.to_pickle(file_name+'.pkl')

    if debug:
        print df.head(20)
    return df

