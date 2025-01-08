import sys
import os

# Add the root directory to sys.path so that models can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import engine, User, Workout, Exercise, Nutrition, HealthMetric
from sqlalchemy.orm import sessionmaker
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
faker = Faker()

# Session setup
Session = sessionmaker(bind=engine)
session = Session()

# Clear existing data
session.query(User).delete()
session.query(Workout).delete()
session.query(Exercise).delete()
session.query(Nutrition).delete()
session.query(HealthMetric).delete()
session.commit()

# Generate users
new_users = [
    User(
        name=faker.name(),
        email=faker.unique.email(),
        age=random.randint(20, 60)
    ) for _ in range(100)
]
session.bulk_save_objects(new_users)
session.commit()

# Add related data for each user
for user in session.query(User).all():
    # Generate workouts with meaningful descriptions
    for _ in range(random.randint(1, 5)):
        workout_desc = random.choice([
            "Full Body Workout", "Cardio Day", "Strength Training", "Leg Day", "HIIT Session"
        ])
        workout = Workout(user=user, description=workout_desc)
        session.add(workout)
        
        # Generate exercises with meaningful names
        for _ in range(random.randint(1, 3)):
            exercise_name = random.choice([
                "Push-up", "Squat", "Deadlift", "Lunges", "Bench Press", "Pull-up", "Plank", "Burpees"
            ])
            session.add(
                Exercise(
                    workout=workout,
                    name=exercise_name,
                    sets=random.randint(1, 5),
                    reps=random.randint(8, 20),
                    weight=round(random.uniform(20, 100), 2)
                )
            )

    # Generate nutrition records with meaningful meal types and unique dates
    for _ in range(random.randint(1, 5)):
        nutrition_date = faker.date_this_year()
        meal_type = random.choice(["Breakfast", "Lunch", "Dinner", "Snack"])
        session.add(
            Nutrition(
                user=user,
                meal=meal_type,
                date=nutrition_date,
                calories=round(random.uniform(200, 700), 2),
                protein=round(random.uniform(10, 50), 2),
                carbs=round(random.uniform(20, 100), 2),
                fats=round(random.uniform(5, 30), 2)
            )
        )

    # Generate health metrics with unique dates and values
    for _ in range(random.randint(1, 5)):
        health_date = faker.date_this_year()
        session.add(
            HealthMetric(
                user=user,
                date=health_date,
                weight=round(random.uniform(50, 100), 2),
                heart_rate=random.randint(60, 100)
            )
        )

# Commit changes
session.commit()
session.close()


# import sys
# import os

# # Add the parent directory to sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from models.database import engine, User, Workout, Exercise, Nutrition, HealthMetric
# from sqlalchemy.orm import sessionmaker
# from faker import Faker
# import random
# from datetime import datetime


# # Add the parent directory to sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# # Initialize Faker
# faker = Faker()

# # Session setup
# Session = sessionmaker(bind=engine)
# session = Session()

# # Clear existing data
# session.query(User).delete()
# session.query(Workout).delete()
# session.query(Exercise).delete()
# session.query(Nutrition).delete()
# session.query(HealthMetric).delete()
# session.commit()

# # Generate users
# new_users = [
#     User(
#         name=faker.name(),
#         email=faker.unique.email(),
#         age=random.randint(20, 60)
#     ) for _ in range(100)
# ]
# session.bulk_save_objects(new_users)
# session.commit()

# # Add related data for each user
# for user in session.query(User).all():
#     # Generate workouts and exercises
#     for _ in range(random.randint(1, 5)):
#         workout = Workout(user=user, description=faker.sentence())
#         session.add(workout)
#         for _ in range(random.randint(1, 3)):
#             session.add(
#                 Exercise(
#                     workout=workout,
#                     name=faker.word(),
#                     sets=random.randint(1, 5),
#                     reps=random.randint(8, 20),
#                     weight=round(random.uniform(20, 100), 2)
#                 )
#             )

#     # Generate nutrition records
#     for _ in range(random.randint(1, 5)):
#         session.add(
#             Nutrition(
#                 user=user,
#                 meal=faker.word(),
#                 calories=round(random.uniform(200, 700), 2),
#                 protein=round(random.uniform(10, 50), 2),
#                 carbs=round(random.uniform(20, 100), 2),
#                 fats=round(random.uniform(5, 30), 2)
#             )
#         )

#     # Generate health metrics
#     for _ in range(random.randint(1, 5)):
#         session.add(
#             HealthMetric(
#                 user=user,
#                 weight=round(random.uniform(50, 100), 2),
#                 heart_rate=random.randint(60, 100)
#             )
#         )

# # Commit changes
# session.commit()
# session.close()
