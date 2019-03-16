# -*- coding: utf-8 -*-
from rest_framework import serializers


class GoodsSerializer(serializers.Serializer):
    # 用两个字段简单的演示, 自己设置 和 goods.model保持一致
    name = serializers.CharField(required=True, max_length=100)
