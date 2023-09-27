from case_creator.create_evaluations import *




def create_disease_case(disease = None):
    new_patient = create_new_patient()
    logging.info("creating new Confirmed_disease...")
    Disease = Model.get("gnuhealth.patient.disease")
    new_disease = Disease()
    new_disease.name = new_patient
    new_disease.pathology = pathology(disease)
    end_date = datetime.now() - timedelta(weeks=1)
    start_date = end_date - timedelta(weeks=8)
    new_disease.diagnosed_date = generate_random_datetime(start_date.strftime('%Y-%m-%d %H:%M:%S'), end_date.strftime('%Y-%m-%d %H:%M:%S'))
    save_delete(new_disease)
    logging.info(
        f"created new confirmed disease {new_disease.id} "
        f"with disease {new_disease.pathology.name} "
        f"to {new_patient.rec_name} "
        f"with id: {new_patient.rec_name}"
    )
    return new_disease


def create_confirmed_disease_case(disease = None):
    new_disease = create_disease_case(disease)
    new_disease.lab_confirmed = True
    save_delete(new_disease)
    logging.info(
        f"created new confirmed disease {new_disease.id} "
        f"with disease {new_disease.pathology.name} "
        )
    return new_disease



def create_random_healed_disease(disease = None):
    new_disease = create_confirmed_disease_case(disease)
    start_date = new_disease.diagnosed_date
    end_date = datetime.now()
    new_disease.healed_date = generate_random_datetime(start_date.strftime('%Y-%m-%d %H:%M:%S'), end_date.strftime('%Y-%m-%d %H:%M:%S'))
    save_delete(new_disease)
    logging.info(f"created new healed disease {new_disease.id}"
        f"with disease {new_disease.pathology.name}"
                 )



if __name__ == "__main__":
    setup_logging("../app.log")
    connect_to_gnu()
    for i in range(5):
        create_confirmed_disease_case()
        create_random_healed_disease()



