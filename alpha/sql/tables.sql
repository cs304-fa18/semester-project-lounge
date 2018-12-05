use c9;

drop table if exists family;
drop table if exists donation;
drop table if exists feedback;
drop table if exists events;
drop table if exists messages;
drop table if exists team;
drop table if exists location;
drop table if exists industry;
drop table if exists user;
    
create table user(
    name varchar(50) not NULL,
    nickname varchar(30),
    email varchar(60) not NULL,
    phnum varchar(10),
    classyear varchar(4),
    username varchar(20) not NULL,
    password varchar(30) not NULL,
    user_type enum("regular","admin") default "regular",
    sprefs enum("all", "class", "overlap", "admin") not NULL,
    primary key(username)
    )
    ENGINE = InnoDB;
    
create table location(
    pid varchar(20) not NULL,
    city varchar(50),
    nearestcity varchar(50),
    state varchar(2),
    country varchar(60),
    primary key(pid),
    foreign key (pid) references user(username)
    on delete restrict on update cascade
    )
    ENGINE = InnoDB;

create table team(
    tname varchar(50),
    `type` enum("club", "league", "college"),
    nearestcity varchar(50),
    state varchar(2),
    country varchar(60),
    pid varchar(20) not NULL,
    primary key(tname, pid),
    foreign key (pid) references user(username)
    on delete restrict on update cascade
    )
    ENGINE = InnoDB;
    
create table industry(
    pid varchar(20) not NULL,
    iname enum("Government and Law", "Technology and Engineering", "Consulting and Finance",
    "Physical and Life Sciences", "Education and Nonprofit", "Health Professions"),
    primary key(iname, pid),
    foreign key (pid) references user(username)
    on delete restrict on update cascade
    )
    ENGINE = InnoDB;
    
create table messages(
    mid int auto_increment,
    sender varchar(20) not NULL,
    receiver varchar(20) not NULL,
    message varchar(140),
    receipt bit not NULL default 0,
    primary key(mid, sender, receiver),
    foreign key (sender) references user(username)
    on delete restrict on update cascade,
    foreign key (receiver) references user(username)
    on delete restrict on update cascade
    )
    ENGINE = InnoDB;
    
create table events(
    ename varchar(50) not NULL,
    city varchar(50),
    state varchar(2),
    country varchar(60),
    description varchar(140),
    edate date not NULL,
    approved bit,
    rsvps int default 0,
    pid varchar(20) not NULL,
    primary key(ename,edate),
    foreign key (pid) references user(username)
    on delete restrict on update cascade
    )
    ENGINE = InnoDB;
    
create table feedback(
    fid int auto_increment,
    subject varchar(50),
    message varchar(140),
    edate date,
    pid varchar(20),
    primary key(fid),
    foreign key (pid) references user(username)
    on delete restrict on update cascade
    )
    ENGINE = InnoDB;
    
create table donation(
    did int auto_increment,
    pid varchar(20) not NULL, 
    item enum("cleats", "uniform", "other"),
    description varchar(140),
    seen bit not NULL default 0,
    primary key(did),
    foreign key (pid) references user(username)
    on delete restrict on update cascade
    )
    ENGINE = InnoDB;
    
create table family(
    name varchar(30),
    predecessor varchar(20), 
    member varchar(20),
    primary key(name, member),
    foreign key (predecessor) references user(username)
    on delete restrict on update cascade,
    foreign key (member) references user(username)
    on delete restrict on update cascade
    )
    ENGINE = InnoDB;