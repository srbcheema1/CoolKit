import getpass

def get_contest_name(folder):
    '''
    takes parameter folder which is name of folder you are in
    returns contest number if possible to detect
    if can't determine then return None
    '''
    user = getpass.getuser()
    if(user == 'srb' or user == 'travis'):
        # I kept for me, you too can use this ready made function
        return srb_contest_name(folder)
    '''
    to use my function just uncomment the line below this
    '''
    # return srb_contest_name(folder)
    return None

def get_problem_name(file_name):
    '''
    takes parameter file_name which is name of file you are working with
    returns problem name if possible to detect
    if can't determine then return None
    '''
    user = getpass.getuser()
    if(user == 'srb' or user == 'travis'):
        # I kept for me, you too can use this ready made function
        return srb_problem_name(file_name) # my way
    '''
    to use my function just uncomment the line below this
    '''
    # return srb_problem_name(file_name) # my way
    return None



def srb_contest_name(folder):
    '''
    my way to get contest name from folder name
    '''
    newstr = ''.join((ch if ch in '0123456789' else ' ') for ch in folder)
    number_list = [int(i) for i in newstr.split()]
    if(len(number_list) == 1):
        return str(number_list[0])
    return None


def srb_problem_name(file_name):
    '''
    my way to get problem name from file_name
    '''
    file_name = file_name.split('.')[0] #chopp off extension
    file_name = file_name.lower()

    # file_name = file_name.replace('_','')
    file_name = file_name.replace('-','')
    file_name = file_name.replace('good','')
    file_name = file_name.replace('test','')
    file_name = file_name.replace('wrong','')
    file_name = file_name.replace('fine','')
    file_name = file_name.replace('bad','')

    mapp = {
        'one':'A',
        'two':'B',
        'three':'C',
        'four':'D',
        'five':'E',
        'six':'F',
        'seven':'G',
        'eight':'H',
        'nine':'I',

    }


    for key in mapp.keys():
        if(key in file_name):
            return mapp[key]

    if(len(file_name) == 1 and file_name.isalpha()):
        return file_name.upper()

    name_arr = file_name.split('_')
    for part in name_arr:
        if(len(part) == 1 and part.isalpha()):
            return part.upper()

    newstr = ''.join((ch if ch in '0123456789' else ' ') for ch in file_name)
    num_arr = newstr.split(' ')
    if(len(num_arr) == 1):
        numm = int(num_arr[0])
        if(numm < 26):
            return chr(ord('A') + numm - 1)

    return None

if __name__ == "__main__":
    folder = input('enter folder name : ')
    print(get_contest_name(folder))
    file_name = input('enter file name : ')
    print(get_problem_name(file_name))

