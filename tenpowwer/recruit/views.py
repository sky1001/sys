from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from recruit.models import City, Enterprise, Recruit
from recruit.serializer import CitySerializer, EnterpriseSerializer, EnterpriseSerializerSimple, RecruitSerializer, \
    RecruitSerializerSimple


class CityViewSet(ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()

    # 获取热门城市列表
    @action(methods=["GET"], detail=False, url_path="hotlist")
    def hot_list(self, request):
        cities = self.get_queryset().filter(ishot=1)
        serializer = self.get_serializer(instance=cities, many=True)
        return Response(serializer.data)

class EnterpriseViewSet(ModelViewSet):
    queryset = Enterprise.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return EnterpriseSerializer
        else:
            return EnterpriseSerializerSimple

    # 按访问量获取最热的企业   4个最火的企业
    @action(methods=["GET"], detail=False, url_path="search/hotlist")
    def get_hot_enterprise(self, request):
        hot_enterprises = self.get_queryset().order_by("-visits")[0:4]
        serializer = self.get_serializer(instance=hot_enterprises, many=True)
        return Response(serializer.data)

class RecruitViewSet(ModelViewSet):
    queryset = Recruit.objects.filter(state="1").order_by("-createtime")

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RecruitSerializer
        else:
            return RecruitSerializerSimple

    # 招聘首页获取最新的4个职位
    @action(methods=["GET"], detail=False, url_path="search/latest")
    def get_latest_job(self, request):
        jobs = self.get_queryset()[0:4]
        serializer = self.get_serializer(instance=jobs, many=True)
        return Response(serializer.data)

    # 招聘首页获取推荐的4个职位
    # 简单实现,和最新职位一致,后续再调整
    @action(methods=["GET"], detail=False, url_path="search/recommend")
    def get_recommend_job(self, request):
        jobs = self.get_queryset()[0:4]
        serializer = self.get_serializer(instance=jobs, many=True)
        return Response(serializer.data)


