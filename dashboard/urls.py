from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    DashboardHome,
    #Designation
    DesignationsView,
    DesignationsUpdate,
    DesignationsDelete,
    DesignationsTable,
    #customer
    CustomersView,
    CustomersUpdate,
    CustomersDelete,
    CustomersTable,
    #Quotations
    QuotationsCreate,
    QuotationsView,
    QuotationsUpdate,
    QuotationsTable,
    QuotationsDelete,
    QuotationsPrint,
    QuotationsDetailsCreate,
    QuotationsDetailsView,
    QuotationsDetailsUpdate,
    QuotationsDetailsDelete,
    QuotationsDetailsSum,
    #Invoices
    InvoicesCreate,
    InvoicesView,
    InvoicesUpdate,
    InvoicesDelete,
    InvoicesTable,
    InvoicesPrint,
    InvoicesDetailsCreate,
    InvoicesDetailsView,
    InvoicesDetailsUpdate,
    InvoicesDetailsDelete,
    InvoicesDetailsSum,
    #Vouchers
    ReceiptVoucher,
    PaymentVoucher,
    VoucherCounts,
    LatestVoucher,
    PrintVoucher,
    #Reports
    AccountStatement,
    GetCustomer,
    ReceiptStatement,
    PaymentStatement,
    #Users
    UserRegistration,
    UsersView,
    UserLogin,
    UserLogout
)


