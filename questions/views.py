from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status
from .models import Questions, QuestionImages
from .serializers import QuestionSerializer, QuestionImageSerializer   
from rest_framework import generics  
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.
 
@api_view(['GET']) 
def get_all_questions(request, package_id):
    """
    Get all questions for a specific package
    Returns all questions associated with the given package ID
    """
    # Filter questions by package ID and order by question ID
    obj = Questions.objects.filter(package_id=package_id).order_by('id') 

    # Serialize the filtered questions data
    serial = QuestionSerializer(obj, many=True) 

    return Response(serial.data)

# Generic views for CRUD operations
class add_questions(generics.ListCreateAPIView):
    """
    Generic view for listing and creating questions
    Provides standard CRUD operations for Questions model
    """
    # permission_classes = (IsAuthenticated,)
    queryset = Questions.objects.all()
    serializer_class = QuestionSerializer


@api_view(['PUT'])
def edit_question_by_id(request, id):
    """
    Edit a specific question by its ID
    Updates question content, options, explanation, and correct answer
    """
    # Copy request data to avoid modifying original data
    data = request.data.copy()
    print("data is ", data)
    
    # Get the question object by ID
    obj = Questions.objects.get(id=id)
    
    try:
        # Update question fields with new data
        obj.test_content = data['test_content']
        obj.option_A = data['option_A']
        obj.option_B = data['option_B']
        obj.option_C = data['option_C']
        obj.option_D = data['option_D']
        obj.option_E = data['option_E']
        obj.explanation = data['explanation']
        obj.right_answer = data['right_answer']
        
        # Save the updated question
        obj.save()
        
        return Response('تم تعديل السؤال بنجاح', status=200)
   
    except Exception as e:
        return Response('فشل في تعديل السؤال', status=500)


@api_view(['DELETE'])
def delete_question_by_id(request, id):
    """
    Delete a specific question by its ID
    Removes the question and all related images from the database
    """
    try:
        # Get the question object or return 404 if not found
        question = get_object_or_404(Questions, id=id)
        
        # Delete the question (this will also delete related QuestionImages due to CASCADE)
        question.delete()
        
        return Response('تم حذف السؤال بنجاح', status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response('فشل في حذف السؤال', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddQuestionImages(generics.ListCreateAPIView):
    """
    Generic view for listing and creating question images
    Handles file uploads for question images
    """
    # Configure parsers for handling file uploads
    parser_classes = (MultiPartParser, FormParser)
    queryset = QuestionImages.objects.all()
    serializer_class = QuestionImageSerializer

@api_view(['GET'])
def get_question_images(request, test_id):
    """
    Get question images for a specific test and field name
    Returns images associated with a particular field of a question
    """
    # Get the field name from query parameters
    field_name = request.GET.get('field_name')
    
    # Filter images by test ID and field name
    obj = QuestionImages.objects.filter(test_id=test_id, field_name=field_name)
    
    # Serialize the filtered images data
    serial = QuestionImageSerializer(obj, many=True)
    
    return Response(serial.data, status=200)
 

@api_view(['GET'])
def get_all_question_images(request, test_id):
    """
    Get all question images for a specific test
    Returns all images associated with the given test ID
    """
    # Filter all images by test ID and order by image ID
    obj = QuestionImages.objects.filter(test_id=test_id).order_by('id')
    
    # Serialize the filtered images data
    serial = QuestionImageSerializer(obj, many=True)
    
    return Response(serial.data, status=200)
 
 