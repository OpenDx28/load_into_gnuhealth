import logging
from proteus import ModelList
from case_creator import *
from datetime import datetime
from dateutil.relativedelta import relativedelta


def create_UCI():
    '''
    create a ward called UCI
    :return: a 'gnuhealth.hospital.ward' model
    '''
    def create_UCI_unit():
        new_unit = Model.get('gnuhealth.hospital.unit')()
        new_unit.name = "UCI"
        new_unit.institution = Model.get('gnuhealth.institution')(1)
        new_unit.save()
        return new_unit
    uci_unit = create_UCI_unit()
    new_ward = Model.get('gnuhealth.hospital.ward')()
    new_ward.name = "UCI"
    new_ward.unit = uci_unit
    new_ward.floor = "2"
    save_delete(new_ward)
    return new_ward
def duplicate_bed(original):
    '''
    Copy a bed product to create a new one
    :param original: a bed in model 'product.product'
    :return: a bed in model 'product.product'
    '''
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
    '''
    Make a list of all beds (as product)
    :return: a list of Models : 'product.product'
    '''
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



def create_new_free_bed():
    '''
    Create a free bed in the hospital as place for a patient
    :return:
    '''

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

    bed_product = create_new_bed_as_product()
    Bed = Model.get('gnuhealth.hospital.bed')
    # # todo creo que en este caso esto no afecta porque rodas scuestan lo mismo
    # bed_type = random.choice(bed_types)
    new_bed = Bed()
    new_bed.name = bed_product
    new_bed.state = 'free'
    save_delete(new_bed)
    logging.info(f"created free with rec name {new_bed.rec_name} and id: {new_bed.id} ")
    return new_bed




def create_occupied_bed():
    '''
    Choose a  free bed ramdomly a change ir state to ocuppied
    :return: model gnuhealth.hospital.bed
    '''
    # TODO not sure if this is woking
    free_beds = list_free_bed()
    new_bed = random.choice(free_beds)
    new_bed.state = 'occupied'
    save_delete(new_bed)
    logging.info(f"Bed {new_bed.rec_name} with id: {new_bed.id} occupated")
    return new_bed

def create_admission(admission_type = 'urgent',in_ward = False,):
    """
    Creación de altas de casos previamente confirmados.
    :return:
    """
    # create a open evaluation (a patient with a confirmed disease)
    from case_creator.create_disease import create_random_confirmed_disease_case
    disease = create_random_confirmed_disease_case()
    patient = disease.name
    bed = create_new_free_bed()
    time_hospitalization = random.randint(1, 90)
    start_date = datetime.now()
    end_date = start_date + relativedelta(days=time_hospitalization)
    inpatient = Model.get('gnuhealth.inpatient.registration')()
    inpatient.discharge_date = end_date
    inpatient.bed = bed
    save_delete(bed)
    inpatient.admission_reason = disease.pathology
    inpatient.hospitalization_date = start_date
    inpatient.patient = patient
    if admission_type:
        inpatient.admission_type = 'urgent'
    else:
        tmp = inpatient._fields["admission_type"]["selection"]
        admission_type = [item[0] for item in tmp]
        inpatient.admission_type = random.choice(admission_type)
    # admission_type = fields.Selection([
    #     (None, ''),
    #     ('routine', 'Routine'),
    #     ('maternity', 'Maternity'),
    #     ('elective', 'Elective'),
    #     ('urgent', 'Urgent'),
    #     ('emergency', 'Emergency'),
    if in_ward:
        inpatient.icu = in_ward
    inpatient.click('admission') # TODO el paciente no pasa a admission
    save_delete(inpatient)
    # TODO need Confirm y Admission para que esté completp
    logging.info(f"create inpatient: {patient.name} with pathology {disease.pathology.name} date admisssion {inpatient.hospitalization_date} statimated discharge date {inpatient.discharge_date}")
    return inpatient

def create_discharge(disease = None, reason = None):
    # reasons:
    inpatient = create_admission(disease)
    inpatient.discharge_dx = inpatient.admission_reason
    if reason:
        inpatient.discharge_reason = reason
    else:
        tmp = inpatient._fields["discharge_reason"]["selection"]
        discharge_selection = [item[0] for item in tmp]
        inpatient.discharge_reason = random.choice(discharge_selection)
    save_delete(inpatient)
    logging.info(f"inpatient {inpatient.patient.name} discharged for {inpatient.discharge_reason} after {inpatient.discharge_dx}")
    return inpatient

if __name__ == "__main__":
    setup_logging("../app.log")

    connect_to_gnu()
    #
    # for _ in range(20):
    #     create_free_bed()


    # create_admission()
    create_admission(in_ward=True)
    # create_discharge()

