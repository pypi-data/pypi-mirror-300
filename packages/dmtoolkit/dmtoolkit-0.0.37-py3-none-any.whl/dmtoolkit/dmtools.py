import dice

from dmtoolkit.apis.dndbeyondapi import DnDBeyondAPI
from dmtoolkit.apis.open5e.open5efeature import Open5eFeature
from dmtoolkit.apis.open5e.open5eitem import Open5eItem
from dmtoolkit.apis.open5e.open5emonster import Open5eMonster
from dmtoolkit.apis.open5e.open5erules import Open5eRules


def get_dndbeyond_character(dnd_id):
    return DnDBeyondAPI.getcharacter(dnd_id)


def get_monster(obj_id):
    return Open5eMonster.get(obj_id)


def get_item(obj_id):
    return Open5eItem.get(obj_id)


def get_rules(obj_id):
    return Open5eRules.get(obj_id)


def get_feature(obj_id):
    return Open5eFeature.get(obj_id)


def search_monster(name):
    return Open5eMonster.search(name)


def search_item(name):
    return Open5eItem.search(name)


def search_rules(name):
    return Open5eRules.search(name)


def search_feature(name):
    return Open5eFeature.search(name)


def dice_roll(roll):
    return dice.roll(roll)
