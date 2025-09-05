from rest_framework import serializers
from .models import TestPackage

class TestPackageSerializer(serializers.ModelSerializer):
    """
    Basic serializer for TestPackage model
    Used for listing and displaying test package information
    Includes all essential fields for package overview
    """
    class Meta:
        model = TestPackage 
        # Define fields for basic package information display
        fields = [
            'id', 'package_name', 'units', 'Class', 'number_of_apps', 
            'publisher_name', 'price', 'date_added', 'number_of_purchases', 
            'publisher_id', 'subject_name', 'number_of_questions'
        ]


class CreatePackages(serializers.ModelSerializer):
    """
    Serializer for creating and updating test packages
    Used for POST and PUT operations with full field access
    Includes all model fields for complete package management
    """
    class Meta:
        model = TestPackage
        # Include all fields for complete package creation and updates
        fields = '__all__'
    
    def validate_package_name(self, value):
        """
        Custom validation for package name
        Ensures package name meets minimum requirements
        """
        if len(value.strip()) < 3:
            raise serializers.ValidationError("اسم الحزمة يجب أن يكون 3 أحرف على الأقل")
        return value
    
    def validate_price(self, value):
        """
        Custom validation for price field
        Ensures price is positive and reasonable
        """
        if value > 50000:
            raise serializers.ValidationError("السعر لا يمكن أن يتجاوز 50000")
        return value
    
    def validate_number_of_questions(self, value):
        """
        Custom validation for number of questions
        Ensures reasonable question count
        """
        if value <= 0:
            raise serializers.ValidationError("عدد الأسئلة يجب أن يكون أكبر من صفر")
        if value > 1000:
            raise serializers.ValidationError("عدد الأسئلة لا يمكن أن يتجاوز 1000")
        return value


class TestPackageDetailsSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for specific test package information
    Used for detailed package views with essential fields only
    Focuses on core package details for detailed display
    """
    class Meta:
        model = TestPackage
        # Define essential fields for detailed package information
        fields = [
            'package_name', 'units', 'Class', 'subject_name', 
            'price', 'number_of_questions'
        ]
