import pandas as pd
import csv
from lists.models import School
from django.core.management.base import BaseCommand


tmp_data_escuelas=pd.read_csv('static/data/escuelas.csv',sep=',', encoding='iso-8859-1').fillna(" ")


class Command(BaseCommand):
    def handle(self, **options):
        escuelas = [
            School(
                name=row['escuela'],
                address=row['direccion'],
                address_reference=row['referencia'],
                provincia=row['provincia'],
                canton=row['canton'],
                parroquia=row['parroquia']
        )
            for _, row in tmp_data_escuelas.iterrows()
        ]

        School.objects.bulk_create(escuelas)