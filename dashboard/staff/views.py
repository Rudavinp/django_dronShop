from django.template.response import TemplateResponse
from django.shortcuts import redirect, get_object_or_404
from account.models import User
from .forms import StaffForm
from django.contrib.sites.models import Site




def staff_list(request):
    staff = User.objects.filter(is_staff=True)
    all = User.objects.all()
    ctx = {'staff':all}
    cur_site = Site.objects.get_current()
    print('alalal', cur_site)
    return TemplateResponse(request, 'dashboard/staff/list.html', ctx)


def staff_detail(request, staff_pk):
    staff = get_object_or_404(User, pk=staff_pk)
    form = StaffForm(request.POST or None, instance=staff)
    if form.is_valid():
        form.save()
        return redirect('dashboard:staff-list')
    ctx = {'staff':staff, 'form':form}
    return TemplateResponse(request, 'dashboard/staff/details.html', ctx)