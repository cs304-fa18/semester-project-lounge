use lounge_db;

delete from donation;

insert into donation (pid, item, description) 
    values ("ltso", "cleats", "Lightly used, size 7"),
    ("rtang", "uniform", "Size M top, size S shorts"),
    ("tdeshong", "other", "Size S running shorts");