from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import *
import pickle
import numpy as np
import os


def home(request):
    return render(request, 'index.html')

def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')

def doctor(request):
    return render(request, 'doctor.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # In a real app, we might save this or send an email
        return render(request, 'contact.html', {'message': 'Signal Transmitted Successfully! Our faculty will respond via secure channel.'})
    return render(request, 'contact.html')

def predict(request):
    return render(request, 'predict.html')

def predict_disease(request):
    if request.method == "POST":
        user_symptoms = request.POST.get('symptoms', '').lower()
        
        result = "Inconclusive"
        medication = "General Wellness Checklist"
        confidence = 50
        
        model_path = os.path.join(settings.BASE_DIR, 'disease_model.pkl')
        meta_path = os.path.join(settings.BASE_DIR, 'model_metadata.pkl')
        
        if os.path.exists(model_path) and os.path.exists(meta_path):
            try:
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)
                with open(meta_path, 'rb') as f:
                    meta = pickle.load(f)
                
                all_symptoms = meta['all_symptoms']
                symptom_to_idx = meta['symptom_to_idx']
            except Exception as e:
                print(f"Model Load Error: {e}")
                return render(request, 'predict.html', {'result': "System Calibration Required", 'medication': "Please contact support to refresh diagnostic models.", 'confidence': 0})
            
            # Create feature vector
            X = np.zeros(len(all_symptoms))
            found_any = False
            for s in all_symptoms:
                if s.lower() in user_symptoms:
                    X[symptom_to_idx[s]] = 1
                    found_any = True
            
            if found_any:
                prediction = model.predict([X])[0]
                # Get confidence (probability)
                probs = model.predict_proba([X])[0]
                conf = np.max(probs) * 100
                
                result = prediction
                confidence = int(conf)
                
                # Dynamic advice based on disease
                advice_map = {
                    'Fungal infection': 'Antifungal creams, keep skin dry.',
                    'Allergy': 'Antihistamines, avoid allergens.',
                    'GERD': 'Antacids, avoid spicy food.',
                    'Chronic cholestasis': 'Hepatoprotective meds, consult specialist.',
                    'Drug Reaction': 'Stop medication, seek emergency care.',
                    'Peptic ulcer diseae': 'Proton pump inhibitors, avoid NSAIDs.',
                    'AIDS': 'Antiretroviral therapy, consult infectious disease expert.',
                    'Diabetes': 'Metformin, insulin, low sugar diet.',
                    'Gastroenteritis': 'Rehydration salts, probiotics.',
                    'Bronchial Asthma': 'Bronchodilators, inhalers.',
                    'Hypertension': 'Antihypertensives, low salt diet.',
                    'Migraine': 'Pain relievers, rest in dark room.',
                    'Jaundice': 'Liver supplements, rest.',
                    'Malaria': 'Antimalarial drugs (Chloroquine/Artemether).',
                    'Chicken pox': 'Antivirals, calamine lotion.',
                    'Dengue': 'Hydration, paracetamol (avoid aspirin).',
                    'Typhoid': 'Antibiotics, fluid intake.',
                    'Tuberculosis': 'Long-term antitubercular regimen.',
                    'Common Cold': 'Rest, fluids, paracetamol.',
                    'Pneumonia': 'Antibiotics, rest, oxygen if needed.',
                    'Heart attack': 'EMERGENCY: Call hospital immediately.',
                    'Varicose veins': 'Compression stockings, exercise.',
                    'Acne': 'Benzoyl peroxide, retinoids.',
                    'Urinary tract infection': 'Antibiotics, cranberry juice.',
                }
                medication = advice_map.get(result, "Consult a clinical specialist for personalized protocol.")

        # Save history if logged in
        patient_id = request.session.get('userid')
        if patient_id:
            Prediction.objects.create(
                patient = Patient.objects.get(id=patient_id),
                symptoms=user_symptoms,
                predicted_disease=result,
                confidence=confidence,
                medication=medication
            )
        
        return render(request, 'predict.html', {
            'result': result, 
            'medication': medication, 
            'confidence': confidence, 
            'active_tab': 'symptoms',
            'accuracy_graph': '/static/plots/accuracy_graph.png',
            'report_link': '/static/plots/classification_report.txt'
        })
    return render(request, 'predict.html')

