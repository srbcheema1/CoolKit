import os
import subprocess
import sys

class C: # for colours
    R = '\033[91m'
    G = '\033[92m'
    Y = '\033[93m'
    E = '\033[0m'


def print_err(msg,colour=''):
    sys.stderr.write(colour+msg+'\n'+C.E)

def print_clr(msg,colour=''):
    print(colour+msg+C.E)

def line_adder(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        lines = [x.strip() for x in f.readlines()]
        if(not line in lines):
            f.seek(0, 0)
            f.write(content + '\n' + line + '\n')


def is_installed(soft):
    dump_out = ' > /dev/null 2>&1'
    help_opt = ' --help '
    a = os.system(soft + help_opt + dump_out)
    if a == 0 or a == 256:
        '''
        0 means return 0
        256 means return 1, generally for those who dont have --help
        if command not found it will return 32512
        '''
        return True
    return False

def _get_supported_package_managers(dependency_map):
    package_managers = set()
    for rules in dependency_map.values():
        for key in rules.keys():
            package_managers.add(key)

    supported_package_managers = set()
    for package_manager in package_managers :
        if is_installed(package_manager) :
            supported_package_managers.add(package_manager)
    
    return supported_package_managers


def install_arg_complete():
    if is_installed('register-python-argcomplete'):
        line = 'eval "$(register-python-argcomplete coolkit)"'
        filename = os.environ['HOME'] + '/.bashrc'
        line_adder(filename,line)


def set_global_config():
    path = abs_path('~/.config/coolkit/global_config.py')
    if(os.path.isfile(path)):
        return
    path_of_default_global_config = '/'.join(abs_path(__file__).split('/')[:-2])+'/extra/global_config.py'
    verify_file('~/.config/coolkit/global_config.py')
    shutil.copy(path_of_default_global_config, path)


def install_dependencies(dependency_map, verbose = False):
    all_installed = True
    package_managers = _get_supported_package_managers(dependency_map)

#--handling-absence-of-package-managers--
    if len(package_managers)==0 :
        if verbose :
            print_err('Error: Unrecognised package manager',C.R)
            print_err('Please contact srbcheema2@gmail.com for full support for your system.')

        for dependency in dependency_map.keys() :
            if not is_installed(dependency) :
                print_err('Please install ' + dependency + ' dependency manually',C.R)
                all_installed = False
#--absence-of-package-managers-handled-
    else :
        if verbose :
            print_clr('Package managers detected ', C.G ) 
            for package_manager in package_managers :
                print(package_manager) #distinction of package managers

        for dependency in dependency_map.keys():

            if is_installed(dependency):
                if verbose :
                    print_clr('.:Dependency '+dependency+' already installed...',C.G)
                continue

            rules = dependency_map[dependency]

            print_clr('.:Installing ' + C.E + dependency + C.G +' dependency' , C.G) #distinction of dependency
            
            for package_manger in package_managers :
                os.system(rules[package_manager])
                if is_installed(dependency) :#else try other package managers
                    break

            if not is_installed(dependency):
                print_err('please install ' + dependency + ' dependency manually',C.Y)
                for package_manager in package_managers :
                    print_err('try command : '+rules[package_manager],C.Y)
                all_installed = False

    return all_installed


if __name__ == '__main__':
    dependency_map = {
        'register-python-argcomplete':{
            'apt':'sudo apt install python-argcomplete',#debian/ubuntu-based
            'pacman':'sudo pacman -S python-argcomplete',#arch-based
            'yum':'sudo yum -y install python-argcomplete',#red-hat
            'dnf':'sudo dnf install python-argcomplete',#fedora
            'zypper':'sudo zypper install python-argcomplete',#suse
        },
        'figlet':{
            'apt':'sudo apt install figlet',
            'pacman':'sudo pacman -S figlet',
            'yum':'sudo yum -y install figlet',
            'dnf':'sudo dnf install figlet',
            'zypper':'sudo zypper install figlet',
        },
    }
    install_dependencies( dependency_map , verbose=True )
    install_arg_complete()
