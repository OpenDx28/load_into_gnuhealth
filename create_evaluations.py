import json

from proteus import config, Model
import statistics
from datetime import date
from faker import Faker
import pandas as pd


def connect_to_gnu():
    user = 'admin'
    password = "opendx28"
    dbname = "ghs1"
    hostname = 'localhost'
    port = '8000'
    health_server = 'http://' + user + ':' + password + '@' + hostname + ':' + port + '/' + dbname + '/'
    conf = config.set_xmlrpc(health_server)
    return conf


def get_pathology(pathology_name):
    Pathology = Model.get('gnuhealth.pathology')
    pathology = Pathology.find([("name", "ilike", pathology_name)])[0]
    return pathology


def generate_random_datetime(start_date, end_date):
    import random
    from datetime import datetime, timedelta

    # Initialize Faker
    fake = Faker()
    # Convert start_date and end_date strings to datetime objects
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

    # Calculate the time difference in seconds
    time_difference = (end_datetime - start_datetime).total_seconds()

    # Generate a random time delta within the range
    random_seconds = random.randint(0, int(time_difference))
    random_timedelta = timedelta(seconds=random_seconds)

    # Calculate the random datetime within the range
    random_datetime = start_datetime + random_timedelta

    return random_datetime


def generate_random_endtime(start_datetime):
    import random
    from datetime import datetime, timedelta
    random_seconds = random.randint(200, int(2000))
    random_timedelta = timedelta(seconds=random_seconds)
    # Calculate the random datetime within the range
    random_datetime = start_datetime + random_timedelta
    return random_datetime


def create_new_patient():
    print("creating new party:...")
    fake = Faker()

    # create fake name
    name = fake.name()

    # create fake email
    email = fake.email()

    # create fake gender
    gender = fake.random_element(elements=('m', 'f'))

    dob = fake.date_of_birth()

    Party = Model.get('party.party')
    Patient = Model.get('gnuhealth.patient')

    # new party data
    new_party = Party()
    new_party.name = name
    new_party.email = email
    new_party.is_person = True
    new_party.gender = gender
    new_party.is_patient = True
    new_party.dob = dob
    # return new_party
    try:
        new_party.save()
    except Exception as e:
        new_party.delete
        print("<p>Error: %s</p>" % str(e))
    print(f"new party saved as:")
    print(f"new party id: {new_party.id}")
    print(f"new party name: {new_party.name}")

    # create new party

    new_patient = Patient()
    new_patient.name = new_party
    new_patient.gender = gender
    new_patient.save()
    try:
        new_patient.save()
    except Exception as e:
        new_party.delete
        print("<p>Error: %s</p>" % str(e))
        return None
    print(f"new patient saved as:")
    print(f"new patient id{new_patient.id}")
    print(f"new patient name{new_patient.name}")
    return new_patient


def create_evaluation(desease):
    # creo un nuevo paciente
    new_patient = create_new_patient()

    print("creating new evaluation...")
    # abro una nueva evaluation
    Evaluation = Model.get('gnuhealth.patient.evaluation')

    # open new evaluation
    new_evaluation = Evaluation()
    if new_evaluation.id > 0:
        raise ValueError(f"party is not a new registrer id: {new_evaluation.id}")

    # get Codordara, Cameron as Health Professional
    healthprof_1 = Model.get('gnuhealth.healthprofessional')(1)
    new_evaluation.healthprof = healthprof_1

    # asign patient
    new_evaluation.patient = new_patient

    # get pathology and asign it as desease
    eval_pathology = get_pathology(desease)
    new_evaluation.diagnosis = eval_pathology

    # create start and end evaluation time
    start_date = '2023-08-01 00:00:00'
    end_date = '2023-08-31 23:59:59'
    eval_start = generate_random_datetime(start_date, end_date)
    eval_endtime = generate_random_endtime(eval_start)
    new_evaluation.evaluation_start = eval_start
    new_evaluation.evaluation_endtime = eval_endtime

    # signature and dischage
    # TODO hacer un random con las posibilidades
    new_evaluation.state = "signed"
    new_evaluation.discharge_reason = 'home'
    # todo la evaluación no se cierra...
    try:
        new_evaluation.save()
    except Exception as e:
        new_evaluation.delete
        print("<p>Error: %s</p>" % str(e))
        raise e
    return new_patient, new_evaluation


if __name__ == "__main__":
    connect_to_gnu()
    patient, evaluation = create_evaluation("Yellow fever")
    print(evaluation.id)






