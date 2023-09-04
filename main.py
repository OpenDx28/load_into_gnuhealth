from case_creator import connect_to_gnu, setup_logging,get_diseases_csv, get_random_pathology, create_new_party_person
from case_creator.create_evaluations import create_evaluation
from case_creator.create_disease import create_random_confirmed_disease_case, create_random_healed_disease
from case_creator.create_death_certificate import create_random_death_certificate
from case_creator.create_admission import create_new_free_bed, create_admission

USER = "admin"
DB = "ghs"
HOSTNAME = 'test1.medtec4susdev.org'
PORT = ""
PASSWORD = "opendx28"

if __name__ == "__main__":

    setup_logging("app.log")

    # localmente por defecto
    connect_to_gnu()
    # connect_to_gnu(user = USER,
    #                password = PASSWORD,
    #                dbname = DB,
    #                hostname = HOSTNAME,
    #                port = PORT)


    for i in range(1):
        create_evaluation()
        create_random_confirmed_disease_case()
        create_random_healed_disease()
        create_random_death_certificate()



    # Create some free beds en Admissions
    for _ in range(10):
        creatce_free_bed()

    for _ in range(3):
        create_new_free_bed()


# create_evaluation(disease="cholera")
