from Colour import Colour
class Dummy_user:
    def __init__(self,uname,title,rat,m_rat,m_title,friends,rdate):
        self.user_name = uname
        self.title = title
        self.rating = rat
        self.max_rating = m_rat
        self.max_title = m_title
        self.friends = friends
        self.reg_date = rdate
        self.colour = Colour.get_colour(self.title)
        self.div = 2
        if(int(self.rating) >= 1700):
            self.div = 1

    def print_data(self):
        print(self.colour + self.title + Colour.END)
        print(self.colour + self.user_name + Colour.END)
        print('Contest rating: '+self.colour + self.rating + Colour.END,end='')
        print('(max. ' + Colour.get_colour(self.max_title) + self.max_title + ',' + self.max_rating + Colour.END + ')')
        print('Friend of: ' + self.friends + ' users')
        print('Registered: '+self.reg_date)

