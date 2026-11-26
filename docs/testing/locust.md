# Locust load testing

## Tool

Locust is an open-source Python API load-testing tool. It generates concurrent
virtual users and reports throughput, response latency, failures, and request
distribution through a web interface or CLI.

This test targets the cinema project's local Django API. It measures the
screening catalogue, screening details, movie details, and health endpoint.
The main bottleneck scenario is listing all screenings while many users open
the cinema schedule at the same time.

## Data

From the repository root, start the local stack and clear the demo data first:

```powershell
docker compose up --build -d
docker compose exec backend python manage.py seed_demo --clear --screenings 10000 --tickets 50000
```

The seeder creates 10,000 screenings and 50,000 booked-seat records distributed
across those screenings. It may take several minutes. Re-running without
`--clear` is rejected if cinema data already exists.

To use the small demo dataset instead:

```powershell
docker compose exec backend python manage.py seed_demo --clear
```

The Locust container is available at `http://localhost:8089`.

## Installation and start

Locust runs inside Docker, so Docker Desktop and Docker Compose are sufficient:

```powershell
docker compose up --build -d locust
```

Open `http://localhost:8089`, set host to `http://backend:8000`, and start a
test. The repository script is
[`tests/load/locustfile.py`](../../tests/load/locustfile.py).

CLI mode can run the same scenario without the browser:

```powershell
docker compose run --rm locust -f /mnt/locust/locustfile.py --host http://backend:8000 --users 100 --spawn-rate 10 --run-time 2m --headless
```

Stop services after testing:

```powershell
docker compose down
```

## Scenario

Each virtual user waits between 0.2 and 1.0 seconds and randomly performs:

- 8/14: `GET /api/cinema/screenings/` to load the screening schedule;
- 3/14: `GET /api/cinema/screenings/[id]/` to open one screening;
- 2/14: `GET /api/cinema/movies/[id]/` to open one movie;
- 1/14: `GET /api/cinema/` for a service health check.

The 100-user schedule-list test represents the premiere-opening load pattern:
many users load the same catalogue concurrently. The detail requests check
whether ORM joins and primary-key lookups remain stable under the same load.

## Measurements

Tests were run on the repository's local Docker Compose stack using the
PostgreSQL 16 container, 10,000 screening dataset, and 50,000 ticket dataset.

| Run | Users | Duration | Requests/s | p50 | p95 | Failures |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Screening catalogue baseline | 20 | 30 s | 2.11 | 1.3 s | 21 s | 0 |

The measured aggregate used 58 completed requests. The complete screening
catalogue was the slowest endpoint: its average and p95 latency were roughly
20 s under only 20 concurrent users, and the 100-user attempt reached degraded
latency early. Locust reported no HTTP failures in the 20-user run.

## Results and conclusion

The response latency and failure rate show that the screening list is not usable
under the target's current size and concurrency. The 20-user p95 was about
21 s, so the 100-user result would require a query and response-size
optimization before it can meet premiere traffic. The first checks are:

- the `(start_time, id)` index already used by `Screening`;
- Django queryset select/join count;
- whether an API pagination or date filter should be added;
- whether a short server-side cache is appropriate for the public schedule.

The detail endpoints should also be compared separately. A simple index cannot
fix serialisation or join work by itself, so SQL and result size should be
confirmed with `EXPLAIN ANALYZE` before changing schema or code.
