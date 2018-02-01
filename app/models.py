from . import db,app

class Matches(db.Model):
    matchId= db.Column(db.String(13),primary_key=True)
    team= db.Column(db.String(40),primary_key=True)
    win_lose= db.Column(db.String(40))
    mdate= db.Column(db.Date)
    inns=db.Column(db.Integer)

    def __init__(self,matchId,team,win_lose,mdate,inns):
        self.matchId=matchId
        self.team=team
        self.win_lose=win_lose
        self.mdate= mdate
        self.inns=inns

class Player(db.Model):
    # id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    matchId= db.Column(db.String(13),db.ForeignKey('matches.matchId'),primary_key=True)
    plid = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    born = db.Column(db.String(500))
    team = db.Column(db.String(20))
    ptype=db.Column(db.String(20))
    batStyle=db.Column(db.String(40))
    bowStyle=db.Column(db.String(40))

    def __init__(self,matchId,plid,name,born,team,ptype,batStyle,bowStyle):
        # self.id=id
        self.matchId=matchId
        self.plid=plid
        self.name=name
        self.born=born
        self.team=team
        self.ptype=ptype
        self.batStyle=batStyle
        self.bowStyle=bowStyle

class Venue(db.Model):
    matchId= db.Column(db.String(13),db.ForeignKey('matches.matchId'),primary_key=True)
    venue=db.Column(db.String(50))
    
    def __init__(self,matchId,venue):
        self.matchId=matchId
        self.venue=venue