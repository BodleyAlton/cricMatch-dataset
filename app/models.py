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

class MatchBatStats(db.Model):
   matchId= db.Column(db.String(13),db.ForeignKey('matches.matchId'),primary_key=True)
   plid = db.Column(db.Integer,primary_key=True)
   outt= db.Column(db.String(4))
   out_by= db.Column(db.Integer)
   strRate= db.Column(db.FLOAT)
   movers=db.Column(db.Integer)
   b_faced=db.Column(db.Integer)
   runs= db.Column(db.Integer)
   fours = db.Column(db.Integer)
   sixes= db.Column(db.Integer)
   
   def __init__(self,matchId,plid,outt,out_by,strRate,movers,b_faced,runs,fours,sixes):
       self.matchId=matchId
       self.plid=plid
       self.outt=outt
       self.out_by=out_by
       self.strRate=strRate
       self.movers=movers
       self.b_faced=b_faced
       self.runs=runs
       self.fours=fours
       self.sixes

class MatchBowStats(db.Model):
    matchId= db.Column(db.String(13),db.ForeignKey('matches.matchId'),primary_key=True)
    plid = db.Column(db.Integer,primary_key=True)
    noBall=db.Column(db.Integer)
    overs= db.Column(db.Integer)
    movers=db.Column(db.Integer)
    runs_c=db.Column(db.Integer)
    wickets=db.Column(db.Integer)
    econ=db.Column(db.Integer)
    zero=db.Column(db.Integer)
    fours=db.Column(db.Integer)
    sixes=db.Column(db.Integer)
    wides=db.Column(db.Integer)
    
    def __init__(self,matchId,plid,noBall,overs,movers,runs_c,wickets,econ,zero,fours,sixes,wides):
        self.matchId=matchId
        self.plid=plid
        self.noBall=noBall
        self.overs=overs
        self.movers=movers
        self.runs_c=runs_c
        self.wickets=wickets
        self.econ=econ
        self.zero=zero
        self.fours=fours
        self.sixes=sixes
        self.wides=wides

class Venue(db.Model):
    matchId= db.Column(db.String(13),db.ForeignKey('matches.matchId'),primary_key=True)
    venue=db.Column(db.String(50))
    
    def __init__(self,matchId,venue):
        self.matchId=matchId
        self.venue=venue

# class CareerBatStats(db.Model):
#     plid = db.Column(db.Integer,primary_key=True)
#     date= mdate= db.Column(db.Date)
#     matches=db.Column(db.Integer)
#     inns_bat=db.Column(db.Integer)
#     NotOut=db.Column(db.Integer)
#     runs=db.Column(db.Integer)
#     HS=db.Column(db.Integer)
#     ave=db.Column(db.Integer)
#     b_faced=db.Column(db.Integer)
#     strRate=db.Column(db.Float)
#     hnds=db.Column(db.Integer)
#     fiftys=db.Column(db.Integer)
#     sixes=db.Column(db.Integer)
#     fours=db.Column(db.Integer)
#     catches=db.Column(db.Integer)
#     stumped=db.Column(db.Integer)
    
#     def __init__(self,plid,date,matches,inns_bat,NotOut,runs,HS,ave,b_faced,strRate,hnds,fiftys,sixes,fours,catches,stumped):
#         self.plid=plid
#         self.date=date
#         self.matches=matches
#         self.inns_bat=inns_bat
#         self.NotOut=NotOut
#         self.runs=runs
#         self.HS=HS
#         self.ave=ave
#         self.b_faced=b_faced
#         self.strRate=strRate
#         self.hnds=hnds
#         self.fiftys=fiftys
#         self.sixes=sixes
#         self.fours=fours
#         self.catches=catches
#         self.stumped=stumped
        
# class CareerBowStats(db.Model):
#     plid = db.Column(db.Integer,primary_key=True)
#     date= mdate= db.Column(db.Date)
#     matches=db.Column(db.Integer)
#     inns_bow=db.Column(db.Integer)
#     balls=db.Column(db.Integer)
#     runs_c=db.Column(db.Integer)
#     wickets=db.Column(db.Integer)
#     BBI=db.Column(db.Integer)
#     BBM=db.Column(db.Integer)
    
    