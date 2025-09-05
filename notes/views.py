from django.shortcuts import get_object_or_404, render
from rest_framework import generics  
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Notes, NoteImages
from .serializers import NoteFilterSerializer, NoteSerializer, NoteImagesSerializer, NoteInfoForEditSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from .filters import NoteFilter
from rest_framework import status


# Generic views for CRUD operations
class addNote(generics.ListCreateAPIView):
    """
    Generic view for listing and creating notes
    Provides standard CRUD operations for Notes model
    Handles both GET (list) and POST (create) operations
    """
    # permission_classes = (IsAuthenticated,)
    queryset = Notes.objects.all()
    serializer_class = NoteSerializer


class addNoteImages(generics.ListCreateAPIView):
    """
    Generic view for listing and creating note images
    Handles file uploads for note images
    Configured with MultiPartParser and FormParser for file handling
    """
    # Configure parsers for handling file uploads
    parser_classes = (MultiPartParser, FormParser)
    # permission_classes = (IsAuthenticated,)
    queryset = NoteImages.objects.all() 
    serializer_class = NoteImagesSerializer


@api_view(['GET']) 
def getNoteImages(request, id):
    """
    Get all images associated with a specific note
    Returns all images linked to the note by note ID
    """
    # Filter images by note ID
    query = NoteImages.objects.filter(note_id=id)
    
    # Serialize the filtered images data
    serial = NoteImagesSerializer(query, many=True)
    
    return Response(serial.data)


@api_view(['GET']) 
def GetNoteWithContent(request, id):
    """
    Get a single note with full content by its ID
    Returns complete note information including all content
    """
    # Get the note object by ID
    obj = Notes.objects.get(id=id) 
    
    # Serialize the note data with full content
    serial = NoteSerializer(obj)
    
    return Response(serial.data)


@api_view(['GET'])
def get_by_filter(request, subject_name):
    """
    Get notes filtered by subject name, price, and class
    Returns paginated list of notes matching the specified criteria
    Excludes note content for preview purposes
    """
    # Get query parameters for filtering
    price = request.GET.get('price', None)
    Class = request.GET.get('Class', None)
    count = request.GET.get('count', None)
    limit = request.GET.get('limit', None)
    name = request.GET.get('name', None)
    publisher_name = request.GET.get('publisher_name', None)
 
    # Filter notes by subject, class, and maximum price
    queryset = Notes.objects.filter(subject_name=subject_name, Class=Class, price__lte=price)  
  
    if name is not None:
        queryset = queryset.filter(title__icontains=name)
    if publisher_name is not None:
        queryset = queryset.filter(publisher_name__icontains=publisher_name)
    # Serialize the filtered notes data (without content)
    serializer = NoteFilterSerializer(queryset, many=True)

    # Convert pagination parameters to integers
    count = int(count)
    limit = int(limit)

    # Calculate pagination boundaries
    begin = min((count - 1) * limit, len(serializer.data))
    end = min(count * limit, len(serializer.data))
    num = len(serializer.data) 
   
    return Response({'notes': serializer.data[begin:end], 'number_of_notes': num}, status=200)


@api_view(['GET'])
def GetNotesWithoutContentByTeacherID(request, publisher_id):
    """
    Get all notes published by a specific teacher
    Returns paginated list of notes without content for the specified publisher
    """
    # Filter notes by publisher ID
    queryset = Notes.objects.filter(publisher_id=publisher_id)   
    
    # Serialize the filtered notes data (without content)
    serializer = NoteFilterSerializer(queryset, many=True)
 
    # Get pagination parameters
    limit = request.GET.get('limit')
    count = request.GET.get('count')
    
    # Convert pagination parameters to integers if provided
    if count:
        count = int(count)
    if limit:
        limit = int(limit)

    # Calculate pagination boundaries
    begin = min((count - 1) * limit, len(serializer.data))
    end = min(count * limit, len(serializer.data))
    num = len(serializer.data) 
   
    return Response({'notes': serializer.data[begin:end], 'number_of_notes': num}, status=200)


@api_view(['GET'])
def GetNoteWithoutContent(request, id):
    """
    Get a single note without content by its ID
    Returns note information excluding the main content for preview purposes
    """
    # Filter notes by ID
    obj = Notes.objects.filter(id=id) 
    
    # Serialize the note data without content
    serializer = NoteFilterSerializer(obj, many=True)
    
    return Response(serializer.data)


@api_view(['PUT'])
def IncreaseNumberOfReads(request, id):
    """
    Increase the read count for a specific note
    Increments the note's read counter by 1
    """
    # Get the note object or return 404 if not found
    note = get_object_or_404(Notes, id=id)
    
    # Increment the read count
    note.number_of_reads += 1 
    
    # Save the updated note
    note.save()
    
    return Response('تم زيادة عدد القراء بنجاح', status=200)


@api_view(['PUT'])
def IncreaseNumberOfPurchases(request, id):
    """
    Increase the purchase count for a specific note
    Increments the note's purchase counter by 1
    """
    try:
        # Get the note object or return 404 if not found
        note = get_object_or_404(Notes, id=id)
        
        # Increment the purchase count
        note.number_of_purchases += 1
        
        # Save the updated note
        note.save()
        
        return Response('تم زيادة عدد المشتريات بنجاح', status=200)
    except Exception as e:
        return Response('فشل في زيادة عدد المشتريات', status=500)


@api_view(['PUT'])
def edit_note_by_id(request, id):
    """
    Edit a specific note by its ID
    Updates note fields with new data provided in the request
    """
    # Copy request data to avoid modifying original data
    data = request.data.copy()
    
    # Get the note object by ID
    obj = Notes.objects.get(id=id)
    
    try:
        # Update all editable fields if provided in the request
        if 'title' in data:
            obj.title = data['title']
        if 'subject_name' in data:
            obj.subject_name = data['subject_name']
        if 'Class' in data:
            obj.Class = data['Class']
        if 'content' in data:
            obj.content = data['content']
        if 'price' in data:
            obj.price = data['price']
        
        # Save the updated note
        obj.save()
        
        return Response('تم تعديل الملاحظة بنجاح', status=200)
   
    except Exception as e:
        return Response('فشل في تعديل الملاحظة', status=500)
   

@api_view(['DELETE'])
def delete_note_by_id(request, id):
    """
    Delete a specific note by its ID
    Removes the note and all related images from the database
    """
    try:
        # Get the note object or return 404 if not found
        note = get_object_or_404(Notes, id=id)
        
        # Delete the note (this will also delete related NoteImages due to CASCADE)
        note.delete()
        
        return Response('تم حذف الملاحظة بنجاح', status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response('فشل في حذف الملاحظة', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET']) 
def get_note_info_for_edit(request, id):
    """
    Get note information for editing purposes
    Returns note data needed for editing, excluding sensitive content
    """
    # Get the note object by ID
    obj = Notes.objects.get(id=id) 
    
    # Serialize the note data for editing
    serial = NoteInfoForEditSerializer(obj)
    
    return Response(serial.data)
