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

Frontend on Vue 3 ja Vite'i rakendus. Käivituv vaade on avaleht ning
navigatsioon on määratud komponendis
[`frontend/src/components/Navbar.vue`](frontend/src/components/Navbar.vue).
Kasutusel on järgmised marsruudid:

| Marsruut | Vaade | Hetkeseis |
| --- | --- | --- |
| `/` | avaleht | kuvab tulevaste seanssidega filme API andmete põhjal |
| `/KinoKava` | kinokava | vaate alus on olemas |
| `/filmid` | filmid | kuvab filme ning filtreerib žanri ja seansi tüübi järgi |
| `/kinod` | kinod | vaate alus on olemas |
| `/kasutaja` | kasutaja | vaate alus on olemas |
| `/zanrid` | žanrid | vaate alus on olemas |
| `/broneerimine` | broneerimine | vaate alus on olemas |

Filmi- ja avaleht kasutavad keskkonnamuutujat `VITE_API_URL`. Kui muutuja on
määramata, kasutatakse arenduses aadressi `http://localhost:8000`. Need vaated
laevad filmid ja seansid otspunktidest `/api/cinema/movies/` ning
`/api/cinema/screenings/`.

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

Testid kontrollivad praegu tervisekontrolli otspunkti. Frontendi tootmisjärgu
koostamiseks:

```powershell
docker compose exec frontend npm run build
```

Frontend'i arendusserveri saab käivitada ka ilma Dockerita:

```powershell
cd frontend
npm install
npm run dev
```

## Keskkonnamuutujad

Docker Compose loeb juurkausta `.env` failist järgmisi väärtusi:

| Muutuja | Vaikeväärtus | Kasutus |
| --- | --- | --- |
| `POSTGRES_DB` | `appdb` | PostgreSQL-i andmebaasi nimi |
| `POSTGRES_USER` | `Admin` | PostgreSQL-i kasutaja |
| `POSTGRES_PASSWORD` | `pro123` | PostgreSQL-i parool arenduskeskkonnas |
| `DJANGO_SECRET_KEY` | `dev-secret-key` | Django arenduskeskkonna salavõti |

Frontendi `VITE_API_URL` määrab backendi HTTP-aadressi. Arenduse vaikeväärtus
on `http://localhost:8000`; Docker Compose määrab sama väärtuse konteineris.
Tootmises tuleb kõik vaikeväärtused ja arenduse salavõti asendada sobivate
keskkonnapõhiste väärtustega.

## Arendusjärjekord

Soovituslik järgmine tööjärjekord:

1. lisada kasutajate autentimine ning sisendandmete valideerimine;
2. rakendada broneerimise, istekohtade lukustamise ja maksete töövood;
3. lisada arvustuste API;
4. siduda Vue kasutajaliides backendiga ning lisada kasutusjuhud;
5. lisada iga uue kasutusjuhu juurde automaattestid.
