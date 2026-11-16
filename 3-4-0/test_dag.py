from airflow.sdk import dag, task
from pendulum import datetime


@dag(
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["3-4-0", "test"],
)
def test_dag():
    @task
    def say_hello():
        return "hello"

    @task
    def shout(message: str):
        print(message.upper())

    shout(say_hello())


test_dag()

if __name__ == "__main__":
    test_dag().test()
