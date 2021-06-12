from locust import HttpUser, TaskSet, task, between, constant, SequentialTaskSet
import logging
import random

default_header = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}


class SequentialTasks(SequentialTaskSet):

    @task
    def first_task(self):
        self.client.get("/401")
        logging.info("first task - /401")

    @task
    def second_task(self):
        self.client.get("/402")
        logging.info("second task - /402")

    @task
    def third_task(self):
        self.client.get("/403")
        logging.info("third task - /403")

    def on_stop(self):
        logging.info("Finishing sequential")


class TestTasks(TaskSet):
    logging.info("Starting TestTasks")

    @task(2)
    def main_page(self):
        self.client.get("/")

    @task(5)
    def random_code(self):
        codes = [100, 101, 200, 201, 202, 203, 204, 226, 300, 304, 305, 400, 403, 404, 414, 422, 444, 500, 508, 511]
        code = random.choice(codes)
        response = self.client.get("/" + str(code))
        logging.info(f"Drawn code: {code}")
        # print(response.text)

    @task(3)
    class NestedTaskSet(TaskSet):
        wait_time = constant(1)

        def on_start(self):
            logging.info("Starting NestedTaskSet")

        @task(5)
        def status_code_401(self):
            response = self.client.get("/401")
            logging.info(f"status code dla '/401': {response.status_code}")

        @task(4)
        def status_501(self):
            self.client.get("/501")
            logging.info("/501")

        @task(1)
        def stop(self):
            self.interrupt()

        def on_stop(self):
            logging.info(f" {self.user.name}Leaving NestedTaskSet")

    @task
    def stop(self):
        self.interrupt()

    def on_stop(self):
        logging.info(f"{self.user.name} is leaving TestTasks")


class TestUser(HttpUser):
    wait_time = between(0.5, 2.5)
    # tasks = [TestTasks, SequentialTasks]
    tasks = {TestTasks: 1, SequentialTasks: 3}
    name = "TestUser"
    host = "https://httpstatusdogs.com"

    def on_start(self):
        self.client.get("/", headers=default_header)
