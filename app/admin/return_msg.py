class Msg:
    def __init__(self):
        super().__init__()

    def Success(self, date=None, count=None):
        data = {"code": 0, "msg": "成功", 'count': count, 'data': date}
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
