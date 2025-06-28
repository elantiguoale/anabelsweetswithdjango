from django.contrib import admin
from .models import Post, CakeSubmission

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



