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
