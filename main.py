import random

from case_creator import connect_to_gnu, setup_logging,get_diseases_csv, get_random_pathology, create_new_party_person,DISEASES_SCV
from case_creator.create_evaluations import create_evaluation
from case_creator.create_disease import create_confirmed_disease_case, create_random_healed_disease
from case_creator.create_death_certificate import create_random_death_certificate
from case_creator.create_admission import create_new_free_bed, create_admission, create_discharge
from case_creator.create_new_borns import create_delivery
from case_creator.create_surgeries import create_surgery

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


if __name__ == "__main__":

    setup_logging("app.log")

    # localmente por defecto
    connect_to_gnu()
    # connect_to_gnu(user = USER,
    #                password = PASSWORD,
    #                dbname = DB,
    #                hostname = HOSTNAME,
    #                port = PORT)

    push_all_diseases_cases()
    push_newborns()
    for _ in range(2):
        push_surgeries()
    # push_random_cases(2)
