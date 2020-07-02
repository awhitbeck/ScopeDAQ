from utils import *

if __name__ == "__main__":
    run_name=sys.argv[1]
    df = load_data(run_name)
    if run_name[-1]=='/' : run_name=run_name[:-1]
    df.to_pickle(run_name+'.pkl')
