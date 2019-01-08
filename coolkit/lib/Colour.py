import sys

from srblib import Colour as srbColour

class Colour(srbColour):
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
2600 - 3000 Red     International grandmaster   1
2200 - 2599 red     Grandmaster                 1
2050 - 2199 Orange  International master        1
1900 - 2049 Orange  Master                      1
1700 - 1899 Violet  Candidate master            1
1500 - 1699 Blue    Expert                      2
1350 - 1499 Green   Specialist                  2
1200 - 1349 Green   Pupil                       2
0000 - 1199 Gray    Newbie                      2
'''

