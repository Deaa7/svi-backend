# وثائق تطبيق Django التعليمي

## نظرة عامة على التطبيق

هذا تطبيق Django تعليمي مصمم لإدارة المحتوى التعليمي والتفاعل بين الطلاب والمعلمين. يدعم التطبيق نظاماً شاملاً لإدارة الملاحظات والاختبارات والمحتوى المدفوع.

## التقنيات المستخدمة

### 1. Django Framework
- **الغرض**: إطار عمل الويب الرئيسي
- **الفوائد**: 
  - إدارة قواعد البيانات التلقائية (ORM)
  - نظام URL routing متقدم
  - إدارة المستخدمين والمصادقة
  - واجهة إدارة مدمجة

### 2. Django REST Framework (DRF)
- **الغرض**: بناء APIs RESTful
- **الفوائد**:
  - Serializers لتحويل البيانات
  - Generic Views للعمليات CRUD
  - نظام Permissions متقدم
  - تصفح API تلقائي

### 3. JWT Authentication
- **الغرض**: نظام مصادقة آمن
- **الفوائد**:
  - Tokens آمنة ومؤقتة
  - دعم Refresh Tokens
  - لا حاجة لحفظ حالة في الخادم

### 4. MySQL Database
- **الغرض**: قاعدة البيانات الرئيسية
- **الفوائد**:
  - أداء عالي
  - دعم المعاملات المعقدة
  - قابلية التوسع

### 5. Pillow
- **الغرض**: معالجة الصور
- **الفوائد**:
  - رفع ومعالجة صور الملاحظات والاختبارات
  - تحسين جودة الصور

### 6. CORS Headers
- **الغرض**: السماح بالطلبات من مصادر مختلفة
- **الفوائد**:
  - دعم التطبيقات الأمامية
  - مرونة في التطوير

---

## نماذج قاعدة البيانات (Models)

### 1. نموذج المستخدمين (User Model)

```python
class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_teacher = models.BooleanField(default=False)
```

**الغرض**: إدارة المستخدمين الأساسيين
**الحقول**:
- `email`: البريد الإلكتروني (فريد)
- `is_teacher`: تحديد نوع المستخدم (معلم أم طالب)

### 2. نموذج ملف الطالب (Profile_Student)

```python
class Profile_Student(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=127, default="", blank=True)
    city = models.CharField(max_length=50, default="", blank=True)
    school = models.CharField(max_length=200, default="-", blank=True)
    phone_number = models.CharField(max_length=15, default="-", blank=True)
    Class = models.CharField(max_length=2, default='12', blank=True)
    balance = models.IntegerField(default=0)
    gender = models.CharField(max_length=1, default="M")
```

**الغرض**: تخزين معلومات الطلاب الشخصية والأكاديمية
**الحقول**:
- `user`: ربط مع نموذج المستخدم
- `full_name`: الاسم الكامل
- `city`: المدينة
- `school`: المدرسة
- `phone_number`: رقم الهاتف
- `Class`: الصف الدراسي
- `balance`: الرصيد المالي
- `gender`: الجنس

### 3. نموذج ملف المعلم (Profile_Teacher)

```python
class Profile_Teacher(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=127, default="", blank=True)
    studying_subjects = models.CharField(max_length=100, choices=subject_choices)
    image = models.ImageField(upload_to="TeachersImages/", null=True, blank=True)
    bio = models.CharField(default='', max_length=5000, blank=True, null=True)
    total_net = models.IntegerField(default=0, blank=True)
    created_at = models.DateField(auto_now_add=True)
    city = models.CharField(max_length=50, default="", blank=True)
    Class = models.CharField(max_length=15, choices=class_choices, blank=True, default='12')
    gender = models.CharField(default='M', max_length=1)
    teaching_in_school = models.CharField(default='', max_length=255, blank=True, null=True)
    teaching_in_institutions = models.CharField(default='', max_length=500, blank=True, null=True)
    number_of_exams = models.IntegerField(default=0, blank=True)
    number_of_notes = models.IntegerField(default=0, blank=True)
    phone_number = models.CharField(max_length=15, default='-', blank=True)
    another_phone_number = models.CharField(max_length=15, default='-', blank=True)
    telegram_link = models.CharField(default='', max_length=500, blank=True, null=True)
    whatsapp_link = models.CharField(default='', max_length=500, blank=True, null=True)
    facebook_link = models.CharField(default='', max_length=500, blank=True, null=True)
    instagram_link = models.CharField(default='', max_length=500, blank=True, null=True)
```

