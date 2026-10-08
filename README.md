# TA-24A-3 kinoprojekt

Projekt kasutab Vue + Vite'i kasutajaliidest, Django backend'i ja PostgreSQL-i.
Django migratsioonid haldavad andmebaasi skeemi; `project.sql` ei käivitu
Dockeriga käivitamisel automaatselt.

## Eeldused

- Docker Desktop koos Docker Compose'iga
- Git

## Käivitamine

1. Ava terminalis projekti juurkaust.
2. Ehita ja käivita teenused:

   ```powershell
   docker compose up --build -d
   ```

3. Loo või uuenda andmebaasi tabelid Django migratsioonidega:

   ```powershell
   docker compose exec backend python manage.py migrate
   ```

4. Lisa Fakeriga genereeritud demoandmed:

   ```powershell
   docker compose exec backend python manage.py seed_demo
   ```

   Seeder loob muu hulgas 120 seanssi ja 120 broneeringut. Seoste terviklus
   tagatakse välisvõtmetega ning broneeritud istekoht valitakse sama seansi
   saalist. Seeder ei kirjuta olemasolevaid kinoandmeid üle. Nende
   kustutamiseks ja uuesti loomiseks kasuta teadlikult:

   ```powershell
   docker compose exec backend python manage.py seed_demo --clear
   ```

5. Ava teenused:

   - Frontend: <http://localhost:5173>
   - Django backend: <http://localhost:8000>
   - PostgreSQL: `localhost:5432`

Peata teenused käsuga `docker compose down`. Andmebaasi andmed jäävad
Docker volume'isse alles. Kohaliku andmebaasi ja demoandmete kustutamiseks
kasuta `docker compose down -v`.

## Migratsioonide muutmine

Kui muudad Django mudeleid, loo migratsioon ja rakenda see:

```powershell
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate
```

`kino` rakenduse lähtekood on kaustas [`backend/kino`](backend/kino).
