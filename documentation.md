# Backend: keel, ORM ja raamistik

**Stack:** Python + Django, Vue + Vite, PostgreSQL

## Keel: Python

- Loetav ja lihtne õppida
- Hea Postgresi tugi (`psycopg`)
- Frontend (Vue) on eraldi, suhtlus käib JSON API kaudu, seega keel ei pea sama olema

## Variandid

### A) Django + Django ORM + Django REST Framework (DRF)

**Plussid**
- Postgres on Djangos põhitoetatud
- `inspectdb` loeb olemasoleva andmebaasi mudeliteks (sobib, kuna `project.sql` on enne valmis)
- Migratsioonid ja adminpaneel on kaasas
- Postgresi võimalused (CHECK, JSONField, `ExclusionConstraint` ristuvate seansside vältimiseks)
- Suur kogukond ja palju materjali

**Miinused**
- Django on "kood enne" tööriist, `inspectdb` mudelid vajavad käsitsi puhastamist
- Tuleb valida: kas tabeleid haldab SQL-fail (`managed = False`) või Django migratsioonid
- DRF on omaette õppimine (serializer'id, viewset'id)

### B) Django + Django ORM + Django Ninja

**Plussid**
- Sama ORM ja `inspectdb` nagu A
- Lühem ja loetavam API kood (tüübivihjed)
- Automaatne API dokumentatsioon

**Miinused**
- Väiksem kogukond ja vähem õppematerjali kui DRF-il
- Tunnis ei käsitletud
- Filtreerimine ja lehekülgedeks jagamine tuleb rohkem käsitsi teha

### C) FastAPI + SQLAlchemy + Alembic

**Plussid**
- Täielik SQL-i kontroll, sobib keeruliste aruannete jaoks
- SQLAlchemy oskab olemasolevat andmebaasi sisse lugida (reflection)
- Kiire ja automaatne API dokumentatsioon

**Miinused**
- Autentimine, admin ja muu tuleb ise kokku panna
- Järsem õppimiskõver
- Ei kasuta Djangot, mis on minu valitud stack
- Projekti mahu jaoks liiga võimas

## Valik: Django + Django ORM + DRF

- Sobib minu stackiga, lisatööriistu pole vaja
- `inspectdb` lahendab SQL-first töövoo
- Adminpaneel, kasutajad ja migratsioonid on valmis, saan keskenduda kinoloogikale
- Hea dokumentatsioon ja kogukond
- Sobib projekti mahuga

<<<<<<< HEAD
**Mida arvestan:** pean otsustama, kas struktuuri haldab SQL-fail või Django, et need ei läheks lahku.

## Cinema rakenduse arendamise algus

Django rakendus `cinema` asub kaustas `backend/cinema` ja on registreeritud
projektis `config.settings`. Esimene kontroll-otsapunkt on:

```text
GET /api/cinema/
```

Kohalikus Docker-keskkonnas käivita backend nii:

```bash
docker compose up --build
```

Seejärel ava `http://localhost:8000/api/cinema/`. Eduka käivituse vastus on:

```json
{"app": "cinema", "status": "ok"}
```

## Andmemudel

Andmebaasi põhiskeem on kirjeldatud Django mudelites failis
`backend/cinema/models.py`. Mudelid kasutavad `Meta.db_table` ja `db_column`
väärtusi, et ühendada Pythonis loetavad nimed olemasolevate SQL-tabelite ja
-veergudega.

Praegu on kaetud järgmised domeeniobjektid:

- kasutajad (`User`)
- kinod, kinosaalid ja istekohad (`Cinema`, `CinemaHall`, `Seat`)
- filmid ja žanrid (`Movie`, `Genre`, `MovieGenre`)
- seansid (`Screening`)
- broneeringud ja broneeritud kohad (`Booking`, `BookedSeat`)
- maksed ja arvustused (`Payment`, `Review`)

Mudelitel on lisaks seostele ka andmebaasi piirangud: samas saalis ei saa
olla kahte sama rea ja numbri kombinatsiooniga kohta, üks istekoht saab olla
ühe seansi jooksul broneeritud ainult üks kord ning seansi lõpp peab olema
pärast algust.

Esialgne migratsioon asub failis
`backend/cinema/migrations/0001_initial.py`. Kui andmebaas luuakse Django
migratsioonide abil, käivita:

```bash
docker compose exec backend python manage.py migrate
```

Kui kasutad olemasoleva skeemi laadimiseks `project.sql` faili, ära loo sama
skeemi teist korda migratsiooniga. Sellisel juhul tuleb valida üks skeemi
haldaja: kas SQL-fail või Django migratsioonid. Pärast mudelite muutmist loo
uus migratsioon käsuga `makemigrations` ja rakenda see käsuga `migrate`.

Edasine soovituslik järjekord:

1. Loo andmebaasiühendus ja lae olemasolev `project.sql` PostgreSQL-i või
   otsusta kasutada Django esialgset migratsiooni.
2. Lisa esmalt filmide lugemise API, seejärel kinode, saalide ja seansside API.
3. Lisa broneerimise, maksete ja arvustuste kasutusjuhud.
4. Lisa iga uue kasutusjuhu juurde testid `cinema/tests.py` või eraldi
   `cinema/tests/` kausta.
=======
**Skeemi haldamine:** andmebaasi skeemi haldavad Django mudelid ja migratsioonid.
`project.sql` on algne skeemikirjeldus, kuid rakenduse käivitamisel seda ei
impordita ega kasutata skeemi uuendamiseks. Uued skeemimuudatused tuleb teha
Django mudelites ja salvestada migratsioonidena.
>>>>>>> f7a394a (Seeder and demodata Add and readme change)
