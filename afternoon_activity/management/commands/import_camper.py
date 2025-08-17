import pandas as pd
from django.core.management.base import BaseCommand
from afternoon_activity.models import Camper, SessionCabin

class Command(BaseCommand):
    help = 'Import campers from an Excel file'

    def handle(self, *args, **kwargs):
        # Load the Excel file
        df = pd.read_excel('/Users/joe/Desktop/Capstone/Afternoon-Activity/afternoon_activity/campers.xlsx')

        # Retrieve the SessionCabin instance for session 1, cabin 1
        

        # Iterate over the rows of the DataFrame and create Camper objects
        for index, row in df.iterrows():
            camper = Camper.objects.create(first_name=row['First_Name'], last_name=row['Last_Name'])
            session_cabin = SessionCabin.objects.get(session__session_number=row['Session'], cabin__cabin_number=row['Cabin'])
            camper.session_cabin.add(session_cabin)
            self.stdout.write('Added camper: ' + str(camper) + ' to ' + str(session_cabin))


        self.stdout.write(self.style.SUCCESS('Successfully imported campers'))
