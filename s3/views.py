from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
import boto3
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import subprocess

s3 = boto3.client('s3')

@csrf_exempt
def index(request):
    return render(request,'index.html')

@csrf_exempt
def list_obj(request):
    paginator = s3.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=request.POST['bucket'], Prefix=request.POST['prefix'])
    obj_list = []

    if request.method == 'POST':
        for page in pages:
            contents = page["Contents"]
            for obj in contents:
                obj_list.append(obj["Key"])
    data = {'obj_list': obj_list}
    return JsonResponse(data)

@csrf_exempt
def pitr(request):
    if request.method == 'POST':
        bucket = request.POST['bucket']
        prefix = request.POST['prefix']
        time = request.POST['time']
        dest = request.POST['dest']
        try :
            do_restore(bucket, prefix, time, dest)
            print("done")
            return HttpResponse("done")
        except:
            return HttpResponse("error")

def do_restore(bucket, prefix, time, dest):
    cmd2 = "s3-pit-restore -b demogo-datasync-jimini -d recovery-dst -p 0 -t "
    cmd2 += '"' + "06-11-2020 15:00:00 +0900" + '"'
    cmd = "s3-pit-restore " + "-b " + bucket + " -B " + dest + " -p " + prefix + " -t "
    cmd += '"' + time + '"'
    print(cmd2)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()
    return process.returncode
