from case_creator.create_evaluations import *




def create_random_disease_case():
    new_patient = create_new_patient()
    logging.info("creating new Confirmed_disease...")
    Disease = Model.get("gnuhealth.patient.disease")
    new_disease = Disease()
    new_disease.name = new_patient
    new_disease.pathology = get_random_pathology()
    save_delete(new_disease)
    logging.info(
        f"created new confirmed disease {new_disease.id} "
        f"with disease {new_disease.pathology.name} "
        f"to {new_patient.rec_name} "
        f"with id: {new_patient.rec_name}"
    )
    return new_disease


def create_random_confirmed_disease_case():
    new_disease = create_random_disease_case()
    new_disease.lab_confirmed = True
    save_delete(new_disease)
    logging.info(
        f"created new confirmed disease {new_disease.id} "
        f"with disease {new_disease.pathology.name} "
        )
    return new_disease



def create_random_healed_disease():
    new_disease = create_random_confirmed_disease_case()
    start_date = '2022-08-01 00:00:00'
    end_date = '2023-08-1 23:59:59'
    new_disease.healed_date = generate_random_datetime(start_date,end_date)
    save_delete(new_disease)
    logging.info(f"created new healed disease {new_disease.id}"
        f"with disease {new_disease.pathology.name}"
                 )



if __name__ == "__main__":
    setup_logging("../app.log")
    connect_to_gnu()
    for i in range(2):
        create_random_confirmed_disease_case()
        create_random_healed_disease()



