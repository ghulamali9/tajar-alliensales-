from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,JsonResponse
from django.core import serializers
from django.template.loader import render_to_string
from django.views.generic import View
from django.contrib import messages
from django.db.models import Sum
from .mixins import AjaxFormMixin
from django.db import connection
from .forms import DesignationForm,CustomersForm
from .models import (
    Designation,
    Customers,
    Quotations,
    QuotationsDetails,
    Invoices,
    InvoicesDetails,
    Transactions,
    Vouchers
)
import datetime
import json as simplejson

#Home
class DashboardHome(View):
    def get(self, request, *args, **kwargs):
        customers=Customers.objects.filter(is_deleted=False).count()
        users=User.objects.filter(is_active=True).count()
        quotations=Quotations.objects.filter(is_deleted=False).count()
        invoices=Invoices.objects.filter(is_deleted=False).count()
        context={
            'customers':customers,
            'users':users,
            'quotations':quotations,
            'invoices':invoices
        }
        return render(request, 'dashboard/home.html',context)


#Designation
class DesignationsView(View, AjaxFormMixin):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            form = DesignationForm()
            desg = Designation.objects.filter(is_deleted=False).order_by('id')
            context = {
                'form': form,
                'desg' : desg
            }
        return render(request, 'dashboard/designation.html', context)


    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = DesignationForm(request.POST)
            if form.is_valid():
                form.save()
        return HttpResponse()        


class DesignationsUpdate(View):
    def get(self, request, id=0, *args, **kwargs):
        data = {}
        desg = get_object_or_404(Designation, id=id)
        form = DesignationForm(instance=desg)
        context = {
            'form' : form
        }
        data['html_form'] = render_to_string('dashboard/designation-edit/update.html',context,request=request)
        return JsonResponse(data)    


    def post(self, request, id=0, *args, **kwargs):
        data = {}
        desg = get_object_or_404(Designation, id=id)
        if request.method == 'POST':
            form = DesignationForm(request.POST, instance=desg)
            if form.is_valid():
                form.save()
                date = datetime.datetime.strftime(datetime.date.today(),'%Y-%m-%d')
                Designation.objects.filter(pk=id).update(is_updated=True, updated_on=date)
                data['form_is_valid'] = True
            else:
                data['form_is_valid'] = False
        return JsonResponse(data)       


class DesignationsDelete(View):
    def get(self,request,id=0,*args,**kwargs):
        data = {}
        desg = get_object_or_404(Designation,id=id)
        context = {
            'desg' : desg
        }
        data['html_form'] = render_to_string('dashboard/designation-edit/delete.html',context,request=request)
        return JsonResponse(data)


    def post(self,request,id=0,*args,**kwargs):
        data = {}
        if request.method == 'POST':
            date = datetime.datetime.strftime(datetime.date.today(),'%Y-%m-%d')
            Designation.objects.filter(pk=id).update(is_deleted=True, deleted_on=date)
            data['form_is_valid'] = True
        return JsonResponse(data)


class DesignationsTable(View):
    def get(self, request, *args,**kwargs):
        desg = Designation.objects.filter(is_deleted=False).order_by('id')
        data = serializers.serialize('json', desg)
        return JsonResponse({"data":data})      



