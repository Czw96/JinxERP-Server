from django.db.models import TextChoices


class TextChoicesEx(TextChoices):

    @classmethod
    def get_value(cls, label):
        for choice in cls:
            if choice.label == label:
                return choice.value
        return None

    @classmethod
    def get_label_list(cls):
        return (item[1] for item in cls.choices)


class ClientLevel(TextChoicesEx):
    """客户等级"""

    LEVEL0 = ('lv0', '普通客户')
    LEVEL1 = ('lv1', '一级客户')
    LEVEL2 = ('lv2', '二级客户')
    LEVEL3 = ('lv3', '三级客户')


__all__ = [
    'ClientLevel',
]
