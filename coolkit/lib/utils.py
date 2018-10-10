try:
    import getpass
except:
    err = """
    You haven't installed the required dependencies.
    """
    import sys, traceback,os
    sys.stderr.write(err)
    if(os.environ['HOME'] == 'srb'):
        traceback.print_exc()
    sys.exit(1)

class utils:
    def __init__(self):
        pass

    @staticmethod
    def shrink(string,max_len=50,stoppers=[32,10,13]):
        min_len = max_len - 10
        temp, flag = "", False
        i, j = 0, 0
        while(i < len(string)):
            flag = False
            if ord(string[i]) in stoppers: temp+=' '
            else: temp+=string[i]

            if(j == max_len or (j > min_len and (ord(string[i]) in stoppers))):
                temp+='\n'
                j = 0

            while(i < len(string) and ord(string[i]) in stoppers):
                flag = True
                i+=1

            if(flag): i-=1
            j+=1
            i+=1

        return temp

    @staticmethod
    def do_online_test():
        '''
        for running pytest on travis
        '''
        user = getpass.getuser()
        if(user == 'travis'):
            return False
        return True
