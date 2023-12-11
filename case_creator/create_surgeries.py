from case_creator import *
from datetime import datetime, timedelta
import random
from datetime import datetime, timedelta
from case_creator.create_disease import create_disease_case


def create_surgery(clavien_dindo = None):
    model = 'gnuhealth.surgery'
    Surgery = Model.get(model)
    new_surgery = Surgery()
    disease_case = create_disease_case()
    new_surgery.patient = disease_case.name
    new_surgery.pathology = disease_case.pathology
    new_surgery.institution = Model.get('gnuhealth.institution')(1)
    new_surgery.operating_room = Model.get('gnuhealth.hospital.or')(1)
    report_surgery_date_time = generate_random_datetime((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
                                                                datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    new_surgery.report_surgery_date = report_surgery_date_time.date()
    new_surgery.report_surgery_time = report_surgery_date_time.time()
    new_surgery.surgery_date = generate_random_datetime(report_surgery_date_time.strftime('%Y-%m-%d %H:%M:%S'),
                                                        (report_surgery_date_time + timedelta(weeks=1)).strftime('%Y-%m-%d %H:%M:%S'))
    new_surgery.surgery_end_date = generate_random_datetime(new_surgery.surgery_date.strftime('%Y-%m-%d %H:%M:%S'),
                                                            (new_surgery.surgery_date + timedelta(days=1)).strftime(
                                                                '%Y-%m-%d %H:%M:%S'))
    new_surgery.click('confirmed')
    new_surgery.click('start')
    new_surgery.surgery_end_date = generate_random_datetime(new_surgery.surgery_date.strftime('%Y-%m-%d %H:%M:%S'),
                                                            (new_surgery.surgery_date + timedelta(days=1)).strftime(
                                                                '%Y-%m-%d %H:%M:%S'))
    save_delete(new_surgery)
    new_surgery.click('done')
    if clavien_dindo:
        new_surgery.clavien_dindo = clavien_dindo
    else:
        new_surgery.clavien_dindo = random.choice(['grade1', 'grade2', 'grade3','grade3a', 'grade4', 'grade4a','grade4b', 'grade5'])
    new_surgery.surgery_end_date = generate_random_datetime(new_surgery.surgery_date.strftime('%Y-%m-%d %H:%M:%S'),
                                                            (new_surgery.surgery_date + timedelta(days=1)).strftime(
                                                                '%Y-%m-%d %H:%M:%S'))
    save_delete(new_surgery)
    new_surgery.click('signsurgery')

#
# if __name__ == "__main__":
#     connect_to_gnu()
#     create_surgery('grade5')




