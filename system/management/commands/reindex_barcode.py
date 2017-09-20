from django.core.management.base import BaseCommand, CommandError
from system.models import *
import time
# import additional classes/modules as needed
# from myapp.models import Book

class Command(BaseCommand):
    help = 'ReIndex Barcodes'

    def get_all_letters_barcode(self):
        start_time = time.time()
        print('Started  ---------{:.0f} seconds ---------'.format(time.time()- start_time))

        LettersData = Letters.objects.filter(client='59ba80136dc7720d28bfc297')
        for index, eachLetter in enumerate(LettersData):
            if not index%20000:
                print ("Processed %s records ..." %index)
                print('Time to process for now  ---------{:.0f} seconds ---------'.format(time.time() - start_time))

            for eachRecord in eachLetter['value']:
                if eachRecord['name'] in ('barcode', 'баркод'):
                    eachLetter['barcode'] = eachRecord['value']
                    eachLetter.save()

    def handle(self, *args, **options):
        self.get_all_letters_barcode()
        print ('Done with reIndexing!')

        # For example:
        # books = Book.objects.filter(author="bob")
        # for book in books:
        #    book.name = "Bob"
        #    book.save()
