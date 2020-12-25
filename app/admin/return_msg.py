class Msg:
    def __init__(self):
        super().__init__()

    def Success(self, date=None, count=None, msg='成功'):
        data = {"code": 0, "msg": msg, 'count': count, 'data': date}
        return data

    def Error(self, date='接口访问失败'):
        data = {
            "code": -1
            , "msg": date
        }
        return data

    def ReNone(self, message):
        if message is None:
            return ''
        else:
            return message

    def ChangMsg(self, msg):
        the_one = int(msg.split('-')[0])
        the_two = int(msg.split('-')[-1])
        if the_one > the_two:
            return msg
        else:
            return str(the_two) + '-' + str(the_one)

    def ReturnNone(self, data):
        if data is None or 0:
            return 0.0
        else:
            return data

    def Count_pro(self, left, right):
        if left == 0.0 and right == 0.0:
            return 0
        else:
            return round((left / (left + right)) * 100, 2)
