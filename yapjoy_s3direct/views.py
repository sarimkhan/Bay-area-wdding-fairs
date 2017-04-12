import json

from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from datetime import datetime
from .utils import create_upload_data, get_at
from django.views.decorators.csrf import csrf_exempt

DESTINATIONS = getattr(settings, 'S3DIRECT_DESTINATIONS', None)


@require_POST
@csrf_exempt
def get_upload_params(request):
    print 'here'
    print DESTINATIONS
    content_type = request.POST['type']
    filename = "%s_%s"%(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),request.POST['name'])
    print filename

    dest = DESTINATIONS.get(request.POST['dest'])
    print "Destination: ",dest
    if not dest:
        data = json.dumps({'error': 'File destination does not exist.'})
        return HttpResponse(data, content_type="application/json", status=400)

    key = get_at(0, dest)
    auth = get_at(1, dest)
    allowed = get_at(2, dest)
    acl = get_at(3, dest)
    bucket = get_at(4, dest)
    cache_control = get_at(5, dest)
    content_disposition = get_at(6, dest)

    if not acl:
        acl = 'public-read'

    if not key:
        data = json.dumps({'error': 'Missing destination path.'})
        return HttpResponse(data, content_type="application/json", status=403)

    if auth and not auth(request.user):
        data = json.dumps({'error': 'Permission denied.'})
        return HttpResponse(data, content_type="application/json", status=403)

    if (allowed and content_type not in allowed) and allowed != '*':
        data = json.dumps({'error': 'Invalid file type (%s).' % content_type})
        return HttpResponse(data, content_type="application/json", status=400)

    if hasattr(key, '__call__'):
        key = key(filename)
    else:
        key = '%s/%s' % (key,filename)
    print key
    print filename

    data = create_upload_data(content_type, key, acl, bucket, cache_control, content_disposition)
    print json.dumps(data)
    return HttpResponse(json.dumps(data), content_type="application/json")