from django.shortcuts import render, redirect
from .models import Document
from django.contrib.auth.decorators import login_required
from .forms import DocumentForm, SignDocumentForm
from .utils import bs12
from django.contrib.auth.models import User

@login_required
def home(request):
    documents = Document.objects.all()
    last_three_objects = Document.objects.all().order_by('-id')[:4]
    last_three_user = User.objects.all().order_by('-id')[:4]
    last_user = User.objects.all().first
    user_count = User.objects.count()
    last_registered_user = User.objects.latest('date_joined')

    context = {
        'documents': documents,
        'last_three_objects': last_three_objects,
        'user_count': user_count,
        'last_registered_user': last_registered_user,
        'last_user': last_user,
        'last_three_user': last_three_user,
    }
    return render(request, 'backend/index.html', context)

def doc_list(request):
    documents = Document.objects.all()
    return render(request, 'backend/doc_list.html', {'documents': documents})

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file with the associated user
            document = form.save(commit=False)
            document.uploaded_by = request.user
            # print(bs12(request.FILES['file'].read(), request.user.private_key))
            document.save()

            # Now that the file is saved, sign its content
            # signed_content = bs12(request.FILES['file'].read(), request.user.private_key)

            # Update the document with the signed content and status
            document.file = request.FILES['file']
            document.status = 'не подписан'
            document.save()

            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'backend/upload_document.html', {'form': form})

@login_required
def sign_document(request):
    documents = Document.objects.all()  # Get all unsigned documents
    if request.method == 'POST':
        form = SignDocumentForm(request.POST)
        if form.is_valid():
            document_ids = form.cleaned_data.get('documents')
            for document_id in document_ids:
                document = Document.objects.get(name=document_id)
                document.status = 'подписан'  # Set status to "pending"
                document.count = document.count + 1
                document.save()
            return redirect('home')
    else:
        # Pass document IDs to the form
        initial_data = {'documents': [document.id for document in documents]}
        form = SignDocumentForm(initial=initial_data)
    return render(request, 'backend/sign_document.html', {'form': form, 'documents': documents})
