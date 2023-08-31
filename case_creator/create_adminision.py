import logging
from proteus import ModelList
from case_creator import *
from datetime import datetime
from dateutil.relativedelta import relativedelta


def duplicate_bed(original):
    Bed = Model.get('product.product')
    copied_bed = Bed()
    for field in Bed._fields:
        # Evita copiar campos que no deben ser duplicados directamente
        if field not in ['id', 'create_date',"code","rec_name","suffix_code","write_date","write_uid","cost_prices"]:
            if original._fields[field] ["readonly"] == False and original._fields[field] ["required"] == True:
                attribute = getattr(original, field)
                try:
                    setattr(copied_bed, field, attribute)
                except Exception as e:
                    logging.error("<p>Error: %s</p>" % str(e))
                    copied_bed.delete()
                    logging.info((f"new_record id: {copied_bed.id} deleted"))
                    raise e


    return copied_bed

def list_bed_product():
    l = list()
    all_products = Model.get('product.product').find([])
    for prod in all_products:
        if prod.is_bed == True:
            l.append(prod)
    return l

def list_free_bed():
    l = list()
    Bed = Model.get('gnuhealth.hospital.bed')
    beds = Bed.find([])
    for b in beds:
        if b.state == 'free':
            l.append(b)
    return l

def create_new_bed_as_product():
    '''
    Createa new bed in the hospital as product
    :return:
    '''
    original_bed = Model.get('product.product')(393)
    copied_bed = duplicate_bed(original_bed)
    number = generate_random_code_6_digits()
    copied_bed.rec_name = f"[BED {number}] {number}"
    copied_bed.code = f"[BED {number}]"
    copied_bed.suffix_code = f"BED {number}"
    copied_bed.is_bed = True
    save_delete(copied_bed)
    logging.info(f"created bed with code {copied_bed.code} ")
    return copied_bed

def create_new_free_bed(bed_product):
    '''
    Create a free bed in the hospital as place for a patient
    :return:
    '''
    Bed = Model.get('gnuhealth.hospital.bed')
    # # todo creo que en este caso esto no afecta porque rodas scuestan lo mismo
    # bed_type = random.choice(bed_types)
    new_bed = Bed()
    new_bed.name = bed_product
    new_bed.state = 'free'
    save_delete(new_bed)
    logging.info(f"created free with rec name {new_bed.rec_name} and id: {new_bed.id} ")
    return new_bed

def create_free_bed():
    new_bed = create_new_bed_as_product()
    bed_place = create_new_free_bed(new_bed)
    return bed_place




def create_occupied_bed():

    # TODO: en el sistema no aparecen las camas ocupadas.. parece que hay que crear un admision?
    free_beds = list_free_bed()
    new_bed = random.choice(free_beds)
    new_bed.state = 'occupied'
    save_delete(new_bed)
    logging.info(f"Bed {new_bed.rec_name} with id: {new_bed.id} occupated")
    return new_bed

def create_admission():
    """
    Creación de altas de casos previamente confirmados.
    :return:
    """


    from create_disease import create_random_confirmed_disease_case

    # create a open evaluation (a patient with a confirmed disease)
    disease = create_random_confirmed_disease_case()
    patient = disease.name
    bed = create_free_bed()
    time_hospitalization = random.randint(1, 90)
    start_date = datetime.now()
    end_date = start_date + relativedelta(days=time_hospitalization)
    inpatient = Model.get('gnuhealth.inpatient.registration')()
    inpatient.discharge_date = end_date
    inpatient.bed = bed
    bed.state = 'occupied'
    save_delete(bed)
    inpatient.admission_reason = disease.pathology
    inpatient.hospitalization_date = start_date
    inpatient.patient = patient
    inpatient.admission_type = 'urgent'
    save_delete(inpatient)
    # TODO need Confirm y Admission para que esté completp
    logging.info(f"create inpatient: {patient.name} with pathology {disease.pathology.name} date admisssion {inpatient.hospitalization_date} statimated discharge date {inpatient.discharge_date}")
    return inpatient

# if __name__ == "__main__":
#     setup_logging("../app.log")
#
#     connect_to_gnu()
#
#     for _ in range(20):
#         create_free_bed()
#
#
#     create_admission()

