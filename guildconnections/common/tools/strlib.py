# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-4-24
#

"""
strlib.py
"""

def after(s, pat):
    # returns the substring after pat in s.
    # if pat is not in s, then return a null string!
    pos = s.find(pat)
    if pos != -1:
        return s[pos + len(pat):]
    return ""


def rafter(s, pat):
    # returns the substring after pat in s.
    # if pat is not in s, then return a null string!
    pos = s.rfind(pat)
    if pos != -1:
        return s[pos + len(pat):]
    return ""


def before(s, pat):
    # returns the substring before pat in s.
    # if pat is not in s, then return a null string!
    pos = s.find(pat)
    if pos != -1:
        return s[:pos]
    return ""


def rbefore(s, pat):
    # returns the substring before pat in s.
    # if pat is not in s, then return a null string!
    pos = s.rfind(pat)
    if pos != -1:
        return s[pos + len(pat):]
    return ""


def between(s, bpat, apat):
    # returns substring between bpat and apat in s.
    # if bpat or apat is not in s, then return a null string.
    start = s.find(bpat)
    if start != -1:
        end = s[start + len(bpat):].find(apat)
        if end != -1:
            return s[start + len(bpat):start + len(bpat) + end]
        return ""
    return ""

def rbetween(s, bpat, apat):
    # returns substring between bpat and apat in s.
    # if bpat or apat is not in s, then return a null string.
    end = s.rfind(apat)
    if end != -1:
        before = s[:end].rfind(bpat)
        if before != -1:
            return s[before + len(bpat):end]
        return ""
    return ""


if __name__ == "__main__":
    s = '<a href="the quick brown fox">test1</a><a href="jumps over">test2</a>'
    print 'input string:\n', s
    print 'before(x, "<a")=', before(s, "<a")
    print 'rbefore(x, "<a")=', rbefore(s, "<a")
    print 'after(x, "<a")=', after(s, "<a")
    print 'rafter(x, "<a")=', rafter(s, "<a")

    print 'before(s, "</a>")=', before(s, "</a>")
    print 'after (s, "\">\")=', after(s, '">')
    print """rafter (s,  '">\')=""", rafter(s, '">')
    print 'between( s, ">","</a>")=', between(s, ">", "</a>")
    print 'rbetween(s, ">","</a>")=', rbetween(s, ">", "</a>")
