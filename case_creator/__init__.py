import logging
from proteus import config, Model
import pandas as pd
from faker import Faker
import random
import os

SCRIPT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DISEASES_SCV = f"/{SCRIPT_DIRECTORY}/diseases.csv"


def setup_logging(log_filename, log_level=logging.INFO):
    """
    Set up basic logging configuration.

    Parameters:
    - log_filename (str): The name of the file to log messages to.
    - log_level: The root logger level (default is logging.INFO).
    """
    # Set up the basic configuration
    logging.basicConfig(filename=log_filename,
                        level=log_level,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def connect_to_gnu(user = 'admin',
                   password = 'opendx28',
                   dbname = 'ghs',
                   hostname = 'localhost',
                   port = '8001'):

    health_server = 'http://' + user + ':' + password + '@' + hostname + ':' + port + '/' + dbname + '/'
    logging.info(f"trying to connect to {health_server}")
    conf = config.set_xmlrpc(health_server)
    logging.info(f"connected to conf")
    return conf

def get_last_record(ModelName):
    MyModel = Model.get(ModelName)
    last = MyModel.find([], order=[("id", "DESC")], limit=1)
    return last[0]

def print_record_fields(record):
    for field_name, field in record._fields.items():
        value = getattr(record, field_name)
        # Printing basic information about each field and its value
        print(f"{field_name} ({type(field).__name__}): {value}")

def save_delete(new_record):
    try:
        new_record.save()
    except Exception as e:
        logging.error("<p>Error: %s</p>" % str(e))
        new_record.delete()
        logging.info((f"new_record {new_record.rec_name} id: {new_record.id} deleted"))
        raise e


def get_diseases_csv(file):
    df = pd.read_csv(file)
    return df.loc[:,"gnu_health_name" ].to_list()


def get_pathology(pathology_name):
    Pathology = Model.get('gnuhealth.pathology')
    pathology = Pathology.find([("name", "ilike", pathology_name)])
    if len(pathology) > 0:
        pathology = pathology[0]
        return pathology
    else:
        logging.info(f"non pathology named: {pathology_name}")
        return None


def get_random_pathology():

    diseases_list = get_diseases_csv(DISEASES_SCV)
    pathology = None
    while pathology is None:
        disease = random.choice(diseases_list)
        pathology = get_pathology(disease)
    return pathology

def pathology(disease = None):
    if not disease:
        pathology = get_random_pathology()
    else:
        pathology = get_pathology(disease)
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


def generate_random_code_6_digits():
    return random.randint(100000, 999999)

def create_new_party_person():
    logging.info("creating new party as person ")
    fake = Faker()

    # create fake name
    name = fake.name()

    # create fake email
    email = fake.email()

    # create fake gender
    gender = fake.random_element(elements=('m', 'f'))

    dob = fake.date_of_birth()

    Party = Model.get('party.party')
    # new party data
    new_party = Party()
    new_party.name = name
    new_party.email = email
    new_party.is_person = True
    new_party.gender = gender
    new_party.is_patient = True
    new_party.dob = dob
    save_delete(new_party)
    logging.info(f"new party saved as:")
    logging.info(f"new party id: {new_party.id}")
    logging.info(f"new party name: {new_party.name}")
    return new_party


def create_new_patient():
    logging.info("creating new party:...")

    Patient = Model.get('gnuhealth.patient')
    # create new party
    new_party = create_new_party_person()
    new_patient = Patient()
    new_patient.name = create_new_party_person()
    new_patient.gender = new_party.gender
    new_patient.save()
    save_delete(new_patient)
    logging.info(f"new patient saved as:")
    logging.info(f"new patient id{new_patient.id}")
    logging.info(f"new patient name{new_patient.name}")
    return new_patient


def create_new_doctor():
    # new party data
    new_doctor = create_new_party_person()
    new_doctor.is_healthprof = True
    # TODO HAY QUE HACER MÁS COSAS
    save_delete(new_doctor)
    return new_doctor
