from django.http import JsonResponse

from app.admin.return_msg import Msg

class Ce:
    def __init__(self):
        super().__init__()
        self.POST = None

    def Ceshi(self):
        print(self)
        return JsonResponse(Msg().Success(),safe=False)
