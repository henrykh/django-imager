from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from imager_user.models import ImagerProfile
from django.views.generic import UpdateView


@login_required
def profile(request):
    context = {'name': request.user}
    return render(request, 'profile.html', context)


@login_required

def profile_edit(request):
    context = {'name': request.user}
    return render(request, 'profile_edit.html', context)


# class ProfileEdit(UpdateView):
#     def user_passes_test(self, request):
#         if request.user.is_authenticated():
#             self.object = self.get_object()
#             return self.object.user == request.user
#         return False

#     def dispatch(self, request, *args, **kwargs):
#         if not self.user_passes_test(request):
#             return redirect_to_login(request.get_full_path())
#         return super(ProfileEdit, self).dispatch(
#             request, *args, **kwargs)

#     def get_success_url(self):
#         return self.request.GET['src']

#     form_class = PhotoUpdateViewForm
#     model = ImagerProfile
#     template_name = 'profile_edit.html'