**الغرض**: تخزين معلومات المعلمين المهنية والشخصية
**الحقول المهمة**:
- `studying_subjects`: المواد التي يدرسها المعلم
- `image`: صورة المعلم
- `bio`: السيرة الذاتية
- `total_net`: إجمالي الأرباح
- `teaching_in_school`: خبرة التدريس في المدارس
- `teaching_in_institutions`: خبرة التدريس في المؤسسات
- `number_of_exams`: عدد الاختبارات المنشورة
- `number_of_notes`: عدد الملاحظات المنشورة
- روابط التواصل الاجتماعي

### 4. نموذج الملاحظات (Notes)

```python
class Notes(models.Model):
    title = models.CharField(max_length=2000)
    subject_name = models.CharField(max_length=25, default='math', blank=True)
    Class = models.CharField(max_length=25, default='12', blank=True)
    publisher_id = models.BigIntegerField(default=1, blank=True)
    publisher_name = models.CharField(max_length=127, default='SVI', blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=False)
    price = models.IntegerField(default=0, blank=True)
    number_of_reads = models.IntegerField(default=0, editable=False, null=True, blank=True)
    number_of_purchases = models.IntegerField(default=0, editable=False)
```

**الغرض**: تخزين الملاحظات التعليمية
**الحقول**:
- `title`: عنوان الملاحظة
- `subject_name`: اسم المادة
- `Class`: الصف الدراسي
- `publisher_id`: معرف الناشر
- `publisher_name`: اسم الناشر
- `date_uploaded`: تاريخ الرفع
- `content`: محتوى الملاحظة
- `price`: السعر
- `number_of_reads`: عدد القراءات
- `number_of_purchases`: عدد المشتريات

### 5. نموذج صور الملاحظات (NoteImages)

```python
class NoteImages(models.Model):
    note_id = models.ForeignKey(Notes, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="ImagesForNotes/", null=True, blank=True)
```

**الغرض**: ربط الصور بالملاحظات
**الحقول**:
- `note_id`: ربط مع الملاحظة
- `images`: ملف الصورة

### 6. نموذج حزم الاختبارات (TestPackage)

```python
class TestPackage(models.Model):
    package_name = models.CharField(max_length=500)
    publisher_id = models.BigIntegerField(default=1)
    publisher_name = models.CharField(max_length=127, default='SVI', blank=True)
    units = models.CharField(max_length=1000)
    Class = models.CharField(max_length=2, default='12')
    subject_name = models.CharField(max_length=25, default='math', blank=True)
    price = models.IntegerField(default=0, blank=True)
    date_added = models.DateField(auto_now_add=True)
    number_of_apps = models.IntegerField(default=0, blank=True, editable=False)
    number_of_purchases = models.IntegerField(default=0, editable=False)
    number_of_questions = models.IntegerField(default=0, blank=True)
```

**الغرض**: تخزين حزم الاختبارات
**الحقول**:
- `package_name`: اسم الحزمة
- `units`: الوحدات المشمولة
- `number_of_apps`: عدد التطبيقات
- `number_of_questions`: عدد الأسئلة

### 7. نموذج الأسئلة (Questions)

```python
class Questions(models.Model):
    package = models.ForeignKey(TestPackage, on_delete=models.CASCADE)
    test_content = models.TextField()
    option_A = models.TextField(null=True, blank=True)
    option_B = models.TextField(null=True, blank=True)
    option_C = models.TextField(null=True, blank=True)
    option_D = models.TextField(null=True, blank=True)
    option_E = models.TextField(null=True, blank=True)
    right_answer = models.CharField(max_length=5, default='A')
    explanation = models.TextField(default='لا يتوفر شرح للإجابة', null=True, blank=True)
```

**الغرض**: تخزين أسئلة الاختبارات
**الحقول**:
- `package`: ربط مع حزمة الاختبار
- `test_content`: نص السؤال
- `option_A` إلى `option_E`: خيارات الإجابة
- `right_answer`: الإجابة الصحيحة
- `explanation`: شرح الإجابة

### 8. نموذج صور الأسئلة (QuestionImages)

```python
class QuestionImages(models.Model):
    test_id = models.ForeignKey(Questions, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100, choices=field_name_choices, default='test_content')
    images = models.ImageField(upload_to="ImagesForQuestions/", null=True, blank=True)
```

**الغرض**: ربط الصور بالأسئلة
**الحقول**:
- `test_id`: ربط مع السؤال
- `field_name`: تحديد جزء السؤال (السؤال، الخيارات، الشرح)
- `images`: ملف الصورة

### 9. نموذج الاختبارات المكتملة (DoneExams)

```python
class DoneExams(models.Model):
    student = models.ForeignKey(Profile_Student, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=25)
    exam_name = models.CharField(max_length=100)
    exam_id = models.CharField(max_length=50)
    publisher_id = models.IntegerField(default=1)
    publisher_name = models.CharField(max_length=127, default='SVI', blank=True)
    date_of_application = models.DateField(auto_now_add=True, blank=True)
    result = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.IntegerField(default=0)
    time_taken = models.TimeField(default='00:00:00', blank=True)
```

