# -*- coding: utf-8 -*-
import re
import dateparser
import datetime

now = datetime.datetime.now()
now_year = unicode("%s" % (now.year))
now_month = unicode("%s" % (now.month))

special_dates = {
    "Christmas Eve":"[ADVAN]12-24 ",
    "Taiwanese Festival": "[ADVAN]10-10 ",

}


def repl(matchobj):
    """
    Analyzes incoming strings and replace matching date field to ISO-8601 format
    according to https://en.wikipedia.org/wiki/Date_format_by_country#cite_note-113
    and http://www.iso.org/iso/home/standards/iso8601.htm
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

    ch_YMD = re.search(ur'(\S*)(\d+)年(\d+)月(\d+)日(\S*)', matchobj.group(1))  # 2016年7月14日
    if ch_YMD:
        return u'[ENTRY_YMD]:' + ch_YMD.group(1) + unicode(
            unicode(ch_YMD.group(2)) + '-' + unicode(ch_YMD.group(3))) + '-' + unicode(ch_YMD.group(4)) + ch_YMD.group(5)

    ch_YM = re.search(u'(\S*)(\d+)年(\d+)月(\S*)', matchobj.group(1))  # 2016年10月
    if ch_YM:
        return u'[ENTRYd]:' + ch_YM.group(1) + unicode(
            unicode(ch_YM.group(2)) + '-' + unicode(ch_YM.group(3))) + ch_YM.group(4)

    ch_MD = re.search(u'(\S*)(\d{1,2})月(\d{1,2})日(\S*)', matchobj.group(1))  # 10月10日
    if ch_MD:
        return u'[ENTRYe]:{0}{1}-{2}{3}'.format(ch_MD.group(1), unicode(ch_MD.group(2)), unicode(ch_MD.group(3)),
                                                 ch_MD.group(4))

    ch_this_M = re.search(u'(\S*)同年(\d{1,2})月(\S*)', matchobj.group(1))  # 同年10月
    if ch_this_M:
        return u'[ENTRYf]:{0}{1}-{2}{3}'.format(ch_this_M.group(1), unicode(now_year), ch_this_M.group(2), ch_this_M.group(3))

    ch_this_D = re.search(u'(\S*)本月(\d{1,2})日(\S*)', matchobj.group(1))  # 本月10日
    if ch_this_D:
        return u'[ENTRYg]:{0}{1}-{2}{3}'.format(ch_this_D.group(1), unicode(now_month), ch_this_D.group(2),
                                            ch_this_D.group(3))

    return matchobj.group(1)


def mapping_replace(text):
    """

    :rtype: unicode
    :type: unicode
    :param text: string from client requested page
    :return: string
    """
    robj = re.compile('|'.join(special_dates.keys()))
    result = robj.sub(lambda m: special_dates[m.group(0)], text)


    # testing = re.findall(ur'(Jan|Feb|Mar|Apr|May|June|July|Aug|Sept|Oct|Nov|Dec)', text, flags=re.MULTILINE)
    # if testing: print testing

    line = re.sub(r'(\S+)', repl, result, flags=re.MULTILINE)
    return line
