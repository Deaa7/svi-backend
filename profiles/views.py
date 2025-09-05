from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Profile_Teacher, Profile_Student
from users.models import User
from django.db.models import Q
from .serializers import ProfileTeacherSerializer, TeacherPreviewSerializer, StudentOwnProfile, StudentProfileUpdateSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from test_packages.models import TestPackage
from notes.models import Notes

# Create your views here.

@api_view(['GET'])
def get_teacher_preview(request):
    """
    Get a filtered preview of teachers based on search criteria
    Returns paginated list of teachers matching the specified filters
    """
    # Get query parameters for filtering
    Class = request.GET.get('Class')
    subject_name = request.GET.get('subject_name')
    city = request.GET.get('city')
    count = request.GET.get('count')
    limit = request.GET.get('limit')
    name = request.GET.get('name')

    # Filter teachers by class (including those who teach both 9 and 12)
    result = Profile_Teacher.objects.filter(Q(Class=Class) | Q(Class='9_12'))
    
    if name is not None:
        result = result.filter(full_name__icontains=name)
    
    # Apply city filter if not 'all'
    if city != 'all':
        result = result.filter(city=city)
    
    # Apply subject filter if not 'عرض الكل' (Show All)
    if subject_name != 'عرض الكل':
        # Special handling for physics and chemistry (can be combined)
        if subject_name == 'physics' or subject_name == 'chemistry':
            result = result.filter(Q(studying_subjects=subject_name) | Q(studying_subjects='physics_chemistry'))
        else:
            result = result.filter(studying_subjects=subject_name)
    
    # Serialize the filtered teacher data
    serial = TeacherPreviewSerializer(result, many=True)

    # Apply pagination
    begin = (int(count) - 1) * int(limit)
    end = int(count) * int(limit)

    return Response({'teacher_preview': serial.data[begin:end], 'number': len(serial.data)}, status=200)


@api_view(['GET'])
def get_teacher_info(request, id):
    """
    Get detailed information about a specific teacher
    Returns complete teacher profile data
    """
    # Get the teacher profile by user ID
    query = Profile_Teacher.objects.get(user=id)
    
    # Serialize the teacher data
    serial = ProfileTeacherSerializer(query)

    return Response(serial.data, status=200)


@api_view(['POST'])
def increase_number_of_teacher_exams(request, id):
    """
    Increase the exam count for a specific teacher
    Increments the teacher's exam counter by 1
    """
    # Get the teacher profile by user ID
    obj = Profile_Teacher.objects.get(user=id)
    
    # Increment the exam count
    obj.number_of_exams += 1
    
    # Save the updated profile
    obj.save()
    
    return Response('تم زيادة عدد اختبارات المعلم بنجاح', status=200)


@api_view(['POST'])
def decrease_number_of_teacher_exams(request, id):
    """
    Decrease the exam count for a specific teacher
    Decrements the teacher's exam counter by 1
    """
    # Get the teacher profile by user ID
    obj = Profile_Teacher.objects.get(user=id)
    
    # Decrement the exam count
    obj.number_of_exams -= 1
    
    # Save the updated profile
    obj.save()
    
    return Response('تم تقليل عدد اختبارات المعلم بنجاح', status=200)


@api_view(['POST'])
def increase_number_of_teacher_notes(request, id):
    """
    Increase the notes count for a specific teacher
    Increments the teacher's notes counter by 1
    """
    # Get the teacher profile by user ID
    obj = Profile_Teacher.objects.get(user=id)
    
    # Increment the notes count
    obj.number_of_notes += 1
    
    # Save the updated profile
    obj.save()
    
    return Response('تم زيادة عدد ملاحظات المعلم بنجاح', status=200)


@api_view(['POST'])
def decrease_number_of_teacher_notes(request, id):
    """
    Decrease the notes count for a specific teacher
    Decrements the teacher's notes counter by 1
    """
    # Get the teacher profile by user ID
    obj = Profile_Teacher.objects.get(user=id)
    
    # Decrement the notes count
    obj.number_of_notes -= 1
    
    # Save the updated profile
    obj.save()
    
    return Response('تم تقليل عدد ملاحظات المعلم بنجاح', status=200)