**الغرض**: تتبع الاختبارات المكتملة من قبل الطلاب
**الحقول**:
- `student`: الطالب
- `exam_name`: اسم الاختبار
- `result`: النتيجة
- `time_taken`: الوقت المستغرق

### 10. نموذج المحتوى المدفوع (StudentPremiumContent)

```python
class StudentPremiumContent(models.Model):
    student = models.ForeignKey(Profile_Student, on_delete=models.DO_NOTHING)
    student_name = models.CharField(max_length=256, default="")
    Class = models.CharField(max_length=25)
    type = models.CharField(max_length=25)
    subject_name = models.CharField(max_length=25)
    content_id = models.BigIntegerField()
    content_name = models.CharField(max_length=2000)
    publisher_id = models.ForeignKey(Profile_Teacher, on_delete=models.DO_NOTHING)
    publisher_name = models.CharField(max_length=127)
    purchase_date = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_expiry = models.DateField()
    is_expired = models.BooleanField(default=False)
```

**الغرض**: تتبع المحتوى المدفوع المشترى من قبل الطلاب
**الحقول**:
- `type`: نوع المحتوى (اختبار، ملاحظة)
- `content_id`: معرف المحتوى
- `purchase_date`: تاريخ الشراء
- `date_of_expiry`: تاريخ انتهاء الصلاحية
- `is_expired`: حالة انتهاء الصلاحية

### 11. نموذج قراءة الملاحظات (StudentReadNotes)

```python
class StudentReadNotes(models.Model):
    student = models.ForeignKey(Profile_Student, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=25)
    note_name = models.CharField(max_length=2000)
    note_id = models.ForeignKey(Notes, on_delete=models.CASCADE)
    publisher_id = models.BigIntegerField()
    publisher_name = models.CharField(max_length=127)
    number_of_reads = models.IntegerField(default=1)
    first_read_at = models.DateTimeField(auto_now_add=True)
    last_read_at = models.DateTimeField(auto_now=True)
```

**الغرض**: تتبع قراءة الطلاب للملاحظات
**الحقول**:
- `number_of_reads`: عدد مرات القراءة
- `first_read_at`: أول مرة قرأها
- `last_read_at`: آخر مرة قرأها

### 12. نموذج تتبع المواد (StudentSubjectTracking)

```python
class StudentSubjectTracking(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    Class = models.CharField(max_length=2, default='12')
    subject_name = models.CharField(max_length=25)
    number_of_notes = models.IntegerField(default=0)
    number_of_exams = models.IntegerField(default=0)
```

**الغرض**: تتبع تقدم الطلاب في المواد المختلفة
**الحقول**:
- `number_of_notes`: عدد الملاحظات المكتملة
- `number_of_exams`: عدد الاختبارات المكتملة

---

## نقاط النهاية (API Endpoints)

### 1. إدارة المستخدمين (Users)