def chatbot(request):
    patient_id = request.session.get('userid')
    if not patient_id:
        return redirect('/login/')
    
    chat_history = Chatbot.objects.filter(patient_id=patient_id).order_by('-id')[:10]
    return render(request, 'chatbot.html', {'chat_history': reversed(chat_history)})

def chatbot_query(request):
    if request.method == "POST":
        query = request.POST.get('query', '').lower()
        patient_id = request.session.get('userid')
        
        if patient_id:
            # Professional Clinical Knowledge Base
            clinical_insights = {
                "headache": "Bad headaches with light sensitivity usually mean migraines. It's best to rest in a dark, quiet room.",
                "abdomen": "Stomach pain can be caused by many things like indigestion or something more serious. Watch if the pain gets worse in one spot.",
                "cough": "A dry cough without a fever is often caused by allergies or dust in the air.",
                "heart": "A fast heartbeat can be caused by stress, caffeine, or sometimes a heart issue.",
                "rash": "Skin rashes after touching something usually mean your skin is irritated or you have an allergy.",
                "paracetamol": "For adults, the usual dose is 1 or 2 tablets (500mg-1000mg) every 4 to 6 hours. Do not take more than 8 tablets in a day.",
                "scrape": "Clean the wound with water, apply some antiseptic cream, and keep it covered with a bandage.",
                "vitamin d": "Vitamin D is important for bones. It's best to check your levels with a blood test before taking high doses.",
                "antibiotic": "If you miss a dose, take it as soon as you remember. Always finish the whole pack even if you feel better.",
                "aspirin": "Don't take Aspirin if you have stomach ulcers, as it can cause bleeding.",
                "back pain": "To avoid back pain, try to sit up straight and exercise your core muscles regularly.",
                "fiber": "Eating more fiber (like fruits and veggies) helps your digestion and keeps your heart healthy.",
                "water": "Try to drink about 8-10 glasses of water a day to stay hydrated.",
                "sleep": "To sleep better, try to go to bed at the same time every night and avoid screens before bed.",
                "blood pressure": "It's a good idea to check your blood pressure once a year. Healthy is usually around 120/80.",
                "viral": "Antibiotics don't work on viruses like the common cold. Rest and fluids are usually best.",
                "cholesterol": "There is 'good' and 'bad' cholesterol. Lowering the 'bad' one helps protect your heart.",
                "finish": "You must finish your full course of antibiotics to make sure all the bacteria are gone.",
                "sprain": "For sprains and strains, use the RICE method: Rest, Ice, Compression, and Elevation.",
                "heart rate": "A normal resting heart rate is between 60 and 100 beats per minute.",
                "diabetes": "Managing diabetes means keeping your blood sugar levels steady with healthy food and exercise.",
                "fever": "A fever is your body's way of fighting infection. Drink plenty of water and rest.",
                "chest pain": "Chest pain can be serious. If it's sharp or spreads to your arms, get medical help immediately.",
                "dizziness": "Feeling dizzy can happen if you stand up too fast, are dehydrated, or have an inner ear issue.",
                "sore throat": "A sore throat is usually from a cold. If it's hard to swallow, a doctor should check it.",
                "insomnia": "Struggling to sleep is often caused by stress or late-night habits.",
                "anxiety": "Anxiety can make you feel tense or worried. Deep breathing and talking to someone can help.",
                "joint pain": "Joint pain can be caused by overuse or arthritis. Gentle movement often helps.",
                "asthma": "Asthma makes it hard to breathe. Use your inhaler and avoid things like smoke or dust.",
                "uti": "A UTI usually causes pain when peeing. It needs to be treated quickly with medicine.",
                "kidney stones": "Kidney stones cause very sharp pain in your side. Drinking lots of water can help prevent them.",
                "thyroid": "The thyroid controls your energy levels. A simple blood test can check if it's working right.",
                "anemia": "Anemia means your blood has low iron, which can make you feel very tired.",
                "dehydration": "Signs of dehydration include dark urine and a dry mouth. Drink water immediately.",
                "flu": "The flu is a bad cold with fever and body aches. Rest is very important.",
                "allergy": "Allergies happen when your body reacts to things like pollen or pets. Antihistamines can help.",
                "eye strain": "Looking at screens for too long strains your eyes. Take a break every 20 minutes.",
                "nausea": "Feeling sick to your stomach can be from food or a virus. Sip water and rest."
            }

            # Map the insight based on keywords
            insight = "Please consult a doctor for a clear medical check."
            for key, val in clinical_insights.items():
                if key in query:
                    insight = val
                    break

            # Professional Clinical Report Format
            bot_response = f"""
            <div class='clinical-protocol-card'>
                <div class='d-flex align-items-center gap-2 mb-3'>
                    <span class='rounded-pill bg-primary bg-opacity-10 text-primary px-3 py-1 x-small fw-bold'>Health Case: {query[:15]}...</span>
                </div>
                <p class='mb-3 text-dark fw-bold fs-6 lh-lg'>{insight}</p>
                <div class='bg-light p-3 rounded-4 border-start border-primary border-4 mb-4'>
                    <p class='mb-0 small text-muted-blue fw-bold'>
                        <i class='fa fa-circle-info me-2 text-primary'></i> Tip: This is a general guide. Please talk to a doctor for a real diagnosis.
                    </p>
                </div>
                <a href='/viewdoctor/' class='btn btn-primary w-100 rounded-pill py-3 fw-bold shadow-lg transform-active d-flex align-items-center justify-content-center gap-3'>
                    <i class='fa fa-calendar-check'></i> BOOK NOW
                </a>
            </div>
            """
            
            chat = Chatbot(patient_id=patient_id, user_message=query, bot_response=bot_response)
            chat.save()
            
    return redirect('/chatbot/')

