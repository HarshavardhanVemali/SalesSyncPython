from django.contrib import admin
from .models import FailedLoginAttempts,Customer, Order, Payment,BillSequence,Supplier,Acquisition,AcquisitionPayment

@admin.register(FailedLoginAttempts)
class FailedLoginAttemptsAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'attempts', 'is_active')
    list_filter = ('device_id', 'attempts', 'is_active')
    search_fields = ('device_id', 'attempts', 'is_active')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'area', 'phone') 
    search_fields = ('name', 'area', 'phone') 
    list_filter = ('area',)  

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('bill_no', 'customer', 'product', 'billing_date', 'amount', 'total_paid', 'balance', 'status', 'updated_time')
    search_fields = ('bill_no', 'customer__name', 'product') 
    list_filter = ('status', 'billing_date') 
    ordering = ('-billing_date',) 
    readonly_fields = ('balance', 'total_paid', 'status')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_date', 'paid_amount', 'payment_method', 'remarks')
    search_fields = ('order__bill_no', 'order__customer__name', 'payment_method') 
    list_filter = ('payment_method', 'payment_date') 
    ordering = ('-payment_date',) 

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_name', 'phone', 'email', 'gst_number') 
    search_fields = ('name', 'company_name', 'phone', 'email', 'gst_number') 
    list_filter = ('company_name',) 
    ordering = ('name',) 
    readonly_fields = ('gst_number',) 

    fieldsets = (
        (None, {
            'fields': ('name', 'company_name', 'address', 'phone', 'email', 'gst_number')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        """Customize read-only fields dynamically."""
        if obj: 
            return self.readonly_fields + ('gst_number',)
        return self.readonly_fields

class AcquisitionPaymentInline(admin.TabularInline):
    model = AcquisitionPayment
    extra = 1 
    
    
class AcquisitionAdmin(admin.ModelAdmin):
    list_display = ('invoice_no', 'supplier', 'product', 'purchase_date', 'amount', 'total_paid', 'balance', 'status')
    list_filter = ('supplier', 'purchase_date', 'status')
    search_fields = ('invoice_no', 'product', 'supplier__name') 
    date_hierarchy = 'purchase_date'
    inlines = [AcquisitionPaymentInline] 
    readonly_fields = ('created_time', 'updated_time', 'invoice_no','balance')
    
    def save_model(self, request, obj, form, change):
        if not obj.invoice_no:
            
            obj.invoice_no = f"INV-{obj.id}-{obj.purchase_date.strftime('%Y%m%d')}"
        
        obj.balance = obj.amount-obj.total_paid
    
        if obj.total_paid == 0:
            obj.status = 'unpaid'
        elif obj.total_paid < obj.amount:
            obj.status = 'partially_paid'
        else:
            obj.status = 'paid'
       
        super().save_model(request, obj, form, change)

class AcquisitionPaymentAdmin(admin.ModelAdmin):
    list_display = ('acquisition', 'payment_date', 'paid_amount', 'payment_method')
    list_filter = ('payment_date', 'payment_method')
    search_fields = ('acquisition__invoice_no', 'acquisition__supplier__name')
    date_hierarchy = 'payment_date'
    readonly_fields = ('created_time',)

    
    def save_model(self, request, obj, form, change):
        
        super().save_model(request, obj, form, change)

        acquisition = obj.acquisition
        acquisition.total_paid += obj.paid_amount
        acquisition.save()

        acquisition.balance = acquisition.amount - acquisition.total_paid
        
        if acquisition.total_paid == 0:
            acquisition.status = 'unpaid'
        elif acquisition.total_paid < acquisition.amount:
            acquisition.status = 'partially_paid'
        else:
            acquisition.status = 'paid'
        acquisition.save()
        


admin.site.register(Acquisition, AcquisitionAdmin)
admin.site.register(AcquisitionPayment, AcquisitionPaymentAdmin)

admin.site.register(BillSequence)

