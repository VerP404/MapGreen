from django.shortcuts import render
from django.shortcuts import redirect
from .models import Object, TypeObject
from .forms import ObjectForm


def index(request):
    objects = Object.objects.filter(is_published=True).values('name', 'description', 'latitude', 'longitude')
    types = TypeObject.objects.all()
    return render(request, 'map_app/index.html', {'objects': list(objects), 'types': types})

def add_object(request):
    if request.method == 'POST':
        form = ObjectForm(request.POST, request.FILES)
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.user = request.user
            if 'latitude' in request.POST and request.POST['latitude']:
                new_object.latitude = request.POST['latitude']
                new_object.longitude = request.POST['longitude']
            if 'polygon' in request.POST and request.POST['polygon']:
                new_object.polygon = request.POST['polygon']
            new_object.save()
            return redirect('index')
    else:
        form = ObjectForm()
    return render(request, 'map_app/add_object.html', {'form': form})