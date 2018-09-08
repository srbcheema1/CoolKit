class Contest:
    def __init__():
        pass

    @staticmethod
    def get_short_contest_name(contest):
        contest = contest.replace("Codeforces","CF")
        contest = contest.replace("Educational","EDU")
        contest = contest.replace("Elimination","ELM")
        contest = contest.replace("Rated","R")
        contest = contest.replace("rated","R")
        contest = contest.replace("Round","RD")
        contest = contest.replace("Div. 2","D2")
        contest = contest.replace("Div. 1","D1")
        contest = contest.replace("[TBD]","D-")
        if(len(contest) > 30):
            contest = contest[0:30]
        return contest

    @staticmethod
    def get_formatted_time(time,offset = '03:00'):
        date,time = time.split()
        month,date = date.split('/')[:-1]
        date = int(date)

        hour,mins = time.split(':')
        hour = int(hour)
        mins = int(mins)

        off_h,off_m = offset.split(':')
        off_h = int(off_h)
        off_m = int(off_m)

        mins = mins + off_m
        if(mins >= 60):
            mins -= 60
            hour += 1

        hour = hour + off_h
        if(hour >= 24):
            hour -= 24
            date +=1

        return str(date).zfill(2) + '-' + month + ' ' + str(hour).zfill(2) + ':' + str(mins).zfill(2)
