import logging

import requests
from bs4 import BeautifulSoup
from django.db import transaction

from apps.timetable.models import Course, Department, Lesson


def parsing(start=1, end=270):
    try:
        for i in range(start, end):
            logging.info(f"Parsing {i}")
            try:
                url = f"http://timetable.manas.edu.kg/department-printer/{i}"
                response = requests.get(url)
                html_content = response.text
                soup = BeautifulSoup(html_content, "html.parser")

                extract_timetable_data(soup)
            except Exception as e:
                logging.error(e)
    except Exception as e:
        logging.error(e)


def extract_timetable_data(soup):
    course_number, department_name = soup.find("h3").text.strip().split("- sınıf")

    department_name = department_name.strip()
    course_number = course_number.strip()

    department, created = Department.objects.get_or_create(name=department_name)

    course, created = Course.objects.get_or_create(department=department, course=int(course_number))

    table = soup.find("table")

    for row in table.find_all("tr")[1:]:

        cells = row.find_all("td")
        time = cells[0].text.strip()
        for i in range(1, 6):
            if cells[i].find_all("div") == []:
                create_data(course=course, day=i, time=time, lessons=cells[i].text.strip(), is_true=False)
            else:
                create_data(course=course, day=i, time=time, lessons=cells[i].find_all("div"))


@transaction.atomic
def create_data(course, day, time, lessons, is_true=True):
    if is_true:
        for i in lessons:
            data = [t.strip() for t in i.strings]
            Lesson.objects.create(course=course, day=day, time=time, name=data[0], teacher=data[1], room=data[2])
    else:
        Lesson.objects.create(course=course, day=day, time=time, name=lessons)
