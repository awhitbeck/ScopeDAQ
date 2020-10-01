from utils import *
r.gROOT.ProcessLine(".L ~/tdrstyle.C")
r.gROOT.ProcessLine("setTDRStyle()")

channel_list=[1]

if __name__ == "__main__":
    run_name=sys.argv[1]
    df = load_data(run_name)

    #########################
    ## average pulse shape
    #########################
    legend_entry=[]
    for i in channel_list:
        ch_filter=df['channel']==i
        #print ch_filter
        #print len(ch_filter)
        #print len(df)
        ts=df[ch_filter]['time'].values[0]*1e9
        #print ts
        vs=np.sum(df[ch_filter]['voltage'].values)
        plt.plot(ts,vs)
        legend_entry.append('Channel'+str(i))

    plt.legend(legend_entry)
    plt.xlabel('Time [ns]')
    plt.ylabel('Amplitude (A.U.)')
    plt.savefig('average_pulses.png')
    #plt.show()
    plt.clf()
    plt.cla()

    #########################
    ### plot integrated charges
    #########################
    h=r.TH1F('h',';Charge [A.U.];Events',75,0,75)
    g1=r.TF1('g1','gaus',20,35)
    g1.SetLineColor(2)
    g2=r.TF1('g2','gaus',35,45)
    g2.SetLineColor(4)
    g3=r.TF1('g3','gaus',45,55)
    g3.SetLineColor(6)
    g4=r.TF1('g4','gaus',57,65)
    g4.SetLineColor(3)

    for c in df[ch_filter]['charge']:
        h.Fill(c)

    can=r.TCanvas('can','can',500,500)

    h.SetLineColor(1)
    h.SetLineWidth(2)
    h.Draw()

    h.Fit('g1','R')
    h.Fit('g2','R')
    h.Fit('g3','R')
    h.Fit('g4','R')
    
    g1.Draw("SAME")
    g2.Draw("SAME")
    g3.Draw("SAME")
    g4.Draw("SAME")

    can.SaveAs('led_response.png')

