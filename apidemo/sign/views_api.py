from django.core.exceptions import ValidationError
from django.http import JsonResponse

from sign.models import Event

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

