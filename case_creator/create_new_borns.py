from case_creator import *
from datetime import datetime, timedelta
import random


def create_delivery(result = 'live_birth'):
    new_patient = create_new_patient(gender='f')
    logging.info("creating new evaluation...")
    Pregnancy = Model.get('gnuhealth.patient.pregnancy')
    new_pregnancy = Pregnancy()
    new_pregnancy.name = new_patient
    new_pregnancy.fetuses = 1
    new_pregnancy.gravida = random.choice(range(1,5))
    new_pregnancy.current_pregnancy = False
    new_pregnancy.pregnancy_end_result =  result
    new_pregnancy.pregnancy_end_date = generate_random_datetime((datetime.now()- timedelta(weeks=1)).strftime('%Y-%m-%d %H:%M:%S'),
                                                                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                                )
    new_pregnancy.lmp = generate_random_datetime((new_pregnancy.pregnancy_end_date - timedelta(weeks=42)).strftime('%Y-%m-%d %H:%M:%S'),
                                                 (new_pregnancy.pregnancy_end_date - timedelta(weeks=38)).strftime('%Y-%m-%d %H:%M:%S')
                                                 ) # ultima regla
    new_pregnancy.institution = Model.get('gnuhealth.institution')(1)
    new_pregnancy.healthprof = Model.get('gnuhealth.healthprofessional')(1)
    save_delete(new_pregnancy)
    new_perinatal = create_perinatal_info(new_pregnancy)
    new_pregnancy.perinatal.append(new_perinatal)
    save_delete(new_pregnancy)
    return new_pregnancy


def create_perinatal_info(pregnancy):
    Perinatal = Model.get('gnuhealth.perinatal')
    new_perinatal_info = Perinatal()
    new_perinatal_info.name = pregnancy
    new_perinatal_info.fetus_presentation = random.choice(['','cephalic','breech', 'shoulder'])
    new_perinatal_info.admission_code = str(generate_random_code_6_digits())
    new_perinatal_info.admission_date = pregnancy.pregnancy_end_date
    new_perinatal_info.start_labor_mode = random.choice(['v', 've', 'vf' , 'c'])
    save_delete(new_perinatal_info)
    return new_perinatal_info




# if __name__ == "__main__":
#     # setup_logging()
#     connect_to_gnu()
#     for result in ['live_birth', 'abortion','stillbirth']:
#         create_delivery(result = result)

















