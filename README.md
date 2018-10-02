# CoolKit

[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.ocm/srbcheema1/CoolKit/issues)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](https://github.com/srbcheema1/CoolKit)
[![HitCount](http://hits.dwyl.io/srbcheema1/CoolKit.svg)](http://hits.dwyl.io/srbcheema1/CoolKit)

CoolKit is `Coding + ToolKit`, A command-line tool used to automate your programming experience.


### Installation

#### Build from Source

- Clone the repository and checkout to stable commit
```
git clone https://github.com/srbcheema1/CoolKit
cd CoolKit
git checkout v0.0.1
```

- install requirements
```
python3 -m pip install --user -r requirements.txt
```
- Add CoolKit repository to PATH
```
echo export PATH="$PATH":"`pwd`" >> ~/.bashrc
source ~/.bashrc
```
- test for coolkit installation
```
coolkit --help
```
- if it displays help message you are ready to go.



### Usage

```
srb@srb-pc:$ coolkit --help
usage: coolkit [-h] {init,set,run,submit,fetch,config} ...

positional arguments:
  {init,set,run,submit,fetch,config}

optional arguments:
  -h, --help            show this help message and exit
```

```
suboptions are:
    init        initilize a directory as coolkit directory
    set         set value of coolkit variables.
    config      set config values like username, password.
    fetch       fetch a contest to use it for offline testing.
    run         run a code file against provided testcases
    submit      submit a code to online judge. and output the verdict.
```

```
For more help regarding suboptions run:

coolkit init -h
coolkit set -h
coolkit config -h
coolkit fetch -h
coolkit run -h
coolkit submit -h
```


### Supported sites

- codeforces

### Examples

[![Contest_Example_1](https://raw.githubusercontent.com/srbcheema1/CheemaFy/master/myPlugins/extra_things/png_images/coolkit/contest_example_1_1.png)](https://github.com/srbcheema1/)


### Similar Tools

- It is worth it to mention few other tools that I was using from a year or so. I have really loved those tools and also used some of their modules/functions in this tool. Those tools are [Acedit](https://github.com/coderick14/ACedIt) and [Idne](https://github.com/endiliey/idne/blob/master/idne.py).


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


### Development by

Developer / Author: [Srb Cheema](https://github.com/srbcheema1/)
