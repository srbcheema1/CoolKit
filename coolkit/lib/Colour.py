class Colour:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    GRAY = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

    DARKGRAY = '\033[30m'
    DARKRED = '\033[31m'
    DARKGREEN = '\033[32m'
    DARKYELLOW = '\033[33m'
    DARKBLUE = '\033[34m'
    DARKPURPLE = '\033[35m'
    DARKCYAN = '\033[36m'
    DARKWHITE = '\033[37m'

    FULLDARKGRAY = '\033[40m'
    FULLDARKRED = '\033[41m'
    FULLDARKGREEN = '\033[42m'
    FULLDARKYELLOW = '\033[43m'
    FULLDARKBLUE = '\033[44m'
    FULLDARKPURPLE = '\033[45m'
    FULLDARKCYAN = '\033[46m'
    FULLDARKWHITE = '\033[47m'

    FULLGRAY = '\033[100m'
    FULLRED = '\033[101m'
    FULLGREEN = '\033[102m'
    FULLYELLOW = '\033[103m'
    FULLBLUE = '\033[104m'
    FULLPURPLE = '\033[105m'
    FULLCYAN = '\033[106m'
    FULLWHITE = '\033[107m'

    @staticmethod
    def get_colour(title):
        title = title.lower()
        Colour_map = {
                "legendary grandmaster":Colour.DARKRED,
                "international grandmaster":Colour.DARKRED,
                "grandmaster":Colour.RED,
                "international master":Colour.DARKYELLOW,
                "master":Colour.DARKYELLOW,
                "candidate master":Colour.DARKPURPLE,
                "expert":Colour.DARKBLUE,
                "specialist":Colour.GREEN,
                "pupil":Colour.GREEN,
                "newbie":Colour.GRAY,
                "":'',
                None:''
                }
        return Colour_map[title]

'''
3000 - 9999 Darkred Legendary grandmaster       1
2600 - 3000 Red	    International grandmaster	1
2200 - 2599	red	    Grandmaster	                1
2050 - 2199	Orange	International master	    1
1900 - 2049	Orange	Master	                    1
1700 - 1899	Violet	Candidate master	        1
1500 - 1699	Blue	Expert	                    2
1350 - 1499	Green	Specialist	                2
1200 - 1349	Green	Pupil	                    2
0000 - 1199	Gray	Newbie	                    2
'''
