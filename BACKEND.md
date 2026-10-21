# Backendi keel, ORM-id ja raamistikud

## Valitud keel: Python

Valisime backendi keeleks Pythoni. Põhjused:

- Python on loetav ja lihtne õppida, nii et mõlemad arendajad saavad koodist aru.
- Pythonis on mitu küpset veebiraamistikku ja ORM-i, mis toetavad nii
  PostgreSQL-i kui MariaDB/MySQL-i. Kui peaksime andmebaasi vahetama, ei pea
  keelt vahetama.
- Andmete genereerimiseks on olemas Faker, millega tegime `seed_demo` käsu.

Meie andmebaas on PostgreSQL 16 (vt [`project.sql`](project.sql)). Kõik allpool
võrreldud variandid toetavad nii PostgreSQL-i kui MariaDB/MySQL-i.

## Variandid

### 1. Django + Django ORM

Django on "kõik ühes" raamistik: selles on olemas ORM, migratsioonid,
admin-paneel, kasutajate autentimine, vormide valideerimine ja testimise
tööriistad. Tabelid kirjeldatakse Pythoni klassidena (`models.py`) ja Django
genereerib nende põhjal migratsioonid.

**Plussid meie projekti jaoks**

- Migratsioonid on sisse ehitatud: `makemigrations` ja `migrate`. Kui lisame
  näiteks uudiste tabeli, piisab mudeli lisamisest.
- Kuna tegime SQL-i enne valmis, oli oluline, et ORM saaks olemasoleva
  skeemiga kohaneda. Django `db_table` ja `db_column` lubavad hoida Pythonis
  ingliskeelseid nimesid (`title`), aga andmebaasis meie eestikeelseid
  (`pealkiri`). Olemasolevast andmebaasist saab mudelid ka automaatselt sisse
  lugeda käsuga `inspectdb`.
- Piirangud, mida kino vajab (koht on seansil broneeritud ainult üks kord,
  seansi lõpp on pärast algust), saab kirjutada otse mudelisse
  (`UniqueConstraint`, `CheckConstraint`).
- Admin-paneel annab kohe võimaluse filme, seansse ja saale käsitsi lisada,
  ilma et peaksime selleks eraldi kasutajaliidest tegema.
- Dokumentatsioon on väga põhjalik ja kogukond suur, enamikule vigadele leiab
  vastuse.

**Miinused**

- Raamistik on suur ja sellel on oma kindel viis asjade tegemiseks. Alguses
  tuleb õppida, kuhu mis fail käib.
- JSON API jaoks on vaja lisaks Django REST Frameworki (või käsitsi
  `JsonResponse`), sest Django ise on mõeldud pigem HTML-lehtede jaoks.
- Migratsioonid eeldavad, et skeemi omanik on Django. Kui keegi muudab
  tabelit DataGripis käsitsi, lähevad mudelid ja andmebaas lahku.

### 2. FastAPI + SQLAlchemy + Alembic

FastAPI on kerge ja kiire API-raamistik. Andmebaasiga ise ei tegele, selle
jaoks kasutatakse SQLAlchemy ORM-i ja migratsioonideks Alembicut. Sisend- ja
väljundandmed kirjeldatakse Pydanticu mudelitega ning API dokumentatsioon
(Swagger) tekib automaatselt.

**Plussid meie projekti jaoks**

- Vue frontend vajab ainult JSON API-t ja FastAPI on just selleks tehtud.
  Automaatne Swaggeri leht teeb frontendi ja backendi koostöö lihtsamaks.
- SQLAlchemy on väga paindlik: keerulisemad päringud, näiteks "vabad kohad
  sellel seansil", saab kirjutada peaaegu nagu SQL-i.
- SQLAlchemy oskab olemasolevat andmebaasi sisse lugeda (automap või
  `sqlacodegen`), mis sobib, kui SQL on enne valmis.

**Miinused**

- Tuleb kokku panna kolm eraldi tööriista (FastAPI, SQLAlchemy, Alembic) ja
  seadistada need ise. Admin-paneeli, autentimist ega kasutajate haldust pole.
- SQLAlchemy õppimise lävi on kõrge, selles on kaks erinevat stiili (Core ja
  ORM) ning dokumentatsioon on mahukas.
- Alembic ei tuvasta kõiki muudatusi automaatselt, migratsioone tuleb
  rohkem käsitsi üle kontrollida.

### 3. Flask + Peewee

Flask on minimaalne raamistik, kus on ainult marsruudid (URL -> funktsioon).
Peewee on väike ja lihtne ORM, mille mudelid näevad välja sarnased Django
omadele.

**Plussid meie projekti jaoks**

- Väga väike ja kiire selgeks saada, sobib väikesele projektile.
- Peewee'l on tööriist `pwiz`, mis loeb olemasolevast andmebaasist mudelid
  sisse, nii et meie valmis SQL-ist saaks kohe koodi.
- Vähe "maagiat": on lihtne aru saada, mis päring andmebaasi läheb.

**Miinused**

- Peewee migratsioonid (`playhouse.migrate`) tuleb kirjutada käsitsi, ei ole
  automaatset `makemigrations` sarnast lahendust. Meie skeem muutub veel
  (uudised, istekohtade lukustamine), nii et see oleks palju lisatööd.
- Peewee kogukond on palju väiksem kui Djangol või SQLAlchemyl.
- Autentimise, valideerimise ja admin-paneeli peab ise juurde ehitama või
  eraldi lisadena otsima.

## Võrdlus

| | Django ORM | FastAPI + SQLAlchemy | Flask + Peewee |
| --- | --- | --- | --- |
| PostgreSQL / MariaDB | jah / jah | jah / jah | jah / jah |
| Olemasoleva DB sisselugemine | `inspectdb` | automap, `sqlacodegen` | `pwiz` |
| Migratsioonid | sisse ehitatud, automaatsed | Alembic, osaliselt automaatsed | käsitsi |
| Admin ja autentimine | olemas | pole | pole |
| Õppimise lävi | keskmine | kõrge | madal |
| Kogukond ja dokumentatsioon | väga suur | suur | väike |

## Valik: Django + Django ORM

Valisime Django, sest meie projektis on palju omavahel seotud tabeleid
(kinod, saalid, kohad, seansid, broneeringud, maksed) ja skeem muutub veel.
Selle juures on kõige suurem abi automaatsetest migratsioonidest, mis on
Djangos sisse ehitatud. Peewee puhul peaksime neid käsitsi kirjutama ja
SQLAlchemy puhul seadistama eraldi tööriista.

Kuna SQL-skeem oli enne valmis, oli oluline, et ORM ei sunniks tabeleid ümber
nimetama. Django `db_table` ja `db_column` lubasid meie eestikeelsed tabelid ja
veerud alles jätta.

Kinoprojektis on vaja ka kasutajaid, sisselogimist ja võimalust filme ja
seansse lisada. Django annab need kohe kaasa (admin-paneel, autentimine).
FastAPI oleks puhta API jaoks kergem ja kiirem, aga meie projekti suuruse
juures ei ole kiirus probleem ja puuduvate osade ise ehitamine võtaks rohkem
aega kui Django õppimine.

Praeguseks on mudelid ([`backend/cinema/models.py`](backend/cinema/models.py)),
migratsioonid ja demoandmete seeder Djangos tehtud. Järgmise sammuna lisame
API otspunktid.
