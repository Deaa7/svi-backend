from django.urls import path
from . import views

urlpatterns = [ 
    path('GetNoteWithContent/<int:id>/', views.GetNoteWithContent),    # id بيعرض الملاحظات مع المحتوى من خلال
    path('GetNoteWithoutContent/<int:id>/', views.GetNoteWithoutContent),                # id بيعرض الملاحظات بدون المحتوى من خلال 
    path('add_note/', views.addNote.as_view()),             # لاضافة ملاحظات من خلال ادخال بيانات او لعرض الملاحظات بدون ادخالها
    path('addNoteImages/', views.addNoteImages.as_view()), # اضافة صور للملاحظات 
    path('get_by_filter/<str:subject_name>/', views.get_by_filter),   # عرض الملاحظات بدون المحتوى مع فلترة حسب اسم الناشر والسعر
    path('IncreaseNumberOfReads/<int:id>/', views.IncreaseNumberOfReads),        #زيادة عدد القراء بمقدر واحد
    path('IncreaseNumberOfPurchases/<int:id>/', views.IncreaseNumberOfPurchases),        #زيادة عدد المشتريات بمقدر واحد
    path('getNoteImages/<int:id>/',views.getNoteImages),
    path('edit_note_by_id/<int:id>/',views.edit_note_by_id),
    path('delete_note_by_id/<int:id>/',views.delete_note_by_id),
    path('GetNotesWithoutContentByTeacherID/<int:publisher_id>/',views.GetNotesWithoutContentByTeacherID    ),
    path('get_note_info_for_edit/<int:id>/',views.get_note_info_for_edit    ),

]
