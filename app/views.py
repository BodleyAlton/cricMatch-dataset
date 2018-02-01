from app import app,db
from models import *
from lxml import html
from flask import request
import requests
import csv,os

@app.route('/run',methods=["GET"])
def mdata():
    print os.getcwd()
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
    