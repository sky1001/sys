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

    # 公司信息访问量
    @action(methods=['put'], detail=True)
    def visit(self, request, pk):
        enterprise = self.get_object()
        enterprise.visits += 1
        enterprise.save()
        return Response({'success': True, 'message': '更新成功'})

    # 收藏企业
    @action(methods=['post'], detail=True)
    def collect(self, request, pk):
        try:
            user = request.user
        except Exception:
            user = None
        if user is not None and user.is_authenticated:
            enterprise = self.get_object()
            enterprise.users.add(user)
            enterprise.save()
            return Response({'success': True, 'message': '收藏成功'})
        else:
            return Response({'success': False, 'message': '未登录'}, status=400)
            # 收藏企业 enterprise/{pk}/collect/

    # 取消收藏企业
    @action(methods=['post'], detail=True)
    def cancelcollect(self, request, pk):
        try:
            user = request.user
        except Exception:
            user = None
        if user is not None and user.is_authenticated:
            enterprise = self.get_object()
            enterprise.users.remove(user)
            enterprise.save()
            return Response({'success': True, 'message': '取消收藏成功'})
        else:
            return Response({'success': False, 'message': '未登录'}, status=400)


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

    # 根据城市名称和关键字搜索职位
    @action(methods=["POST"], detail=False, url_path="search/city/keyword")
    def search_job(self, request):
        cityname = request.data.get('cityname')
        keyword = request.data.get('keyword')
        jobs = self.get_queryset()
        ret_jobs = []
        # 没选城市  也没给关键词  查所有职位
        if (not cityname or cityname=='全部')and not keyword:
            ret_jobs = jobs
        # 有城市  没有关键词  查该城市的所有职位
        elif cityname and not keyword:
            for job in jobs:
                if job.city == cityname:
                    ret_jobs.append(job)
        #  没城市  但有关键词  查包含关键词的所有职位
        elif (not cityname or cityname=='全部') and keyword:
            for job in jobs:
                if job.jobname.lower().find(keyword.lower()) != -1:
                    ret_jobs.append(job)
        # 既有城市 又有关键词  查询指定职位
        else:
            for job in jobs:
                if job.city == cityname and job.jobname.lower().find(keyword.lower()) != -1:
                    ret_jobs.append(job)


        serializer = self.get_serializer(instance=ret_jobs, many=True)
        return Response(serializer.data)

    # 招聘信息访问量
    @action(methods=['put'], detail=True)
    def visit(self, request, pk):
        recruit = self.get_object()
        recruit.visits += 1
        recruit.save()
        return Response({'success': True, 'message': '更新成功'})

    # 收藏招聘信息
    @action(methods=['post'], detail=True)
    def collect(self, request, pk):
        try:
            user = request.user
        except Exception:
            user = None

        if user is not None and user.is_authenticated:
            recruit = self.get_object()
            recruit.users.add(user)
            recruit.save()
            return Response({'success':True,'message':'收藏成功'})
        else:
            return Response({'success':False,'message':'未登录'}, status=400)


    # 取消收藏招聘信息
    @action(methods=['post'], detail=True)
    def cancelcollect(self, request, pk):
        try:
            user = request.user
        except Exception:
            user = None

        if user is not None and user.is_authenticated:
            recruit = self.get_object()
            recruit.users.remove(user)
            recruit.save()
            return Response({'success': True, 'message': '取消收藏成功'})
        else:
            return Response({'success': False, 'message': '未登录'}, status=400)

