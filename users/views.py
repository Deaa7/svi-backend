from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import SingUpSerializer, UserSerializer
from .models import User
from profiles.models import Profile_Teacher , Profile_Student

# Dictionary mapping English subject names to Arabic names for teacher bio generation
subject_arabic_names={
     'math':'رياضيات' ,
    'physics':'فيزياء' ,
    'chemistry':'كيمياء' ,
    'science':'علوم' ,
    'arabic':'عربي' ,
    'english':'إنكليزي' ,
    'france':'فرنسي' ,
    'islam':'ديانة' ,
    'physics_chemistry':'فيزياء و كيمياء' ,
    'geography':'اجتماعيات' ,
}
 

@api_view(["POST"])
def register(request):
    """
    User registration endpoint
    Handles both teacher and student registration with profile creation
    """
    # Extract data from the request
    data = request.data
    
    # Validate the registration data using serializer
    user = SingUpSerializer(data=data)
    if user.is_valid():
        # Initialize error tracking variables
        error_object = {}
        info_error = False

        # Check if email is already registered
        if User.objects.filter(email=data["email"]).exists():
            error_object['email'] = 'هذا البريد الإلكتروني مسجل بالفعل'
            info_error = True

        # Check if username is already taken
        if User.objects.filter(username=data["username"]).exists():
            error_object['username'] = 'اسم المستخدم هذا مسجل بالفعل'
            info_error = True
        
        # If there are validation errors, return them
        if info_error:
            return Response(
                error_object,
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            # Create the user account with hashed password
            user = User.objects.create(
                username=data["username"],
                email=data["email"],
                password=make_password(data["password"]),
                is_teacher=data["is_teacher"],
            )
            
            # Handle teacher profile creation
            if data["is_teacher"]:
                # Generate bio based on gender and subject
                bio = ""
                if data['gender'] == 'M':
                    bio = 'استاذ متخصص في تدريس مادة '
                else:
                    bio = "آنسة متخصصة في تدريس مادة "
                
                bio += subject_arabic_names[data["studying_subjects"]]
                
                # Get and update teacher profile
                teacher = Profile_Teacher.objects.get(user=user)
                teacher.full_name = data["full_name"]
                teacher.phone_number = data["phone_number"]
                teacher.Class = data["Class"]
                teacher.studying_subjects = data["studying_subjects"]
                teacher.city = data["city"]
                teacher.gender = data["gender"]
                teacher.bio = bio

                teacher.save()
            else:
                # Handle student profile creation
                student = Profile_Student.objects.get(user=user)
                student.full_name = data["full_name"]
                student.phone_number = data["phone_number"]
                student.Class = data["Class"]
                student.city = data["city"]
                student.school = data["school"]
                student.gender = data["gender"]
                
                student.save()

            return Response(
                {"details": "تم تسجيل حسابك بنجاح!"},
                status=status.HTTP_201_CREATED
            )
      
    else:
        # Return serializer validation errors
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["POST"])
def login(request):
    """
    User login endpoint
    Authenticates user credentials and returns JWT tokens with profile information
    """
    # Get user by username or return 404 if not found
    user = get_object_or_404(User, username=request.data["username"])
    profile = "initial value"
    
    # Verify password
    if not user.check_password(request.data["password"]):
        return Response(
            {"Error": "كلمة المرور غير صحيحة"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    # Generate JWT tokens for the user
    refresh = RefreshToken.for_user(user)

    # Prepare user data for response
    data = {
        "username": request.data["username"],
        "password": request.data["password"]
    }

    # Serialize user data
    serializer = UserSerializer(instance=user)
    
    # Handle teacher login response
    if user.is_teacher:
        profile = Profile_Teacher.objects.get(user=user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": serializer.data,
                "full_name": profile.full_name,
                "gender": profile.gender,
                "Class": profile.Class,
                "city": profile.city,
            },
            status=status.HTTP_200_OK,
        )

    else:
        # Handle student login response
        profile = Profile_Student.objects.get(user=user)
        
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": serializer.data,
                "full_name": profile.full_name,
                "gender": profile.gender,
                "Class": profile.Class,
                "city": profile.city,
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """
    User logout endpoint
    Blacklists the refresh token to invalidate the session
    """
    permission_classes = (IsAuthenticated,)
  
    def post(self, request):
        # Get user by username
        user = get_object_or_404(User, username=request.data["username"])
        user.save()
        
        try:
            # Get refresh token from request data
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response(
                    "رمز التحديث مطلوب", 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response("تم تسجيل الخروج بنجاح", status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response(
                f"{e} فشل في تسجيل الخروج", 
                status=status.HTTP_406_NOT_ACCEPTABLE
            )


class TokenRefreshViewCustom(generics.GenericAPIView):
    """
    Custom token refresh endpoint
    Refreshes access token using refresh token and returns updated user information
    """

    def post(self, request, *args, **kwargs):
        # Get refresh token from request data
        refresh_token = request.data.get("refresh")

        # Validate refresh token presence
        if not refresh_token:
            print('Refresh token is required')
            return Response(
                {"detail": "رمز التحديث مطلوب"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Create refresh token object
            refresh = RefreshToken(refresh_token)

            # Get user by ID from token
            user = User.objects.get(id=refresh["user_id"])
            profile = ""
            Class = "12"
            
            # Get appropriate profile based on user type
            if user.is_teacher:
                profile = Profile_Teacher.objects.get(user=user.id)
            else:
                profile = Profile_Student.objects.get(user=user.id)
                Class = profile.Class 
                
            # Generate new access token
            new_access_token = str(refresh.access_token)
            
            # Handle profile image if exists
            image = None
            if hasattr(profile, 'image') and profile.image:
                image = profile.image.url

            return Response(
                {
                    "access": new_access_token,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "is_teacher": user.is_teacher,
                        "full_name": profile.full_name,
                        "gender": profile.gender,
                        "image": image,
                        "Class": Class,
                    },
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print('here is error', e)
            return Response(
                {"detail": "رمز التحديث غير صحيح أو المستخدم غير موجود"},
                status=status.HTTP_400_BAD_REQUEST,
            )
