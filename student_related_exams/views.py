from .models import DoneExams
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from .serializers import DoneExamsSerializer, GetExamsDone 

from .models import DoneExams  


class ExamDoneRecord(ListCreateAPIView):
    """
    Generic view for listing and creating exam completion records
    Provides standard CRUD operations for DoneExams model
    """
    queryset = []
    serializer_class = DoneExamsSerializer
  

@api_view(['GET'])
def get_exams_done_by_student_id(request, id):
    """
    Get all exams completed by a specific student with pagination
    Returns paginated list of exams that the student has completed
    """
    # Get pagination parameters from query string
    count = request.GET.get('count')
    limit = request.GET.get('limit')

    # Filter exams by student ID to get all exams completed by this student
    exams = DoneExams.objects.filter(student=id)

    # Serialize the filtered exam data
    serial = GetExamsDone(exams, many=True)
  
    # Apply pagination to the results
    begin = (int(count) - 1) * int(limit)
    end = int(count) * int(limit)
 
    return Response({
        'exams': serial.data[begin:end], 
        'number_of_exams': len(serial.data)
    }, status=200)

 