from django.views.generic.base import *
from django.views.generic.list import *
from django.shortcuts import *
from django.http import *
from braces.views import *
from system.models import *
import xlrd, datetime, csv
from datetime import timedelta
from django.http import HttpResponse
import time

class FileImport(LoginRequiredMixin, GroupRequiredMixin, ListView ):
    group_required = u'paper_operator'
    template_name = 'operators/import/import-file.html'
    context_object_name = 'objects_list'
    queryset = Clients.objects

    def post(self,request):
        client = request.POST.get('client', False)
        if client:
            file_list = request.FILES.getlist('filename')
            for opened_file in file_list:
            # uploaded_file = request.FILES['filename'].read()
                uploaded_file = opened_file.read()
                filename = opened_file.name
                if filename:
                    status = self.file_handler(uploaded_file, filename, client)
                    if status:
                        baseImportObject = basesImported(dateImported=datetime.datetime.now(), client=client, filename=filename).save()
                    else:
                        return render(request, 'operators/import/error.html', context={'msg': 'Проблем при зареждането на файла'})
                else:
                    return render(request, 'operators/import/error.html', context={'msg': 'Некоректен файл'})
            return render(request, 'operators/import/success.html')

    def xls_reader(self, uploaded_file, filename):
        try:
            infilename = uploaded_file
            totalrecords = 0
            mainlist = []
            inbook = xlrd.open_workbook(file_contents=uploaded_file)
            for k in range(inbook.nsheets):
                insheet = inbook.sheet_by_index(k)
                header = []
                for k in range(1):
                    for n in range(insheet.ncols):
                        header.append(str(insheet.cell(rowx=k, colx=n).value).lower())

                for m in range(1, insheet.nrows):  # skip header
                    mainlist.append([])
                    totalrecords += 1
                    for n in range(insheet.ncols):
                        if insheet.cell_type(rowx=m, colx=n) == 3:  # date
                            date_value = datetime.datetime(
                                *(xlrd.xldate_as_tuple(insheet.cell_value(rowx=m, colx=n), inbook.datemode))).strftime(
                                '%d.%m.%Y')
                            mainlist[-1].append({'name': header[n], 'value': date_value})
                        elif insheet.cell_type(rowx=m, colx=n) == 2:  # float
                            float_value = str(int(insheet.cell_value(rowx=m, colx=n)))
                            mainlist[-1].append({'name': header[n], 'value': float_value})
                        elif insheet.cell_type(rowx=m, colx=n) == 5:  # error
                            mainlist[-1].append({'name': header[n], 'value': 'NONE'})
                        else:  # unicode, empty or blank
                            unicode_value = str(insheet.cell(rowx=m, colx=n).value)
                            mainlist[-1].append({'name': header[n], 'value': unicode_value})
                    mainlist[-1].append({'name': 'filename', 'value': str(filename)})
                    mainlist[-1].append({'name': 'sheetname', 'value': insheet.name})
        except:
            return False
        return mainlist

    def file_handler(self, uploaded_file, filename, client):
        start_time = time.time()
        mainlist  = self.xls_reader(uploaded_file=uploaded_file, filename=filename)
        print('Loaded XLS file ---------%s seconds ---------' % (time.time() - start_time))

        current_client = Clients.objects.get(id=client)
        if mainlist:
            save_list = []
            print ('Build barcode_list time ---------%s seconds ---------' %(time.time() - start_time))
            for eachRecord in mainlist:
                to_save = True
                letter = Letters(print_date=datetime.datetime.now())
                value = []
                for eachValue in eachRecord:
                    if eachValue['name'] == 'barcode' or eachValue['name'] == 'баркод':
                        letter.barcode = eachValue['value']
                    letters_valuesObject = Letters_values(**eachValue)
                    value.append(letters_valuesObject)
                # if to_save:
                letter.value = value
                letter.client = current_client.to_dbref()
                save_list.append(letter)
                # end if to_save
            print('build values time ---------%s seconds ---------' % (time.time() - start_time))

            if save_list:
                Letters.objects.insert(save_list)
            print ('End-Loading file ---------%s seconds --------- loaded %s records' %(time.time() - start_time, len(save_list)))
            return True

    def get_context_data(self, **kwargs):
        context = super(FileImport, self).get_context_data(**kwargs)
        return context

class HomeView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    group_required = 'paper_operator'
    template_name='operators/home_operator.html'

class PreviewView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    group_required = 'paper_operator'
    template_name='operators/preview/preview.html'
    context_object_name = 'frontData'
    queryset = Letters.objects
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super(PreviewView, self).get_context_data(**kwargs)
        frontData = {
            'headers':[],
            'row':[] #[{'items':[]}]
        }
        # page = self.request.GET.get('page', 1)
        for eachHeader in Letters.objects.first().value:
            frontData['headers'].append(eachHeader['name'])

        context['Header'] = frontData['headers']

        return context

class ClientCreate(LoginRequiredMixin, GroupRequiredMixin, TemplateView ):
    group_required = u'paper_operator'
    template_name = 'operators/clients/clients-create.html'
    # context_object_name = 'objects_list'
    # queryset = Clients.objects

    def post(self,request):
        clientName = request.POST.get('clientname', False)
        # projectName = request.POST.get('projectname', False)

        if clientName:
            clientObject = Clients(name=clientName)
            clientObject.save()
            return render(request, 'clients/success.html')
        else:
            return render(request, 'clients/error.html')

