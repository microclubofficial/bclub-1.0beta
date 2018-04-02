from forums.permission import (RestfulView, is_confirmed)


class ReplyList(RestfulView):
    @is_confirmed
    def post(self, id):
        return True

reply_list_permission = ReplyList()