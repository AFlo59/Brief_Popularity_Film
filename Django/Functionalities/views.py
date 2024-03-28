from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def test_view(request):
    return render(request, 'test.html')