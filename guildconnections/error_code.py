# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2013 Woo-cupid(iampurse#vip.qq.com)
#
#===============================================================================
#
#          | "400"  ; Section 10.4.1: Bad Request
#          | "401"  ; Section 10.4.2: Unauthorized
#          | "402"  ; Section 10.4.3: Payment Required
#          | "403"  ; Section 10.4.4: Forbidden
#          | "404"  ; Section 10.4.5: Not Found
#          | "405"  ; Section 10.4.6: Method Not Allowed
#          | "406"  ; Section 10.4.7: Not Acceptable
#          | "407"  ; Section 10.4.8: Proxy Authentication Required
#          | "408"  ; Section 10.4.9: Request Time-out
#          | "409"  ; Section 10.4.10: Conflict
#          | "410"  ; Section 10.4.11: Gone
#          | "411"  ; Section 10.4.12: Length Required
#          | "412"  ; Section 10.4.13: Precondition Failed
#          | "413"  ; Section 10.4.14: Request Entity Too Large
#          | "414"  ; Section 10.4.15: Request-URI Too Large
#          | "415"  ; Section 10.4.16: Unsupported Media Type
#          | "416"  ; Section 10.4.17: Requested range not satisfiable
#          | "417"  ; Section 10.4.18: Expectation Failed
#          | "500"  ; Section 10.5.1: Internal Server Error
#          | "501"  ; Section 10.5.2: Not Implemented
#          | "502"  ; Section 10.5.3: Bad Gateway
#          | "503"  ; Section 10.5.4: Service Unavailable
#          | "504"  ; Section 10.5.5: Gateway Time-out
#          | "505"  ; Section 10.5.6: HTTP Version not supported
#          | extension-code
#===============================================================================

EMAIL_DUPLICATE = (409, 'email {} exists.')
ENP_REQUIRED = (406, 'email,name,passwd is required.')
LOGIN_FAILED = (406, 'Wrong email or wrong passwd.')
