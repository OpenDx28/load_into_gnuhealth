from case_creator import *

def create_evaluation(disease=None):
    # creo un nuevo paciente
    new_patient = create_new_patient()
    logging.info("creating new evaluation...")
    # abro una nueva evaluation
    Evaluation = Model.get('gnuhealth.patient.evaluation')

    # open new evaluation
    new_evaluation = Evaluation()

    # get Codordara, Cameron as Health Professional
    healthprof_1 = Model.get('gnuhealth.healthprofessional')(1)
    new_evaluation.healthprof = healthprof_1

    # asign patient
    new_evaluation.patient = new_patient
    new_evaluation.patient = new_patient

    new_evaluation.patient = new_patient
    new_evaluation.diagnosis = pathology(disease)


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
    new_evaluation.click('end_evaluation')
    save_delete(new_evaluation)
    logging.info(
        f"created new evaluation {new_evaluation.id} with diagnosis {new_evaluation.diagnosis.name} for patient {new_patient.rec_name} with id {new_patient.id}")
    return new_patient, new_evaluation


if __name__ == "__main__":
    setup_logging("../app.log")

    connect_to_gnu()

    for i in range(1):
        create_evaluation()






