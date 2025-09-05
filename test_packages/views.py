from .models import TestPackage
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import TestPackageSerializer, CreatePackages, TestPackageDetailsSerializer
from student_related_exams.models import DoneExams
from student_related_exams.serializers import GetSolvedSerializer 
from rest_framework import generics  
from django.shortcuts import get_object_or_404 

@api_view(['GET']) 
def get_all_packages(request, subject_name):
    """
    Get all test packages for a specific subject with filtering and pagination
    Allows filtering by price, number of questions, and sorting options
    """
    # Get query parameters for filtering and pagination
    price = request.GET.get('price')
    limit = request.GET.get('limit')
    count = request.GET.get('count')
    unit = request.GET.get('unit')    
    number_of_questions = request.GET.get('number_of_questions')
    publisher_name = request.GET.get('publisher_name')
    name = request.GET.get('name')
 
    # Filter packages by subject, price, and number of questions
    obj = TestPackage.objects.filter(
        subject_name=subject_name, 
        price__lte=price, 
        number_of_questions__lte=number_of_questions
    )
    
    if name is not None:
        obj = obj.filter(package_name__icontains=name)
    
    
    if publisher_name is not None:
        obj = obj.filter(publisher_name__icontains=publisher_name)
    
    # Add unit filter if unit parameter is provided
    if unit is not None and unit != "عرض الكل":
        obj = obj.filter(units__icontains=unit)
    
 
    # Count total number of exams matching the criteria
    number_of_exams = obj.count()

 
    # Serialize the filtered data
    serial = TestPackageSerializer(obj, many=True)

    # Apply pagination
    begin = (int(count) - 1) * int(limit)
    end = int(count) * int(limit) 
 
    # Ensure pagination bounds are within data length
    begin = min(begin, len(serial.data))
    end = min(end, len(serial.data))
 
    return Response({
        'exams': serial.data[begin:end], 
        'number_of_exams': number_of_exams
    }, status=200)


@api_view(['GET']) 
def get_student_solved_exams(request, subject_name):
    """
    Get all exams solved by a specific student for a given subject
    Returns unique exam IDs that the student has completed
    """
    # Get student ID from query parameters
    user_id = request.GET.get('user_id')

    # Get unique exam IDs that the student has solved for this subject
    user_solved_exams = DoneExams.objects.filter(
        student=user_id, 
        subject_name=subject_name
    ).values('exam_id').distinct()
    
    # Serialize the solved exams data
    serial = GetSolvedSerializer(user_solved_exams, many=True)
  
    return Response(serial.data, status=200)
  
  
# Primary info about the package 
@api_view(['GET']) 
def get_package_details(request, id):
    """
    Get detailed information about a specific test package
    Returns comprehensive package details using TestPackageDetailsSerializer
    """
    # Get the test package by ID
    obj = TestPackage.objects.get(id=id)

    # Serialize with detailed serializer
    serial = TestPackageDetailsSerializer(obj)

    return Response(serial.data, status=200)
 
 
@api_view(['GET']) 
def get_package_info(request, id):
    """
    Get basic information about a specific test package
    Returns basic package information using TestPackageSerializer
    """
    # Get the test package by ID
    obj = TestPackage.objects.filter(id=id)

    # Serialize with basic serializer
    serial = TestPackageSerializer(obj, many=True)

    return Response(serial.data, status=200)
 

@api_view(['PUT']) 
def increase_num_of_apps(request, id):
    """
    Increment the number of applications for a test package
    Tracks how many times the package has been accessed
    """
    # Get the test package by ID
    obj = TestPackage.objects.get(id=id)
    
    # Increment the applications counter
    obj.number_of_apps += 1
    obj.save()

    return Response('تم تحديث عدد التطبيقات بنجاح', status=200)
 
 
@api_view(['PUT']) 
def increase_num_of_purchases(request, id):
    """
    Increment the number of purchases for a test package
    Tracks how many times the package has been purchased
    """
    # Get the test package by ID
    obj = TestPackage.objects.get(id=id)
    
    # Increment the purchases counter
    obj.number_of_purchases += 1
    obj.save()

    return Response('تم تحديث عدد المشتريات بنجاح', status=200)
    
# Generic views for CRUD operations
class create_test_packages(generics.ListCreateAPIView):
    """
    Generic view for listing and creating test packages
    Provides GET (list) and POST (create) functionality
    """
    queryset = TestPackage.objects.all()
    serializer_class = CreatePackages

 
@api_view(['GET'])
def get_packages_by_publisher(request, id):
    """
    Get all test packages published by a specific publisher
    Supports pagination for large result sets
    """
    # Get pagination parameters
    limit = request.GET.get('limit')
    count = request.GET.get('count')

    # Set up filter for publisher ID
    filters = {'publisher_id': id}
 
    # Filter packages by publisher
    obj = TestPackage.objects.filter(**filters)
    number_of_exams = obj.count()

    # Serialize the filtered data
    serial = TestPackageSerializer(obj, many=True)

    # Apply pagination if parameters are provided
    if limit is not None and count is not None:
        try:
            limit = int(limit)
            count = int(count)
            begin = (count - 1) * limit
            end = count * limit
            begin = min(begin, len(serial.data))
            end = min(end, len(serial.data))
            exams = serial.data[begin:end]
        except Exception:
            # If pagination fails, return all data
            exams = serial.data
    else:
        exams = serial.data

    return Response({
        'exams': exams, 
        'number_of_exams': number_of_exams
    }, status=200)

@api_view(['PUT'])
def edit_test_package(request, id):
    """
    Edit a test package by its ID
    Allows partial updates of package information
    """
    try:
        # Get the test package or return 404 if not found
        test_package = get_object_or_404(TestPackage, id=id)
        
        # Validate and update the package data
        serializer = CreatePackages(test_package, data=request.data, partial=True)
        
        if serializer.is_valid():
            # Save the updated package
            serializer.save()
            return Response({
                'message': 'تم تحديث حزمة الاختبار بنجاح',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'البيانات المقدمة غير صحيحة',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'message': 'خطأ في تحديث حزمة الاختبار',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_test_package(request, id):
    """
    Delete a test package by its ID
    Permanently removes the package from the database
    """
    try:
        # Get the test package or return 404 if not found
        test_package = get_object_or_404(TestPackage, id=id)
        package_name = test_package.package_name
        
        # Delete the package
        test_package.delete()
        
        return Response({
            'message': f'تم حذف حزمة الاختبار "{package_name}" بنجاح'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'message': 'خطأ في حذف حزمة الاختبار',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
 
 
 

  