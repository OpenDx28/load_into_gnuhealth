from case_creator import *
from proteus import config, Model



def create_random_death_certificate():
    new_party = create_new_party_person()
    Death = Model.get('gnuhealth.death_certificate')
    new_death = Death()
    # el certificado se lanza contra el party no el patient
    new_death.name = new_party
    new_death.cod = get_random_pathology()
    new_death.signed_by = Model.get('gnuhealth.healthprofessional')(1)
    new_death.country = Model.get('country.country')(208)
    new_death.country_subdivision = Model.get('country.subdivision')(1172)
    code = generate_random_code_6_digits()
    new_death.code = str(code)
    start_date = '2022-08-01 00:00:00'
    end_date = '2023-08-1 23:59:59'
    new_death.dod = generate_random_datetime(start_date,end_date)
    new_death.place_of_death = 'health_center'
    new_death.autopsy = False
    new_death.state = 'done'
    new_death.type_of_death = 'natural'
    new_death.du = None
    save_delete(new_death)
    logging.info(
        f"created new death_certificate {new_death.id} with diagnosis {new_death.cod.name} for party {new_party.name} with id {new_party.id}")
    return new_death


if __name__ == '__main__':
    setup_logging("../app.log")
    connect_to_gnu()
    for i in range(2):
        create_random_death_certificate()

    # TODO firmarlo??


