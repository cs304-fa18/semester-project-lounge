use c9;

insert into user(name,nickname,classyear,username,password,sprefs) values ("Riann","Nut",2019,"rtang","pass","all"),
("Lauren","ebae",2020,"ltso","pass","all"), ("Tam","Briese",2019,"tdeshong","pass","all");
insert into regulars(username,password,sprefs) values("ltso","pass","all");
insert into admins(username,password) values ("rtang","pass"), ("tdeshong","pass");
insert into industry(pid,iname) values ("ltso","Health Professions"), ("tdeshong","Technology and Engineering");
insert into events(ename,city,state,country,description,edate,approved) values("Millyfest","Wellesley","MA","US","tourney","2018-11-12",1);
insert into messages(sender,receiver,message) values ("ltso","tdeshong","hi"), ("ltso","tdeshong","bye"), ("tdeshong","rtang","cool");
insert into team(tname,`type`,nearestcity,state,country,pid) values ("Brute Squad","club","Boston","MA","US","tdeshong"), ("Nightlock","league","SF","CA","US","ltso");
insert into location(pid,city,nearestcity,state,country) values ("ltso","NYC","NYC","NY","US");
insert into feedback(subject,message,edate,pid) values ("practice","good","2018-11-09","rtang"), ("tourney","good","2018-11-09","ltso"), ("party","good","2018-11-09","tdeshong");
insert into donation(pid,item,description) values ("rtang","cleats","adidas size 7"), ("ltso","uniform","2014"), ("tdeshong","money","so much money");
insert into family(fid,name,predecessor,member) values (1,"dynasty","rtang","ltso"), (1,"herd","ltso","tdeshong");
