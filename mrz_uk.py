#!/usr/bin/env python3
"""
MRZ generator for UK passport (TD3, ICAO 9303).
Two lines of 44 characters each.
Issuing country / nationality: GBR
"""

WEIGHTS = [7, 3, 1]


def char_value(c):
    if c == '<':
        return 0
    if c.isdigit():
        return int(c)
    return ord(c) - ord('A') + 10


def check_digit(s):
    return sum(char_value(c) * WEIGHTS[i % 3] for i, c in enumerate(s)) % 10


def pad(s, length, fill='<'):
    s = s.upper().replace(' ', '<')
    return s[:length].ljust(length, fill)


def make_mrz_uk(surname, given_names, passport_no, nationality,
                dob, sex, expiry, personal_no):
    line1 = "P<GBR" + pad(f"{surname}<<{given_names}", 39)

    pno    = pad(passport_no, 9)
    pno_cd = str(check_digit(pno))
    nat    = pad(nationality, 3)
    dob_f  = pad(dob, 6)
    dob_cd = str(check_digit(dob_f))
    exp_f  = pad(expiry, 6)
    exp_cd = str(check_digit(exp_f))
    opt    = pad(personal_no, 14)
    opt_cd = str(check_digit(opt))
    overall_cd = str(check_digit(pno + pno_cd + dob_f + dob_cd + exp_f + exp_cd + opt + opt_cd))

    line2 = pno + pno_cd + nat + dob_f + dob_cd + sex.upper() + exp_f + exp_cd + opt + opt_cd + overall_cd

    assert len(line1) == 44
    assert len(line2) == 44
    return line1, line2


if __name__ == "__main__":
    # Example — replace with real data
    line1, line2 = make_mrz_uk(
        surname="SMITH",
        given_names="JOHN",
        passport_no="123456789",
        nationality="GBR",
        dob="900101",
        sex="M",
        expiry="300101",
        personal_no="",
    )
    print(line1)
    print(line2)
