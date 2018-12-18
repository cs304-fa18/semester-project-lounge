use lounge_db;

insert into user(name,nickname,classyear,username,password,user_type,sprefs) values ("Riann","Nut",2019,"rtang","$2b$12$Tss6Ri.1vwBaAZ/7yrcxNulcqEqs0Qq4YO0PzK/47o97in80u37E2","admin","all"),
("Lauren","ebae",2020,"ltso","$2b$12$NlRSKN4mSlzQAM4WNaECg.8GssbK2vR5mKa1EDPQQ34jfEgR7Rw4C","admin","all"), ("Tam","Briese",2019,"tdeshong"," $2b$12$u36cGqjFEp0PNnnn2xeIjubg2VL8HEqiUzd6YB842lZ86623XgqfS","admin","all");
insert into industry(pid,iname) values ("ltso","Health Professions"), ("tdeshong","Technology and Engineering");
insert into events(ename,city,state,country,description,edate,approved,rsvps,pid) values("Millyfest","Wellesley","MA","US","tourney","2018-11-12",1,0,"ltso");
insert into team(tname,`type`,nearestcity,state,country,pid) values ("Brute Squad","Club","Boston","MA","US","tdeshong"), ("Nightlock","League","SF","CA","US","ltso");
insert into location(pid,city,nearestcity,state,country) values ("ltso","NYC","NYC","NY","US");
insert into feedback(subject,message,edate,pid) values ("practice","good","2018-11-09","rtang"), ("tourney","good","2018-11-09","ltso"), ("party","good","2018-11-09","tdeshong");
insert into donation(pid,item,description) values ("rtang","cleats","adidas size 7"), ("ltso","uniform","2014"), ("tdeshong","money","so much money");
insert into family(name,predecessor,member) values ("dynasty","rtang","ltso"), ("herd","tdeshong","ltso");
insert into picfile(pic,filename) values ('tdeshong','default.jpg'), ('rtang','default.jpg'), ('ltso','default.jpg')