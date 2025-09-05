from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.utils import timezone
from .models import StudentPremiumContent
from .serializers import (
    StudentPremiumContentSerializer,
    StudentPremiumContentPreviewSerializer,
    CreateStudentPremiumContentSerializer,
)    
from profiles.models import Profile_Student, Profile_Teacher


@api_view(['GET'])
def get_premium_content_by_student(request, student_id):
    """
    Get premium content for a specific student with pagination following the same pattern as other apps
    """
    try:
        # Get query parameters for pagination and filtering
        count = request.GET.get('count', 1)
        limit = request.GET.get('limit', 10)
        
        # Filter premium content by student ID
        queryset = StudentPremiumContent.objects.filter(student_id=student_id)
        
        # Serialize the data
        serializer = StudentPremiumContentPreviewSerializer(queryset, many=True)
        
        # Apply pagination
        try:
            count = int(count)
            limit = int(limit)
            begin = (count - 1) * limit
            end = count * limit
            
            # Ensure bounds are within data length
            begin = min(begin, len(serializer.data))
            end = min(end, len(serializer.data))
            
            paginated_data = serializer.data[begin:end]
        except (ValueError, TypeError):
            # If pagination parameters are invalid, return all data
            paginated_data = serializer.data
        
        return Response(
            {
                'premium_content': paginated_data,
                'number_of_premium_content': len(serializer.data)
            },
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        return Response(
            {"error": f"فشل في استرجاع المحتوى المميز: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_premium_content_details(request, id):
    """
    Get detailed information for a specific premium content record
    """
    try:
        # Find the premium content or return 404 if not found
        premium_content = get_object_or_404(StudentPremiumContent, id=id)
        
        # Serialize the data
        serializer = StudentPremiumContentSerializer(premium_content)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": f"فشل في استرجاع تفاصيل المحتوى المميز: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# @api_view(['POST'])
# def create_premium_content(request):
#     """
#     Create a new premium content record for a student
#     """
#     try:
#         # Copy request data to avoid modifying original data
#         data = request.data.copy()
        
#         # Create serializer object to validate data
#         serializer = CreateStudentPremiumContentSerializer(data=data)
        
#         if serializer.is_valid():
#             # Save data to database
#             serializer.save()
            
#             # Get the created instance with full data
#             created_instance = StudentPremiumContent.objects.get(id=serializer.instance.id)
#             full_serializer = StudentPremiumContentSerializer(created_instance)
            
#             return Response(
#                 {
#                     "message": "تم إنشاء المحتوى المميز بنجاح",
#                     "data": full_serializer.data
#                 },
#                 status=status.HTTP_201_CREATED
#             )
#         else:
#             return Response(
#                 serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
            
#     except Exception as e:
#         return Response(
#             {"error": f"فشل في إنشاء المحتوى المميز: {str(e)}"},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )


@api_view(['POST'])
def create_premium_content_with_balance_check(request):
    """
    Create a new premium content record for a student with balance validation.
    This endpoint checks if the student has sufficient balance, deducts it, and creates the premium content.
    """
    try:
        # Copy request data to avoid modifying original data
        data = request.data.copy()
        
        # Validate required fields
        required_fields = ['student', 'price', 'content_id', 'content_name', 'type', 'subject_name', 'Class', 'publisher_id', 'publisher_name', 'date_of_expiry']
        for field in required_fields:
            if field not in data:
                return Response(
                    {
                        "error": f"الحقل المطلوب مفقود: {field}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Get student profile and check if exists
        try:
            student = Profile_Student.objects.get(user_id=data['student'])
        except Profile_Student.DoesNotExist:
            return Response(
                {
                    "error": "لم يتم العثور على الطالب"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Convert price to integer for comparison
        try:
            price = int(data['price'])
        except (ValueError, TypeError):
            return Response(
                {
                    "error": "تنسيق السعر غير صحيح. يجب أن يكون السعر رقماً"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if student has sufficient balance
        if student.balance < price:
            return Response(
                {
                    "success": False,
                    "error": "رصيد غير كافي",
                    "current_balance": student.balance,
                    "required_price": price,
                    "student_id": student.user_id,
                    "student_name": student.full_name
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        
        # Deduct balance from student account
        previous_balance = student.balance
        student.balance -= price
        student.save()
        
        # Create premium content record
        serializer = CreateStudentPremiumContentSerializer(data=data)
        
        if serializer.is_valid():
            # Save premium content to database
            premium_content = serializer.save()
            
            # Increase teacher balance by 70% of the price
            try:
                # Find teacher profile using publisher ID
                teacher = Profile_Teacher.objects.get(user_id=data['publisher_id'])
                
                # Calculate teacher commission (70% of price)
                teacher_commission = int(price * 0.7)
                
                # Add commission to teacher's total net earnings
                teacher.total_net += teacher_commission
                teacher.save()
            except Profile_Teacher.DoesNotExist:
                # Log the error but don't fail the transaction
                pass
            except Exception as e:
                # Log the error but don't fail the transaction
                pass
            
            # Get the created instance with full data
            created_instance = StudentPremiumContent.objects.get(id=premium_content.id)
            full_serializer = StudentPremiumContentSerializer(created_instance)
            
            return Response(
                {
                    "success": True,
                    "message": "تم إنشاء المحتوى المميز بنجاح",
                    "balance_deducted": True,
                    "previous_balance": previous_balance,
                    "new_balance": student.balance,
                    "amount_deducted": price,
                    "teacher_commission_added": teacher_commission if 'teacher_commission' in locals() else None,
                    "premium_content": full_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            # If premium content creation fails, refund the balance
            student.balance = previous_balance
            student.save()
            
            return Response(
                {
                    "success": False,
                    "error": "فشل في إنشاء المحتوى المميز",
                    "validation_errors": serializer.errors,
                    "balance_refunded": True
                },
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        # If any error occurs, try to refund the balance if it was deducted
        if 'student' in locals() and 'previous_balance' in locals():
            try:
                student.balance = previous_balance
                student.save()
            except:
                pass
        
        return Response(
            {"error": f"فشل في إنشاء المحتوى المميز: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def check_premium_access(request, student_id, content_id , content_type):
    """
    Check if a student has premium access to specific content.
    If the content exists but is expired, return has_access: false
    """
    
    try:
        # Get current time
        current_time = timezone.now()
        
        # First, check if the student has any premium content record for this content
        premium_content = StudentPremiumContent.objects.filter(
            student_id=student_id,
            content_id=content_id ,
            type = content_type,
        ).first()
        
        if premium_content:
            # Check if the content has expired
            if premium_content.date_of_expiry < current_time:
                # Content has expired, return false access
                return Response(
                    {
                        "has_access": False,
                        "reason": "انتهت صلاحية المحتوى المميز",
                        "expiry_date": premium_content.date_of_expiry
                    },
                    status=status.HTTP_200_OK
                )
            else:
                # Content is still valid, return true access
                serializer = StudentPremiumContentSerializer(premium_content)
                return Response(
                    {
                        "has_access": True,
                        "premium_content": serializer.data
                    },
                    status=status.HTTP_200_OK
                )
        else:
            # No premium content record found for this student and content
            return Response(
                {
                    "has_access": False,
                    "reason": "لم يتم العثور على محتوى مميز"
                },
                status=status.HTTP_200_OK
            )
            
    except Exception as e:
        return Response(
            {"error": f"فشل في التحقق من الوصول للمحتوى المميز: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def check_content_purchase(request):
    """
    Check if a student has purchased a specific content by type and content ID.
    Query parameters:
    - student_id: ID of the student
    - content_type: Type of content ("exam" or "note")
    - content_id: ID of the specific content
    """
    try:
        # Get query parameters
        student_id = request.GET.get('student_id')
        content_type = request.GET.get('content_type')
        content_id = request.GET.get('content_id')
        
        # Validate required parameters
        if not student_id or not content_type or not content_id:
            return Response(
                {
                    "error": "معاملات مطلوبة مفقودة. يرجى توفير student_id و content_type و content_id"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate content_type
        if content_type not in ['exam', 'note']:
            return Response(
                {
                    "error": "نوع محتوى غير صحيح. يجب أن يكون إما 'exam' أو 'note'"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Convert IDs to integers
        try:
            student_id = int(student_id)
            content_id = int(content_id)
        except ValueError:
            return Response(
                {
                    "error": "تنسيق معرف غير صحيح. يجب أن تكون student_id و content_id أرقام صحيحة"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get current time
        current_time = timezone.now()
        
        # Check if the student has purchased this specific content
        premium_content = StudentPremiumContent.objects.filter(
            student_id=student_id,
            type=content_type,
            content_id=content_id
        ).first()
        
        if premium_content:
            # Check if the content has expired
            if premium_content.date_of_expiry < current_time.date():
                # Store content info before deletion
                content_info = {
                    "has_purchased": True,
                    "is_expired": True,
                    "reason": "انتهت صلاحية المحتوى وتم حذفه",
                    "purchase_date": premium_content.purchase_date,
                    "expiry_date": premium_content.date_of_expiry,
                    "content_name": premium_content.content_name,
                    "subject_name": premium_content.subject_name
                }
                
                # Delete the expired content from the database
                premium_content.delete()
                
                return Response(content_info, status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        "has_purchased": True,
                        "is_expired": False,
                        "purchase_date": premium_content.purchase_date,
                        "expiry_date": premium_content.date_of_expiry,
                        "content_name": premium_content.content_name,
                        "subject_name": premium_content.subject_name
                    },
                    status=status.HTTP_200_OK
                )
        else:
            # No purchase record found
            return Response(
                {
                    "has_purchased": False,
                    "is_expired": False,
                    "reason": "لم يتم العثور على سجل شراء لهذا المحتوى"
                },
                status=status.HTTP_200_OK
            )
            
    except Exception as e:
        return Response(
            {"error": f"فشل في التحقق من شراء المحتوى: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Generic views for CRUD operations
class StudentPremiumContentListCreateView(generics.ListCreateAPIView):
    """
    Generic view for listing and creating StudentPremiumContent
    """
    queryset = StudentPremiumContent.objects.all()
    serializer_class = StudentPremiumContentSerializer
    
    def get_serializer_class(self):
        # Use different serializer for creation and listing
        if self.request.method == 'POST':
            return CreateStudentPremiumContentSerializer
        return StudentPremiumContentSerializer


class StudentPremiumContentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Generic view for retrieving, updating, and deleting StudentPremiumContent
    """
    queryset = StudentPremiumContent.objects.all()
    serializer_class = StudentPremiumContentSerializer
