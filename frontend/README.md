# Kinokava frontend

Vue 3 ja Vite'i kasutajaliides TA-24A-3 kinoprojektile. Rakendus kasutab
`<script setup>` süntaksiga Vue komponente ja Vue Routerit.

## Käivitamine

Paigalda sõltuvused ja käivita arendusserver:

```powershell
npm install
npm run dev
```

Vite käivitab rakenduse vaikimisi aadressil <http://localhost:5173>.
Backendi aadressi saab määrata keskkonnamuutujaga:

```powershell
$env:VITE_API_URL = "http://localhost:8000"
npm run dev
```

Kui `VITE_API_URL` puudub, kasutab rakendus sama backendi vaikeaadressi.
Docker Compose'i kaudu käivitamisel määratakse muutuja automaatselt.

## Kasulikud käsud

```powershell
npm run build
npm run preview
```

Rakenduse üldine arhitektuur, API otspunktid ja Docker Compose'i juhised on
projekti juurkausta failis [`documentation.md`](../documentation.md).