class BarcodeChecker(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    group_required = u'paper_operator'
    template_name = 'operators/letters/barcode-checker.html'

    def post(self, request):
        # return Status OK (200), JSON {Letter information}
        start_time = time.time()
        print('start values time ---------%s seconds ---------' % (time.time()- start_time))
        barcode = request.POST.get('barcode', False)
        cause = request.POST.get('reason', False)
        lettersObject = Letters.objects.filter(barcode=barcode)
        # lettersObject = Letters.objects.get(value__name='баркод', value__value=barcode)
        if lettersObject:
            lettersObject = lettersObject[0]
            deliverObject = Delivery(status = 'Недоставено', reason = cause)
            lettersObject.status = [deliverObject]
            lettersObject.operatorMarked = request.user.id
            lettersObject.status_date = datetime.datetime.now().replace(microsecond=0, hour=0, minute=0, second=0)
            lettersObject.save()
            print('return values time ---------%s seconds ---------' % (time.time() - start_time))
            return HttpResponse ('OK', status=200)
        else:
            return HttpResponse('bad input', status=204)
        
class ProjectCreate(LoginRequiredMixin, GroupRequiredMixin, ListView ):
    group_required = u'paper_operator'
    template_name = 'operators/clients/project-create.html'
    queryset = Clients.objects

    def post(self,request):
        clientName = request.POST.get('clientname', False)
        projectName = request.POST.get('projectname', False)

        if clientName and projectName:
            clientObject = Clients.objects(name=clientName).first()
            tempProjectObject = Projects(name=projectName)
            tempProjectObject.save()
            clientObject.projects.append(tempProjectObject)
            clientObject.save()
            return render(request, 'operators/clients/success.html')
        else:
            return render(request, 'operators/clients/error.html')

class ExportReport(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    group_required = u'paper_operator'
    template_name = 'operators/queries/export_by_date.html'

    def get_context_data(self, **kwargs):
        context = super(ExportReport, self).get_context_data(**kwargs)
        context['allClients'] = Clients.objects()
        return context

    def post(self, request):
        clientID = request.POST.get('client', False)
        clientObject = Clients.objects.get(id=clientID)
        days = int(request.POST.get('days', False))
        start_date, end_date = request.POST.get('request_dates', False).split('-')
        start_date =  datetime.datetime.strptime(start_date.strip(), '%d/%m/%Y')
        end_date =  datetime.datetime.strptime(end_date.strip(), '%d/%m/%Y')
        if days:
            substract_date = datetime.datetime.now().replace(microsecond=0, hour=0, minute=0, second=0) - timedelta(days=days)
            lettersData = Letters.objects.filter(client=clientID, status_date__gte=substract_date)
        else:
            lettersData = Letters.objects.filter(client=clientID, status_date__gt=start_date, status_date__lt=end_date)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = u'attachment; filename="report-today.csv"'
        writer = csv.writer(response, delimiter='\t')

        for letterObj in lettersData:
            row = []
            for letterValue in letterObj.value:
                row.extend([letterValue['value']])
            row.extend([letterObj.status[-1].status, letterObj.status[-1].reason])
            writer.writerow(row)

        return response

class SearchLetters(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    group_required = u'paper_operator'
    template_name = 'operators/queries/search-letters.html'

    def get_context_data(self, **kwargs):
        context = super(SearchLetters, self).get_context_data(**kwargs)
        context['allClients'] = Clients.objects()
        return context

    def post(self, request):
        searched_value = request.POST.get('searched_value', False)
        clientID = request.POST.get('client', False)
        lettersData = Letters.objects.filter(client=clientID, value__value__icontains=str(searched_value))
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="searched-report.csv"'
        writer = csv.writer(response, delimiter='\t')

        for letterObj in lettersData:
            row = []
            for letterValue in letterObj.value:
                row.extend([letterValue['value']])
            try:
                row.extend([letterObj.status[-1].status, letterObj.status[-1].reason])
            except:
                row.extend(['Не е обработено', 'Не е обработено'])
            writer.writerow(row)

        return response

class ClientStatistics(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    group_required = u'paper_operator'
    template_name = 'operators/queries/client-statistics.html'

    def get_context_data(self, **kwargs):
        context = super(ClientStatistics, self).get_context_data(**kwargs)
        allClients = Clients.objects()
        frontData = []
        for eachClient in allClients:
            counter_undelivered = Letters.objects.filter(client=eachClient.id, operatorMarked__exists=True).count()
            counter_delivered = Letters.objects.filter(client=eachClient.id, operatorMarked__exists=False).count()
            counter_total = Letters.objects.filter(client=eachClient.id).count()
            frontData.append({'clientName': eachClient.name,
                              'counter_undelivered':counter_undelivered,
                              'counter_total':counter_total,
                              'counter_delivered': counter_delivered})
        context['frontData'] = frontData
        return context

class RemoveClient(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    group_required = u'paper_operator'
    template_name = 'operators/administration/remove-client.html'

    def get_context_data(self, **kwargs):
        context = super(RemoveClient, self).get_context_data(**kwargs)
        context['allClients'] = Clients.objects()
        return context

    def post(self, request):
        clientID = request.POST.get('client', False)
        clientObject = Clients.objects.get(id=clientID)
        lettersData = Letters.objects.filter(client=clientID)
        lettersData.delete()
        clientObject.delete()
        return render(request, 'operators/administration/remove-success.html')

