from case_creator import connect_to_gnu, setup_logging,get_diseases_csv, get_random_pathology
from case_creator.create_evaluations import create_evaluation
from case_creator.create_disease import create_random_confirmed_disease_case, create_random_healed_disease
from case_creator.create_death_certificate import create_random_death_certificate

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


    for i in range(50):
        create_evaluation()
        create_random_confirmed_disease_case()
        create_random_healed_disease()
        create_random_death_certificate()


