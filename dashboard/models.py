from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import datetime


class Designation(models.Model):
    designation = models.CharField(max_length=250)
    is_updated = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateField(default=datetime.date.today)
    updated_on = models.DateField(auto_now=False,null=True)
    deleted_on = models.DateField(auto_now=False,null=True)
    def __str__(self):
        return self.designation


class Customers(models.Model):
    customer_name = models.CharField(max_length=250)
    customer_email = models.EmailField()
    customer_address = models.TextField()
    customer_phone = PhoneNumberField()
    customer_designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    is_updated = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateField(default=datetime.date.today)
    updated_on = models.DateField(auto_now=False,null=True)
    deleted_on = models.DateField(auto_now=False,null=True)
    def __str__(self):
        return self.customer_name


class Quotations(models.Model):
    customer_name = models.ForeignKey(Customers, on_delete=models.CASCADE,null=True)
    total_discount_amount = models.FloatField(default=0)
    total_discount_percentage = models.FloatField(default=0)
    total_amount = models.FloatField(default=0)
    remarks = models.TextField(max_length=250)
    date = models.DateField(default=datetime.date.today)
    is_updated = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateField(default=datetime.date.today)
    updated_on = models.DateField(auto_now=False,null=True)
    deleted_on = models.DateField(auto_now=False,null=True)


class QuotationsDetails(models.Model):
    quatation_id = models.ForeignKey(Quotations,null=True,on_delete=models.CASCADE)
    material = models.CharField(max_length=250)
    unit = models.IntegerField(default=0)
    rate = models.IntegerField(default=0)
    discount_percentage = models.FloatField(default=0)
    discount_amount = models.FloatField(default=0)
    net_amount = models.FloatField(default=0)
    is_updated = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateField(default=datetime.date.today)
    updated_on = models.DateField(auto_now=False,null=True)
    deleted_on = models.DateField(auto_now=False,null=True)    


class Invoices(models.Model):
    customer_name = models.ForeignKey(Customers, on_delete=models.CASCADE,null=True)
    total_discount_amount = models.FloatField(default=0)
    total_discount_percentage = models.FloatField(default=0)
    total_amount = models.FloatField(default=0)
    net_amount = models.FloatField(default=0)
    remarks = models.CharField(max_length=250)
    delivery = models.CharField(max_length=250)
    payment_remarks = models.CharField(max_length=250)
    invoice_valid = models.CharField(max_length=250)
    lpo_number = models.CharField(max_length=250)
    date = models.DateField(default=datetime.date.today)
    is_updated = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateField(default=datetime.date.today)
    updated_on = models.DateField(auto_now=False,null=True)
    deleted_on = models.DateField(auto_now=False,null=True)


class InvoicesDetails(models.Model):
    invoice_id = models.ForeignKey(Invoices,null=True,on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    unit = models.IntegerField(default=0)
    rate = models.IntegerField(default=0)
    discount_percentage = models.FloatField(default=0)
    discount_amount = models.FloatField(default=0)
    net_amount = models.FloatField(default=0)
    is_updated = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateField(default=datetime.date.today)
    updated_on = models.DateField(auto_now=False,null=True)
    deleted_on = models.DateField(auto_now=False,null=True)


class Vouchers(models.Model):
    typeT = models.CharField(max_length=250)
    customer_name = models.ForeignKey(Customers, on_delete=models.CASCADE,null=True)
    debit = models.FloatField(default=0)
    credit = models.FloatField(default=0)
    remarks = models.CharField(max_length=250)
    is_updated = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateField(default=datetime.date.today)
    updated_on = models.DateField(auto_now=False,null=True)
    deleted_on = models.DateField(auto_now=False,null=True)


class Transactions(models.Model):
    invoice_id = models.ForeignKey(Invoices,null=True,on_delete=models.CASCADE)
    voucher_id = models.ForeignKey(Vouchers,null=True,on_delete=models.CASCADE)
    customer_name = models.ForeignKey(Customers, on_delete=models.CASCADE,null=True)
    amount = models.FloatField(default=0)
    typeT = models.CharField(max_length=250)
    date = models.DateField(default=datetime.date.today)
    remarks = models.CharField(max_length=250)
    is_updated = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateField(default=datetime.date.today)
    updated_on = models.DateField(auto_now=False,null=True)
    deleted_on = models.DateField(auto_now=False,null=True)






