import datetime

from django.db import models
from django.utils.functional import cached_property

from vip.models import Vip


class User(models.Model):
    """
    phonenum	手机号
    nickname	昵称
    sex	性别
    birth_year	出生年
    birth_month	出生月
    birth_day	出生日
    avatar	个人形象
    location	常居地
    """

    LOCATIONS = (
        ('bj', '北京'),
        ('sz', '深圳'),
        ('sh', '上海'),
        ('gz', '广州'),
        ('cd', '成都'),
        ('dl', '大连'),
    )

    SEXS = (
        (0, '全部'),
        (1, '男'),
        (2, '女')
    )

    phonenum = models.CharField(max_length=11, unique=True)
    nickname = models.CharField(max_length=32)
    sex = models.IntegerField(default=0, choices=SEXS)
    birth_year = models.IntegerField(default=2000)
    birth_month = models.IntegerField(default=1)
    birth_day = models.IntegerField(default=1)
    avatar = models.CharField(max_length=256)
    location = models.CharField(max_length=64, choices=LOCATIONS)

    vip_id = models.IntegerField(default=1)

    # @property
    @cached_property
    def age(self):
        today = datetime.date.today()
        birthday = datetime.date(self.birth_year, self.birth_month, self.birth_day)

        return (today - birthday).days // 365

    @property
    def profile(self):
        """
        user.profile.location
        :return:
        """
        if not hasattr(self, '_profile'):
            self._profile, _ = Profile.get_or_create(id=self.id)

            # try:
            #     self._profile = Profile.get(id=self.id)
            # except Profile.DoesNotExist:
            #     self._profile = Profile.objects.create(id=self.id)

        return self._profile

    @property
    def vip(self):
        """
        用户 vip 信息
        :return:
        """
        if not hasattr(self, '_vip'):
            self._vip = Vip.get(id=self.vip_id)

        return self._vip

    def to_dict(self):
        return {
            'id': self.id,
            'phonenum': self.phonenum,
            'nickname': self.nickname,
            'sex': self.sex,
            'avatar': self.avatar,
            'location': self.location,
            'age': self.age
        }

    class Meta:
        db_table = 'users'


class Profile(models.Model):
    """
    | location       | 目标城市                 |
    | min_distance   | 最小查找范围             |
    | max_distance   | 最大查找范围             |
    | min_dating_age | 最小交友年龄             |
    | max_dating_age | 最大交友年龄             |
    | dating_sex     | 匹配的性别               |
    | vibration      | 开启震动                 |
    | only_matche    | 不让为匹配的人看我的相册 |
    | auto_play      | 自动播放视频             |

    user.profile.location

    """

    LOCATIONS = (
        ('bj', '北京'),
        ('sz', '深圳'),
        ('sh', '上海'),
        ('gz', '广州'),
        ('cd', '成都'),
        ('dl', '大连'),
    )

    SEXS = (
        (0, '全部'),
        (1, '男'),
        (2, '女')
    )

    location = models.CharField(max_length=64, choices=LOCATIONS)

    min_distance = models.IntegerField(default=1)
    max_distance = models.IntegerField(default=10)

    min_dating_age = models.IntegerField(default=18)
    max_dating_age = models.IntegerField(default=81)

    dating_sex = models.IntegerField(default=0, choices=SEXS)

    vibration = models.BooleanField(default=True)
    only_matche = models.BooleanField(default=True)
    auto_play = models.BooleanField(default=True)

    class Meta:
        db_table = 'profiles'
