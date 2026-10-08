# TA-24A-3 kinoprojekt

Kinoprojekti tehniline alus kasutab Vue 3 ja Vite'i kasutajaliidest, Django
backend'i ning PostgreSQL-i andmebaasi. Kõik kolm teenust on kirjeldatud failis
`docker-compose.yml`.

## Projekti hetkeseis

Praeguseks on olemas:

- Docker Compose'i arenduskeskkond PostgreSQL-i, Django ja Vue jaoks;
- Django `cinema` rakendus ning PostgreSQL-iga ühendatud mudelid;
- Django migratsioonid andmebaasi skeemi loomiseks ja muutmiseks;
- tervisekontrolli otspunkt `GET /api/cinema/`;
- `seed_demo` käsk seotud näidisandmete loomiseks;
- esialgne Vue/Vite'i kasutajaliides.

Kasutajaliideses ei ole veel kinokataloogi, autentimist, broneerimist ega
maksete töövoogu. Backendis on praegu lisaks mudelitele realiseeritud ainult
tervisekontrolli otspunkt.

## Tehnoloogiad

- **Frontend:** Vue 3, Vite, Node.js 20
- **Backend:** Python 3.12, Django 5
- **Andmebaas:** PostgreSQL 16
- **Arenduskeskkond:** Docker Compose

## Eeldused

- Docker Desktop koos Docker Compose'iga
- Git

## Käivitamine

Käivita käsud projekti juurkaustast:

```powershell
docker compose up --build -d
docker compose exec backend python manage.py migrate
```

Teenused on seejärel kättesaadavad:

- frontend: <http://localhost:5173>
- backend: <http://localhost:8000>
- tervisekontroll: <http://localhost:8000/api/cinema/>
- PostgreSQL: `localhost:5432`

Tervisekontrolli õnnestunud vastus on:

```json
{"app": "cinema", "status": "ok"}
```

Demoandmete loomiseks käivita:

```powershell
docker compose exec backend python manage.py seed_demo
```

Seeder loob fikseeritud algväärtusega seotud andmed: 40 kasutajat, 3 kino,
9 saali, 864 istekohta, 20 filmi, 10 žanri, 120 seanssi, 120 broneeringut,
120 makset ja 60 arvustust. Olemasolevaid kinoandmeid vaikimisi üle ei
kirjutata. Andmete teadlikuks kustutamiseks ja uuesti loomiseks kasuta:

```powershell
docker compose exec backend python manage.py seed_demo --clear
```

Peata teenused käsuga:

```powershell
docker compose down
```

Konteinerite peatamisel jäävad PostgreSQL-i andmed Docker volume'isse alles.
Nii konteinerite kui ka andmebaasiandmete kustutamiseks kasuta ainult siis,
kui see on soovitud:

```powershell
docker compose down -v
```

## Arendus

Kui muudad Django mudeleid, loo ja rakenda migratsioon:

```powershell
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate
```

Backendi testide käivitamine:

```powershell
docker compose exec backend python manage.py test
```

Frontendist tootmisversiooni koostamine:

```powershell
docker compose exec frontend npm run build
```

Täiendav tehniline kirjeldus, andmemudel ja arendusplaan on failis
[`documentation.md`](documentation.md).

## Git workflow 

Kasutame töövoogu, kus `main` sisaldab alati viimast stabiilset versiooni.
Mõlemad arendajad teevad oma ülesanded eraldi branch'is ning muudatused
jõuavad `main`-i Pull Request'i kaudu.

### Branchide põhimõte

Ära tee otse `main`-i commit'e. Iga ülesanne või parandus saab oma branch'i:

```text
main
├── feature/user-login
├── feature/movie-page
├── fix/mobile-layout
└── docs/update-readme
```

Branchi nimekujud:

- `feature/<ülesanne>` – uus funktsionaalsus;
- `fix/<probleem>` – vea parandus;
- `refactor/<teema>` – koodi ümberkorraldamine ilma käitumist muutmata;
- `docs/<teema>` – dokumentatsiooni muudatus.

### Uue ülesande alustamine

Alusta alati värske `main`-i pealt:

```powershell
git switch main
git pull origin main
git switch -c feature/my-task
```

Üks branch peaks käsitlema ühte selgelt piiritletud ülesannet. Kui kaks
arendajat töötavad sama suure funktsionaalsuse kallal, jaga see võimalusel
eraldi ülesanneteks ja branch'ideks, näiteks `feature/login-ui` ja
`feature/login-api`. See vähendab merge-konflikte.

### Commitimise reeglid

Commit olgu väike ja sisaldagu ühte loogilist muudatust. Väldi commit'e nagu
`update`, `changes` või `finished everything`.

Soovitatav vorm on:

```text
<tüüp>: <lühike kirjeldus>
```

Näited:

```text
feat: add login form
fix: show booking validation error
refactor: simplify movie query
test: add booking tests
docs: update development workflow
```

Töö käigus:

```powershell
git status
git add <muudetud-failid>
git commit -m "feat: add movie filtering"
git push -u origin feature/my-task
```

Ära lisa ühte commit'i sõltumatuid muudatusi. Enne commitimist kontrolli,
et lisad ainult selle ülesandega seotud failid.

### `main`-i muudatuste sünkroonimine

Kui teine arendaja on oma Pull Request'i `main`-i merge'inud, uuenda enda
branch'i enne töö jätkamist:

```powershell
git switch main
git pull origin main
git switch feature/my-task
git rebase main
git push --force-with-lease origin feature/my-task
```

`rebase` sobib branch'i puhul, mida kasutad ainult sina. Kui branch'i kasutab
mitu inimest, kasuta selle asemel merge'i:

```powershell
git switch feature/my-task
git merge main
git push origin feature/my-task
```

Konflikti korral lahenda konflikt, testi projekt üle ning lõpeta rebase või
merge vastava Git'i juhise järgi. Ära kasuta tavalist `--force` käsku, sest
see võib teise arendaja commit'id kustutada.

### Pull Request'i protsess

Kui ülesanne on valmis:

```powershell
git push -u origin feature/my-task
```

Ava GitHubis Pull Request kujul:

```text
feature/my-task -> main
```

Pull Request'is kirjelda:

- mida muudeti;
- kuidas muudatust testida;
- millised piirangud või lahtised küsimused on teada;
- vajadusel lisa ekraanipildid.

Teine arendaja vaatab koodi üle, testib muudatust ja kontrollib, et
olemasolev funktsionaalsus ei ole katki. Pärast review'd ja edukat testimist
merge'itakse Pull Request `main`-i. `main`-i otse pushimine peaks olema
keelatud.

Enne Pull Request'i kontrolli vähemalt:

```powershell
docker compose exec backend python manage.py test
docker compose exec frontend npm run build
```

### Tööpäeva lõpp ja branch'i koristamine

Pärast Pull Request'i merge'imist uuenda kohalikku `main`-i ja kustuta
mittevajalik kohalik branch:

```powershell
git switch main
git pull origin main
git branch -d feature/my-task
```

Nii jäävad branchid lühiajaliseks, `main` püsib ülevaatlik ja mõlemad
arendajad alustavad järgmisi ülesandeid samast lähtekohast.