def book_appointment(request):
    doctor_id = request.GET.get('doctor_id')
    doc = Doctor.objects.get(id=doctor_id)
    return render(request, 'book_appointment.html', {'doctor': doc})

def confirm_booking(request):
    if request.method == "POST":
        doctor_id = request.POST.get('doctor_id')
        patient_id = request.session.get('userid')
        date = request.POST.get('date')
        
        if not patient_id:
            return redirect('/login/')
            
        patient = Patient.objects.get(id=patient_id)
        doctor = Doctor.objects.get(id=doctor_id)
        
        # Generate Token
        last_app = Appointment.objects.filter(doctor=doctor, appointment_date=date).order_by('-token_number').first()
        token = (last_app.token_number + 1) if last_app and last_app.token_number else 1
        
        appointment = Appointment(patient=patient, doctor=doctor, appointment_date=date, status='Pending', token_number=token)
        appointment.save()
        
        return redirect('/appointments/')
        
    return redirect('/home/')

def appointments(request):
    if 'did' in request.session:
        did = request.session.get('did')
        results = Appointment.objects.filter(doctor_id=did).order_by('-id')
    elif 'userid' in request.session:
        uid = request.session.get('userid')
        results = Appointment.objects.filter(patient_id=uid).order_by('-id')
    elif 'admin' in request.session:
        results = Appointment.objects.all().order_by('-id')
    else:
        return redirect('/login/')
    
    total = results.count()
    pending = results.filter(status='Pending').count()
    completed = results.filter(status='Completed').count()
    
    return render(request, 'appointments.html', {
        'result': results,
        'total': total,
        'pending': pending,
        'completed': completed
    })

