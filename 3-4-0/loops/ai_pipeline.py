import random
from datetime import datetime
from airflow.sdk import dag, task, task_group

# 1. Define the "until" condition (The Gate Task)
# This function runs after every loop iteration. Returning True breaks the loop.
def grade_is_accurate_enough(*, loop):
    """Stop looping if the essay score hits 90+."""
    current_score = loop.result
    print(f"Checking criteria... Current iteration score: {current_score}")
    
    # True means STOP looping. False means RUN ANOTHER ITERATION.
    return current_score >= 90


@dag(
    dag_id="dynamic_ai_refinement_loop",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
)
def ai_pipeline():

    # 2. Group the tasks that need to repeat dynamically
    @task_group()
    def refine_essay():
        
        @task
        def generate_or_edit_essay():
            print("LLM is editing/generating the essay based on feedback...")
            # Imagine real LLM generation happens here

        @task
        def score_essay():
            # In a real workflow, you'd pull the essay and evaluate it.
            # Here, we simulate a score that generally improves.
            score = random.randint(50, 100)
            print(f"Critic evaluated essay. Score: {score}")
            return score  # This return value becomes 'loop.result'

        # Set the dependency chain inside the group
        generate_or_edit_essay() >> score_essay()

    # 3. Apply the .loop() modifier to the Task Group
    # This requires max_iterations to guarantee it can't run forever.
    looped_refinement = refine_essay.loop(
        until=grade_is_accurate_enough, 
        max_iterations=5
    )

    @task
    def publish_essay():
        print("Success! The essay met quality standards and has been published.")

    # 4. Define overall DAG execution flow
    looped_refinement >> publish_essay()

# Instantiate the DAG
ai_pipeline()

