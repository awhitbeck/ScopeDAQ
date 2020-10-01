from utils import *

channel_list=[4]

if __name__ == "__main__":
    run_name=sys.argv[1]
    dir_name=run_name.split('/')[-2]
    print dir_name
    df = load_data(run_name)

    #########################
    ## average pulse shape
    #########################
    for i in channel_list:
        ch_filter=(df['channel']==i)
        #print ch_filter
        #print len(ch_filter)
        #print len(df)
        ts=df[ch_filter]['time'].values[0]*1e9
        #print ts
        vs=np.sum(df[ch_filter]['voltage'].values)
        plt.plot(ts,vs)

    plt.legend('Channel'.join(map(str,channel_list)))
    plt.xlabel('Time [ns]')
    plt.ylabel('Amplitude (A.U.)')
    plt.savefig(dir_name+'_average_pulses.png')
    #plt.show()
    plt.clf()
    plt.cla()

    df['charge']=np.subtract(df['charge'],df['baseline'])

    #########################
    ## get charge for channels 1 and 4 for each event
    #########################
    events = np.unique(df['event_number'])
    charge_pairs=[]
    for event in events : 
        event_filter = df['event_number']==event
        ch4_filter=df['channel']==4
        ch1_filter=df['channel']==1
        if len(df[event_filter&ch1_filter]['charge'].values) != 1 or len(df[event_filter&ch4_filter]['charge'].values) != 1 : 
            print 'there are duplicates or not enough pulses in event',event
        else : 
            charge_pairs.append([df[event_filter&ch1_filter]['charge'].values[0],df[event_filter&ch4_filter]['charge'].values[0]])

    charge1=np.transpose(charge_pairs)[0]
    charge1=np.divide(charge1,12.)
    charge4=np.transpose(charge_pairs)[1]
    charge4=np.divide(charge4,12.)

    plt.hist2d(charge1,charge4,bins=[np.arange(0,400,10),np.arange(0,400,10)])
    #plt.scatter(charge1,charge4,alpha=0.1)
    plt.subplots_adjust(left=.14,bottom=.14,top=1.00)
    plt.xlabel('Channel 1 Charge [PEs]')
    plt.ylabel('Channel 4 Charge [PEs]')
    plt.savefig(dir_name+'_charge_correlation.png')
    #plt.show()
    plt.clf()
    plt.cla()

    #########################
    ### plot integrated charges
    #########################
    low_bin=0
    high_bin=400
    bin_width=20
    ch1_bins=plt.hist(charge1,bins=np.arange(low_bin,high_bin,bin_width),histtype='step')
    ch4_bins=plt.hist(charge4,bins=np.arange(low_bin,high_bin,bin_width),histtype='step')
    plt.legend(['Channel 1','Channel 4'])
    plt.xlabel('Charge [PEs]')
    plt.ylabel('Events')
    plt.yscale('log')
    plt.savefig(dir_name+'_response.png')
    #plt.show()
    plt.clf()
    plt.cla()

    print 'channel 1 mean',np.mean(charge1)
    print 'channel 1 MPV',ch1_bins[1][np.argmax(ch1_bins[0])]+bin_width/2.
    print 'channel 4 mean',np.mean(charge4)
    print 'channel 4 MPV',ch4_bins[1][np.argmax(ch4_bins[0])]+bin_width/2.
    

    #########################
    ### plot a pulse
    #########################
    #t,v=get_pulse(20200627162332256,4)
    #gr=r.TGraph(len(t),t,v)
    #gr.Draw("AC")

    # ch4_filter=df['channel']==4
    # ch1_filter=df['channel']==1
    # plt.hist(df[ch4_filter]['charge'].values,np.arange(0,5000,100),histtype='step')
    # plt.hist(df[ch1_filter]['charge'].values,np.arange(0,5000,100),histtype='step')
    # plt.legend(['channel 4','channel 1'])
    # plt.show()
    # print 'channel 4 mean',np.mean(df[ch4_filter]['charge'].values)
    # print 'channel 1 mean',np.mean(df[ch1_filter]['charge'].values)
