from django.contrib import admin
from django.urls import path
import api
import api.urls
from api import views

urlpatterns = [
    path('api/getuserdetails/',views.getuserdetails,name='getuserdetails'),
    path('api/resetpassword/',views.resetpassword,name='resetpassword'),
    path('/api/adduser/',views.adduser,name='adduser'),
    path('/api/adminlogin/',views.adminlogin,name='adminlogin'),
    path('/api/updateusertype/',views.updateusertype,name='updateusertype'),
    path('/api/deleteusers/',views.deleteusers,name='deleteusers'),
    path('/api/adminlogin/',views.adminlogin,name='adminlogin'),
    path('/api/addreport/',views.addreport,name='addreport'),
    path('/api/getreports/',views.getreports,name='getreports'),
    path('/api/addpayment/',views.addpayment,name='addpayment'),
    path('/api/generateledger/',views.generateledger,name='generateledger'),
    path('/api/generate_excel_ledger/',views.generate_excel_ledger,name='generate_excel_ledger'),
    path('/api/import_excel_data/',views.import_excel_data,name='import_excel_data'),
    path('/api/logout_admin/',views.logout_admin,name='logout_admin'),
]
