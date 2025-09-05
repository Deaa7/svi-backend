from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.db.models import Q
from .models import StudentPremiumContent


@admin.register(StudentPremiumContent)
class StudentPremiumContentAdmin(admin.ModelAdmin):
    """
    Admin interface for StudentPremiumContent model
    Provides comprehensive search, filtering, and management capabilities
    """
    
    # List display configuration - fields shown in the list view
    list_display = [
        'id',
        'student',
        'student_name',
        'content_id',
        'publisher_name',
        'subject_name',
        'Class',
        'price',
        'purchase_date',
        'expiry_status',
        'days_remaining'
    ]
    
    # List filters - sidebar filters for quick filtering
    list_filter = [
        'subject_name',
        'student_name',
        'Class',
        'type',
        'purchase_date',
        'date_of_expiry',
        'publisher_name',
    ]
    
    # Enhanced search functionality with multiple parameters
    search_fields = [
        'content_id',  # Search by content ID
        'publisher_name',  # Search by publisher name
        'subject_name',  # Search by subject name
        'Class',  # Search by class
        'type',  # Search by content type
        'student_name'
    ]
    
    # Fields to display in the form when editing
    fields = [
        'content_id',
        'student',
        'Class',
        'type',
        'subject_name',
        'content_name',
        'publisher_id',
        'publisher_name',
        'price',
        'date_of_expiry',
        'purchase_date'
    ]
    
    # Read-only fields that cannot be edited
    readonly_fields = ['purchase_date']
    
    # Default ordering of records
    ordering = ['-purchase_date']
    
    # Number of items displayed per page
    list_per_page = 25
    
    # Enable date hierarchy navigation
    date_hierarchy = 'purchase_date'
    
    # Enable selection checkboxes for bulk actions
    list_select_related = ['student', 'publisher_id']
 
    def expiry_status(self, obj):
        """
        Display expiry status with color coding
        Shows whether content is active or expired with visual indicators
        """
        current_time = timezone.now()
        
        # Ensure both dates are datetime objects for comparison
        if hasattr(obj.date_of_expiry, 'date'):
            # It's already a datetime object
            expiry_datetime = obj.date_of_expiry
        else:
            # It's a date object, convert to datetime
            from datetime import datetime, time
            expiry_datetime = timezone.make_aware(
                datetime.combine(obj.date_of_expiry, time.max)
            )
        
        if expiry_datetime < current_time:
            return format_html(
                '<span style="color: red; font-weight: bold;">EXPIRED</span><br/>'
                '<small>{}</small>',
                expiry_datetime.strftime('%Y-%m-%d %H:%M')
            )
        else:
            return format_html(
                '<span style="color: green; font-weight: bold;">ACTIVE</span><br/>'
                '<small>{}</small>',
                expiry_datetime.strftime('%Y-%m-%d %H:%M')
            )
    expiry_status.short_description = 'Status'
    expiry_status.admin_order_field = 'date_of_expiry'
    
    def days_remaining(self, obj):
        """
        Calculate and display days remaining until expiry
        Shows color-coded information about remaining time
        """
        current_time = timezone.now()
        
        # Ensure both dates are datetime objects for comparison
        if hasattr(obj.date_of_expiry, 'date'):
            # It's already a datetime object
            expiry_datetime = obj.date_of_expiry
        else:
            # It's a date object, convert to datetime
            from datetime import datetime, time
            expiry_datetime = timezone.make_aware(
                datetime.combine(obj.date_of_expiry, time.max)
            )
        
        if expiry_datetime < current_time:
            delta = current_time - expiry_datetime
            return format_html(
                '<span style="color: red;">Expired {} days ago</span>',
                delta.days
            )
        else:
            delta = expiry_datetime - current_time
            days = delta.days
            if days == 0:
                return format_html('<span style="color: orange;">Expires today</span>')
            elif days <= 7:
                return format_html('<span style="color: orange;">{} days</span>', days)
            else:
                return format_html('<span style="color: green;">{} days</span>', days)
    days_remaining.short_description = 'Days Remaining'
    
    # Custom actions for bulk operations
    actions = ['mark_as_expired', 'extend_expiry_30_days', 'extend_expiry_90_days']
    
    def mark_as_expired(self, request, queryset):
        """
        Mark selected premium content as expired
        Sets the expiry date to current time for selected records
        """
        current_time = timezone.now()
        updated = queryset.update(date_of_expiry=current_time)
        self.message_user(
            request,
            f'{updated} premium content records marked as expired.'
        )
    mark_as_expired.short_description = "Mark selected items as expired"
    
    def extend_expiry_30_days(self, request, queryset):
        """
        Extend expiry by 30 days for selected records
        Useful for extending access to premium content
        """
        from datetime import timedelta
        for obj in queryset:
            obj.date_of_expiry += timedelta(days=30)
            obj.save()
        self.message_user(
            request,
            f'{queryset.count()} premium content records extended by 30 days.'
        )
    extend_expiry_30_days.short_description = "Extend expiry by 30 days"
    
    def extend_expiry_90_days(self, request, queryset):
        """
        Extend expiry by 90 days for selected records
        Useful for long-term extensions of premium content access
        """
        from datetime import timedelta
        for obj in queryset:
            obj.date_of_expiry += timedelta(days=90)
            obj.save()
        self.message_user(
            request,
            f'{queryset.count()} premium content records extended by 90 days.'
        )
    extend_expiry_90_days.short_description = "Extend expiry by 90 days"
    
    # Custom queryset for better performance
    def get_queryset(self, request):
        """
        Optimize queryset with select_related for better performance
        Reduces database queries by prefetching related objects
        """
        queryset = super().get_queryset(request)
        return queryset.select_related('student', 'publisher_id')
    
    def get_search_results(self, request, queryset, search_term):
        """
        Enhanced search functionality with multiple search parameters
        Allows searching across multiple fields with improved logic
        """
        # Start with the base queryset
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        
        # If no search term, return the original queryset
        if not search_term:
            return queryset, use_distinct
        
        # Create a Q object for complex search queries
        search_query = Q()
        
        # Search in student-related fields
        search_query |= Q(student__full_name__icontains=search_term)
        search_query |= Q(student__user__email__icontains=search_term)
        
        # Search in content-related fields
        search_query |= Q(content_name__icontains=search_term)
        search_query |= Q(content_id__icontains=search_term)
        
        # Search in publisher-related fields
        search_query |= Q(publisher_name__icontains=search_term)
        search_query |= Q(publisher_id__full_name__icontains=search_term)
        
        # Search in subject and class fields
        search_query |= Q(subject_name__icontains=search_term)
        search_query |= Q(Class__icontains=search_term)
        search_query |= Q(type__icontains=search_term)
        
        # Apply the search query
        queryset = queryset.filter(search_query)
        
        return queryset, True