#### تسجيل مستخدم جديد
- **URL**: `/users/register/`
- **Method**: `POST`
- **المعاملات**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string",
    "is_teacher": "boolean"
  }
  ```
- **الاستجابة**:
  ```json
  {
    "message": "User created successfully",
    "user_id": "integer"
  }
  ```

#### تسجيل الدخول
- **URL**: `/users/login/`
- **Method**: `POST`
- **المعاملات**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **الاستجابة**:
  ```json
  {
    "access": "string",
    "refresh": "string",
    "user_id": "integer",
    "is_teacher": "boolean"
  }
  ```

#### تسجيل الخروج
- **URL**: `/users/logout/`
- **Method**: `POST`
- **المعاملات**: `refresh_token`
- **الاستجابة**:
  ```json
  {
    "message": "Logged out successfully"
  }
  ```

#### تحديث التوكن
- **URL**: `/users/refresh/`
- **Method**: `POST`
- **المعاملات**:
  ```json
  {
    "refresh": "string"
  }
  ```
- **الاستجابة**:
  ```json
  {
    "access": "string"
  }
  ```

### 2. إدارة الملفات الشخصية (Profiles)

#### الحصول على معاينة المعلمين
- **URL**: `/profiles/get_teacher_preview/`
- **Method**: `GET`
- **المعاملات**:
  - `Class`: الصف الدراسي
  - `subject_name`: اسم المادة
  - `city`: المدينة
  - `count`: رقم الصفحة
  - `limit`: عدد النتائج في الصفحة
  - `name`: اسم المعلم (اختياري)
- **الاستجابة**:
  ```json
  [
    {
      "id": "integer",
      "full_name": "string",
      "studying_subjects": "string",
      "image": "string",
      "bio": "string",
      "city": "string",
      "Class": "string",
      "number_of_exams": "integer",
      "number_of_notes": "integer"
    }
  ]
  ```

#### الحصول على معلومات معلم
- **URL**: `/profiles/get_teacher_info/<int:id>/`
- **Method**: `GET`
- **المعاملات**: `id` (معرف المعلم)
- **الاستجابة**:
  ```json
  {
    "id": "integer",
    "full_name": "string",
    "studying_subjects": "string",
    "image": "string",
    "bio": "string",
    "city": "string",
    "Class": "string",
    "teaching_in_school": "string",
    "teaching_in_institutions": "string",
    "phone_number": "string",
    "telegram_link": "string",
    "whatsapp_link": "string",
    "facebook_link": "string",
    "instagram_link": "string",
    "number_of_exams": "integer",
    "number_of_notes": "integer"
  }
  ```

#### تحديث ملف المعلم
- **URL**: `/profiles/update_teacher_profile/<int:id>/`
- **Method**: `PUT`
- **المعاملات**: `id` (معرف المعلم)
- **البيانات**:
  ```json
  {
    "full_name": "string",
    "studying_subjects": "string",
    "bio": "string",
    "city": "string",
    "Class": "string",
    "teaching_in_school": "string",
    "teaching_in_institutions": "string",
    "phone_number": "string",
    "another_phone_number": "string",
    "telegram_link": "string",
    "whatsapp_link": "string",
    "facebook_link": "string",
    "instagram_link": "string"
  }
  ```

#### الحصول على معلومات الطالب
- **URL**: `/profiles/get_student_own_profile_info/<int:id>/`
- **Method**: `GET`
- **المعاملات**: `id` (معرف الطالب)
- **الاستجابة**:
  ```json
  {
    "id": "integer",
    "full_name": "string",
    "city": "string",
    "school": "string",
    "phone_number": "string",
    "Class": "string",
    "balance": "integer",
    "gender": "string"
  }
  ```

#### تحديث ملف الطالب
- **URL**: `/profiles/update_student_profile/<int:id>/`
- **Method**: `PUT`
- **المعاملات**: `id` (معرف الطالب)
- **البيانات**:
  ```json
  {
    "full_name": "string",
    "city": "string",
    "school": "string",
    "phone_number": "string",
    "Class": "string",
    "gender": "string"
  }
  ```

#### فحص رصيد الطالب
- **URL**: `/profiles/check_student_balance/`
- **Method**: `POST`
- **البيانات**:
  ```json
  {
    "student_id": "integer",
    "required_amount": "integer"
  }
  ```
- **الاستجابة**:
  ```json
  {
    "has_sufficient_balance": "boolean",
    "current_balance": "integer",
    "required_amount": "integer"
  }
  ```

### 3. إدارة الملاحظات (Notes)

#### الحصول على ملاحظة مع المحتوى
- **URL**: `/notes/GetNoteWithContent/<int:id>/`
- **Method**: `GET`
- **المعاملات**: `id` (معرف الملاحظة)
- **الاستجابة**:
  ```json
  {
    "id": "integer",
    "title": "string",
    "subject_name": "string",
    "Class": "string",
    "publisher_id": "integer",
    "publisher_name": "string",
    "date_uploaded": "datetime",
    "content": "string",
    "price": "integer",
    "number_of_reads": "integer",
    "number_of_purchases": "integer",
    "number_of_comments": "integer"
  }
  ```

#### الحصول على ملاحظة بدون المحتوى
- **URL**: `/notes/GetNoteWithoutContent/<int:id>/`
- **Method**: `GET`
- **المعاملات**: `id` (معرف الملاحظة)
- **الاستجابة**: نفس الاستجابة السابقة بدون حقل `content`

#### إضافة ملاحظة جديدة
- **URL**: `/notes/add_note/`
- **Method**: `POST`
- **البيانات**:
  ```json
  {
    "title": "string",
    "subject_name": "string",
    "Class": "string",
    "publisher_id": "integer",
    "publisher_name": "string",
    "content": "string",
    "price": "integer"
  }
  ```

#### إضافة صور للملاحظة
- **URL**: `/notes/addNoteImages/`
- **Method**: `POST`
- **البيانات**: `FormData`
  - `note_id`: معرف الملاحظة
  - `images`: ملف الصورة

#### الحصول على الملاحظات بالفلترة
- **URL**: `/notes/get_by_filter/<str:subject_name>/`
- **Method**: `GET`
- **المعاملات**: `subject_name` (اسم المادة)
- **الاستجابة**: قائمة بالملاحظات المفلترة

#### زيادة عدد القراءات
- **URL**: `/notes/IncreaseNumberOfReads/<int:id>/`
- **Method**: `POST`
- **المعاملات**: `id` (معرف الملاحظة)
- **الاستجابة**:
  ```json
  {
    "message": "Number of reads increased successfully"
  }
  ```

#### زيادة عدد المشتريات
- **URL**: `/notes/IncreaseNumberOfPurchases/<int:id>/`
- **Method**: `POST`
- **المعاملات**: `id` (معرف الملاحظة)
- **الاستجابة**:
  ```json
  {
    "message": "Number of purchases increased successfully"
  }
  ```

#### الحصول على صور الملاحظة
- **URL**: `/notes/getNoteImages/<int:id>/`
- **Method**: `GET`
- **المعاملات**: `id` (معرف الملاحظة)
- **الاستجابة**:
  ```json
  [
    {
      "id": "integer",
      "note_id": "integer",
      "images": "string"
    }
  ]
  ```

#### تعديل الملاحظة
- **URL**: `/notes/edit_note_by_id/<int:id>/`
- **Method**: `PUT`
- **المعاملات**: `id` (معرف الملاحظة)
- **البيانات**: نفس بيانات إضافة الملاحظة

#### حذف الملاحظة
- **URL**: `/notes/delete_note_by_id/<int:id>/`
- **Method**: `DELETE`
- **المعاملات**: `id` (معرف الملاحظة)
- **الاستجابة**:
  ```json
  {
    "message": "Note deleted successfully"
  }
  ```

#### الحصول على ملاحظات المعلم
- **URL**: `/notes/GetNotesWithoutContentByTeacherID/<int:publisher_id>/`
- **Method**: `GET`
- **المعاملات**: `publisher_id` (معرف المعلم)
- **الاستجابة**: قائمة بملاحظات المعلم

#### الحصول على معلومات الملاحظة للتعديل
- **URL**: `/notes/get_note_info_for_edit/<int:id>/`
- **Method**: `GET`
- **المعاملات**: `id` (معرف الملاحظة)
- **الاستجابة**: معلومات الملاحظة كاملة

### 4. إدارة الأسئلة (Questions)

#### الحصول على جميع أسئلة الحزمة
- **URL**: `/questions/all_questions/<int:package_id>/`
- **Method**: `GET`
- **المعاملات**: `package_id` (معرف حزمة الاختبار)
- **الاستجابة**:
  ```json
  [
    {
      "id": "integer",
      "package": "integer",
      "test_content": "string",
      "option_A": "string",
      "option_B": "string",
      "option_C": "string",
      "option_D": "string",
      "option_E": "string",
      "right_answer": "string",
      "explanation": "string"
    }
  ]
  ```

#### إضافة أسئلة جديدة
- **URL**: `/questions/add_questions/`
- **Method**: `POST`
- **البيانات**:
  ```json
  {
    "package": "integer",
    "test_content": "string",
    "option_A": "string",
    "option_B": "string",
    "option_C": "string",
    "option_D": "string",
    "option_E": "string",
    "right_answer": "string",
    "explanation": "string"
  }
  ```

#### إضافة صور للأسئلة
- **URL**: `/questions/add_question_images/`
- **Method**: `POST`
- **البيانات**: `FormData`
  - `test_id`: معرف السؤال
  - `field_name`: نوع الحقل (test_content, option_A, etc.)
  - `images`: ملف الصورة

#### الحصول على صور السؤال
- **URL**: `/questions/get_question_images/<int:test_id>/`
- **Method**: `GET`
- **المعاملات**: `test_id` (معرف السؤال)
- **الاستجابة**:
  ```json
  [
    {
      "id": "integer",
      "test_id": "integer",
      "field_name": "string",
      "images": "string"
    }
  ]
  ```

#### تعديل السؤال
- **URL**: `/questions/edit_question_by_id/<int:id>/`
- **Method**: `PUT`
- **المعاملات**: `id` (معرف السؤال)
- **البيانات**: نفس بيانات إضافة السؤال

#### حذف السؤال
- **URL**: `/questions/delete_question_by_id/<int:id>/`
- **Method**: `DELETE`
- **المعاملات**: `id` (معرف السؤال)
- **الاستجابة**:
  ```json
  {
    "message": "Question deleted successfully"
  }
  ```

### 5. إدارة حزم الاختبارات (Test Packages)

#### الحصول على الحزم حسب المادة
- **URL**: `/test_packages/get_packages/<str:subject_name>/`
- **Method**: `GET`
- **المعاملات**: `subject_name` (اسم المادة)
- **الاستجابة**:
  ```json
  [
    {
      "id": "integer",
      "package_name": "string",
      "publisher_id": "integer",
      "publisher_name": "string",
      "units": "string",
      "Class": "string",
      "subject_name": "string",
      "price": "integer",
      "date_added": "date",
      "number_of_apps": "integer",
      "number_of_purchases": "integer",
      "number_of_questions": "integer"
    }
  ]
  ```

#### الحصول على الاختبارات المحلولة من قبل الطالب
- **URL**: `/test_packages/get_student_solved_exams/<str:subject_name>/`
- **Method**: `GET`
- **المعاملات**: `subject_name` (اسم المادة)
- **الاستجابة**: قائمة بالاختبارات المحلولة

#### الحصول على معلومات حزمة واحدة
- **URL**: `/test_packages/get_single_package/<int:id>/`
- **Method**: `GET`
- **المعاملات**: `id` (معرف الحزمة)
- **الاستجابة**: معلومات الحزمة

#### زيادة عدد التطبيقات
- **URL**: `/test_packages/increase_num_of_apps/<int:id>/`
- **Method**: `POST`
- **المعاملات**: `id` (معرف الحزمة)
- **الاستجابة**:
  ```json
  {
    "message": "Number of applications increased successfully"
  }
  ```

#### زيادة عدد المشتريات
- **URL**: `/test_packages/increase_number_of_purchases/<int:id>/`
- **Method**: `POST`
- **المعاملات**: `id` (معرف الحزمة)
- **الاستجابة**:
  ```json
  {
    "message": "Number of purchases increased successfully"
  }
  ```

#### إنشاء حزمة اختبار جديدة
- **URL**: `/test_packages/create_test_packages/`
- **Method**: `POST`
- **البيانات**:
  ```json
  {
    "package_name": "string",
    "publisher_id": "integer",
    "publisher_name": "string",
    "units": "string",
    "Class": "string",
    "subject_name": "string",
    "price": "integer",
    "number_of_questions": "integer"
  }
  ```

#### الحصول على تفاصيل الحزمة
- **URL**: `/test_packages/get_package_details/<int:id>/`
- **Method**: `GET`
- **المعاملات**: `id` (معرف الحزمة)
- **الاستجابة**: تفاصيل الحزمة مع الأسئلة

#### الحصول على حزم المعلم
- **URL**: `/test_packages/get_test_packages_by_publisher_id/<int:id>/`
- **Method**: `GET`
- **المعاملات**: `id` (معرف المعلم)
- **الاستجابة**: قائمة بحزم المعلم

#### تعديل حزمة الاختبار
- **URL**: `/test_packages/edit_test_package/<int:id>/`
- **Method**: `PUT`
- **المعاملات**: `id` (معرف الحزمة)
- **البيانات**: نفس بيانات إنشاء الحزمة

#### حذف حزمة الاختبار
- **URL**: `/test_packages/delete_test_package/<int:id>/`
- **Method**: `DELETE`
- **المعاملات**: `id` (معرف الحزمة)
- **الاستجابة**:
  ```json
  {
    "message": "Test package deleted successfully"
  }
  ```

### 6. إدارة الاختبارات المكتملة (Student Related Exams)

#### تسجيل اختبار مكتمل
- **URL**: `/StudentRelatedExams/examDoneRecord/`
- **Method**: `POST`
- **البيانات**:
  ```json
  {
    "student": "integer",
    "subject_name": "string",
    "exam_name": "string",
    "exam_id": "string",
    "publisher_id": "integer",
    "publisher_name": "string",
    "result": "decimal",
    "price": "integer",
    "time_taken": "time"
  }
  ```

#### الحصول على الاختبارات المكتملة للطالب
- **URL**: `/StudentRelatedExams/student_done_exams/<int:id>/`
- **Method**: `GET`
- **المعاملات**: `id` (معرف الطالب)
- **الاستجابة**:
  ```json
  [
    {
      "id": "integer",
      "student": "integer",
      "subject_name": "string",
      "exam_name": "string",
      "exam_id": "string",
      "publisher_id": "integer",
      "publisher_name": "string",
      "date_of_application": "date",
      "result": "decimal",
      "price": "integer",
      "time_taken": "time"
    }
  ]
  ```

### 7. إدارة المحتوى المدفوع (Student Premium Content)

#### الحصول على المحتوى المدفوع للطالب
- **URL**: `/StudentPremiumContent/student/<int:student_id>/`
- **Method**: `GET`
- **المعاملات**: `student_id` (معرف الطالب)
- **الاستجابة**:
  ```json
  [
    {
      "id": "integer",
      "student": "integer",
      "student_name": "string",
      "Class": "string",
      "type": "string",
      "subject_name": "string",
      "content_id": "integer",
      "content_name": "string",
      "publisher_id": "integer",
      "publisher_name": "string",
      "purchase_date": "date",
      "price": "decimal",
      "date_of_expiry": "date",
      "is_expired": "boolean"
    }
  ]
  ```

#### الحصول على تفاصيل المحتوى المدفوع
- **URL**: `/StudentPremiumContent/details/<int:id>/`
- **Method**: `GET`
- **المعاملات**: `id` (معرف المحتوى المدفوع)
- **الاستجابة**: تفاصيل المحتوى المدفوع

#### إنشاء محتوى مدفوع مع فحص الرصيد
- **URL**: `/StudentPremiumContent/create-with-balance-check/`
- **Method**: `POST`
- **البيانات**:
  ```json
  {
    "student": "integer",
    "student_name": "string",
    "Class": "string",
    "type": "string",
    "subject_name": "string",
    "content_id": "integer",
    "content_name": "string",
    "publisher_id": "integer",
    "publisher_name": "string",
    "price": "decimal",
    "date_of_expiry": "date"
  }
  ```

#### فحص الوصول للمحتوى المدفوع
- **URL**: `/StudentPremiumContent/check-access/<int:student_id>/<int:content_id>/<str:content_type>/`
- **Method**: `GET`
- **المعاملات**: 
  - `student_id` (معرف الطالب)
  - `content_id` (معرف المحتوى)
  - `content_type` (نوع المحتوى)
- **الاستجابة**:
  ```json
  {
    "has_access": "boolean",
    "is_expired": "boolean",
    "expiry_date": "date"
  }
  ```

#### فحص شراء المحتوى
- **URL**: `/StudentPremiumContent/check-purchase/`
- **Method**: `POST`
- **البيانات**:
  ```json
  {
    "student_id": "integer",
    "content_id": "integer",
    "content_type": "string"
  }
  ```
- **الاستجابة**:
  ```json
  {
    "has_purchased": "boolean"
  }
  ```

### 8. إدارة قراءة الملاحظات (Student Read Notes)

#### إنشاء سجل قراءة ملاحظة
- **URL**: `/StudentReadNotes/create/`
- **Method**: `POST`
- **البيانات**:
  ```json
  {
    "student": "integer",
    "subject_name": "string",
    "note_name": "string",
    "note_id": "integer",
    "publisher_id": "integer",
    "publisher_name": "string"
  }
  ```

#### زيادة عدد القراءات
- **URL**: `/StudentReadNotes/increase_reads/<int:id>/`
- **Method**: `POST`
- **المعاملات**: `id` (معرف سجل القراءة)
- **الاستجابة**:
  ```json
  {
    "message": "Number of reads increased successfully"
  }
  ```

#### الحصول على الملاحظات المقروءة للطالب
- **URL**: `/StudentReadNotes/get_read_notes/<int:student_id>/`
- **Method**: `GET`
- **المعاملات**: `student_id` (معرف الطالب)
- **الاستجابة**:
  ```json
  [
    {
      "id": "integer",
      "student": "integer",
      "subject_name": "string",
      "note_name": "string",
      "note_id": "integer",
      "publisher_id": "integer",
      "publisher_name": "string",
      "number_of_reads": "integer",
      "first_read_at": "datetime",
      "last_read_at": "datetime"
    }
  ]
  ```

### 9. إدارة تتبع المواد (Student Subject Tracking)

#### إنشاء سجل تتبع مادة
- **URL**: `/StudentSubjectTracking/create/`
- **Method**: `POST`
- **البيانات**:
  ```json
  {
    "student": "integer",
    "Class": "string",
    "subject_name": "string",
    "number_of_notes": "integer",
    "number_of_exams": "integer"
  }
  ```

#### الحصول على تتبع المواد للطالب والصف
- **URL**: `/StudentSubjectTracking/student/<int:student_id>/class/<str:Class>/`
- **Method**: `GET`
- **المعاملات**: 
  - `student_id` (معرف الطالب)
  - `Class` (الصف الدراسي)
- **الاستجابة**:
  ```json
  [
    {
      "id": "integer",
      "student": "integer",
      "Class": "string",
      "subject_name": "string",
      "number_of_notes": "integer",
      "number_of_exams": "integer"
    }
  ]
  ```

### 10. المصادقة (Authentication)

#### الحصول على توكن
- **URL**: `/token/`
- **Method**: `POST`
- **البيانات**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **الاستجابة**:
  ```json
  {
    "access": "string",
    "refresh": "string"
  }
  ```

#### تحديث التوكن
- **URL**: `/token/refresh/`
- **Method**: `POST`
- **البيانات**:
  ```json
  {
    "refresh": "string"
  }
  ```
- **الاستجابة**:
  ```json
  {
    "access": "string"
  }
  ```

---

## تقنيات Django المستخدمة

### 1. Django ORM (Object-Relational Mapping)
- **الغرض**: التفاعل مع قاعدة البيانات باستخدام كود Python
- **الفوائد**:
  - كتابة استعلامات قاعدة البيانات بلغة Python
  - حماية من SQL Injection
  - سهولة في الصيانة والتطوير

### 2. Django Signals
- **الغرض**: تنفيذ إجراءات تلقائية عند حدوث أحداث معينة
- **الاستخدام في التطبيق**:
  - إنشاء ملفات شخصية تلقائياً عند تسجيل مستخدم جديد
  - حذف ملفات الصور عند حذف السجلات

### 3. Django Generic Views
- **الغرض**: تبسيط كتابة Views للعمليات الشائعة
- **الأنواع المستخدمة**:
  - `ListCreateAPIView`: لعرض القوائم وإنشاء سجلات جديدة
  - `RetrieveUpdateDestroyAPIView`: لعرض وتعديل وحذف سجل واحد

### 4. Django Serializers
- **الغرض**: تحويل البيانات بين JSON و Python objects
- **الفوائد**:
  - التحقق من صحة البيانات
  - تحويل البيانات تلقائياً
  - دعم العلاقات المعقدة

### 5. Django Permissions
- **الغرض**: التحكم في الوصول للـ APIs
- **الأنواع المستخدمة**:
  - `IsAuthenticated`: يتطلب تسجيل دخول
  - `IsOwnerOrReadOnly`: يسمح للمالك بالتعديل

### 6. Django File Upload
- **الغرض**: رفع ومعالجة الملفات
- **الميزات**:
  - رفع الصور للملاحظات والأسئلة
  - تخزين آمن للملفات
  - معالجة تلقائية لأحجام الصور

### 7. Django Pagination
- **الغرض**: تقسيم النتائج إلى صفحات
- **الفوائد**:
  - تحسين الأداء
  - تجربة مستخدم أفضل
  - تقليل استهلاك الذاكرة

### 8. Django CORS
- **الغرض**: السماح بالطلبات من مصادر مختلفة
- **الفوائد**:
  - دعم التطبيقات الأمامية
  - مرونة في التطوير
  - دعم التطبيقات المحمولة

### 9. Django JWT
- **الغرض**: نظام مصادقة آمن
- **الميزات**:
  - Tokens مؤقتة وآمنة
  - دعم Refresh Tokens
  - لا حاجة لحفظ حالة في الخادم

### 10. Django Database Relationships
- **الأنواع المستخدمة**:
  - `OneToOneField`: علاقة واحد لواحد
  - `ForeignKey`: علاقة واحد لكثير
  - `ManyToManyField`: علاقة كثير لكثير

---

## إعدادات المشروع

### قاعدة البيانات
- **النوع**: MySQL
- **الاسم**: svi-5th-project
- **المضيف**: localhost
- **المنفذ**: 3306

### الملفات الثابتة والوسائط
- **المجلد الثابت**: `staticfiles/`
- **مجلد الوسائط**: `media/`
- **URL الوسائط**: `/media/`

### JWT Settings
- **مدة صلاحية Access Token**: يوم واحد
- **مدة صلاحية Refresh Token**: 90 يوم
- **تناوب Refresh Tokens**: مفعل
- **القائمة السوداء بعد التناوب**: مفعل

### CORS Settings
- **السماح بجميع المصادر**: مفعل
- **السماح بجميع الأصول**: مفعل

---

## ملاحظات مهمة

1. **الأمان**: يجب تغيير `SECRET_KEY` في الإنتاج
2. **قاعدة البيانات**: يجب استخدام قاعدة بيانات منفصلة للإنتاج
3. **الملفات**: يجب إعداد تخزين سحابي للملفات في الإنتاج
4. **CORS**: يجب تقييد المصادر المسموحة في الإنتاج
5. **JWT**: يجب استخدام مفاتيح أقوى في الإنتاج

---

## استكشاف الأخطاء

### مشاكل شائعة:
1. **خطأ في قاعدة البيانات**: تحقق من إعدادات الاتصال
2. **خطأ في رفع الملفات**: تحقق من إعدادات الوسائط
3. **خطأ في المصادقة**: تحقق من صحة التوكن
4. **خطأ في CORS**: تحقق من إعدادات CORS

### نصائح للتطوير:
1. استخدم Django Debug Toolbar للتطوير
2. فعّل logging لمراقبة الأخطاء
3. استخدم Django Extensions للأدوات الإضافية
4. راجع Django Best Practices

---

هذه الوثائق تغطي جميع جوانب التطبيق من النماذج إلى نقاط النهاية والتقنيات المستخدمة. يمكن استخدامها كمرجع للمطورين الجدد أو كدليل للصيانة والتطوير المستقبلي.
