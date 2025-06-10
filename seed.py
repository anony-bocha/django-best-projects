from faker import Faker
import random
from .models import Department, Student, StudentID
from django.db.models import Sum
fake = Faker()
from .models import *
def create_subject_marks(n):
    try:
        student_objs = Student.objects.all()
        for student in student_objs:
            subjects = Subject.objects.all()
            for subject in subjects:
                SubjectMarks.objects.create(
                    subject = subject,
                    student = student,
                    marks = random.randint(0 , 100)
                )
    except Exception as e:
        print(e)

def seed_db(n=10) -> None:
    try:
        departments_objs = Department.objects.all()
        if not departments_objs:
            print("No departments found. Please add departments before seeding students.")
            return
        
        for _ in range(n):
            department = random.choice(departments_objs)  # safer & cleaner
            student_id_str = f'STU-{random.randint(100, 999)}'
            student_name = fake.name()
            student_email = fake.email()
            student_age = random.randint(20, 30)
            student_address = fake.address()

            # Create StudentID object
            student_id_obj = StudentID.objects.create(student_id=student_id_str)

            # Create Student and link StudentID object
            student_obj = Student.objects.create(
                department=department,
                student_id=student_id_obj,  # <-- using object, not raw string
                student_name=student_name,
                student_email=student_email,
                student_age=student_age,
                student_address=student_address,
            )
    except Exception as e:
        print("Error while seeding:", e)


def generate_report_card():
    print('called')
    ranks = Student.objects.annotate(marks = Sum('studentmarks__marks')).order_by('marks' , '-student_age')
    i=1
    for rank in ranks:
        print(rank)
        ReportCard.objects.create(
            student = rank ,
            student_rank = i
        )
        i = i + 1