use c9;

drop table if exists picfile;
create table picfile (
    pic varchar(20) primary key,
    filename varchar(50),
    foreign key (pic) references user(username) 
    on delete cascade on update cascade
);
describe picfile;
