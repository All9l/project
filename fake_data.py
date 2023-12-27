import requests
import random
from faker import Faker

fake = Faker()
api_url = 'http://127.0.0.1:800'

def create_group():
    group_data = {
        "Faculty": fake.word(),
        "GroupCode": fake.word(),
        "Course": random.randint(1, 5),
        "StudentsNum": random.randint(20, 50),
    }
    response = requests.post(f"{api_url}/groups/", json=group_data)
    if response.status_code == 201:
        print(f"Group created successfully: {response.json()}")
        return response.json()
    else:
        print(f"Failed to create group: {response.text}")
        return None

def create_subject():
    subject_data = {
        "Name": fake.word(),
        "Hours": random.randint(20, 100),
        "Department": fake.word(),
    }
    response = requests.post(f"{api_url}/subjects/", json=subject_data)
    if response.status_code == 201:
        print(f"Subject created successfully: {response.json()}")
        return response.json()
    else:
        print(f"Failed to create subject: {response.text}")
        return None

def create_session():
    groups = requests.get(f"{api_url}/groups/").json()
    subjects = requests.get(f"{api_url}/subjects/").json()

    if not groups or not subjects:
        print("No groups or subjects available to create a session.")
        return

    group = random.choice(groups)
    subject = random.choice(subjects)

    session_data = {
        "Professor": fake.name(),
        "DateSession": fake.date_this_year(),
        "ControlType": random.choice(["Exam", "Test", "Assignment"]),
        "GroupId": group["id"],
        "SubId": subject["id"],
    }
    response = requests.post(f"{api_url}/sessions/", json=session_data)
    if response.status_code == 201:
        print(f"Session created successfully: {response.json()}")
    else:
        print(f"Failed to create session: {response.text}")


created_groups = [create_group() for _ in range(100) if create_group()]
created_subjects = [create_subject() for _ in range(100) if create_subject()]
for _ in range(150):
    create_session()
