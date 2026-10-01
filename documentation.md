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

**Mida arvestan:** pean otsustama, kas struktuuri haldab SQL-fail või Django, et need ei läheks lahku.