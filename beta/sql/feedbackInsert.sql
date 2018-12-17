use lounge_db;

delete from feedback;

insert into feedback (pid, subject, message, edate) 
    values ("ltso", NULL, "Riann did so well with the CSS!!!!!!!! :D", NULL),
    ("rtang", "practice", "Just wanted to let captains know that practice was great!", "2018-12-10"),
    (NULL, NULL, "I wish the team was more transparent about how profits are spent", NULL);