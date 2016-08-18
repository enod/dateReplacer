# -*- coding: utf-8 -*-
import re
import dateparser


def repl(matchobj):
    """
    Analyzes incoming strings and replace matching date field to ISO-8601 format
    according to https://en.wikipedia.org/wiki/Date_format_by_country#cite_note-113
    :rtype: unicode
    :param matchobj: regex group object. To see value -> .group(1)
    :return: unicode string

    """
    jp_trad =  re.search(ur'(\S*)平成(\d{1,2})年(\d+)月(\d{1,2})日(\S*)', matchobj.group(1))  # 平成28年10月10日
    if jp_trad:
        return u'[ENTRYh]:' + unicode(unicode(int(jp_trad.group(2)) + 1988) + '-' + jp_trad.group(3) + '-' + jp_trad.group(4)) + jp_trad.group(5)
    trad_taiwan = re.search(ur'(\S*)民國(\d+)年(\d+)月(\d+)日(\S*)', matchobj.group(1))  # 民國105年10月10日
    if trad_taiwan:
        return u'[ENTRYa]:' + trad_taiwan.group(1) + unicode(
            unicode(int(trad_taiwan.group(2)) + 1911) + '-' + trad_taiwan.group(3) + '-' + trad_taiwan.group(
                4)) + trad_taiwan.group(5)
    simple_dash = re.search(u'[0-9]{1,4}-[0-9]{2}-[0-9]{2}', matchobj.group(1))  # 2016-10-10
    if simple_dash:
        return u'[ENTRYb]:' + unicode(dateparser.parse(simple_dash.group(0)))
    # ch_YMD = re.search(ur'(\S*)(\d+)年(\d+)月(\d+)日(\S*)', matchobj.group(1))  # 2016年7月14日
    ch_YM = re.search(u'(\S*)(\d+)年(\d+)月(\S*)', matchobj.group(1))  # 2016年10月
    if ch_YM:
        return u'[ENTRYd]:' + ch_YM.group(1) + unicode(
            dateparser.parse(unicode(ch_YM.group(2)) + '-' + unicode(ch_YM.group(3)))) + ch_YM.group(1)
    return matchobj.group(1)


def mapping_replace(text):
    """

    :rtype: unicode
    :type: unicode
    :param text: string from client requested page
    :return: string
    """

    line = re.sub(r'(\S+)', repl, text, flags=re.MULTILINE)
    return line
