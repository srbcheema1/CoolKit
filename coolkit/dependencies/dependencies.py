dependency_map = {
        'register-python-argcomplete':{
            'apt':'sudo apt install python-argcomplete',#debian/ubuntu-based
            'pacman':'sudo pacman -S python-argcomplete',#arch-based
            'yum':'sudo yum -y install python-argcomplete',#red-hat
            'dnf':'sudo dnf install python-argcomplete',#fedora
            'zypper':'sudo zypper install python-argcomplete',#suse
        },
}
