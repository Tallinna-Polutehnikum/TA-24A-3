import random

from locust import HttpUser, between, task


class CinemaApiUser(HttpUser):
    wait_time = between(0.2, 1.0)

    def on_start(self):
        movies_response = self.client.get(
            "/api/cinema/movies/",
            name="GET /api/cinema/movies/",
        )
        screenings_response = self.client.get(
            "/api/cinema/screenings/",
            name="GET /api/cinema/screenings/",
        )

        movies = movies_response.json().get("results", []) if movies_response.ok else []
        screenings = (
            screenings_response.json().get("results", [])
            if screenings_response.ok
            else []
        )
        self.movie_ids = [movie["id"] for movie in movies]
        self.screening_ids = [screening["id"] for screening in screenings]

    @task(8)
    def list_screenings(self):
        self.client.get(
            "/api/cinema/screenings/",
            name="GET /api/cinema/screenings/",
        )

    @task(3)
    def screening_detail(self):
        if not self.screening_ids:
            self.list_screenings()
            return

        screening_id = random.choice(self.screening_ids)
        self.client.get(
            f"/api/cinema/screenings/{screening_id}/",
            name="GET /api/cinema/screenings/[id]/",
        )

    @task(2)
    def movie_detail(self):
        if not self.movie_ids:
            self.client.get(
                "/api/cinema/movies/",
                name="GET /api/cinema/movies/",
            )
            return

        movie_id = random.choice(self.movie_ids)
        self.client.get(
            f"/api/cinema/movies/{movie_id}/",
            name="GET /api/cinema/movies/[id]/",
        )

    @task(1)
    def health(self):
        self.client.get(
            "/api/cinema/",
            name="GET /api/cinema/",
        )
