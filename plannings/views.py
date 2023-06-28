from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from plannings.models import Planning
from plannings.serializers import PlanningSerializer


@csrf_exempt
def planning_info(request, pk):
    try:
        print(f"planning_info.Planning id={pk}")
        plan = Planning.objects.get(pk=pk)
    except Planning.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PlanningSerializer(plan)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PlanningSerializer(plan, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        plan.delete()
        return HttpResponse(status=204)


@csrf_exempt
def planning_list(request):
    print("planning_list:Request => {}".format(request))
    if request.method == 'GET':
        plans = Planning.objects.all()
        serializer = PlanningSerializer(plans, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        print("planning_list:POST.data => {}".format(data))
        serializer = PlanningSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        print("Invalid data sent to Serializer errors: {}".format(serializer.errors))
        return JsonResponse(serializer.errors, status=400)