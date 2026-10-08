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

Praegu on realiseeritud üks kontroll-otspunkt:

```text
GET /api/cinema/
```

Vastus:

```json
{"app": "cinema", "status": "ok"}
```

Admini URL on `/admin/`, kuid eraldi autentimise, administraatori kasutaja
loomise ega domeeni CRUD-otspunktide rakendust projekt praegu ei sisalda.

### Frontend

Frontend on Vue 3 ja Vite'i algne rakendus. Käivituv vaade kasutab komponenti
`frontend/src/components/HelloWorld.vue`; kinode, filmide, seansside,
broneeringute ja maksete kasutajaliides tuleb veel ehitada.

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

## Arendusjärjekord

Soovituslik järgmine tööjärjekord:

1. lisada backendile filmide, kinode, saalide ja seansside lugemise API;
2. lisada kasutajate autentimine ning sisendandmete valideerimine;
3. rakendada broneerimise, istekohtade lukustamise ja maksete töövood;
4. lisada arvustuste API;
5. siduda Vue kasutajaliides backendiga ning lisada kasutusjuhud;
6. lisada iga uue kasutusjuhu juurde automaattestid.
