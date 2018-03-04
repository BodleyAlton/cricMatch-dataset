from app import app,db
from models import *
from lxml import html
from flask import request, jsonify
import requests
import csv,os

@app.route('/run',methods=["GET"])
def mdata():
    print (os.getcwd())
    root=os.getcwd()
    with open(root +"/app/files/match_data.csv","r") as file,  open(root+"/app/files/match_players.csv","r") as pfile, open (root+"/app/files/match_venue.csv","r") as vfile:
        readf(file)
        readpf(pfile)
        readvf(vfile)
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
    return "updt match"
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
    return "Plyr"
def readvf(vfile):
    count=0
    readvf=csv.DictReader(vfile,delimiter=",")
    for line in readvf:
        vmid=line['matchID']
        venue=line['venue']
        vdbUpdate(vmid,venue)
        count+=1
        print "Ven:",count
    return "ven"
def mdbUpdate(matchID,win_lose,team,date,inns):
    match= Matches(matchID,team,win_lose,date,inns)
    db.session.add(match)
    db.session.commit()
    print "mcmt"
    return "Mdt"
    
@app.route('/matchStats',methods=["GET"])
def matchStats():
    plyr_Bat=[]
    plyr_Bow=[]
    matchid="ODI no. 2952"
    page=requests.get("http://www.espncricinfo.com/series/13426/scorecard/406193/Australia-vs-West-Indies-2nd-ODI-west-indies-in-australia-odi-series/")
    tree=html.fromstring(page.content)
    i=0
    while i <2:
        name1= tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section batsmen']/div[1]/div[2]/div[1]/a/text()"%(i))
        plid=extPlid(tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section batsmen']/div[1]/div[2]/div[1]/a/@href"%(i))[0])
        out1= tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section batsmen']/div[1]/div[2]/div[2]/a/text()"%(i))
        stats=tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section batsmen']/div[1]/div[2]/div[@class='cell runs']/text()"%(i))
        plyr_Bat.append([name1,plid,out1,stats])
        x=2
        while x < (len(tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section batsmen']/div[@class='flex-row']"%i))-3):
            print "I:",i
            Name=tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section batsmen']/div[%x]/div[1]/div[1]/a/text()"%(i,x))
            Outb=(tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section batsmen']/div[%x]/div[1]/div[2]/a/text()"%(i,x)))#.translate(None, '\ u 2020')
            Stats=tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section batsmen']/div[%x]/div[1]/div[@class='cell runs']/text()"%(i,x))
            plyr_Bat.append([Name,plid,Outb,Stats])
            x+=1
        i+=1
    print "BATS:",plyr_Bat
    Stat=[]
    plyr_Bow=[]
    i=0
    while i <2:
        print "LEN td:",len(tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section bowling']/table/tbody/tr"%(i)))
        t=1
        while t < (len(tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section bowling']/table/tbody/tr"%(i)))+1):
            name1= tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section bowling']/table/tbody/tr[%i]/td[1]/a/text()"%(i,t))
            plid=extPlid(tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section bowling']/table/tbody/tr[%i]/td[1]/a/@href"%(i,t))[0])
            p=3
            while p < (len(tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section bowling']/table/tbody/tr[1]/td"%(i)))):
                stats=tree.xpath("//div[@id='gp-inning-0%i']/div[@class='scorecard-section bowling']/table/tbody/tr[%i]/td[%i]/text()"%(i,t,p))[0]
                Stat.append(stats)
                p+=1
            plyr_Bow.append([name1,plid,Stat])
            Stat=[]
            t+=1
        i+=1
    print "BOWS:",plyr_Bow 
    
    
    return "LA"

def updateMBS(Name,Outb,Stats,matchid,plid,out_by):
    plyr=[]
    strRate=Stats[5]
    movers=Stats[1]
    b_faced=Stats[2]
    runs=Stats[0]
    fours=Stats[3]
    sixes=Stats[4]
    plyr.append([matchid,plid,outt,out_by,strRate,movers,b_faced,runs,fours,sixes])
    
def extPlid(link):
    plid=link.translate(None,'http://www.espncricinfo.com/ci/content/player/.html')
    return plid
    
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
    playr= Player(pmid,plid,name[0],born[0][1:],team,ptype,batStyle,bowStyle)
    db.session.add(playr)
    db.session.commit()
    print "ODI#:",pmid
    print "Plid:",plid

def vdbUpdate(vmid,venue):
    venueU= Venue(vmid,venue)
    db.session.add(venueU)
    db.session.commit()
    print "V:",vmid

@app.route('/player')
def player():
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