from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Worker, Attendance, WorkerCard

class WorkerAdmin(admin.ModelAdmin):
    # Display worker's ID, name, department, and QR code preview
    list_display = ('worker_id', 'first_name', 'last_name', 'department', 'qr_code_preview')
    
    # Allow searching by first name, last name, or email
    search_fields = ('first_name', 'last_name', 'email')
    
    # Preview the QR code image in the admin list view
    def qr_code_preview(self, obj):
        if obj.qr_code:
            return mark_safe(f'<img src="{obj.qr_code.url}" width="50" height="50" />')
        return "No QR Code"
    qr_code_preview.short_description = 'QR Code'

class WorkerCardAdmin(admin.ModelAdmin):
    # Display worker's name, card number, and a preview of the card image
    list_display = ('worker', 'card_number', 'card_image_preview')

    # Allow searching by worker's name and card number
    search_fields = ('worker__first_name', 'worker__last_name', 'card_number')

    # Preview the card image in the admin list view
    def card_image_preview(self, obj):
        if obj.card_image:
            return mark_safe(f'<img src="{obj.card_image.url}" width="100" height="100" />')
        return "No Card Image"
    card_image_preview.short_description = 'Card Image'

    # Add an action for generating the card image
    def generate_card_image_action(self, request, queryset):
        for card in queryset:
            card.generate_card_image()
        self.message_user(request, "Selected cards' images have been generated.")
    generate_card_image_action.short_description = "Generate Card Images"

    # Add custom action to the admin panel
    actions = ['generate_card_image_action']

# Register Worker and WorkerCard models with the custom admin classes
admin.site.register(Worker, WorkerAdmin)
admin.site.register(WorkerCard, WorkerCardAdmin)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    # Display worker, time of scanning, and event name in the list view
    list_display = ('worker', 'scanned_at', 'event_name')
    
    # Add filters to easily filter records by scanned time and event
    list_filter = ('scanned_at', 'event_name')
    
    # Allow searching by worker's first name, last name, and event name
    search_fields = ('worker__first_name', 'worker__last_name', 'event_name')
