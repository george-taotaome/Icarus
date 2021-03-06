import config
from aiohttp import web

from app import app
from lib.utils import get_today_start_timestamp
from model.log_manage import MANAGE_OPERATION, ManageLog
from model.notif import NOTIF_TYPE
from model._post import POST_TYPES, POST_STATE, POST_VISIBLE
from model.log_manage import ManageLog, MANAGE_OPERATION as MOP
from model.user import USER_GROUP
from slim.base.view import BaseView
from slim.retcode import RETCODE
from view import route
from view.user import UserMixin
from view.ws import WSR


@app.timer(10, exit_when=None)
async def user_online():
    for ws in WSR.connections:
        if not ws.closed:
            await ws.send_json(['user.online', len(WSR.count)])


@route('misc')
class TestBaseView(UserMixin, BaseView):
    @classmethod
    def interface(cls):
        cls.use('info', 'GET')

    async def info(self):
        extra = {
            'midnight_time': get_today_start_timestamp()
        }

        # 每日首次访问奖励
        if self.current_user:
            daily_reward = self.current_user.daily_access_reward()
            if daily_reward:
                extra['daily_reward'] = {
                    'exp': daily_reward
                }

        self.finish(RETCODE.SUCCESS, {
            'extra': extra,

            'POST_TYPES': POST_TYPES.to_dict(),
            'POST_TYPES_TXT': POST_TYPES.txt,
            'POST_STATE': POST_STATE.to_dict(),
            'POST_STATE_TXT': POST_STATE.txt,
            'POST_VISIBLE': POST_VISIBLE.to_dict(),
            'POST_VISIBLE_TXT': POST_VISIBLE.txt,

            'MANAGE_OPERATION': MANAGE_OPERATION.to_dict(),
            'MANAGE_OPERATION_TXT': MANAGE_OPERATION.txt,

            'USER_GROUP': USER_GROUP.to_dict(),
            'USER_GROUP_TXT': USER_GROUP.txt,
            'USER_GROUP_TO_ROLE': USER_GROUP.GROUP_TO_ROLE,

            'NOTIF_TYPE': NOTIF_TYPE.to_dict(),

            'BACKEND_CONFIG': {
                'USER_NICKNAME_MIN': config.USER_NICKNAME_MIN,
                'USER_NICKNAME_MAX': config.USER_NICKNAME_MAX,
                'USER_NICKNAME_CN_FOR_REG_MIN': config.USER_NICKNAME_CN_FOR_REG_MIN,
                'USER_NICKNAME_FOR_REG_MIN': config.USER_NICKNAME_FOR_REG_MIN,
                'USER_NICKNAME_FOR_REG_MAX': config.USER_NICKNAME_FOR_REG_MAX,
                'USER_PASSWORD_MIN': config.USER_PASSWORD_MIN,
                'USER_PASSWORD_MAX': config.USER_PASSWORD_MAX,

                'TOPIC_TITLE_LENGTH_MIN': config.TOPIC_TITLE_LENGTH_MIN,
                'TOPIC_TITLE_LENGTH_MAX': config.TOPIC_TITLE_LENGTH_MAX,
                'TOPIC_CONTENT_LENGTH_MAX': config.TOPIC_CONTENT_LENGTH_MAX,

                'UPLOAD_STATIC_HOST': config.UPLOAD_STATIC_HOST,
                'UPLOAD_QINIU_DEADLINE_OFFSET': config.UPLOAD_QINIU_DEADLINE_OFFSET,
            },

            'NICKNAME_MIN': config.USER_NICKNAME_MIN,
            'NICKNAME_MAX': config.USER_NICKNAME_MAX,
            'NICKNAME_CN_FOR_REG_MIN': config.USER_NICKNAME_CN_FOR_REG_MIN,
            'NICKNAME_FOR_REG_MIN': config.USER_NICKNAME_FOR_REG_MIN,
            'NICKNAME_FOR_REG_MAX': config.USER_NICKNAME_FOR_REG_MAX,
            'PASSWORD_MIN': config.USER_PASSWORD_MIN,
            'PASSWORD_MAX': config.USER_PASSWORD_MAX,

            'TOPIC_TITLE_LENGTH_MIN': config.TOPIC_TITLE_LENGTH_MIN,
            'TOPIC_TITLE_LENGTH_MAX': config.TOPIC_TITLE_LENGTH_MAX,
            'TOPIC_CONTENT_LENGTH_MAX': config.TOPIC_CONTENT_LENGTH_MAX,

            'retcode': RETCODE.to_dict(),
            'retinfo_cn': RETCODE.txt_cn,
        })