class UpdateTeacherProfile(APIView):
    """
    API view for updating teacher profile information
    Handles file uploads for profile images
    """
    # Configure parsers for handling file uploads
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, id, *args, **kwargs):
        """
        Update teacher profile with new information
        Handles both text data and image file uploads
        """
        try:
            # Get the teacher profile by user ID
            teacher = Profile_Teacher.objects.get(user=id)
            
            # Copy request data to avoid modifying original data
            data = request.data.copy()

            # Update teacher profile fields
            teacher.phone_number = data['phone_number']
            teacher.another_phone_number = data['another_phone_number']
            teacher.teaching_in_school = data['teaching_in_school']
            teacher.teaching_in_institutions = data['teaching_in_institutions']
            teacher.bio = data['bio']
            teacher.facebook_link = data['facebook_link']
            teacher.instagram_link = data['instagram_link']
            teacher.whatsapp_link = data['whatsapp_link']
            teacher.telegram_link = data['telegram_link']
            teacher.studying_subjects = data['studying_subjects']
            teacher.city = data['city']
            teacher.Class = data['Class']
            
            # Handle image upload if provided
            if request.FILES:
                teacher.image = request.FILES['image']

            # Save the updated profile
            teacher.save()

            return Response('تم تحديث الملف الشخصي بنجاح', status=200)
        
        except Exception as e:
            print('here is error ', e)
            return Response('فشل في تحديث الملف الشخصي', status=405)


class UpdateStudentProfile(APIView):
    """
    API view for updating student profile information
    Uses serializer for validation and data handling
    """
    
    def post(self, request, id, *args, **kwargs):
        """
        Update student profile with new information
        Validates data using serializer before saving
        """
        try:
            # Get the student profile by user ID
            student = Profile_Student.objects.get(user=id)
            
            # Use serializer for validation and data handling
            serializer = StudentProfileUpdateSerializer(student, data=request.data, partial=True)
            
            if serializer.is_valid():
                # Save the validated data
                serializer.save()
                return Response({
                    'message': 'تم تحديث الملف الشخصي للطالب بنجاح',
                    'data': serializer.data
                }, status=200)
            else:
                return Response({
                    'message': 'فشل في التحقق من صحة البيانات',
                    'errors': serializer.errors
                }, status=400)
        
        except Profile_Student.DoesNotExist:
            return Response({
                'message': 'لم يتم العثور على الملف الشخصي للطالب'
            }, status=404)
        except Exception as e:
            print('Error updating student profile:', e)
            return Response({
                'message': 'فشل في التحديث',
                'error': str(e)
            }, status=500)


################################################ student apis:

@api_view(['GET'])
def get_student_own_profile_info(request, id):
    """
    Get student's own profile information
    Returns student profile data for the specified user ID
    """
    # Get the student profile by user ID
    student = Profile_Student.objects.get(user=id)

    # Serialize the student profile data
    serial = StudentOwnProfile(student)
    return Response(serial.data, status=200)


@api_view(['GET'])
def check_student_balance(request):
    """
    Check if a student has sufficient balance to purchase content
    If sufficient, deducts the amount from student's balance
    Query parameters:
    - student_id: ID of the student
    - price: Required amount to check against balance
    """
    try:
        # Get query parameters
        student_id = request.GET.get('student_id')
        price = request.GET.get('price')
        
        # Validate required parameters
        if not student_id or not price:
            return Response(
                {
                    "error": "البيانات المطلوبة مفقودة. يرجى توفير معرف الطالب والسعر"
                },
                status=400
            )
        
        # Convert parameters to integers
        try:
            student_id = int(student_id)
            price = int(price)
        except ValueError:
            return Response(
                {
                    "error": "تنسيق غير صحيح. يجب أن يكون معرف الطالب والسعر أرقام صحيحة"
                },
                status=400
            )
        
        # Validate price is positive
        if price < 0:
            return Response(
                {
                    "error": "يجب أن يكون السعر رقم موجب"
                },
                status=400
            )
        
        # Get student profile
        try:
            student = Profile_Student.objects.get(user_id=student_id)
        except Profile_Student.DoesNotExist:
            return Response(
                {
                    "error": "لم يتم العثور على الطالب"
                },
                status=404
            )
        
        # Check if balance is sufficient
        has_sufficient_balance = student.balance >= price
        
        if has_sufficient_balance:
            # Decrease the student's balance by the price
            student.balance -= price
            student.save()
            
            return Response(
                {
                    "has_sufficient_balance": True,
                    "balance_decreased": True,
                    "previous_balance": student.balance + price,
                    "new_balance": student.balance,
                    "amount_deducted": price,
                    "student_id": student_id,
                    "student_name": student.full_name
                },
                status=200
            )
        else:
            return Response(
                {
                    "has_sufficient_balance": False,
                    "balance_decreased": False,
                    "current_balance": student.balance,
                    "required_price": price,
                    "student_id": student_id,
                    "student_name": student.full_name
                },
                status=200
            )
        
    except Exception as e:
        return Response(
            {"error": f"فشل في التحقق من رصيد الطالب: {str(e)}"},
            status=500
        ) 

 