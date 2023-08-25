from case_creator import connect_to_gnu,DISEASES_SCV
from proteus import config, Model
import re
import pandas as pd


def get_diseases_dhis_gnu():
    def create_diseases_dict(dhis_diseases):
        gnu_diseases = list()
        diseases = dict()
        for i in dhis_diseases:
            pathologies = Model.get('gnuhealth.pathology')
            records = pathologies.find([('name', 'ilike', f'%{i}%')])
            diseases[i] = records
        return diseases

    def get_as_df(diseases_dict):
        df = pd.DataFrame(columns=["dhis2_name", "gnu_health_name", "gnu_health_code"])
        n = 0
        for k, v in diseases_dict.items():
            for i in v:
                df.loc[n] = [k, i.name, i.code]
                n = n + 1
        return df

    dhis_list =  [
    'Acute Flacid Paralysis (confirmed cases VDPV)',
    'Cholera (Confirmed cases)',
    'Dengue Fever (Confirmed cases)',
    'Diarrhoea with blood (Shigella)  (Confirmed cases)',
    'Diptheria (Confirmed cases)',
    'Measles (Confirmed cases)',
    'Pertussis (Confirmed cases)',
    'Plague (Confirmed cases)',
    'Rabies  (Confirmed cases)',
    'Rubella (Confirmed cases)',
    'Viral hemorrhagic fever (confirmed cases)',
    'Yellow Fever (Confirmed cases)',
    'Acute Flacid Paralysis (confirmed cases WPV)']

    clean_list = [re.sub(r'\s*\([^)]*\)', '', item).strip() for item in dhis_list]
    diseases_dict = create_diseases_dict(dhis_list)
    df = get_as_df(diseases_dict)
    df.to_csv(DISEASES_SCV)

