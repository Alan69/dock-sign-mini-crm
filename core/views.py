from django.shortcuts import render, get_object_or_404, redirect
from .models import Document, DockSignGroup
from django.contrib.auth.decorators import login_required
from .forms import DocumentForm, SignDocumentForm, AddUserForm, SignDocumentForm2, DockSignGroupForm
from .utils import bs12
from django.contrib.auth.models import User
from django.contrib import messages

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

@login_required
def docksigngroup_detail(request, pk):
    group = get_object_or_404(DockSignGroup, pk=pk)
    add_user_form = AddUserForm()
    sign_form = SignDocumentForm2(instance=group)

    if request.method == 'POST':
        if 'add_user' in request.POST:
            add_user_form = AddUserForm(request.POST)
            if add_user_form.is_valid():
                username = add_user_form.cleaned_data['username']
                try:
                    new_user = User.objects.get(username=username)
                    if group.add_user(request.user, new_user):
                        messages.success(request, f"User {username} added to the group.")
                    else:
                        messages.error(request, "You do not have permission to add users to this group.")
                except User.DoesNotExist:
                    add_user_form.add_error('username', 'User does not exist')
            else:
                messages.error(request, "Error adding user.")
        elif 'sign_document' in request.POST:
            sign_form = SignDocumentForm2(request.POST, instance=group)
            if sign_form.is_valid():
                group.sign_document(request.user)
                messages.success(request, "Document signed successfully.")
            else:
                messages.error(request, "Error signing document.")

        return redirect(docksigngroup_detail, pk=group.pk)

    context = {
        'group': group,
        'add_user_form': add_user_form,
        'sign_form': sign_form,
    }
    return render(request, 'backend/docksigngroup_detail.html', context)

def create_docksigngroup(request):
    if request.method == 'POST':
        form = DockSignGroupForm(request.POST)
        if form.is_valid():
            docksigngroup = form.save(commit=False)
            docksigngroup.created_by = request.user  # Assign the current user as the creator
            docksigngroup.save()
            form.save_m2m()  # Save the many-to-many relationships
            return redirect(docksigngroup_detail, pk=docksigngroup.pk)  # Redirect to detail view
    else:
        form = DockSignGroupForm()
    
    context = {
        'form': form,
    }
    return render(request, 'backend/create_docksigngroup.html', context)

@login_required
def user_docksigngroups(request):
    # Fetch all DockSignGroup instances where the current user is a member
    groups = DockSignGroup.objects.filter(users=request.user)
    
    context = {
        'groups': groups,
    }
    return render(request, 'backend/user_docksigngroups.html', context)