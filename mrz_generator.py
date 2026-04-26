#!/usr/bin/env python3
"""
MRZ (Machine Readable Zone) generator for TD3 (passport) format per ICAO 9303.
Two lines of 44 characters each.
"""

MRZ_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
WEIGHTS = [7, 3, 1]


def char_value(c):
    if c == '<':
        return 0
    if c.isdigit():
        return int(c)
    return ord(c) - ord('A') + 10


def check_digit(s):
    total = sum(char_value(c) * WEIGHTS[i % 3] for i, c in enumerate(s))
    return total % 10


def pad(s, length, fill='<'):
    s = s.upper().replace(' ', '<')
    return s[:length].ljust(length, fill)


def make_mrz(
    surname, given_names, passport_no, nationality,
    dob, sex, expiry, issuing_country, personal_no
):
    # --- Line 1 ---
    doc_type = "P<"
    country = pad(issuing_country, 3)
    name_field = pad(f"{surname}<<{given_names}", 39)
    line1 = doc_type + country + name_field

    # --- Line 2 ---
    pno = pad(passport_no, 9)
    pno_cd = str(check_digit(pno))

    nat = pad(nationality, 3)

    dob_fmt = pad(dob, 6)          # YYMMDD
    dob_cd = str(check_digit(dob_fmt))

    sex_char = sex.upper()

    exp_fmt = pad(expiry, 6)       # YYMMDD
    exp_cd = str(check_digit(exp_fmt))

    opt = pad(personal_no, 14)
    opt_cd = str(check_digit(opt))

    # Overall check digit covers: pno+pno_cd, dob+dob_cd, exp+exp_cd+opt+opt_cd
    composite = pno + pno_cd + dob_fmt + dob_cd + exp_fmt + exp_cd + opt + opt_cd
    overall_cd = str(check_digit(composite))

    line2 = pno + pno_cd + nat + dob_fmt + dob_cd + sex_char + exp_fmt + exp_cd + opt + opt_cd + overall_cd

    assert len(line1) == 44, f"Line 1 length {len(line1)} != 44"
    assert len(line2) == 44, f"Line 2 length {len(line2)} != 44"

    return line1, line2


if __name__ == "__main__":
    line1, line2 = make_mrz(
        surname="TEST",
        given_names="MARK",
        passport_no="KE1234567",
        nationality="EST",
        dob="950516",        # 16.05.1995 → YYMMDD
        sex="M",
        expiry="280613",     # 13.06.2028 → YYMMDD
        issuing_country="EST",
        personal_no="39505165587",
    )

    print("MRZ (ICAO 9303 TD3 — Estonian passport):")
    print(f"Line 1: {line1}")
    print(f"Line 2: {line2}")
    print()
    print("Breakdown:")
    print(f"  Doc type + country : {line1[:5]}")
    print(f"  Name field         : {line1[5:]}")
    print(f"  Passport No + CD   : {line2[:10]}")
    print(f"  Nationality        : {line2[10:13]}")
    print(f"  DOB + CD           : {line2[13:20]}")
    print(f"  Sex                : {line2[20]}")
    print(f"  Expiry + CD        : {line2[21:28]}")
    print(f"  Personal No + CD   : {line2[28:43]}")
    print(f"  Overall CD         : {line2[43]}")
