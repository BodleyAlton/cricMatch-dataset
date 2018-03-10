from app import app,db
from models import *
from lxml import html
from flask import request, jsonify
import requests,csv,os,time

@app.route('/run',methods=["GET"])
def mdata():
    print (os.getcwd())
    root=os.getcwd()
    with open(root +"/app/files/match_data.csv","r") as file,  open(root+"/app/files/match_players.csv","r") as pfile, open (root+"/app/files/match_venue.csv","r") as vfile:
        readf(file)
        readpf(pfile)
        readvf(vfile)
    # matchStats()
    return "goooo"

def readf(file):
    count=0
    reader= csv.DictReader(file, delimiter=',')
    for line in reader:
        matchID=line['matchId']
        win_lose=line['win_lose']
        team=line['team']
        date=line['date(m/d/y)']
        inns= line['inns']
        mdbUpdate(matchID,win_lose,team,date,inns) #Update match table in database
        count+=1
        print "match:",count
def readpf(pfile):
    count=0
    readpf=csv.DictReader(pfile, delimiter=',')
    for row in readpf:
        pmid=row['matchID']
        plid=row['plid']
        team=row['team']
        pdbUpdate(pmid,plid,team) #Update player table in database
        count+=1
        print "Plyr:",count
def readvf(vfile):
    count=0
    readvf=csv.DictReader(vfile,delimiter=",")
    for line in readvf:
        vmid=line['matchID']
        venue=line['venue']
        vdbUpdate(vmid,venue)
        count+=1
        print "Ven:",count
def mdbUpdate(matchID,win_lose,team,date,inns):
    match= Matches(matchID,team,win_lose,date,inns)
    db.session.add(match)
    db.session.commit()

def pdbUpdate(pmid,plid,team):
    page= requests.get("http://www.espncricinfo.com/westindies/content/player/%s.html"%(plid))
    tree = html.fromstring(page.content)
    name= tree.xpath("//div[@class='pnl490M']/div[2]/div/p[1]/span/text()")
    born= tree.xpath("//div[@class='pnl490M']/div[2]/div/p[b='Born']/span/text()")
    batStyle=tree.xpath("//div[@class='pnl490M']/div[2]/div/p[b='Batting style']/span/text()")
    bowStyle=tree.xpath("//div[@class='pnl490M']/div[2]/div/p[b='Bowling style']/span/text()")
    ptype=tree.xpath("//div[@class='pnl490M']/div[2]/div/p[b='Playing role']/span/text()")
    if ptype != []:
        ptype=ptype[0]
    else:
        ptype=None
    if batStyle != []:
        batStyle=batStyle[0]
    else:
        batStyle= None
    if bowStyle != []:
        bowStyle=bowStyle[0]
    else:
        bowStyle=None
    print name
    print born
    print born[0]
    print born[0][1:]
    playr= Player(pmid,plid,name[0],born[0][1:],team,ptype,batStyle,bowStyle)
    db.session.add(playr)
    db.session.commit()

def vdbUpdate(vmid,venue):
    venueU= Venue(vmid,venue)
    db.session.add(venueU)
    db.session.commit()
    print "V:",vmid