def addregister(request):
    if request.method=="POST":
        a=request.POST.get('name') 
        b=request.POST.get('email')
        c=request.POST.get('password')
        d=request.POST.get('phone')
        e=request.POST.get('age')
        if not e:
            e = 0
        f=request.POST.get('gender')
        ins=Patient(name=a,email=b,password=c,phone=d,age=e,gender=f)
        ins.save()
    return render(request,"index.html", {'message':'Successfully Registered'})
def login(request):
    return render(request,'login.html')

def addlogin(request):
    email=request.POST.get('email')
    password=request.POST.get('password')
    if email=='admin@gmail.com' and password=='admin':
        request.session['admin@gmail.com']='admin@gmail.com'
        request.session['admin']='admin'
        return render(request,'index.html')
    
    elif Admin.objects.filter(email=email, password=password).exists():
        admin = Admin.objects.get(email=email, password=password)
        request.session['admin'] = admin.name
        return render(request, 'index.html')

    elif Patient.objects.filter(email=email,password=password).exists():
        userdetails=Patient.objects.get(email=email,password=password)
        if userdetails.email==request.POST['email']:
            request.session['userid']=userdetails.id
            request.session['username']=userdetails.name 
            return redirect('/home/')  
        
    elif Doctor.objects.filter(email=email,password=password).exists():
        userdetails=Doctor.objects.get(email=email,password=password)
        if userdetails.email==request.POST['email']:
            request.session['did']=userdetails.id
            request.session['doctorname']=userdetails.name 
            return redirect('/home/')
        else:
            return render(request, "login.html", {'message': 'Invalid Email or Password'})
    else:
        return render(request, 'login.html', {'message':'Invalid Email or Password'})

def send_feedback(request):
    if 'userid' not in request.session:
        return redirect('/login/')
    
    if request.method == "POST":
        uid = request.session.get('userid')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        patient = Patient.objects.get(id=uid)
        
        Feedback.objects.create(patient=patient, subject=subject, message=message)
        return render(request, "index.html", {'message': 'Feedback Sent Successfully'})
    
    # View history for patient
    feedbacks = Feedback.objects.filter(patient_id=request.session.get('userid')).order_by('-date')
    return render(request, "feedback.html", {'feedbacks': feedbacks})

def add_review(request):
    if 'userid' not in request.session:
        return redirect('/login/')
    
    if request.method == "POST":
        uid = request.session.get('userid')
        did = request.POST.get('doctor_id')
        rating = request.POST.get('rating')
        comments = request.POST.get('comments')
        
        patient = Patient.objects.get(id=uid)
        doctor = Doctor.objects.get(id=did)
        
        Review.objects.create(patient=patient, doctor=doctor, rating=rating, comments=comments)
        return render(request, "index.html", {'message': 'Review Submitted Successfully'})
    
    doctor_id = request.GET.get('doctor_id')
    doc = Doctor.objects.get(id=doctor_id)
    return render(request, "add_review.html", {'doctor': doc})

def view_feedback(request):
    if 'admin' not in request.session:
        return redirect('/login')
    
    feedbacks = Feedback.objects.all().order_by('-date')
    return render(request, "admin_feedback.html", {'feedbacks': feedbacks})

def admin_respond_feedback(request):
    if 'admin' not in request.session:
        return redirect('/login')
    
    if request.method == "POST":
        fid = request.POST.get('fid')
        res = request.POST.get('response')
        Feedback.objects.filter(id=fid).update(response=res)
        
    return redirect('/view_feedback')

def logout(request):
    session_keys=list(request.session.keys())   
    for key in session_keys:
            del request.session[key] 
    return redirect(index)

def viewuser(request):
    user=Patient.objects.all()
    return render(request,'viewuser.html',{'result':user})  

