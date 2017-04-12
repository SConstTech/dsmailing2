from django.core.urlresolvers import reverse
from django.views.generic.base import *
from django.views.generic.list import *
from django.shortcuts import *
from django.http import *
from braces.views import *
from system.models import *
import xlrd, datetime, _thread

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class FileImport(LoginRequiredMixin, GroupRequiredMixin, ListView ):
    group_required = u'paper_operator'
    template_name = 'import/import-file.html'
    context_object_name = 'objects_list'
    queryset = Clients.objects

    # def get(self, request):
    #     # return HttpResponse(_('Delivered'))
    #     print (Clients.objects)
    #     return render(request, template_name='import/import-file.html')
    def post(self,request):
        project = request.POST.get('project', False)
        if project:
            uploaded_file = request.FILES['filename'].read()
            filename = request.FILES['filename'].name
            if filename:
                status = self.file_handler(uploaded_file, filename)
                if status:
                    return render(request, 'import/success.html')
                else:
                    return render(request, 'import/error.html', context={'msg': 'Проблем при зареждането на файла'})
            else:
                return render(request, 'import/error.html', context={'msg': 'Некоректен файл'})
        else:
            return render(request, 'import/error.html', context={'msg': 'Не е избран коректен проект'})

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

    def file_handler(self, uploaded_file, filename):
        infilename = uploaded_file
        mainlist = []
        totalrecords = 0
        print('loading ...')

        mainlist  = self.xls_reader(uploaded_file=uploaded_file, filename=filename)
        if mainlist:
            for eachRecord in mainlist:
                letter = Letters(status='Delivered', print_date=datetime.datetime.now())
                value = []
                for eachValue in eachRecord:
                    #         print (eachValue)
                    letters_valuesObject = Letters_values(name=eachValue['name'], value=eachValue['value'])
                    value.append(letters_valuesObject)
                letter.value = value
                letter.save()
            return True

    def get_context_data(self, **kwargs):
        context = super(FileImport, self).get_context_data(**kwargs)
        return context

    def thread_import(self, name, value):
        # TODO - Do the thread/Queue import of bases
        pass

class HomeView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    group_required = 'paper_operator'
    template_name='index_operator.html'

class PreviewView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    group_required = 'paper_operator'
    template_name='preview/preview.html'
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
    template_name = 'clients/clients-create.html'
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
    template_name = 'clients/clients-create.html'

    def post(self):
        # TODO: find posted barcode in the base and mark it as undelivered with the posted reason
        # return Status OK (200), JSON {Letter information}


class ProjectCreate(LoginRequiredMixin, GroupRequiredMixin, ListView ):
    group_required = u'paper_operator'
    template_name = 'clients/project-create.html'
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
            return render(request, 'clients/success.html')
        else:
            return render(request, 'clients/error.html')
