from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserWorkerForm
from .models import Worker, Attendance
from django.http import JsonResponse

def home(request):
    return render(request, 'home.html')

def success_view(request):
    # Retrieve the registered user and worker data from the session
    registered_worker = request.session.get('registered_worker')

    # Clear session data to prevent displaying it again
    request.session.pop('registered_worker', None)

    return render(request, 'success.html', {'registered_worker': registered_worker})

def give_view(request):
    return render(request, 'give.html')

# Worker registration view
def worker_user(request):
    if request.method == 'POST':
        form = UserWorkerForm(request.POST, request.FILES)
        if form.is_valid():
            worker_instance = form.save(commit=False)
            worker_instance.save()  # Generates the QR code and worker ID
            
            # Store worker data in session
            request.session['registered_worker'] = {
                'first_name': worker_instance.first_name,
                'last_name': worker_instance.last_name,
                'department': worker_instance.department,
                'worker_id': str(worker_instance.worker_id),
                'qr_code_url': worker_instance.qr_code.url,
            }
            return redirect('success')
    else:
        form = UserWorkerForm()

    return render(request, 'worker.html', {'form': form})

# View all worker cards
def worker_cards(request):
    workers = Worker.objects.all()
    return render(request, 'worker_cards.html', {'workers': workers})

# Worker detail view
def worker_detail(request, worker_id):
    worker = get_object_or_404(Worker, worker_id=worker_id)
    return render(request, 'worker_detail.html', {'worker': worker})

# Record attendance view
def record_attendance(request):
    if request.method == 'POST':
        barcode = request.POST.get('barcode')
        event_name = request.POST.get('event_name', 'General Event')

        # Find the worker by barcode (assuming barcode is worker_id or QR code)
        worker = get_object_or_404(Worker, worker_id=barcode)  # Adjust based on your barcode logic
        
        # Record attendance
        attendance = Attendance.objects.create(worker=worker, event_name=event_name)
        return JsonResponse({'success': True, 'message': 'Attendance recorded.', 'worker': worker.worker_id})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
