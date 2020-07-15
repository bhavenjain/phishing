from django.shortcuts import render
import requests
import subprocess
from subprocess import run
from subprocess import PIPE
import sys

def button(request):
	return render(request,'homepage.htm')

def external(request):
	inp = request.POST.get('param')
	out = run([sys.executable,'/Users/Bhaven/bhaven/python/hackathon/buttonpython/test.py',inp,],shell = False,stdout = PIPE )
	print(out)
	return render(request,'homepage.htm',{'data1':out.stdout})
