# CoolKit

[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.ocm/srbcheema1/CoolKit/issues)
[![a srbcheema1 production](https://img.shields.io/badge/-a%20srbcheema1%20production-blue.svg)](https://github.com/srbcheema1)
[![Build status](https://api.travis-ci.org/srbcheema1/CoolKit.svg?branch=master)](https://travis-ci.org/srbcheema1/CoolKit)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](https://github.com/srbcheema1/CoolKit)
[![HitCount](http://hits.dwyl.io/srbcheema1/CoolKit.svg)](http://hits.dwyl.io/srbcheema1/CoolKit)

**CoolKit** is `Coding + ToolKit`, A command-line tool used to automate your programming experience.


### Installation

#### Install using pip

- Use pip to install, user `--user` flag
```
sudo python3 -m pip install coolkit
```

#### Build from Source

- Clone the repository and checkout to stable commit
```
git clone https://github.com/srbcheema1/CoolKit
cd CoolKit
git checkout <latest_version say: v0.0.x>
```

- install requirements
```
python3 -m pip install --user -r requirements.txt
```
- Install CoolKit
```
python3 setup.py install --user
```

#### Verify installation
- check for working
```
coolkit --help
```
- if it displays help message you are ready to go.


#### troubleshooting
- In case `coolkit -h` is not working, ensure that binary path is in PATH.
Add line `export PATH=$PATH:"~/.local/bin"` in your `~/.bashrc` or `~/.zshrc`.

- bash users run these commands
```
echo export PATH="$PATH":"~/.local/bin" >> ~/.bashrc
source ~/.bashrc
```
- zsh users run these commands
```
echo export PATH="$PATH":"~/.local/bin" >> ~/.zshrc
source ~/.zshrc
```

#### Make it more smart
- **Highly Recommended to use this feature to harness the full potential of coolkit**
- you can make your coolkit to autodetect your `contest` and `problem` from your nomenclature of files and directories.
- to do so you will need to redefine `get_contest_name` and `get_problem_name` in `~/.config/coolkit/global_config.py`.
- you may define your own functions or use pre-build functions by uncommenting these lines:
```
# return srb_contest_name(folder)
# return srb_problem_name(file_name)
```
- feel free to ping me on `srbcheema2@gmail.com` to make a `global_config.py` file for you as per your nomenclature.


### Usage

```
srb@srb-pc:$ coolkit --help
usage: Coolkit [-h] [-v] {init,set,run,submit,fetch,config,view} ...

positional arguments:
  {init,set,run,submit,fetch,config,view}

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         display version number
```

```
suboptions are:
    init        initilize a directory as coolkit directory
    set         set value of coolkit variables.
    config      set config values like username, password.
    fetch       fetch a contest to use it for offline testing.
    run         run a code file against provided testcases
    submit      submit a code to online judge. and output the verdict.
    view        view a user, contest, problem, friends-standings or upcoming contest
```

```
For more help regarding suboptions run:

coolkit init -h
coolkit set -h
coolkit config -h
coolkit fetch -h
coolkit run -h
coolkit submit -h
coolkit view -h
```


### Supported sites

- codeforces

### Examples

#### init
init an empty repository
```
srb@srb-pc:$ coolkit init
```
#### set
set value of coolkit-variables for contest, prob, site, contest-type
```
srb@srb-pc:$ coolkit set -c 535
srb@srb-pc:$ coolkit set -p A
srb@srb-pc:$ coolkit set -t gym
```

#### config
set value of global configuration variables like username, password
```
srb@srb-pc:$ coolkit config --user srbcheema1
srb@srb-pc:$ coolkit config --pswd I_wont_write_it_here_xD
```

#### fetch
fetch a contest, if you are standing in a coolkit folder then by default it will fetch a contest configured in that folder unless you provide using `-c` option. outside a coolkit repo it is necessary to provide contest name using `-c`
```
srb@srb-pc:$ coolkit fetch
srb@srb-pc:$ coolkit fetch -c 1025
```
#### run
run a problem against sample test cases. you can provide problem name using `-p` option, if you dont provide a problem name it will try to automatically detect the problem name using rules specified in `~/.config/coolkit/global_config.py`. **you can modify this file as you want**.
if it is unable to detect file name then it will try to remember last problem you ran and run the test cases against it.
```
srb@srb-pc:$ coolkit run one.cpp
Prob name not provided, trying to detect from filename
running one.cpp file for A prob on 837
srb@srb-pc:$ coolkit run soln.cpp
Prob name not provided, trying to detect from filename
Unable to detect prob name from file name
```

There is a cool new feature: you may add your own custom input/outputs to test against binary during run command. just add these to files to your present working directory `Input.txt` and `Output.txt` containing input and output respectively.


#### submit
Submit a file on online judge and show you report through desktop notification. **it wont submit a file if it fails on local sample test cases**. Still if you want to submit a file use `-f` flag
```
srb@srb-pc:$ coolkit submit one.cpp
srb@srb-pc:$ coolkit submit one.cpp -p A
srb@srb-pc:$ coolkit submit one.cpp -p A -f
```
#### view
```
srb@srb-pc:$ coolkit view user srbcheema1
srb@srb-pc:$ coolkit view prob A
srb@srb-pc:$ coolkit view contest 535
srb@srb-pc:$ coolkit view upcoming
srb@srb-pc:$ coolkit view friends
srb@srb-pc:$ coolkit view standings
```

### Demo for a contest

[![Contest_Example_1](https://raw.githubusercontent.com/srbcheema1/CheemaFy/master/myPlugins/extra_things/png_images/coolkit/contest_example_1_1.png)](https://github.com/srbcheema1/)


### Similar Tools

- It is worth it to mention few other tools that I was using from a year or so. I have really loved those tools and also used some of their modules/functions in this tool. Those tools are [SpojPi](https://github.com/nimitbhardwaj/SpojPI), [Acedit](https://github.com/coderick14/ACedIt) and [Idne](https://github.com/endiliey/idne/blob/master/idne.py).


### Note

- Coolkit is smart enough to detect a directory is coolkit repo or not. it automatically initilizes a directory as a coolkit directory in case it is not. Still I have provided `init` option. Its main purpose is to initilize a coolkit directory inside another coolkit directory. by default it will copy parent configurations for once which you can change lateron.
- Coolkit is smart enough to detect your program name from your filename. Have a look at `get_problem_name` in `global_config.py` file. you can suggest imporvements in that function.
- Coolkit is smart enough to detect your contest name from your directory name. Have a look at `get_contest_name` in `global_config.py` file. you can suggest imporvements in that function.
- To suggest me improvements you can open an issue, make an PR, mail me or contact me on links provided below. I am working to provide a flexible way for users to modify their own way of detection.
- In case of any bug/issue, Please report this to srbcheema2@gmail.com. Or, even better, submit a PR to fix it!


### Contact / Social Media

[![Github](https://raw.githubusercontent.com/srbcheema1/CheemaFy/master/myPlugins/extra_things/png_images/social/github.png)](https://github.com/srbcheema1/)
[![LinkedIn](https://raw.githubusercontent.com/srbcheema1/CheemaFy/master/myPlugins/extra_things/png_images/social/linkedin-48x48.png)](https://www.linkedin.com/in/srbcheema1/)
[![Facebook](https://raw.githubusercontent.com/srbcheema1/CheemaFy/master/myPlugins/extra_things/png_images/social/fb.png)](https://www.facebook.com/srbcheema/)


### Developed by

Developer / Author: [Srb Cheema](https://github.com/srbcheema1/)
