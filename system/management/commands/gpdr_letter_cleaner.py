from django.core.management.base import BaseCommand, CommandError
from system.models import *
import time, datetime
# import additional classes/modules as needed
# from myapp.models import Book

class Command(BaseCommand):
    help = 'GPDR Remove records older than 90 days'

    def gpdr_removal(self):
        older_than = datetime.datetime.now() - datetime.timedelta(days=90)
        LettersData = Letters.objects.filter(print_date__lte = older_than).delete()

        # TODO: Send email with the deleted count (LettersData contains it) to it, iemilov, aasenov
        # print (LettersData)

    def handle(self, *args, **options):
        self.gpdr_removal()
        print ('Done with GPDR removal!')