class ExpiryStatusFilter(admin.SimpleListFilter):
    """
    Custom filter for expiry status
    Provides filtering options for active, expired, and expiring content
    """
    title = 'Expiry Status'
    parameter_name = 'expiry_status'
    
    def lookups(self, request, model_admin):
        """
        Define the filter options available in the admin interface
        """
        return (
            ('active', 'Active'),
            ('expired', 'Expired'),
            ('expiring_soon', 'Expiring in 7 days'),
            ('expiring_today', 'Expiring today'),
        )
    
    def queryset(self, request, queryset):
        """
        Apply the selected filter to the queryset
        Filters records based on their expiry status
        """
        current_time = timezone.now()
        
        if self.value() == 'active':
            # Show only active (non-expired) content
            return queryset.filter(date_of_expiry__gte=current_time)
        
        elif self.value() == 'expired':
            # Show only expired content
            return queryset.filter(date_of_expiry__lt=current_time)
        
        elif self.value() == 'expiring_soon':
            # Show content expiring within 7 days
            from datetime import timedelta
            seven_days_later = current_time + timedelta(days=7)
            return queryset.filter(
                date_of_expiry__gte=current_time,
                date_of_expiry__lte=seven_days_later
            )
        
        elif self.value() == 'expiring_today':
            # Show content expiring today
            from datetime import timedelta
            tomorrow = current_time + timedelta(days=1)
            return queryset.filter(
                date_of_expiry__gte=current_time,
                date_of_expiry__lt=tomorrow
            )