def viewdoctor(request):
    specialization = request.GET.get('specialization')
    if specialization:
        user = Doctor.objects.filter(specialization=specialization)
    else:
        user = Doctor.objects.all()
    
    # Get unique specializations for the filter
    specialties = Doctor.objects.values_list('specialization', flat=True).distinct()
    
    return render(request, 'viewdoctor.html', {
        'result': user, 
        'specialties': specialties,
        'selected_specialty': specialization
    })


def adddoctor(request):
    if request.method=="POST":
        a = request.POST.get('name') 
        b = request.POST.get('email')
        c = request.POST.get('password')
        d = request.POST.get('phone')
        e = request.POST.get('specialization')
        f = request.POST.get('experience')
        if not f:
            f = 0
        myfile = request.FILES['image'] 
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        ins = Doctor(name=a, email=b, password=c, phone=d, specialization=e, experience=f, image=filename)
        ins.save()
    return render(request, "index.html", {'message': 'Successfully Registered'})

def view_history(request):
    patient_id = request.session.get('userid')
    if not patient_id:
        return redirect('/login')
    symptom_results = Prediction.objects.filter(patient_id=patient_id).order_by('-date')
    return render(request, 'history.html', {'symptom_result': symptom_results})

def view_prescriptions(request):
    patient_id = request.session.get('userid')
    if not patient_id:
        return redirect('/login')
    consultations = Consultation.objects.filter(patient_id=patient_id)
    prescriptions = Prescription.objects.filter(consultation__in=consultations)
    return render(request, 'prescriptions.html', {'result': prescriptions})

def update_appointment_status(request):
    if request.method == "POST":
        app_id = request.POST.get('app_id')
        status = request.POST.get('status')
        Appointment.objects.filter(id=app_id).update(status=status)
    return redirect('/appointments')


def add_slot(request):
    if 'did' not in request.session:
        return redirect('/login')
    
    if request.method == "POST":
        date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location', 'Clinic')
        capacity = int(request.POST.get('capacity', 1))
        did = request.session.get('did')
        doctor = Doctor.objects.get(id=did)
        
        for _ in range(capacity):
            Slot.objects.create(doctor=doctor, date=date, time=time, location=location, status='Available')
        return render(request, "index.html", {'message': f'Slot Added Successfully with capacity: {capacity}'})
    
    return render(request, "add_slot.html")

from datetime import date

def view_slots(request):
    doctor_id = request.GET.get('doctor_id')
    doctor = Doctor.objects.get(id=doctor_id)
    today = date.today()
    slots_qs = Slot.objects.filter(doctor=doctor, status='Available', date__gte=today).order_by('date', 'time')
    
    # Intelligent grouping for capacity support
    unique_slots = []
    seen_times = set()
    for s in slots_qs:
        time_key = (s.date, s.time)
        if time_key not in seen_times:
            unique_slots.append(s)
            seen_times.add(time_key)
            
    reviews = Review.objects.filter(doctor=doctor).order_by('-date')
    return render(request, "view_slots.html", {'doctor': doctor, 'slots': unique_slots, 'reviews': reviews})

def book_slot(request):
    if 'userid' not in request.session:
        return redirect('/login/')
    
    if request.method == "POST":
        slot_id = request.POST.get('slot_id')
        uid = request.session.get('userid')
        
        slot = Slot.objects.get(id=slot_id)
        patient = Patient.objects.get(id=uid)
        
        # Check if slot date is in the past
        if slot.date < date.today():
             return redirect('/viewdoctor/')
        
        # Generate Token
        last_app = Appointment.objects.filter(doctor=slot.doctor, appointment_date=slot.date).order_by('-token_number').first()
        token = (last_app.token_number + 1) if last_app and last_app.token_number else 1

        # Create appointment
        Appointment.objects.create(
            patient=patient,
            doctor=slot.doctor,
            slot=slot,
            appointment_date=slot.date,
            status='Pending',
            token_number=token
        )
        
        # Update slot status
        slot.status = 'Booked'
        slot.save()
        return render(request, 'book_slot_confirmation.html', {'doctor': slot.doctor, 'date': slot.date, 'time': slot.time, 'location': slot.location, 'token': token, 'message': 'Booking successfully'})
    
    # GET request: Show confirmation page
    slot_id = request.GET.get('slot_id')
    if not slot_id:
        return redirect('/viewdoctor/')
    slot = Slot.objects.get(id=slot_id)
    return render(request, "book_slot_confirmation.html", {'slot': slot, 'doctor': slot.doctor})

