from django.shortcuts import render
from rest_framework.views import APIView


# Create your views here.

# /videogallery 경로 인식 후 index함수가 호출 됨 index함순s html을 렌더링 context포함해서

class ChallengeMain(APIView):
    def get(self,request):
        return render(request, "challenge/challenge.html")
    
class ChallengeOne(APIView):
    def get(self,request):
        return render(request,"challenge/ch1.html")
    
class ChallengeCompareResult(APIView):
    def get(self, request):
        return render(request, "challenge/compare_result.html")