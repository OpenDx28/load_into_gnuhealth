from evaluations.create_evaluations import *



def save_delete(new_record):
    try:
        new_record.save()
    except Exception as e:
        new_record.delete()
        logging.error("<p>Error: %s</p>" % str(e))
        raise e


def get_random_pathology():
    diseases_list = get_deseases_csv("../deseases.csv")
    pathology = None
    while pathology is None:
        disease = random.choice(diseases_list)
        pathology = get_pathology(disease)
    return pathology

def create_random_confirmed_disease():
    new_patient = create_new_patient()
    logging.info("creating new onfirmed_disease...")
    Disease = Model.get("gnuhealth.patient.disease")
    new_disease = Disease()
    new_disease.name = new_patient
    new_disease.pathology = get_random_pathology()
    new_disease.lab_confirmed = True
    save_delete(new_disease)
    logging.info(
        f"created new confirmed disease {new_disease.id} "
        f"with disease {new_disease.pathology.name} "
        f"to {new_patient.rec_name} "
        f"with id: {new_patient.rec_name}"
        )

if __name__ == "__main__":
    setup_logging("../app.log")
    connect_to_gnu()
    for i in range(2):
        create_random_confirmed_disease()



