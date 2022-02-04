from ctypes.wintypes import PINT
from django.shortcuts import render, redirect
from googletrans import Translator
import googletrans

# Create your views here.
def index(request):
    context = {
        'ndict' : googletrans.LANGUAGES
    }
    if request.method == 'POST':
        bef = request.POST.get('before')
        src = request.POST.get('src', '')
        dest = request.POST.get('dest', '')

        translator = Translator()
        trans1 = translator.translate(bef, src=src, dest=dest)
        print("번역 완료: ", trans1.text)
        context.update({
            'aft' : trans1.text,
            'bef' : bef,
            'src' : src,
            'dest' : dest,
        })
    return render(request, 'trans/index.html', context)