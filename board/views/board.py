from ..responses import *
from ..utils import send_json
from ..models import Board
from ..decorators import login_required
from django.views import View
from django.core.serializers import serialize
import json


class BoardView(View):
    def get(self, request):

        data = getSucceedFunc('board')
        # 특정 게시판 파라미터 추가
        # {{baseUrl}}/board/<board_name>
        # get에서 name 키에 대한 value 값을 받아 -> pk 보단 name이 보편적
        # 특정 게시판의 이름을 파라미터로 저장 -> Board.objects.get로 데이터 read 할때 특정 게시판 정보만 출력.

        # boards = json.loads(
        #     serialize("json", Board.objects.all()))
        try:
            board_num = 10
            if "num" in request.GET:
                board_num = int(request.GET["num"])
            boards = json.loads(
                serialize(
                    "json",
                    Board.objects
                    .filter(pk=request.GET["pk"])
                    .order_by('-id')[:board_num]
                )
            )
            data['data'] = boards
            return send_json(data)
        except:
            boards = json.loads(serialize("json", Board.objects.all()))
            data['data'] = boards
            return send_json(data)

    @login_required
    def post(self, request):
        if 'name' not in request.POST:
            return send_json(illegalArgument)
        if Board.objects.filter(name=request.POST['name']):
            return send_json(postingElementExists)
        Board.objects.create(name=request.POST['name'])
        return send_json(postSucceed)