def cancel_appointment(request):
    if 'userid' not in request.session:
        return redirect('/login/')
    if request.method == "POST":
        app_id = request.POST.get('app_id')
        app = Appointment.objects.get(id=app_id)
        if app.slot:
            app.slot.status = 'Available'
            app.slot.save()
        app.status = 'Cancelled'
        app.save()
        return redirect('/appointments/')
    return redirect('/appointments/')

def log_report(request, patient_id):
    if 'did' not in request.session:
        return redirect('/login')
    patient = Patient.objects.get(id=patient_id)
    return render(request, "log_report.html", {'patient': patient})

def doctor_view_patient_history(request, patient_id):
    if 'did' not in request.session and 'admin' not in request.session:
        return redirect('/login')
    
    patient = Patient.objects.get(id=patient_id)
    # Get all reports/consultations
    consultations = Consultation.objects.filter(patient=patient).order_by('-id')
    
    # Get all predictions
    predictions = Prediction.objects.filter(patient=patient).order_by('-date')
    
    reports_data = []
    for c in consultations:
        prescription = Prescription.objects.filter(consultation=c).first()
        reports_data.append({
            'consultation': c,
            'prescription': prescription
        })
        
    return render(request, 'doctor_patient_history.html', {
        'patient': patient,
        'reports': reports_data,
        'predictions': predictions
    })

def add_report(request):
    if 'did' not in request.session:
        return redirect('/login')
    
    if request.method == "POST":
        patient_id = request.POST.get('patient_id')
        remarks = request.POST.get('remarks')
        medicines = request.POST.get('medicines')
        did = request.session.get('did')
        
        patient = Patient.objects.get(id=patient_id)
        doctor = Doctor.objects.get(id=did)
        
        # Create Consultation
        consultation = Consultation.objects.create(patient=patient, doctor=doctor, remarks=remarks)
        
        # Handle Prescription File
        prescription_filename = None
        if 'prescription_file' in request.FILES:
            myfile = request.FILES['prescription_file']
            fs = FileSystemStorage()
            prescription_filename = fs.save('prescriptions/' + myfile.name, myfile)

        # Create Prescription if medicines or file provided
        if medicines or prescription_filename:
            Prescription.objects.create(
                consultation=consultation, 
                medicines=medicines, 
                prescription_file=prescription_filename
            )
            
        return redirect('/viewuser/')
    return redirect('/doctor/')

def view_reports(request):
    if 'userid' not in request.session:
        return redirect('/login')
    
    uid = request.session.get('userid')
    consultations = Consultation.objects.filter(patient_id=uid).order_by('-id')
    
    reports_data = []
    for c in consultations:
        prescription = Prescription.objects.filter(consultation=c).first()
        reports_data.append({
            'consultation': c,
            'prescription': prescription
        })
        
    return render(request, 'view_reports.html', {'result': reports_data})

def profile(request):
    if 'userid' not in request.session:
        return redirect('/login')
    
    uid = request.session.get('userid')
    patient = Patient.objects.get(id=uid)
    
    if request.method == "POST":
        patient.name = request.POST.get('name')
        patient.email = request.POST.get('email')
        patient.phone = request.POST.get('phone')
        patient.age = request.POST.get('age')
        patient.gender = request.POST.get('gender')
        password = request.POST.get('password')
        if password:
            patient.password = password
        patient.save()
        return render(request, 'profile.html', {'patient': patient, 'message': 'Profile Updated Successfully'})
        
    return render(request, 'profile.html', {'patient': patient})

