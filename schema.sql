DROP DATABASE IF EXISTS matchStats;
CREATE DATABASE matchStats;
use matchStats;
create table matches(
matchId varchar(13) not null,
team varchar(50),
win_lose varchar(4),
mdate date,
inns int(1),
primary key(matchId,team)
);

create table player(
matchId varchar(13) not null,
plid int not null,
name varchar(50),
born varchar(500),
team varchar(20),
ptype varchar(20),
batStyle varchar(40),
bowStyle varchar(40),
primary key(matchId,plid),
foreign key (matchId) references matches(matchId) on delete cascade on update cascade 
);

create table match_bat_stats(
matchId varchar(13) not null,
plid int not null,
outt varchar(4),
out_by int,
strRate float,
movers int,
b_faced int,
runs int,
fours int,
sixes int,
primary key(matchId,plid),
foreign key (matchId,plid) references player(matchId,plid) on delete cascade on update cascade
);

create table match_bow_stats(
matchId varchar(13) not null,
plid int not null,
noBall int,
overs int,
movers int,
runs_c int,
wickets int,
econ int,
zero int,
fours int,
sixes int,
wides int,
primary key(matchId,plid),
foreign key (matchId,plid) references player(matchId,plid) on delete cascade on update cascade
);

create table venue(
matchId varchar(13) not null,
venue varchar(50),
primary key(matchId),
foreign key (matchId) references matches(matchId) on delete cascade on update cascade 
);