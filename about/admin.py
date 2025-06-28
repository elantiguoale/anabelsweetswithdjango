from django.contrib import admin
from .models import Post, CakeSubmission, Order

# Register your models here.
admin.site.register(Post)

@admin.register(CakeSubmission)
class CakeSubmissionAdmin(admin.ModelAdmin):
    list_display = ('cake_name', 'user', 'submission_date', 'approval_status')
    list_filter = ('approval_status', 'submission_date')
    search_fields = ('cake_name', 'user__username', 'description')
    readonly_fields = ('submission_date',)
    actions = ['approve_submissions', 'reject_submissions']
    
    fieldsets = (
        ('Submission Info', {
            'fields': ('user', 'cake_name', 'description', 'image', 'submission_date')
        }),
        ('Admin Review', {
            'fields': ('approval_status', 'admin_notes'),
            'classes': ('collapse',)
        }),
    )
    
    def approve_submissions(self, request, queryset):
        queryset.update(approval_status='approved')
        self.message_user(request, f"{queryset.count()} submissions approved successfully!")
    approve_submissions.short_description = "Approve selected submissions"
    
    def reject_submissions(self, request, queryset):
        queryset.update(approval_status='rejected')
        self.message_user(request, f"{queryset.count()} submissions rejected.")
    reject_submissions.short_description = "Reject selected submissions"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'cake_flavor', 'event_date', 'status', 'is_urgent')
    list_filter = ('status', 'cake_flavor', 'event_type', 'order_date')
    search_fields = ('customer_name', 'customer_email', 'customer_phone', 'design_description')
    readonly_fields = ('order_date', 'updated_date')
    actions = ['confirm_orders', 'mark_in_progress', 'mark_ready', 'mark_completed', 'mark_cancelled']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Order Details', {
            'fields': ('cake_flavor', 'custom_flavor_description', 'cake_size', 'servings')
        }),
        ('Design & Event', {
            'fields': ('design_description', 'special_requests', 'event_date', 'event_type')
        }),
        ('Pricing & Status', {
            'fields': ('estimated_price', 'final_price', 'status')
        }),
        ('Timestamps', {
            'fields': ('order_date', 'updated_date'),
            'classes': ('collapse',)
        }),
        ('Admin Notes', {
            'fields': ('admin_notes',),
            'classes': ('collapse',)
        }),
    )
    
    def is_urgent(self, obj):
        return obj.is_urgent
    is_urgent.boolean = True
    is_urgent.short_description = "Urgent"
    
    def confirm_orders(self, request, queryset):
        queryset.update(status='confirmed')
        self.message_user(request, f"{queryset.count()} orders confirmed!")
    confirm_orders.short_description = "Confirm selected orders"
    
    def mark_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
        self.message_user(request, f"{queryset.count()} orders marked as in progress!")
    mark_in_progress.short_description = "Mark as in progress"
    
    def mark_ready(self, request, queryset):
        queryset.update(status='ready')
        self.message_user(request, f"{queryset.count()} orders marked as ready for pickup!")
    mark_ready.short_description = "Mark as ready for pickup"
    
    def mark_completed(self, request, queryset):
        queryset.update(status='completed')
        self.message_user(request, f"{queryset.count()} orders marked as completed!")
    mark_completed.short_description = "Mark as completed"
    
    def mark_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, f"{queryset.count()} orders marked as cancelled!")
    mark_cancelled.short_description = "Mark as cancelled"



