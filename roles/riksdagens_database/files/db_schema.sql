CREATE TABLE dokument (
hangar_id int,
dok_id TEXT,
rm TEXT,
beteckning TEXT,
doktyp TEXT,
typ TEXT,
subtyp TEXT,
tempbeteckning TEXT,
organ TEXT,
mottagare TEXT,
nummer int,
slutnummer int,
datum datetime,
systemdatum datetime,
publicerad datetime,
titel TEXT,
subtitel TEXT,
status TEXT,
htmlformat TEXT,
relaterat_id TEXT,
source TEXT,
sourceid TEXT,
dokument_url_text TEXT,
dokument_url_html TEXT,
dokumentstatus_url_xml TEXT,
utskottsforslag_url_xml TEXT,
html ntext
);

 
CREATE TABLE dokutskottsforslag (
rm TEXT,
bet TEXT,
punkt int,
beteckning TEXT,
rubrik TEXT,
forslag TEXT,
forslag_del2 TEXT,
beslutstyp TEXT,
beslut TEXT,
motforslag_nummer int,
motforslag_partier TEXT,
votering_id TEXT,
votering_sammanfattning_html TEXT,
votering_ledamot_url_xml TEXT,
vinnare TEXT
);

 
CREATE TABLE dokmotforslag (
nummer int,
rubrik TEXT,
forslag TEXT,
partier TEXT,
typ TEXT,
utskottsforslag_punkt int,
id TEXT
);

 
CREATE TABLE dokaktivitet (
hangar_id int,
kod TEXT,
namn TEXT,
datum datetime,
status TEXT,
ordning TEXT,
process TEXT
);

 
CREATE TABLE dokintressent (
hangar_id int,
intressent_id TEXT,
namn TEXT,
partibet TEXT,
ordning int,
roll TEXT
);

 
CREATE TABLE dokforslag (
hangar_id int,
nummer int,
beteckning TEXT,
lydelse TEXT,
lydelse2 TEXT,
utskottet TEXT,
kammaren TEXT,
behandlas_i TEXT,
kammarbeslutstyp TEXT
);
 
 
 
CREATE TABLE dokuppgift (
hangar_id int,
kod TEXT,
namn TEXT,
text ntext
);

 
CREATE TABLE dokbilaga (
hangar_id int,
dok_id TEXT,
titel TEXT,
subtitel TEXT,
filnamn TEXT,
filstorlek int,
filtyp TEXT,
fil_url TEXT
);

 
CREATE TABLE dokreferens (
hangar_id int,
referenstyp TEXT,
uppgift TEXT,
ref_dok_id TEXT,
ref_dok_typ TEXT,
ref_dok_rm TEXT,
ref_dok_bet TEXT,
ref_dok_titel TEXT,
ref_dok_subtitel TEXT
);

 
CREATE TABLE debatt (
hangar_id int,
video_id TEXT,
video_url TEXT,
tumnagel TEXT,
anf_video_id TEXT,
anf_hangar_id int,
anf_sekunder int,
anf_klockslag TEXT,
datumtid datetime,
talare TEXT,
anf_datum datetime,
anf_typ TEXT,
anf_text TEXT,
anf_beteckning TEXT,
anf_nummer TEXT,
intressent_id TEXT,
parti TEXT,
anf_rm TEXT
);

 
 
CREATE TABLE votering (
rm TEXT, 
beteckning TEXT,
hangar_id int,
votering_id TEXT,
punkt int,
namn TEXT,
intressent_id TEXT,
parti TEXT,
valkrets TEXT,
valkretsnummer int,
iort TEXT,
rost TEXT,
avser TEXT,
votering TEXT,
banknummer int,
fornamn TEXT,
efternamn TEXT,
kon TEXT,
fodd int,
datum datetime
);



CREATE TABLE anforande (
pk int,
dok_id TEXT,
dok_titel TEXT,
dok_hangar_id int,
dok_rm TEXT,
dok_nummer int,
dok_datum datetime,
avsnittsrubrik TEXT,
kammaraktivitet TEXT,
justerat TEXT,
anf_id TEXT,
anf_nummer int,
talare TEXT,
rel_dok_id TEXT,
parti TEXT,
lydelse ntext,
intressent_id TEXT,
intressent_hangar_id int,
replik TEXT,
systemdatum datetime,
källa TEXT,
anf_hangar_id int,
rel_dok_hangar_id int
);



CREATE TABLE person (
id int,
hangar_id int,
intressent_id TEXT,
kontrollsumma TEXT,
född_år smallint,
född datetime,
avliden datetime,
kön TEXT,
förnamn TEXT,
efternamn TEXT,
tilltalsnamn TEXT,
sorteringsnamn TEXT,
iort TEXT,
parti TEXT,
valkrets TEXT,
bänknummer int,
invalsordning int,
status TEXT,
källa TEXT,
källa_id TEXT,
statsråd TEXT,
timestamp datetime,
personid int
);




CREATE TABLE personuppdrag (
id int,
organ_kod TEXT,
hangar_id int,
intressent_id TEXT,
ordningsnummer int,
roll_kod TEXT,
status TEXT,
typ TEXT,
[from] datetime,
tom datetime,
källa TEXT,
källa_id TEXT,
uppgift TEXT
);



CREATE TABLE personuppgift (
id int,
hangar_id int,
intressent_id TEXT,
uppgift_kod TEXT,
uppgift ntext,
källa TEXT,
källa_id TEXT,
uppgift_typ TEXT
);



CREATE TABLE planering (
nyckel int,
id TEXT,
rm TEXT,
typ TEXT,
dokserie_id TEXT,
subtyp TEXT,
bet TEXT,
tempbet TEXT,
intressent TEXT,
nummer int,
slutnummer int,
datum datetime,
publicerad datetime,
status TEXT,
titel TEXT,
subtitel TEXT,
html ntext,
toc ntext,
refcss TEXT,
url TEXT,
uppdaterad datetime,
storlek int,
source TEXT,
wn_expires datetime,
wn_cachekey TEXT,
wn_status TEXT,
wn_checksum TEXT,
wn_nid int,
wn_RawUrl TEXT,
wn_SourceID TEXT,
timestamp datetime,
rel_id TEXT,
klockslag TEXT,
grupp TEXT,
format TEXT,
intressent_id TEXT,
mottagare_id TEXT,
mottagare TEXT,
hangar_id int,
plats TEXT,
slutdatum datetime,
webbtvlive tinyint
);



CREATE TABLE organ (
id int,
kod TEXT,
namn TEXT,
typ TEXT,
status TEXT,
sortering int,
namn_en TEXT,
domän TEXT,
beskrivning TEXT
);



CREATE TABLE roll (
pk int,
kod TEXT,
namn TEXT,
sort int
);



CREATE TABLE riksmote (
pk int,
riksmote TEXT,
id TEXT,
start datetime,
slut datetime,
mandatperiod TEXT
);
