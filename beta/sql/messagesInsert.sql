use lounge_db;

delete from messages;

insert into messages (sender, receiver, message) 
    values ("ltso", "tdeshong", "Hey Tam!"),
    ("tdeshong", "ltso", "Lauren, what's up?"),
    ("ltso", "tdeshong", "You going to the tournament this weekend?"),
    ("tdeshong", "ltso", "Not sure yet. I have a lot of work due Monday...Hbu?"),
    ("ltso", "tdeshong", "I think so! You should come!"),
    ("tdeshong", "ltso", "eh, we'll see"),
    ("rtang", "ltso", "Going to Target. Want anything?"),
    ("ltso", "rtang", "Goldfish please"),
    ("rtang", "ltso", "Ok, will do!"),
    ("rtang", "ltso", "Actually, have another space in the car. Wanna come?"),
    ("ltso", "rtang", "ok"),
    ("rtang", "ltso", "Meet you in gray lot at 6"),
    ("rtang", "tdeshong", "knock knock"),
    ("tdeshong", "rtang", "who's there?"),
    ("rtang", "tdeshong", "interupting cow"),
    ("tdeshong", "rtang", "interupting cow who?"),
    ("rtang", "tdeshong", "moooooo"),
    ("rtang", "tdeshong", "wait...realizing this joke doesn't work over text..."),
    ("tdeshong", "rtang", "...omg riann");