import logging
from proteus import ModelList
from case_creator import *


# TODO TIENE PINTA DE QUE TENGO QUE CREAR CAMAS


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


def create_new_bed():
    original_bed = Model.get('product.product')(393)
    copied_bed = duplicate_bed(original_bed)
    number = generate_random_code_6_digits()
    copied_bed.rec_name = f"[BED {number}] {number}"
    copied_bed.code = f"[BED {number}]"
    copied_bed.suffix_code = f"BED {number}"
    save_delete(copied_bed)
    logging.info(f"created bed with code ")
    return copied_bed


def create_occupied_bed():
    Bed = Model.get('gnuhealth.hospital.bed')
    bed_types = ['gatch',
                 'electric',
                 'stretcher',
                 'low',
                 'low_air_loss',
                 'circo_electric',
                 'clinitron']
    # todo creo que en este caso esto no afecta porque rodas scuestan lo mismo
    bed_type = random.choice(bed_types)
    new_bed = Bed()
    new_bed.bed_type = bed_type
    Bed_product = Model.get('product.product')
    all_beds_products = Bed_product.find([])
    new_bed.name = random.choice(all_beds_products)
    # TODO me saltará un error si no está libre
    new_bed.state = 'occupied'
    # solo existe el ward materminity ahora mismo
    new_bed.ward = Model.get('gnuhealth.hospital.ward')(1)
    new_bed.institution =Model.get('gnuhealth.institution')(1)
    new_bed.cost_prices = [Model.get('product.cost_price')(449)]
    save_delete(new_bed)
    logging.info(f"Created new bec type {new_bed.bed_type} with id: {new_bed.id}")
    return new_bed


if __name__ == "__main__":
    setup_logging("../app.log")

    connect_to_gnu()

    for _ in range(2):
        create_new_bed()
