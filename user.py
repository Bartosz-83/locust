from locust import User, task, constant


class TestUser(User):

    wait_time = constant(1)
    weight = 1

    @task
    def first_task(self):
        print("Executing first task")

    @task
    def second_task(self):
        print("Executing second task")


class SecondUser(User):
    wait_time = constant(1)
    weight = 5

    @task
    def first_task(self):
        print("Second - Executing first task")

    @task
    def second_task(self):
        print("Second - Executing second task")
