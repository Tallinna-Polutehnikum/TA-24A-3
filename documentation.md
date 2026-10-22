# Tehniline dokumentatsioon

## Ülevaade

TA-24A-3 kinoprojekt koosneb kolmest Docker Compose'i teenusest:

| Teenus | Tehnoloogia | Port | Roll |
| --- | --- | --- | --- |
| `frontend` | Vue 3 + Vite, Node.js 20 | 5173 | kasutajaliidese arenduskonteiner |
| `backend` | Python 3.12 + Django 5 | 8000 | domeenimudelid ja HTTP API |
| `db` | PostgreSQL 16 | 5432 | andmete püsiv salvestamine |

Frontend kasutab Vite'i arendusserverit ja backend kasutab Django
arendusserverit. Andmebaasiühenduse seadistus tuleb keskkonnamuutujatest;
Docker Compose'is on vaikimisi andmebaas `appdb`, kasutaja `Admin` ja parool
`pro123`.

## Praegune funktsionaalsus

### Backend

Django projekt asub kaustas [`backend`](backend) ja rakendus kaustas
[`backend/cinema`](backend/cinema). Rakendus on registreeritud
`config.settings` seadistuses.

Tervisekontroll:

```text
GET /api/cinema/
```

Vastus:

```json
{"app": "cinema", "status": "ok"}
```

Avalikud kataloogi lugemis-otspunktid:

| Meetod | Tee | Vastus |
| --- | --- | --- |
| `GET` | `/api/cinema/movies/` | Filmide loend, sh žanrid |
| `GET` | `/api/cinema/movies/<id>/` | Üks film |
| `GET` | `/api/cinema/cinemas/` | Kinode loend |
| `GET` | `/api/cinema/cinemas/<id>/` | Üks kino |
| `GET` | `/api/cinema/halls/` | Saalide loend koos kino nimega |
| `GET` | `/api/cinema/halls/<id>/` | Üks saal |
| `GET` | `/api/cinema/screenings/` | Seansside loend koos filmi, saali ja kino nimedega |
| `GET` | `/api/cinema/screenings/<id>/` | Üks seanss |

Loendite JSON-kuju on `{"results": [...]}`. ID-ga detailpäring tagastab
objekti otse või tundmatu ID korral HTTP 404. Kataloogi otspunktid lubavad
GET- ja HEAD-päringuid ning tagastavad kirjutuspäringutele HTTP 405. Need ei
väljasta kasutaja-, broneeringu- ega makseandmeid.

Admini URL on `/admin/`, kuid eraldi autentimise, administraatori kasutaja
loomise ega kirjutamis-otspunktide rakendust projekt praegu ei sisalda.

### Frontend

Frontend on Vue 3 ja Vite'i rakendus, mille põhikomponent paigaldab ühise
navigatsiooni ja kuvab aktiivse marsruudi vaate. Navigatsioon asub failis
[`frontend/src/components/Navbar.vue`](frontend/src/components/Navbar.vue) ja
marsruudid failis
[`frontend/src/router/index.js`](frontend/src/router/index.js).

Praegu on olemas järgmised marsruudid ja vaated:

| Marsruut | Vaade | Hetkeseis |
| --- | --- | --- |
| `/` | avaleht | alustekst |
| `/KinoKava` | kinokava | alustekst |
| `/filmid` | filmid | alustekst |
| `/kinod` | kinod | alustekst |
| `/kasutaja` | kasutaja | alustekst |
| `/users/<id>` | kasutaja ID järgi | kuvab marsruudi ID-d |
| `/zanrid` | žanrid | alustekst |
| `/broneerimine` | broneerimine | alustekst |

Vaated ei tarbi praegu Django API-d. Kinode, filmide, seansside, kasutajate,
broneeringute ja maksete tegelik kasutajaliides ning autentimine tuleb veel
ehitada. Vana Vite'i näidisvaade `HelloWorld.vue` ei ole rakenduse aktiivne
vaade.

## Andmemudel

Andmebaasi domeenimudelid on failis
[`backend/cinema/models.py`](backend/cinema/models.py). Pythonis kasutatakse
ingliskeelseid väljanimetusi ja olemasoleva SQL-skeemiga sidumiseks
`Meta.db_table` ning `db_column` väärtusi.

Praegu on kirjeldatud järgmised objektid:

- `User` – kasutajad;
- `Cinema`, `CinemaHall`, `Seat` – kinod, saalid ja istekohad;
- `Movie`, `Genre`, `MovieGenre` – filmid ja žanrid;
- `Screening` – seansid;
- `Booking`, `BookedSeat` – broneeringud ja broneeritud kohad;
- `Payment` – maksed;
- `Review` – arvustused.

Olulisemad andmebaasipiirangud:

- istekoht on saalis rea ja numbri kombinatsiooni järgi kordumatu;
- filmi ja žanri seos on kordumatu;
- üks istekoht saab sama seansi jooksul olla broneeritud ainult üks kord;
- seansi lõppaeg peab olema algusajast hilisem;
- arvustuse hinne on vahemikus 1–5.

## Skeemi haldamine ja migratsioonid

Skeemi haldavad Django migratsioonid. Esialgne migratsioon on
[`backend/cinema/migrations/0001_initial.py`](backend/cinema/migrations/0001_initial.py)
ja telefoni välja täpsustus on
[`backend/cinema/migrations/0002_alter_user_phone_number.py`](backend/cinema/migrations/0002_alter_user_phone_number.py).

Käivita olemasolevate migratsioonide rakendamiseks:

```powershell
docker compose exec backend python manage.py migrate
```

Mudelite muutmisel loo uus migratsioon ja rakenda see:

```powershell
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate
```

Juurkaustas olevat `project.sql` faili Docker Compose'i käivitamisel
automaatselt ei laadita. Seda ei tohi kasutada sama skeemi paralleelse
haldajaena koos Django migratsioonidega; projekti praegune skeemiomanik on
Django.

## Demoandmed

Kohandatud management-käsk
[`backend/cinema/management/commands/seed_demo.py`](backend/cinema/management/commands/seed_demo.py)
kasutab Fakerit ja fikseeritud juhuarvu seemneid, et genereerida korratavad
andmed.

```powershell
docker compose exec backend python manage.py seed_demo
```

Käsk katkestab töö, kui andmebaasis on juba kinoandmeid. Olemasolevate
andmete kustutamiseks ja demoandmete uuesti loomiseks tuleb `--clear` lisada
teadlikult:

```powershell
docker compose exec backend python manage.py seed_demo --clear
```

Seeder loob 40 kasutajat, 3 kino, 9 saali, 864 istekohta, 20 filmi,
10 žanri, 120 seanssi, 120 broneeringut, 120 makset ja 60 arvustust.

## Testimine ja ehitamine

Backendi testid:

```powershell
docker compose exec backend python manage.py test
```

Testid kontrollivad tervisekontrolli ja kataloogi otspunkte, sealhulgas loendi-
ja detailpäringuid ning kirjutamispäringute tagasilükkamist. Frontendi
tootmisjärgu koostamiseks:

```powershell
docker compose exec frontend npm run build
```

## Arendusjärjekord

Soovituslik järgmine tööjärjekord:

1. siduda olemasolevad Vue vaated kataloogi API-ga;
2. ehitada filmide, kinode ja seansside tegelikud kataloogivaated;
3. lisada kasutajate autentimine ning sisendandmete valideerimine;
4. rakendada broneerimise, istekohtade lukustamise ja maksete töövood;
5. lisada arvustuste API ja kasutajaliides;
6. lisada iga uue kasutusjuhu juurde automaattestid.
