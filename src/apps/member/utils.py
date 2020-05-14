from commite.models import BaseCommiteMember
from member.models import BaseMember
from core.exceptions import PerdanaError


def get_commitemember_from_basecommitemember(bcm: BaseCommiteMember):
    if hasattr(bcm, 'regionalcommitemember') and bcm.regionalcommitemember:
        return bcm.regionalcommitemember
    elif hasattr(bcm, 'pengprovcommitemember') and bcm.pengprovcommitemember:
        return bcm.pengprovcommitemember
    elif hasattr(bcm, 'pengcabcommitemember') and bcm.pengcabcommitemember:
        return bcm.pengcabcommitemember
    elif hasattr(bcm, 'clubunitcommitemember') and bcm.clubunitcommitemember:
        return bcm.clubunitcommitemember
    else:
        raise PerdanaError(message="object given is not valid instance of BaseCommiteMember")


def get_member_from_basemember(basemember: BaseMember):
    if hasattr(basemember, 'archermember') and basemember.archermember:
        return basemember.archermember
    elif hasattr(basemember, 'basecommitemember') and basemember.basecommitemember:
        return get_commitemember_from_basecommitemember(basemember.basecommitemember)
    else:
        raise PerdanaError(message="object given is not valid instance of BaseMember")
