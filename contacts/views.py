from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Contact
from .forms import ContactRequestForm


@login_required
def contacts_list_view(request):
    friends = Contact.objects.filter(
        from_user=request.user,
        status=Contact.STATUS_ACCEPTED
    )

    incoming_requests = Contact.objects.filter(
        to_user=request.user,
        status=Contact.STATUS_PENDING
    )

    return render(request, 'contacts/contacts_list.html', {
        'friends': friends,
        'incoming_requests': incoming_requests
    })


@login_required
def send_request_view(request):
    if request.method == 'POST':
        form = ContactRequestForm(request.POST, from_user=request.user)
        if form.is_valid():
            to_user = form.cleaned_data['to_user']

            if to_user != request.user:
                Contact.objects.get_or_create(
                    from_user=request.user,
                    to_user=to_user
                )
            return redirect('contacts:list')
    else:
        form = ContactRequestForm(from_user=request.user)

    return render(request, 'contacts/send_request.html', {'form': form})


@login_required
def accept_request_view(request, pk):
    contact = get_object_or_404(
        Contact,
        pk=pk,
        to_user=request.user,
        status=Contact.STATUS_PENDING
    )

    contact.status = Contact.STATUS_ACCEPTED
    contact.save()

    # создаём обратную связь
    Contact.objects.get_or_create(
        from_user=request.user,
        to_user=contact.from_user,
        status=Contact.STATUS_ACCEPTED
    )

    return redirect('contacts:list')


@login_required
def reject_request_view(request, pk):
    contact = get_object_or_404(
        Contact,
        pk=pk,
        to_user=request.user,
        status=Contact.STATUS_PENDING
    )

    contact.status = Contact.STATUS_REJECTED
    contact.save()

    return redirect('contacts:list')