urlpatterns = [
    #home
    path('', login_required(DashboardHome.as_view(),login_url='dashboard-user-login'),name="dashboard-home"),
    #designation
    path('designation/', login_required(DesignationsView.as_view(),login_url='dashboard-user-login'), name="dashboard-designation"),
    path('designation-update/<int:id>', login_required(DesignationsUpdate.as_view(),login_url='dashboard-user-login'), name="dashboard-designation-update"),
    path('designation-delete/<int:id>', login_required(DesignationsDelete.as_view(),login_url='dashboard-user-login'), name="dashboard-designation-delete"),
    path('designation-table/', login_required(DesignationsTable.as_view(),login_url='dashboard-user-login'), name="dashboard-designation-table"),
    #customers
    path('customers/', login_required(CustomersView.as_view(),login_url='dashboard-user-login'), name="dashboard-customers"),
    path('customers-update/<int:id>', login_required(CustomersUpdate.as_view(),login_url='dashboard-user-login'), name="dashboard-customers-update"),
    path('customers-delete/<int:id>', login_required(CustomersDelete.as_view(),login_url='dashboard-user-login'), name="dashboard-customers-delete"),
    path('customers-table/', login_required(CustomersTable.as_view(),login_url='dashboard-user-login'), name="dashboard-customers-table"),
    #quotations
    path('quotations-create/', login_required(QuotationsCreate.as_view(),login_url='dashboard-user-login'), name="dashboard-quotations-create"),
    path('quoations-list/', login_required(QuotationsView.as_view(),login_url='dashboard-user-login'), name="dashboard-quotations-view"),
    path('quotations-update/<int:id>', login_required(QuotationsUpdate.as_view(),login_url='dashboard-user-login'), name="dashboard-quotations-update"),
    path('quotations-table/', login_required(QuotationsTable.as_view(),login_url='dashboard-user-login'), name="dashboard-quotations-table"),
    path('quotations-delete/<int:id>', login_required(QuotationsDelete.as_view(),login_url='dashboard-user-login'),name="dashboard-quotations-delete"),
    path('quotations-print/<int:id>', login_required(QuotationsPrint.as_view(),login_url='dashboard-user-login'),name="dashboard-quotations-print"),
    #quotations details
    path('quotations-details-create/', login_required(QuotationsDetailsCreate.as_view(),login_url='dashboard-user-login'), name="dashboard-quotations-details-create"),
    path('quotations-details-view/<int:id>', login_required(QuotationsDetailsView.as_view(),login_url='dashboard-user-login'), name="dashboard-quotations-details-view"),
    path('quotations-details-update/<str:id>', login_required(QuotationsDetailsUpdate.as_view(),login_url='dashboard-user-login'),name="dashboard-quotations-details-update"),
    path('quotations-details-delete/<int:id>', login_required(QuotationsDetailsDelete.as_view(),login_url='dashboard-user-login'),name="dashboard-quotations-details-delete"),
    path('quotations-details-sum/<int:id>', login_required(QuotationsDetailsSum.as_view(),login_url='dashboard-user-login'),name="dashboard-quotaitons-details-sum"),
    #invoices 
    path('invoices-create/', login_required(InvoicesCreate.as_view(),login_url='dashboard-user-login'), name="dashboard-invoices-create"),
    path('invoices-list/', login_required(InvoicesView.as_view(),login_url='dashboard-user-login'), name="dashboard-invoices-view"),
    path('invoices-update/<int:id>', login_required(InvoicesUpdate.as_view(),login_url='dashboard-user-login'), name="dashboard-invoices-update"),
    path('invoices-delete/<int:id>', login_required(InvoicesDelete.as_view(),login_url='dashboard-user-login'), name="dashboard-invoices-delete"),
    path('invoices-table/', login_required(InvoicesTable.as_view(),login_url='dashboard-user-login'), name="dashboard-invoices-table"),
    path('invoices-print/<int:id>', login_required(InvoicesPrint.as_view(),login_url='dashboard-user-login'),name="dashboard-invoices-print"),
    #invoices details
    path('invoices-details-create/', login_required(InvoicesDetailsCreate.as_view(),login_url='dashboard-user-login'), name="dashboard-invoices-details-create"),
    path('invoices-details-view/<int:id>', login_required(InvoicesDetailsView.as_view(),login_url='dashboard-user-login'), name="dashboard-invoices-details-view"),
    path('invoices-details-update/<str:id>', login_required(InvoicesDetailsUpdate.as_view(),login_url='dashboard-user-login'),name="dashboard-invoices-details-update"),
    path('invoices-details-delete/<int:id>', login_required(InvoicesDetailsDelete.as_view(),login_url='dashboard-user-login'),name="dashboard-invoices-details-delete"),
    path('invoices-details-sum/<int:id>', login_required(InvoicesDetailsSum.as_view(),login_url='dashboard-user-login'),name="dashboard-invoices-details-sum"),
    #vouchers
    path('receipt-voucher/', login_required(ReceiptVoucher.as_view(),login_url='dashboard-user-login'), name="dashboard-receipt-voucher"),
    path('payment-voucher/', login_required(PaymentVoucher.as_view(),login_url='dashboard-user-login'), name="dashboard-payment-voucher"),
    path('voucher-counts/<str:type_>', login_required(VoucherCounts.as_view(),login_url='dashboard-user-login'), name="dashboard-voucher-count"),
    path('latest-voucher/', login_required(LatestVoucher.as_view(),login_url='dashboard-user-login'), name="dashboard-latest-voucher"),
    path('voucher-print/<int:id>', login_required(PrintVoucher.as_view(),login_url='dashboard-user-login'), name="dashboard-voucher-print"),
    #reports
    path('get-customer/<int:id>', login_required(GetCustomer.as_view(),login_url='dashboard-user-login'), name="dashboard-get-customer"),
    path('account-statement/', login_required(AccountStatement.as_view(),login_url='dashboard-user-login'), name="dashboard-account-statement"),   
    path('receipt-statement/', login_required(ReceiptStatement.as_view(),login_url='dashboard-user-login'), name="dashboard-receipt-statement"),
    path('payment-statement/', login_required(PaymentStatement.as_view(),login_url='dashboard-user-login'), name="dashboard-payment-statement"),
    #users
    path('user-registration/', UserRegistration.as_view(), name="dashboard-user-registration"),
    path('users-view/', login_required(UsersView.as_view(),login_url='dashboard-user-login'), name="dashboard-user-view"),   
    path('user-login/', UserLogin.as_view(), name="dashboard-user-login"),
    path('user-logout/', UserLogout.as_view(), name="dashboard-user-logout")
]