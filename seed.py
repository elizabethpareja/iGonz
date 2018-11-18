from configuraciones import *
import psycopg2
conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s port=%s"%(host,database,user,passwd,port))
cur = conn.cursor()
sql ="""
insert into Canciones (nombre, duracion) values
 ('The Dark Side','227'),
 ('Pressure','235'),
 ('Something Human','226'),
 ('Thought Contagion','206'),
 ('Dig Down','228'),

 ('Humility','198'),
 ('Tranz','162'),
 ('Hollywood','293'),
 ('Kansas','248'),
 ('Sorcererz','180'),
 ('Idaho','222'),
 ('Lake Zurich','253'),
 ('Magic City','239'),
 ('Fire Flies','233'),
 ('One Percent','141'),
 ('Souk Eye','274'),

 ('Flesh and Bone','239'),
 ('Runaways','243'),
 ('The Way It Was','231'),
 ('Here With Me','292'),
 ('A Matter of Time','251'),
 ('Deadlines and Commitments','262'),
 ('Miss Atomic Bomb','293'),
 ('The Rising Tide','257'),
 ('Heart of a Girl','274'),
 ('From Here On Out','147'),
 ('Be Still','273'),
 ('Battle Born','313'),
 ('Carry Me Home','224'),
 ('Prize Fighter','279'),

 ('Mr. Brightside','222'),
 ('Somebody Told Me','197'),
 ('Smile Like You Mean It','234'),
 ('All These Things That Ive Done','301'),
 ('When You Were You Young','218'),
 ('Read My Mind','246'),
 ('For Reasons Unknown','212'),
 ('Human','249'),
 ('Spaceman','284'),
 ('A Dustland Fairytale','225'),
 ('Shot At The Night','242'),
 ('Just Another Girl','261'),

 ('Drop It Like Its Hot','266'),
 ('Bang Out','185'),

 ('Give Me The Night','301'),
 ('Love Dance','198'),

 ('Save That Shit','231'),
 ('The Brightside','216'),
 ('U Said','224'),
 ('Problems','209'),

 ('Waiting On My Angel','243')


returning id;
"""
cur.execute(sql)

sql ="""
insert into Autores (nombre) values
('MUSE'),
('Gorillaz'),
('George Benson'),
('Snoop Dogg'),
('Jamie Principle'),
('The Killers'),
('Lil Peep')

returning id;

"""

cur.execute(sql)


sql ="""
insert into Canciones_Autores (cancion_id, autor_id) values
('1','1'),('2','1'),('3','1'),('4','1'),('5','1'),


('6','2'),('6','3'),('7','2'),('8','2'),('8','4'),('8','5'),('9','2'),('10','2'),('11','2'),('12','2'),('13','2'),('14','2'),
('15','2'),('16','2'),

('17','6'),('18','6'),('19','6'),('20','6'),('21','6'),('22','6'),('23','6'),('24','6'),('25','6'),('26','6'),
('27','6'),('28','6'),('29','6'),('30','6'),

('31','6'),('32','6'),('33','6'),('34','6'),('35','6'),('36','6'),('37','6'),('38','6'),('39','6'),('40','6'),
('41','6'),('42','6'),

('43','4'),('44','4'),

('45','3'),('46','3'),

('47','7'),('48','7'),('49','7'),('50','7'),

('51','5')


"""
cur.execute(sql)

sql ="""
insert into Generos (nombre) values
('Hard Rock'),
('Rock Progresivo'),
('Rock Electronico'),
('Rock Espacial'),
('Electronica'),

('Alternativo'),
('Independiente'),

('Indie Rock'),
('New Wave'),
('Rock Alternativo'),
('Heartland Rock'),
('Rock'),

('Westcoast Hip Hop'),
('Rap'),

('Smooth jazz'),

('Trap'),
('Hip Hop')

returning id;
"""
cur.execute(sql)

sql ="""
insert into Canciones_Generos (cancion_id, genero_id) values
('1','6'),('1','7'),('2','6'),('2','7'),('3','6'),('3','7'),('4','6'),('4','7'),('5','6'),('5','7'),


('6','6'),('6','7'),('7','6'),('7','7'),('8','6'),('8','7'),('9','6'),('9','7'),('10','6'),('10','7'),('11','6'),('11','7'),
('12','6'),('12','7'),('13','6'),('13','7'),('14','6'),('14','7'),('15','6'),('15','7'),('16','6'),('16','7'),

('17','6'),('17','7'),('17','12'),('18','6'),('18','7'),('18','12'),('19','6'),('19','7'),('19','12'),('20','6'),
('20','7'),('20','12'),('21','6'),('21','7'),('21','12'),('22','6'),('22','7'),('22','12'),('23','6'),('23','7'),
('23','12'),('24','6'),('24','7'),('24','12'),('25','6'),('25','7'),('25','12'),('26','6'),('26','7'),('26','12'),
('27','6'),('27','7'),('27','12'),('28','6'),('28','7'),('28','12'),('29','6'),('29','7'),('29','12'),('30','6'),
('30','7'),('30','12'),

('31','6'),('31','7'),('31','12'),('32','6'),('32','7'),('32','12'),('33','6'),('33','7'),('33','12'),('34','6'),
('34','7'),('34','12'),('35','6'),('35','7'),('35','12'),('36','6'),('36','7'),('36','12'),('37','6'),('37','7'),
('37','12'),('38','6'),('38','7'),('38','12'),('39','6'),('39','7'),('39','12'),('40','6'),('40','7'),('40','12'),
('41','6'),('41','7'),('41','12'),('42','6'),('42','7'),('42','12'),


('43','13'),('43','14'),('44','13'),('44','14'),

('45','15'),('46','15'),

('47','16'),('47','17'),('48','16'),('48','17'),('49','16'),('49','17'),('50','16'),('50','17'),

('51','5')

"""
cur.execute(sql)

sql ="""
insert into Albumes (nombre,ano) values
('Simulation Theory','2018'),
('The Now Now','2018'),
('Battle Born Deluxe','2012'),
('Direct Hits Deluxe','2013'),
('Rhythm and Gangsta: The Masterpiece','2004'),
('Give Me the Night','1980'),
('Come Over When You Are Sober','2017'),
('Frankie Knuckles Presents','1985')

returning id;
"""
cur.execute(sql)

sql ="""
insert into Canciones_Albumes (cancion_id, album_id) values
('1','1'),('2','1'),('3','1'),('4','1'),('5','1'),

('6','2'),('7','2'),('8','2'),('9','2'),('10','2'),('11','2'),('12','2'),('13','2'),('14','2'),('15','2'),('16','2'),

('17','3'),('18','3'),('19','3'),('20','3'),('21','3'),('22','3'),('23','3'),('24','3'),('25','3'),('26','3'),
('27','3'),('28','3'),('29','3'),('30','3'),

('18','4'),('19','4'),('23','4'),('27','4'),

('31','4'),('32','4'),('33','4'),('34','4'),('35','4'),('36','4'),('37','4'),('38','4'),('39','4'),('40','4'),
('41','4'),('42','4'),

('43','5'),('44','5'),

('45','6'),('46','6'),

('47','7'),('48','7'),('49','7'),('50','7'),

('51','8')

"""
cur.execute(sql)



conn.commit()
cur.close()
conn.close()