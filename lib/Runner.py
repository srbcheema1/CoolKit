try:
    from lib.Colour import Colour
except:
    from Colour import Colour

class Runner:
    def __init__(self,args,prob):
        self.args = args
        self.prob = prob

    def run(self):
        print(Colour.GREEN+'running %s file for %s prob on %s'%(self.args['inp'],self.args['prob'],self.args['contest'])+Colour.END)


