from locust import HttpUser, task, between


class TestHttpUser(HttpUser):

    host = "https://reqres.in"
    wait_time = between(1, 3)

    def on_start(self):
        res = self.client.get("/")
        if res.status_code == 200:
            print(f"Connection to host {self.host} successful!")

    @task
    def get_users(self):
        response = self.client.get("/api/users?page=2")
        print(response.text)
        print(response.status_code)

    @task
    def create_user(self):
        response = self.client.post("/api/users", data='{"name":"morpheus","job":"leader"}')
        print(f"Status odpowiedzi na POST: {response.status_code}")

    def on_stop(self):
        print("Disconnected...")
