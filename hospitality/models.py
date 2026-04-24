from django.db import models
class Admin(models.Model):
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)

class Doctor(models.Model):
    name = models.CharField(max_length=150)
    specialization = models.CharField(max_length=150)
    experience = models.IntegerField()
    email = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    image = models.CharField(max_length=150)

class Patient(models.Model):
    name = models.CharField(max_length=150)
    age = models.IntegerField()
    gender = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    password = models.CharField(max_length=150)

class Slot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=150)
    location = models.CharField(max_length=150, default='Clinic')
    status = models.CharField(max_length=150, default='Available') # Available, Booked

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, null=True)
    appointment_date = models.DateField()
    status = models.CharField(max_length=150)
    token_number = models.IntegerField(null=True, blank=True)

class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    remarks = models.TextField()

class Prescription(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    medicines = models.TextField()
    prescription_file = models.CharField(max_length=150, null=True, blank=True)

class Review(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comments = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

class Prediction(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    symptoms = models.TextField()
    predicted_disease = models.CharField(max_length=150)
    confidence = models.IntegerField()
    medication = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

class ImagePrediction(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    image = models.CharField(max_length=150)
    prediction = models.CharField(max_length=150)
    confidence = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    subject = models.CharField(max_length=150)
    message = models.TextField()
    response = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

class Chatbot(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    user_message = models.TextField()
    bot_response = models.TextField()
