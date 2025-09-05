from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from django.shortcuts import get_object_or_404
from .models import StudentReadNotes
from .serializers import (
    StudentReadNotesSerializer, 
    CreateStudentReadNotesSerializer,
    StudentReadNotesPreviewSerializer
)

@api_view(['POST'])
def create_student_read_note(request):
    """
    Create a new instance of StudentReadNotes
    Handles both creation of new read records and updating existing ones
    Tracks student reading behavior and increments read counts
    """
    try:
        # Copy request data to avoid modifying original data
        data = request.data.copy()
        
        # Check if student already has a read record for this note
        # This prevents duplicate records and allows incrementing existing ones
        existing_record = StudentReadNotes.objects.filter(
            student=data.get('student'),
            note_id=data.get('note_id')
        ).first()
        
        if existing_record:
            # If record exists, increment reads using the model method
            existing_record.increment_reads()
            serializer = StudentReadNotesSerializer(existing_record)
            return Response(
                {
                    "message": "تم زيادة عدد القراءات بنجاح",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        else:
            # Create new record if it doesn't exist
            serializer = CreateStudentReadNotesSerializer(data=data)
            if serializer.is_valid():
                # Save the new record to database
                serializer.save()
                # Get the created instance with full data for response
                created_instance = StudentReadNotes.objects.get(id=serializer.instance.id)
                full_serializer = StudentReadNotesSerializer(created_instance)
                return Response(
                    {
                        "message": "تم إنشاء سجل قراءة الطالب بنجاح",
                        "data": full_serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                # Return validation errors if data is invalid
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
                
    except Exception as e:
        return Response(
            {"error": f"فشل في إنشاء سجل قراءة الطالب: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def increase_number_of_reads(request, id):
    """
    Increase the number of reads for a specific StudentReadNotes instance
    Used for incrementing read counts on existing records
    """
    try:
        # Get the read note record or return 404 if not found
        read_note = get_object_or_404(StudentReadNotes, id=id)
        
        # Increment the read count using the model method
        read_note.increment_reads()
        
        return Response(
            {"message": "تم زيادة عدد القراءات بنجاح"},
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        return Response(
            {"error": f"فشل في زيادة القراءات: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_read_notes(request, student_id):
    """
    Get StudentReadNotes for a specific student with pagination
    Returns paginated list of notes read by the student
    Follows the same pagination pattern as other apps
    """
    try:
        # Get query parameters for pagination
        count = request.GET.get('count', 1)
        limit = request.GET.get('limit', 10)
        
        # Filter read notes by student ID
        # This gets all notes that the student has read
        queryset = StudentReadNotes.objects.filter(student_id=student_id)
        
        # Serialize the data using preview serializer
        serializer = StudentReadNotesPreviewSerializer(queryset, many=True)
        
        # Apply pagination to the results
        try:
            count = int(count)
            limit = int(limit)
            begin = (count - 1) * limit
            end = count * limit
            
            # Ensure pagination bounds are within data length
            begin = min(begin, len(serializer.data))
            end = min(end, len(serializer.data))
            
            paginated_data = serializer.data[begin:end]
        except (ValueError, TypeError):
            # If pagination parameters are invalid, return all data
            paginated_data = serializer.data
            count = 1
            limit = 7
        
        return Response(
            {
                'read_notes': paginated_data,
                'number_of_read_notes': len(serializer.data),
            },
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        return Response(
            {"error": f"فشل في استرجاع الملاحظات المقروءة: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Generic views for CRUD operations
class StudentReadNotesListCreateView(ListCreateAPIView):
    """
    Generic view for listing and creating StudentReadNotes
    Provides standard CRUD operations with automatic serializer selection
    """
    queryset = StudentReadNotes.objects.all()
    serializer_class = StudentReadNotesSerializer
    
    def get_serializer_class(self):
        """
        Dynamically select serializer based on HTTP method
        Uses CreateStudentReadNotesSerializer for POST requests
        Uses StudentReadNotesSerializer for GET requests
        """
        if self.request.method == 'POST':
            return CreateStudentReadNotesSerializer
        return StudentReadNotesSerializer
