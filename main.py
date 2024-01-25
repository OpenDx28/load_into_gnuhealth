import logging
import random

import pandas as pd

from case_creator import connect_to_gnu, setup_logging,get_diseases_csv, get_random_pathology, create_new_party_person,DISEASES_SCV
from case_creator.create_evaluations import create_evaluation
from case_creator.create_disease import create_confirmed_disease_case, create_random_healed_disease
from case_creator.create_death_certificate import create_random_death_certificate
from case_creator.create_admission import create_new_free_bed, create_admission, create_discharge
from case_creator.create_new_borns import create_delivery
from case_creator.create_surgeries import create_surgery
import os

USER = "admin"
DB = "ghs"
HOSTNAME = 'test1.medtec4susdev.org'
PORT = ""
PASSWORD = "opendx28"
ADMISSION_TYPE = [None, 'routine', 'maternity', 'elective', 'urgent', 'emergency']
N_FREE_BEDS = 10
DISEASES = get_diseases_csv(DISEASES_SCV)



def push_random_cases(n):
    cases = [
        create_evaluation,
        create_confirmed_disease_case,
        create_random_healed_disease,
        create_random_death_certificate,
        create_random_death_certificate,
        create_discharge,
        create_admission,
        create_delivery,
        create_surgery
    ]

    for _ in range(n):
        case = random.choice(cases)
        case()

def push_all_diseases_cases():
    for _ in range(N_FREE_BEDS):
        create_new_free_bed()
        create_new_free_bed(in_icu=True)

    for disease in DISEASES:
        create_evaluation(disease=disease)
        create_confirmed_disease_case(disease=disease)
        create_random_healed_disease(disease=disease)
        for authopsy in [True,False]:
            create_random_death_certificate(disease=disease,authopsy=authopsy)
        for admission in ADMISSION_TYPE:
            create_discharge()
            for icu in [True,False]:
                create_admission(admission_type= admission, in_icu=icu)


def push_newborns():
    for result in ['live_birth', 'abortion','stillbirth']:
        create_delivery(result = result)


def push_surgeries(): # todo test
    grades = [None,'grade1', 'grade2', 'grade3','grade3a', 'grade4', 'grade4a','grade4b', 'grade5']
    # grade = random.choice([None,'grade1', 'grade2', 'grade3','grade3a', 'grade4', 'grade4a','grade4b', 'grade5'])
    for grade in grades:
        create_surgery(clavien_dindo=grade)


def push_all_cases():
    push_all_diseases_cases()
    push_newborns()
    for _ in range(2):
        push_surgeries()



if __name__ == "__main__":

    setup_logging()
    connexions = pd.read_csv('connexions.csv')
    for _, connexion in connexions.iterrows():
        connect_to_gnu(user = connexion['user'],
                       password = connexion['password'],
                        dbname= connexion['dbname'],
                       hostname= connexion['hostname'],
                       port= str(connexion['port']))

        n_fake_cases = os.getenv('FAKE_CASES')
        if n_fake_cases:
            int(n_fake_cases)
        else:
            n_fake_cases = 5
        # push_all_cases()
        logging.info(f"creating {n_fake_cases} to {connexion['hostname']}:{connexion['port']}")
        push_random_cases(n_fake_cases)
