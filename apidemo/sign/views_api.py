import time
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import JsonResponse

from sign.models import Event, Guest


#添加发布会接口
def add_event(request):
    if request.method == 'POST':
        eid = request.POST.get('eid', '')  # 发布会id
        name = request.POST.get('name', '')  # 发布会标题
        limit = request.POST.get('limit', '')  # 限制人数
        status = request.POST.get('status', 1)  # 状态
        address = request.POST.get('address', '')  # 地址
        start_time = request.POST.get('start_time', '')  # 发布会时间

        if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
            return JsonResponse({"status": 10021, "message": "参数为空"})

        result = Event.objects.filter(id=eid)
        if result:
            return JsonResponse({"status": 10022, "message": "发布会id已存在"})

        result = Event.objects.filter(name=name)
        if result:
            return JsonResponse({"status": 10023, "message": "发布会名称已存在"})

        try:
            Event.objects.create(id=eid, name=name, limit=limit, status=status, address=address, start_time=start_time)
        except ValidationError:
            error = '日期格式错误'
            return JsonResponse({"status": 10024, 'message': error})

        return JsonResponse({"status":200, "message": "添加发布会成功"})

    else:
        return JsonResponse({"status": 10031, "message": "请求方法错误"})


#发布会查询
def get_event_list(request):
    eid = request.GET.get("eid", "")  # 发布会id
    name = request.GET.get("name", "")  # 发布会名称

    if eid == '' and name == '':
        return JsonResponse({'status': 10021, 'message': '参数不能为空'})

    if eid != '':
        try:
            int(eid)
        except ValueError:
            return JsonResponse({'status': 10025, 'message': 'eid类型错误'})
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 10022, 'message': '查询结果为空'})
        else:
            event['eid'] = result.id
            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse({'status': 200, 'message': 'success', 'data': event})

    if name != '':
        datas = []
        results = Event.objects.filter(name__contains=name)
        if results:
            for r in results:
                event = {}
                event['eid'] = r.id
                event['name'] = r.name
                event['limit'] = r.limit
                event['status'] = r.status
                event['address'] = r.address
                event['start_time'] = r.start_time
                datas.append(event)
            return JsonResponse({'status': 200, 'message': 'success', 'data': datas})
        else:
            return JsonResponse({'status': 10022, 'message': '查询结果为空'})

#用户签到接口
def user_sign(request):
    eid = request.POST.get('eid', '')  # 发布会id
    phone = request.POST.get('phone', '')  # 嘉宾手机号

    if eid == '' or phone == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    try:
        result = Event.objects.get(id=eid)
    except Event.DoesNotExist:
        return JsonResponse({'status': 10022, 'message': 'event id null'})

    if result.status is False:
        return JsonResponse({'status': 10023, 'message': 'event status is not available'})

    event_time = result.start_time  # 发布会时间
    timeArray = time.strptime(str(event_time), "%Y-%m-%d %H:%M:%S")
    e_time = int(time.mktime(timeArray))

    n_time = int(str(time.time()).split(".")[0])  # 当前时间

    if n_time >= e_time:
        return JsonResponse({'status': 10024, 'message': 'event has started'})

    result = Guest.objects.filter(phone=phone)
    if not result:
        return JsonResponse({'status': 10025, 'message': 'user phone null'})
    else:
        for res in result:
            if res.event_id == int(eid):
                break
        else:
            return JsonResponse({'status': 10026, 'message': 'user did not participate in the conference'})

    result = Guest.objects.get(event_id=eid, phone=phone)
    print(result.sign)
    if result.sign is True:
        return JsonResponse({'status': 10027, 'message': 'user has sign in'})
    else:
        result.sign = True
        result.save()
        return JsonResponse({'status': 200, 'message': 'sign success'})