#Customers
class CustomersView(View, AjaxFormMixin):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            form = CustomersForm()
            cus = Customers.objects.filter(is_deleted=False).order_by('id')
            context = {
                'form': form,
                'cus' : cus
            }
        return render(request, 'dashboard/customers.html', context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = CustomersForm(request.POST)
            global errors
            if form.is_valid():
                form.save()
                errors = {}
            else:
                errors = form.errors            
        return HttpResponse(simplejson.dumps(errors))        


class CustomersUpdate(View):
    def get(self, request, id=0, *args, **kwargs):
        data = {}
        cus = get_object_or_404(Customers, id=id)
        form = CustomersForm(instance=cus)
        context = {
            'form' : form
        }
        data['html_form'] = render_to_string('dashboard/customers-edit/update.html',context,request=request)
        return JsonResponse(data)    


    def post(self, request, id=0, *args, **kwargs):
        cus = get_object_or_404(Customers, id=id)
        if request.method == 'POST':
            form = CustomersForm(request.POST, instance=cus)
            global errors
            if form.is_valid():
                form.save()
                date = datetime.datetime.strftime(datetime.date.today(),'%Y-%m-%d')
                Customers.objects.filter(pk=id).update(is_updated=True, updated_on=date)
                errors = {}
            else:
                errors = form.errors
        return JsonResponse(errors)       


class CustomersDelete(View):
    def get(self,request,id=0,*args,**kwargs):
        data = {}
        cus = get_object_or_404(Customers,id=id)
        context = {
            'cus' : cus
        }
        data['html_form'] = render_to_string('dashboard/customers-edit/delete.html',context,request=request)
        return JsonResponse(data)


    def post(self,request,id=0,*args,**kwargs):
        data = {}
        if request.method == 'POST':
            date = datetime.datetime.strftime(datetime.date.today(),'%Y-%m-%d')
            Customers.objects.filter(pk=id).update(is_deleted=True, deleted_on=date)
            data['form_is_valid'] = True
        return JsonResponse(data)


class CustomersTable(View):
    def get(self, request, *args,**kwargs):
        cus = Customers.objects.filter(is_deleted=False).order_by('id')
        data = serializers.serialize('json', cus)
        return JsonResponse({"data":data})      


#Quotations
class QuotationsCreate(View):
    def get(self, request, *args, **kwargs):
        customers = Customers.objects.filter(is_deleted=False).order_by("-id")
        return render(request, 'dashboard/quotation.html',{'customers':customers})        

    def post(self, request, *args, **kwargs):
        response_data = {}
        if request.POST.get('action') == 'post':
            quotation_details = request.POST.getlist('quotation_details[]')
            customer_id = request.POST.get('customer')
            customer_ob = Customers.objects.get(id=customer_id)
            date = request.POST.get('date')
            totaldiscountpercentage = request.POST.get('totaldiscountpercentage')
            totaldiscountamount = request.POST.get('totaldiscountamount')
            totalamount = request.POST.get('totalamount')
            remarks = request.POST.get('remarks')
            response_data['quotation_details'] = quotation_details          
            q = Quotations.objects.create(
                customer_name = customer_ob,
                total_discount_amount = totaldiscountamount,
                total_discount_percentage = totaldiscountpercentage,
                total_amount = totalamount,
                date = date,
                remarks = remarks
            )
            count=0
            for i in range(len(quotation_details)):
                global element1
                if count==0:
                    element1=quotation_details[i]
                global element2    
                if count==1:
                    if quotation_details[i].isnumeric():
                        element2=quotation_details[i]        
                global element3    
                if count==2:
                    element3=quotation_details[i]
                global element4    
                if count==3:
                    element4=quotation_details[i]
                global element5    
                if count==4:
                    element5=quotation_details[i]
                global element6    
                if count==5:
                    element6=quotation_details[i]
                count+=1
                if count==6:    
                    QuotationsDetails.objects.create(
                        quatation_id = q,
                        material = element1,
                        unit =  element2,
                        rate =  element3,
                        discount_percentage = element4,
                        discount_amount = element5,
                        net_amount = element6
                    )
                    count=0
        return JsonResponse(response_data)    
            

class QuotationsView(View):
    def get(self, request, *args, **kwargs):
        quotations = Quotations.objects.filter(is_deleted=False).order_by('-date')
        context = {
            'quotations' : quotations
        }
        return render(request, 'dashboard/quotation-view.html', context)


class QuotationsTable(View):
    def get(self, request, *args, **kwargs):
        q = Quotations.objects.filter(is_deleted=False).order_by('-date')
        data = serializers.serialize('json', q)
        return JsonResponse({"data":data})


class QuotationsUpdate(View):
    def get(self, request, id=0, *args, **kwargs):
        data={}
        quot = get_object_or_404(Quotations,id=id)
        rows = QuotationsDetails.objects.filter(quatation_id=id, is_deleted=False)
        totalamount = QuotationsDetails.objects.filter(quatation_id=id, is_deleted=False).aggregate(Sum('net_amount'))
        context = {
            'quot' : quot,
            'rows'  : rows,
            'total' : totalamount
        }
        data['html_data']= render_to_string('dashboard/quotation-edit/update.html',context,request=request)
        return JsonResponse(data)

    def post(self, request, id=0, *args, **kwargs):
        response_data = {}
        if request.POST.get('action') == 'post':
            totaldiscountpercentage = request.POST.get('totaldiscountpercentage')
            totaldiscountamount = request.POST.get('totaldiscountamount')
            issued_date = request.POST.get('date')
            totalamount = request.POST.get('totalamount')
            date = datetime.datetime.strftime(datetime.date.today(),'%Y-%m-%d')
            Quotations.objects.filter(pk=id).update(
                date=issued_date,
                total_discount_amount=totaldiscountamount,
                total_discount_percentage=totaldiscountpercentage,
                total_amount=totalamount,
                is_updated=True,
                updated_on=date
                )        
        return JsonResponse(response_data)


class QuotationsDelete(View):
    def get(self,request,id=0,*args,**kwargs):
        data = {}
        quotation = get_object_or_404(Quotations,id=id)
        context = {
            'quotation' : quotation
        }
        data['html_form'] = render_to_string('dashboard/quotation-edit/delete.html',context,request=request)
        return JsonResponse(data)

    def post(self, request, id=0, *args, **kwargs):
        response_data={}
        if request.POST.get('action') == 'post':
            date = datetime.datetime.strftime(datetime.date.today(),'%Y-%m-%d')
            Quotations.objects.filter(pk=id).update(
                is_deleted=True,
                deleted_on=date
            )
            QuotationsDetails.objects.filter(quatation_id=id).update(
                is_deleted=True,
                deleted_on=date
            )
        return JsonResponse(response_data)    


class QuotationsPrint(View):
    def get(self, request, id=0, *args, **kwargs):
        quotation=get_object_or_404(Quotations,id=id)
        rows = QuotationsDetails.objects.filter(quatation_id=id, is_deleted=False)
        totalamount_without_discount = QuotationsDetails.objects.filter(quatation_id=id, is_deleted=False).aggregate(Sum('net_amount'))
        context={
            'quotation':quotation,
            'rows':rows,
            'totalamount':totalamount_without_discount
        }
        return render(request, 'dashboard/quotation-edit/print-quotation.html',context)


class QuotationsDetailsCreate(View):
    def post(self, request, *args, **kwargs):
        response_data = {}
        if request.method=='POST':
            quotation_id = request.POST.get('customerid')
            quotation_ob = Quotations.objects.get(id=quotation_id)
            material = request.POST.get('material')
            units = request.POST.get('units')
            rate = request.POST.get('rate')
            discountpercentage = request.POST.get('discountpercent')
            discountamount = request.POST.get('discountamount')
            netamount = request.POST.get('netamount')
            QuotationsDetails.objects.create(
                quatation_id = quotation_ob,
                material = material,
                unit =  units,
                rate =  rate,
                discount_percentage = discountpercentage,
                discount_amount = discountamount,
                net_amount = netamount
            ) 
        return JsonResponse(response_data)       


class QuotationsDetailsView(View):
    def get(self, request, id=0, *args, **kwargs):
        rows = QuotationsDetails.objects.filter(quatation_id=id, is_deleted=False)
        data = serializers.serialize('json', rows)
        return JsonResponse({"data":data})        


class QuotationsDetailsUpdate(View):
    def get(self, request, id=0, *args, **kwargs):
        data={}
        ob = get_object_or_404(QuotationsDetails,id=id)
        context = {
            'ob' : ob
        }
        data['html_data']= render_to_string('dashboard/quotation-edit/update-row.html',context,request=request)
        return JsonResponse(data)

    def post(self, request, id=0, *args, **kwargs):
        response_data = {}
        if request.POST.get('action') == 'post':
            material = request.POST.get('material')
            units = request.POST.get('units')
            rate = request.POST.get('rate')
            discountpercentage = request.POST.get('discountpercent')
            discountamount = request.POST.get('discountamount')
            netamount = request.POST.get('netamount')
            date = datetime.datetime.strftime(datetime.date.today(),'%Y-%m-%d')
            QuotationsDetails.objects.filter(id=id).update(
                material=material,
                unit=units,
                rate=rate,
                discount_percentage=discountpercentage,
                discount_amount=discountamount,
                net_amount=netamount,
                is_updated=True,
                updated_on=date
                )
        return JsonResponse(response_data)


class QuotationsDetailsDelete(View):
    def get(self, request, id=0, *args, **kwargs):
        data={}
        ob = get_object_or_404(QuotationsDetails,id=id)
        context = {
            'ob' : ob
        }
        data['html_data']= render_to_string('dashboard/quotation-edit/delete-row.html',context,request=request)
        return JsonResponse(data)

    def post(self, request, id=0, *args, **kwargs):
        response_data = {}
        if request.POST.get('action') == 'post':
            date = datetime.datetime.strftime(datetime.date.today(),'%Y-%m-%d')
            QuotationsDetails.objects.filter(id=id).update(
                is_deleted=True,
                deleted_on=date
            )
        return JsonResponse(response_data)    


class QuotationsDetailsSum(View):
    def get(self, request, id=0, *args, **kwargs):
        totalamount = QuotationsDetails.objects.filter(quatation_id=id, is_deleted=False).aggregate(Sum('net_amount'))
        return JsonResponse(totalamount)


class InvoicesCreate(View):
    def get(self, request, *args, **kwargs):
        customers = Customers.objects.filter(is_deleted=False).order_by("-id")
        return render(request, 'dashboard/invoice.html',{'customers':customers})

    def post(self, request, *args, **kwargs):
        response_data = {}
        if request.POST.get('action') == 'post':
            quotation_details = request.POST.getlist('invoice_details[]')
            customer_id = request.POST.get('customer')
            customer_ob = Customers.objects.get(id=customer_id)
            date = request.POST.get('date')
            totaldiscountpercentage = request.POST.get('totaldiscountpercentage')
            totaldiscountamount = request.POST.get('totaldiscountamount')
            totalamount = request.POST.get('totalamount')
            remarks = request.POST.get('remarks')
            paymentremarks = request.POST.get('paymentremarks')
            lpo = request.POST.get('lpo')
            invoicevalid = request.POST.get('invoicevalid')
            delivery = request.POST.get('delivery')
            netamount = request.POST.get('netamount')         
            I = Invoices.objects.create(
                customer_name = customer_ob,
                total_discount_amount = totaldiscountamount,
                total_discount_percentage = totaldiscountpercentage,
                total_amount = totalamount,
                net_amount = netamount,
                date = date,
                remarks = remarks,
                delivery = delivery,
                payment_remarks = paymentremarks,
                invoice_valid = invoicevalid,
                lpo_number = lpo
            )
            count=0
            for i in range(len(quotation_details)):
                global element1
                if count==0:
                    element1=quotation_details[i]
                global element2    
                if count==1:
                    if quotation_details[i].isnumeric():
                        element2=quotation_details[i]        
                global element3    
                if count==2:
                    element3=quotation_details[i]
                global element4    
                if count==3:
                    element4=quotation_details[i]
                global element5    
                if count==4:
                    element5=quotation_details[i]
                global element6    
                if count==5:
                    element6=quotation_details[i]
                count+=1
                if count==6:    
                    InvoicesDetails.objects.create(
                        invoice_id = I,
                        description = element1,
                        unit =  element2,
                        rate =  element3,
                        discount_percentage = element4,
                        discount_amount = element5,
                        net_amount = element6
                    )
                    count=0
            Transactions.objects.create(
                invoice_id = I,
                typeT = 'invoice',
                date = date,
                amount = totalamount 
            )
        return JsonResponse(response_data)      


class InvoicesView(View):
    def get(self, request, *args, **kwargs):
        invoices = Invoices.objects.filter(is_deleted=False).order_by('-date')
        context = {
            'invoices' : invoices
        }
        return render(request, 'dashboard/invoice-view.html', context)        


class InvoicesUpdate(View):
    def get(self, request, id=0, *args, **kwargs):
        data={}
        quot = get_object_or_404(Invoices,id=id)
        rows = InvoicesDetails.objects.filter(invoice_id=id, is_deleted=False)
        cus = Customers.objects.filter(is_deleted=False)
        totalamount = InvoicesDetails.objects.filter(invoice_id=id, is_deleted=False).aggregate(Sum('net_amount'))
        context = {
            'quot' : quot,
            'rows'  : rows,
            'total' : totalamount,
            'customers': cus
        }
        data['html_data']= render_to_string('dashboard/invoice-edit/update.html',context,request=request)
        return JsonResponse(data)

    def post(self, request, id=0, *args, **kwargs):
        response_data = {}
        if request.POST.get('action') == 'post':
            totaldiscountpercentage = request.POST.get('totaldiscountpercentage')
            totaldiscountamount = request.POST.get('totaldiscountamount')
            issued_date = request.POST.get('date')
            totalamount = request.POST.get('totalamount')
            netamount = request.POST.get('netamount')
            remarks = request.POST.get('remarks')
            paymentremarks = request.POST.get('paymentremarks')
            lpo = request.POST.get('lpo')
            delivery = request.POST.get('delivery')
            invoicevalid = request.POST.get('invoicevalid')
            customer_id = request.POST.get('customer')
            customer_obj = get_object_or_404(Customers,id=customer_id)
            date = datetime.datetime.strftime(datetime.date.today(),'%Y-%m-%d')
            Invoices.objects.filter(pk=id).update(
                date=issued_date,
                total_discount_amount=totaldiscountamount,
                total_discount_percentage=totaldiscountpercentage,
                total_amount=totalamount,
                customer_name=customer_obj,
                net_amount=netamount,
                remarks=remarks,
                payment_remarks=paymentremarks,
                lpo_number=lpo,
                delivery=delivery,
                invoice_valid=invoicevalid,
                is_updated=True,
                updated_on=date
                )            
        return JsonResponse(response_data)


class InvoicesDelete(View):
    def get(self,request,id=0,*args,**kwargs):
        data = {}
        invoice = get_object_or_404(Invoices,id=id)
        context = {
            'invoice' : invoice
        }
        data['html_form'] = render_to_string('dashboard/invoice-edit/delete.html',context,request=request)
        return JsonResponse(data)

    def post(self, request, id=0, *args, **kwargs):
        response_data={}
        if request.POST.get('action') == 'post':
            date = datetime.datetime.strftime(datetime.date.today(),'%Y-%m-%d')
            Invoices.objects.filter(pk=id).update(
                is_deleted=True,
                deleted_on=date
            )
            InvoicesDetails.objects.filter(invoice_id=id).update(
                is_deleted=True,
                deleted_on=date
            )
            Transactions.objects.filter(invoice_id=id).update(
                is_deleted=True,
                deleted_on=date
            )
        return JsonResponse(response_data)                


class InvoicesTable(View):
    def get(self, request, *args, **kwargs):
        q = Invoices.objects.filter(is_deleted=False).order_by('-date')
        data = serializers.serialize('json', q)
        return JsonResponse({"data":data})


class InvoicesPrint(View):
    def get(self, request, id=0, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM dashboard_invoices AS i JOIN dashboard_customers AS cs ON i.id=%s AND cs.id=i.customer_name_id",[id,])
            invoice=cursor.fetchone()
            columns = [column[0] for column in cursor.description]    
        results=dict(zip(columns, invoice))     
        rows = InvoicesDetails.objects.filter(invoice_id=id, is_deleted=False)
        context={
            'invoice':results,
            'rows':rows,
        }
        return render(request, 'dashboard/invoice-edit/print-invoice.html',context)


class InvoicesDetailsCreate(View):
    def post(self, request, *args, **kwargs):
        response_data = {}
        if request.method=='POST':
            invoice_id = request.POST.get('customerid')
            invoice_ob = Invoices.objects.get(id=invoice_id)
            description = request.POST.get('material')
            units = request.POST.get('units')
            rate = request.POST.get('rate')
            discountpercentage = request.POST.get('discountpercent')
            discountamount = request.POST.get('discountamount')
            netamount = request.POST.get('netamount')
            InvoicesDetails.objects.create(
                invoice_id = invoice_ob,
                description = description,
                unit =  units,
                rate =  rate,
                discount_percentage = discountpercentage,
                discount_amount = discountamount,
                net_amount = netamount
            ) 
        return JsonResponse(response_data)       


class InvoicesDetailsView(View):
    def get(self, request, id=0, *args, **kwargs):
        rows = InvoicesDetails.objects.filter(invoice_id=id, is_deleted=False)
        data = serializers.serialize('json', rows)
        return JsonResponse({"data":data})        


class InvoicesDetailsUpdate(View):
    def get(self, request, id=0, *args, **kwargs):
        data={}
        ob = get_object_or_404(InvoicesDetails,id=id)
        context = {
            'ob' : ob
        }
        data['html_data']= render_to_string('dashboard/invoice-edit/update-row.html',context,request=request)
        return JsonResponse(data)

    def post(self, request, id=0, *args, **kwargs):
        response_data = {}
        if request.POST.get('action') == 'post':
            description = request.POST.get('material')
            units = request.POST.get('units')
            rate = request.POST.get('rate')
            discountpercentage = request.POST.get('discountpercent')
            discountamount = request.POST.get('discountamount')
            netamount = request.POST.get('netamount')
            date = datetime.datetime.strftime(datetime.date.today(),'%Y-%m-%d')
            InvoicesDetails.objects.filter(id=id).update(
                description=description,
                unit=units,
                rate=rate,
                discount_percentage=discountpercentage,
                discount_amount=discountamount,
                net_amount=netamount,
                is_updated=True,
                updated_on=date
                )
        return JsonResponse(response_data)


class InvoicesDetailsDelete(View):
    def get(self, request, id=0, *args, **kwargs):
        data={}
        ob = get_object_or_404(InvoicesDetails,id=id)
        context = {
            'ob' : ob
        }
        data['html_data']= render_to_string('dashboard/invoice-edit/delete-row.html',context,request=request)
        return JsonResponse(data)

    def post(self, request, id=0, *args, **kwargs):
        response_data = {}
        if request.POST.get('action') == 'post':
            date = datetime.datetime.strftime(datetime.date.today(),'%Y-%m-%d')
            InvoicesDetails.objects.filter(id=id).update(
                is_deleted=True,
                deleted_on=date
            )
        return JsonResponse(response_data)        

    
class InvoicesDetailsSum(View):
    def get(self, request, id=0, *args, **kwargs):
        totalamount = InvoicesDetails.objects.filter(invoice_id=id, is_deleted=False).aggregate(Sum('net_amount'))
        return JsonResponse(totalamount)


class ReceiptVoucher(View):
    def get(self,request,*args,**kwargs):
        customers = Customers.objects.filter(is_deleted=False).order_by("-id")
        vouchers_count = Vouchers.objects.filter(is_deleted=False,typeT='receipt').count()
        context = {
            'customers': customers,
            'vouchers':vouchers_count+1
        }
        return render(request,'dashboard/receipt-voucher.html',context)

    def post(self,request,*args,**kwargs):
        response_data = {}
        if request.POST.get('action') == 'post':
            vouchers = request.POST.getlist('vouchers_list[]')    
            totalamount = request.POST.get('total_amount')
            customer = request.POST.get('customer')
            customer_ob = get_object_or_404(Customers,id=customer)
            V = Vouchers.objects.create(
                debit = totalamount,
                customer_name = customer_ob,
                remarks = 'debit',
                typeT='receipt'
            )
            count=0
            for i in range(len(vouchers)):
                global element1
                if count==0:
                    element1=vouchers[i]
                global element2    
                if count==1:
                    customer_id=vouchers[i]
                    customer_ob=get_object_or_404(Customers,id=customer_id)
                    element2=customer_ob        
                global element3    
                if count==2:
                    element3=vouchers[i]
                global element4    
                if count==3:
                    element4=vouchers[i]
                count+=1
                if count==4:    
                    Transactions.objects.create(
                        date = element1,
                        customer_name=element2,
                        remarks =  element3,
                        amount = element4,
                        voucher_id = V,
                        typeT = 'receipt-voucher'
                    )
                    count=0
        return JsonResponse(response_data)    


class PaymentVoucher(View):
    def get(self,request,*args,**kwargs):
        customers = Customers.objects.filter(is_deleted=False).order_by("-id")
        vouchers_count = Vouchers.objects.filter(is_deleted=False,typeT='payment').count()
        context = {
            'customers': customers,
            'vouchers':vouchers_count+1
        }
        return render(request,'dashboard/payment-voucher.html',context)

    def post(self,request,*args,**kwargs):
        response_data = {}
        if request.POST.get('action') == 'post':
            vouchers = request.POST.getlist('vouchers_list[]')    
            totalamount = request.POST.get('total_amount')
            customer = request.POST.get('customer')
            customer_ob = get_object_or_404(Customers,id=customer)
            V = Vouchers.objects.create(
                credit = totalamount,
                remarks = 'credit',
                customer_name = customer_ob,
                typeT = 'payment'
            )
            count=0
            for i in range(len(vouchers)):
                global element1
                if count==0:
                    element1=vouchers[i]
                global element2    
                if count==1:
                    customer_id=vouchers[i]
                    customer_ob=get_object_or_404(Customers,id=customer_id)
                    element2=customer_ob        
                global element3    
                if count==2:
                    element3=vouchers[i]
                global element4    
                if count==3:
                    element4=vouchers[i]
                count+=1
                if count==4:    
                    Transactions.objects.create(
                        date = element1,
                        customer_name=element2,
                        remarks =  element3,
                        amount = element4,
                        voucher_id = V,
                        typeT = 'payment-voucher'
                    )
                    count=0
        return JsonResponse(response_data)    


class VoucherCounts(View):
    def get(self,request,type_=0,*args,**kwargs):
        receiptcount = Vouchers.objects.filter(is_deleted=False,typeT=type_).count()
        context={'counts':receiptcount}
        return JsonResponse(context)   


class LatestVoucher(View):
    def get(self,request,*args,**kwargs):
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(id) FROM dashboard_vouchers")
        data = cursor.fetchone()
        context={
            'data':data
        }
        return JsonResponse(context)


class PrintVoucher(View):
    def get(self, request,id=0,*args,**kwargs):
        transactions = Transactions.objects.filter(voucher_id=id,is_deleted=False)
        context={
            'transactions':transactions,
            'voucher_no':id
        }
        return render(request,'dashboard/print-voucher.html',context)


class AccountStatement(View):
    def get(self,request,*args,**kwargs):
        customers = Customers.objects.filter(is_deleted=False)
        context={
            'customers':customers
        }
        return render(request,'dashboard/account-statement.html',context)                                                                                           

    def post(self,request,*args,**kwargs):
        response_data={}
        if request.POST.get('action')=='post':
            customer_id = request.POST.get('customer')    
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            cursor = connection.cursor()
            cursor.execute("SELECT customer_name FROM dashboard_customers AS DC WHERE DC.id=%s",[customer_id,])
            data2 = cursor.fetchone()
            response_data['data2']=data2
            rows = Vouchers.objects.filter(created_on__range=(from_date,to_date),customer_name=customer_id)
            data1=serializers.serialize('json',rows)
            response_data['data1']=data1
        return JsonResponse(response_data) 


class ReceiptStatement(View):
    def get(self,request,*args,**kwargs):
        customers = Customers.objects.filter(is_deleted=False)
        context={
            'customers':customers
        }
        return render(request,'dashboard/receipt-statement.html',context)                                                                                           

    def post(self,request,*args,**kwargs):
        response_data={}
        if request.POST.get('action')=='post':
            customer_id = request.POST.get('customer')    
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            cursor = connection.cursor()
            cursor.execute("SELECT customer_name FROM dashboard_customers AS DC WHERE DC.id=%s",[customer_id,])
            data2 = cursor.fetchone()
            response_data['data2']=data2
            rows = Vouchers.objects.filter(created_on__range=(from_date,to_date),customer_name=customer_id,typeT='receipt')
            data1=serializers.serialize('json',rows)
            response_data['data1']=data1
        return JsonResponse(response_data) 


class PaymentStatement(View):
    def get(self,request,*args,**kwargs):
        customers = Customers.objects.filter(is_deleted=False)
        context={
            'customers':customers
        }
        return render(request,'dashboard/payment-statement.html',context)                                                                                           

    def post(self,request,*args,**kwargs):
        response_data={}
        if request.POST.get('action')=='post':
            customer_id = request.POST.get('customer')    
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            cursor = connection.cursor()
            cursor.execute("SELECT customer_name FROM dashboard_customers AS DC WHERE DC.id=%s",[customer_id,])
            data2 = cursor.fetchone()
            response_data['data2']=data2
            rows = Vouchers.objects.filter(created_on__range=(from_date,to_date),customer_name=customer_id,typeT='payment')
            data1=serializers.serialize('json',rows)
            response_data['data1']=data1
        return JsonResponse(response_data)


class GetCustomer(View):
    def get(self,request,id=0,*args,**kwargs):
        customers = [Customers.objects.get(id=id)]
        data = serializers.serialize('json', customers)
        return JsonResponse({'data':data})


from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import re
class UserRegistration(View):
    def get(self,request,*args,**kwargs):
        return render(request, 'dashboard/user-registration.html')        

    def post(self,request,*args,**kwargs):
        response_data={}
        if request.POST.get('action')=='post':
            email = request.POST.get('email')
            username = request.POST.get('username')
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            if pass1==pass2:
                global password
                password=make_password(pass1)
                if re.search(regex,email):
                    if User.objects.filter(username=username).exists():
                        messages.add_message(request, messages.WARNING, 'User Already Exists')
                    else:
                        User.objects.create(
                            username=username,
                            last_name=lastname,
                            first_name=firstname,
                            password=password,
                            email=email
                        )
                else:
                    messages.add_message(request, messages.WARNING, 'Invalid Email Address')        
            else:
                messages.add_message(request, messages.WARNING, 'Password Doesn\'t Match')
            django_messages = []       
            for message in messages.get_messages(request):
                django_messages.append({
                    "level": message.level,
                    "message": message.message,
                    "extra_tags": message.tags,
                })   
            response_data['messages'] = django_messages          
        return JsonResponse(response_data)    


from .forms import UserLoginForm
class UserLogin(View):
    def get(self,request,*args,**kwargs):
        form = UserLoginForm()
        return render(request,'dashboard/user-login.html',{'form':form})

    def post(self,request,*args,**kwargs):
        if request.method == 'POST':
            form = UserLoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request,username=username, password=password)
                print(user)
                if user is not None:
                    login(request,user)
                    return redirect('dashboard-home')       
        return render(request,'dashboard/user-login.html',{'form':form}) 


class UserLogout(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('dashboard-user-login')            


class UsersView(View):
    def get(self,request,*args,**kwargs):
        users = User.objects.filter(is_active=True)
        return render(request,'dashboard/users-view.html',{'users':users})           