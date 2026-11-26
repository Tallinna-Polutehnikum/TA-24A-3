# PostgreSQL load testing with pgbench

## Tool and scenario

`pgbench` is PostgreSQL's built-in database benchmarking tool. It runs SQL
transactions concurrently and reports transactions per second, average
latency, and failed transactions. This test measures the database query used
to build the cinema screening catalogue: all screenings, joined to their movie,
hall, and cinema, sorted by start time and ID. The SQL is in
[`tests/pgbench/screenings.sql`](../../tests/pgbench/screenings.sql).

This is a database-only test, not an HTTP/API benchmark: it excludes Django
serialization and network traffic to browsers. The query returns the same
screening and related-cinema fields as the current API.

## Requirements and isolated test database

Docker Desktop with Docker Compose is required; pgbench runs in the PostgreSQL
16 container, so no host installation is needed. The test uses a separate
local database named `cinema_pgbench`, leaving the regular `appdb` database
untouched. Do not point the benchmark at a shared or cloud database.

Start the local database and backend:

```powershell
docker compose up -d db backend
```

Create the test database once, then apply migrations and seed it. The seeder's
`--tickets` option creates bookings; some are cancelled, so the resulting
booked-seat row count is lower than the booking count.

```powershell
docker compose exec -T db sh -c 'createdb -U "$POSTGRES_USER" cinema_pgbench'
docker compose exec -e POSTGRES_DB=cinema_pgbench backend python manage.py migrate --noinput
docker compose exec -e POSTGRES_DB=cinema_pgbench backend python manage.py seed_demo --screenings 10000 --tickets 50000
```

Refresh PostgreSQL statistics and inspect the query plan with
[`tests/pgbench/explain-screenings.sql`](../../tests/pgbench/explain-screenings.sql):

```powershell
docker compose run --rm --entrypoint psql pgbench -d cinema_pgbench -f /scripts/explain-screenings.sql
```

## Run the load test

Run 20 concurrent clients for 30 seconds, using four worker threads:

```powershell
docker compose run --rm pgbench -n -c 20 -j 4 -T 30 --log --log-prefix=/scripts/pgbench_run -f /scripts/screenings.sql
```

`-n` skips pgbench's built-in vacuum step because this custom workload does not
use pgbench's sample tables. The summary includes TPS, average latency, and
failed transactions. The per-transaction log's third column is latency in
microseconds. Calculate the nearest-rank p95 latency from those logs in
PowerShell:

```powershell
$latencies = @(Get-ChildItem tests\pgbench\pgbench_run.* | ForEach-Object { Get-Content $_.FullName } | ForEach-Object { [double](($_ -split '\s+')[2]) })
$sorted = @($latencies | Sort-Object)
$index = [Math]::Ceiling(0.95 * $sorted.Count) - 1
[pscustomobject]@{
    Transactions = $sorted.Count
    P95Ms = [Math]::Round($sorted[$index] / 1000, 2)
}
```

The logs are local test artifacts and can be removed after recording the
results:

```powershell
Remove-Item tests\pgbench\pgbench_run.*
```

## Results

Measured on 2026-11-26 on the local Docker Compose PostgreSQL 16.15 container
with 10,000 screenings, 50,000 bookings, and 33,400 booked-seat rows. The test
used the command above (20 clients, four threads, 30 seconds).

| Transactions | TPS | Average latency | P95 latency | Failed transactions |
| ---: | ---: | ---: | ---: | ---: |
| 8,502 | 283.44 | 70.56 ms | 107.48 ms | 0 (0%) |

`EXPLAIN (ANALYZE, BUFFERS)` returned all 10,000 rows in 14.66 ms on the first
run after statistics were refreshed (10.01 ms on a later repeat). Its plan
used sequential scans and hash joins, followed by an in-memory sort using
about 2,050 kB; all 114 reported buffer accesses were shared-buffer hits. The
existing `(algus_aeg, id)` index was not selected for this full-catalogue
query.

## Conclusion

The database executes the full joined query quickly in isolation, but the
concurrent pgbench average is 70.56 ms and its p95 is 107.48 ms. Every
transaction returns 10,000 rows, so this scenario repeatedly transfers a large
result set even though the query needs only a small in-memory sort. Adding an
index is not supported by this plan for an unfiltered full listing; the planner
prefers a sequential scan. The most useful next optimization is to filter
screenings by date and paginate the API response, then benchmark that
user-facing path separately. The existing start-time index should be
re-evaluated for such selective date queries.