@app.route('/matchStats',methods=["GET"])
def matchStats():
    plyr_Bat=[]
    plyr_Bow=[]
    matchid="ODI no. 3900"
    page=requests.get("http://www.espncricinfo.com/series/11124/scorecard/1098209/West-Indies-vs-India-4th-ODI-india-in-west-indies-odi-series/")
    tree=html.fromstring(page.content)
    i=0
    while i <2:
        # print "top"
        name1= tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section batsmen']/div[1]/div[2]/div[1]/a/text()"%(i))[0]
        plid=extPlid(tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section batsmen']/div[1]/div[2]/div[1]/a/@href"%(i))[0])
        out1= tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section batsmen']/div[1]/div[2]/div[2]/a/text()"%(i))
        print "out",out1
        if out1!=[]:
            
            # out_by=out1[0].split(" ")[-1]
            # out_by=out_by.split("/")[0]
            # print "out_BY:",out_by
            
            out_by=str((out1[0].split(" "))[-1]).translate(None,"/ ( )")
            
            out=str((out1[0].split(" "))[0])
        if "/" in out_by:
            out_by=out_by.split("/")[0]
        stats=tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section batsmen']/div[1]/div[2]/div[@class='cell runs']/text()"%(i))
        plyr_Bat.append([name1,plid,out_by,out,stats])
        x=2
        while x < (len(tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section batsmen']/div[@class='flex-row']"%i))-2):
            # print "X:",x
            Name=tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section batsmen']/div[%i]/div[1]/div[1]/a/text()"%(i,x))
            if Name != []:
                # print "b4 plid"
                plid1=extPlid(tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section batsmen']/div[%i]/div[1]/div[1]/a/@href"%(i,x))[0])
                Outb=(tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section batsmen']/div[%i]/div[1]/div[2]/a/text()"%(i,x)))#.translate(None, '\ u 2020')
                # Outb=(tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section batsmen']/div[%i]/div[1]/div[2]/text()"%(i,x)))#.translate(None, '\ u 2020')
                print "Out:", Outb
                if Outb != []:
                    outm=str((Outb[0].split(" "))[0])
                    
                    Outb=Outb[0].split(" ")[-1]
                    Outb=Outb.split("/")[0]

                    # Outb=str((Outb[0].split(" "))[-1]).translate(None,"/ ( )")
                    print "OOutB:",Outb
                else:
                    Outb=None
                    outm=None
                Stats=tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section batsmen']/div[%i]/div[1]/div[@class='cell runs']/text()"%(i,x))
                plyr_Bat.append([Name[0],plid1,Outb,outm,Stats])
                Name=None
                plid1=None
                Outb=None
                Stats=None
                outm=None
            x+=1
        i+=1
    Stat=[]
    plyr_Bow=[]
    i=0
    while i <2:
        # print "LEN td:",len(tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section bowling']/table/tbody/tr"%(i)))
        t=1
        while t < (len(tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section bowling']/table/tbody/tr"%(i)))+1):
            name1= tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section bowling']/table/tbody/tr[%i]/td[1]/a/text()"%(i,t))
            plid=extPlid(tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section bowling']/table/tbody/tr[%i]/td[1]/a/@href"%(i,t))[0])
            p=3
            while p < (len(tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section bowling']/table/tbody/tr[1]/td"%(i)))):
                stats=tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section bowling']/table/tbody/tr[%i]/td[%i]/text()"%(i,t,p))[0]
                Stat.append(stats)
                p+=1
            plyr_Bow.append([name1[0],plid,Stat])
            Stat=[]
            t+=1
        i+=1
    print "BOWS:",plyr_Bow 
    for p in plyr_Bat:
        # print "p:",(str(p[2]).split(" "))[-1]
        for b in plyr_Bat:
            # print "b:",b[0]
            if (str(p[2]).split(" "))[-1] in b[0]:
                # print "found"
                p.append(b[1])
    print "BAT:",plyr_Bat
    
    for p in plyr_Bat:
        print "plid:",p[1]
        updateMBS(matchid,p)
    for z in plyr_Bow:
        updateMBoS(matchid,z)
    return "LA"
    
def updateMBoS(matchid,z):
    name=z[0][0]
    plid=z[1]
    stats=z[2]
    print "bow stats:",stats
    overs=stats[0]
    movers=stats[1]
    runs_c=stats[2]
    wickets=stats[3]
    econ=stats[4]
    
    zero=stats[5]
    fours=stats[6]
    sixes=stats[7]
    wides=stats[8]
    noBall=stats[9]
    
    # wides=stats[5]
    # noBall=stats[6]
    # zero=None
    # fours=None
    # sixes=None
    player= MatchBowStats(matchid,plid,noBall,overs,movers,runs_c,wickets,econ,zero,fours,sixes,wides)
    db.session.add(player)
    db.session.commit()
    
def updateMBS(matchid,pl):
    name=pl[0]
    plid=pl[1]
    out_by=pl[2]
    outm=pl[3]
    oplid=pl[-1]
    Stats=pl[4]
    print "STATS:",Stats
    print "S4:",Stats[3]
    print "S5:",Stats[4]
    
    strRate=Stats[4]
    b_faced=Stats[1]
    runs=Stats[0]
    fours=Stats[2]
    sixes=Stats[3]
    movers=None
    
    # strRate=Stats[5]
    # movers=Stats[1]
    # b_faced=Stats[2]
    # runs=Stats[0]
    # fours=Stats[3]
    # sixes=Stats[4]
    
    Batsman= MatchBatStats(matchid,plid,outm,out_by,strRate,movers,b_faced,runs,fours,sixes)
    db.session.add(Batsman)
    db.session.commit()
    
def extPlid(link):
    plid=link.translate(None,'http://www.espncricinfo.com/ci/content/player/.html')
    return plid


def date():
    return time.strftime("%Y-%m-%d")
@app.route("/scrape",methods=["GET"])
def scrape(plid):
    datav=[]
    page= requests.get("http://www.espncricinfo.com/westindies/content/player/%s.html"%(plid))
    tree = html.fromstring(page.content)
    a=2
    batting=[]
    bowling=[]
    while a<15:
        data=tree.xpath('//div[@class="pnl490M"]/table/tbody/tr[td[@title="Insights on odi"]]/td[@nowrap="nowrap"][%i]/text()'%a )
        for i in data:
            i=i.translate(None, '\t\n ')
            datav.append(i)
        a+=1
    print "len:",len(datav)
    print datav
    x=0
    while x < len(datav)-1:
        batting.append(datav[x])
        bowling.append(datav[x+1])
        x+=2
    batting.append(datav[-1])
    print "PLID:",plid
    print "BATTING:",batting
    print len(batting)
    print "BOWLING:",bowling
    print len(bowling)
    updDataset(plid,batting,bowling) # Add player to DB

def updDataset(plid,batStats,bowStats):
    print "date",date()
    print "plid",plid
    if bowStats[5]!='0':
        if "/" in bowStats[5]:
            if float(bowStats[5].split('/')[1])==0:
                bbi=0
            else:
                bbi= float(bowStats[5].split('/')[0]) / float(bowStats[5].split('/')[1])
            print "1st"
        else:
            bbi=bowStats[5]
    else:
        print "else"
        bbi=0
    if bowStats[6]!='0':
        if "/" in bowStats[6]:
            print "bbm", bowStats[6]
            if float(bowStats[6].split('/')[1]) == 0:
                bbm=0
            else:
                bbm= float(bowStats[6].split('/')[0]) / float(bowStats[6].split('/')[1])
            print "1st"
        else:
            bbm=bowStats[6]
    else:
        print "else"
        bbm=0
    batting= Batting(plid,date(),batStats[0],batStats[1],batStats[2],batStats[3],batStats[4],batStats[5],batStats[6],batStats[7],batStats[8],batStats[9],batStats[10],batStats[11],batStats[12],batStats[13])
    bowling= Bowling(plid,date(),bowStats[0],bowStats[1],bowStats[2],bowStats[3],bowStats[4],bbi,bbm,bowStats[7],bowStats[8],bowStats[9],bowStats[10],bowStats[11],bowStats[12])
    db.session.add_all([batting,bowling])
    db.session.commit()

#...................WRITE CSV.........................................................
@app.route('/writeCareerStats',methods=["GET"])
def writeBatt():
    batStats=[('plid','date_updated','mat','inns','notout','runs','hs','ave','bf','sr','hnds','fiftys','fours','sixs','ct','st')]
    bowStats=[('plid','date_updated','mat','inns','balls','runs','wkts','bbi','bbm','ave','econ','sr','four','five','tens')]
    for D in db.session.query(Batting.plid,Batting.date_updated,Batting.mat,Batting.inns,Batting.notout,Batting.runs,Batting.hs,Batting.ave,Batting.bf,Batting.sr,Batting.hnds,Batting.fiftys,Batting.fours,Batting.sixs,Batting.ct,Batting.st):
        batStats.append([D.plid,D.date_updated,D.mat,D.inns,D.notout,D.runs,D.hs,D.ave,D.bf,D.sr,D.hnds,D.fiftys,D.fours,D.sixs,D.ct,D.st])
    for B in db.session.query(Bowling.plid,Bowling.date_updated,Bowling.mat,Bowling.inns,Bowling.balls,Bowling.runs,Bowling.wkts,Bowling.bbi,Bowling.bbm,Bowling.ave,Bowling.econ,Bowling.sr,Bowling.fourw,Bowling.fivew,Bowling.tens):
        bowStats.append([B.plid,B.date_updated,B.mat,B.inns,B.balls,B.runs,B.wkts,B.bbi,B.bbm,B.ave,B.econ,B.sr,B.fourw,B.fivew,B.tens])
    
    with open(os.getcwd()+'/app/static/career_batting_stats.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerows(batStats) 
    
    with open(os.getcwd()+'/app/static/career_bowling_stats.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerows(bowStats)
    return "updated"

@app.route('/player')
def playerToCSV():
    player=[]
    matches=[('matchId',"team","ptype","batStyle","bowStyle")]
    for m in db.session.query(Player.matchId,Player.ptype,Player.batStyle,Player.bowStyle,Player.team):
        if m.ptype==None:
            matches.append([m.matchId,m.team,"NA",m.batStyle,m.bowStyle])
        elif m.batStyle==None:
            matches.append([m.matchId,m.team,m.ptype,"NA",m.bowStyle])
        elif m.bowStyle==None:
            matches.append([m.matchId,m.team,m.ptype,m.batStyle,"NA"])
        else:    
            matches.append([m.matchId,m.team,m.ptype,m.batStyle,m.bowStyle])
    with open(os.getcwd()+'/app/files/player_stats.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerows(matches)
    return "/app/files/player_stats.csv was updated"
    
@app.route('/venue')
def get_venue():
    venue=[]
    for v in db.session.query(Venue.matchId,Venue.venue):
        venue.append([v.matchId,v.venue])
    with open(os.getcwd()+'/app/files/venue.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerows(venue)
    return "/app/files/venue.csv was updated"
    