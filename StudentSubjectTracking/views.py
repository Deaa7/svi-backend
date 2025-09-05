from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import StudentSubjectTracking
from .serializers import StudentSubjectTrackingSerializer


class StudentSubjectTrackingCreateView(generics.CreateAPIView):
    """
    Create a new subject tracking instance for a student
    Handles both creation of new tracking records and updating existing ones
    Tracks the number of notes and exams completed by students for each subject
    """
    permission_classes = [IsAuthenticated]
    serializer_class = StudentSubjectTrackingSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Custom create method to handle increase logic
        Manages both creation of new records and updating existing ones
        """
        # Step 1: Get the 'increase' property to determine what to increment
        # This determines whether to increase note count or exam count
        increase_type = request.data.get('increase', 'note')  # Default to 'note' if not specified
        
        # Step 2: Validate that the increase type is valid
        # Only 'note' and 'exam' are allowed as valid increase types
        if increase_type not in ['note', 'exam']:
            return Response({
                'error': 'خاصية الزيادة يجب أن تكون إما "note" أو "exam"'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Step 3: Extract data from request
        # Get the essential data needed for tracking
        student_id = request.data.get('student')
        subject_name = request.data.get('subject_name')
        Class = request.data.get('Class')
        
        # Step 4: Validate required fields
        # Ensure all necessary fields are provided
        if not all([student_id, subject_name, Class]):
            return Response({
                'error': 'الطالب واسم المادة والفصل مطلوبة'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Step 5: Check if tracking record already exists
        # Look for existing record with same student, subject, and class
        existing = StudentSubjectTracking.objects.filter(
            student_id=student_id,
            subject_name=subject_name,
            Class=Class
        ).first()
        
        if existing:
            # SCENARIO A: Record already exists - UPDATE it
            # Increment the appropriate counter based on increase_type
            if increase_type == 'note':
                existing.number_of_notes += 1
            else:  # increase_type == 'exam'
                existing.number_of_exams += 1
            
            # Save the updated record
            existing.save()
            
            # Create response serializer for the updated record
            response_serializer = self.get_serializer(existing)
            
            return Response({
                'message': f'تم تحديث السجل الموجود: زيادة عدد {increase_type} بمقدار 1',
                'data': response_serializer.data
            }, status=status.HTTP_200_OK)
        else:
            # SCENARIO B: Record doesn't exist - CREATE it
            # Prepare data for new record with initial counts
            new_data = {
                'student': student_id,
                'subject_name': subject_name,
                'Class': Class,
                'number_of_notes': 1 if increase_type == 'note' else 0,
                'number_of_exams': 1 if increase_type == 'exam' else 0
            }
            
            # Validate the data using the serializer
            serializer = self.get_serializer(data=new_data)
            serializer.is_valid(raise_exception=True)
            
            # Save the new record to the database
            instance = serializer.save()
            
            return Response({
                'message': f'تم إنشاء سجل جديد مع عدد {increase_type} أولي يساوي 1',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)


class StudentSubjectTrackingByStudentClassView(generics.ListAPIView):
    """
    Retrieve all tracking records by student and class
    Returns a list of subject tracking records for a specific student and class
    Includes related student data for comprehensive information
    """
    permission_classes = [IsAuthenticated]
    serializer_class = StudentSubjectTrackingSerializer
    
    def get_queryset(self):
        """
        Get filtered queryset based on student and class parameters
        Optimizes database queries by using select_related
        """
        # Extract student_id and Class from the URL parameters
        student_id = self.kwargs.get('student_id')
        Class = self.kwargs.get('Class')
        
        # Return filtered queryset with related student data
        # select_related('student') prevents N+1 query problem by fetching student data in one query
        return StudentSubjectTracking.objects.filter(
            student_id=student_id,
            Class=Class
        ).select_related('student').order_by('subject_name')
