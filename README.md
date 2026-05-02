# MRZ Generator — ICAO 9303 TD3 (Estonian Passport)

## Agents

- [Kling anti-parasite remedy ad agent](agents/kling/anti-parasite-remedy-ad-agent.md) — Russian-language prompt agent for creating an ethical Kling video ad concept, storyboard, final prompt, negative prompt, and A/B ad copy for an anti-parasite support product.

## What is MRZ?

MRZ (Machine Readable Zone) is the two-line block at the bottom of a passport photo page, standardised by ICAO Doc 9303. Each line is **44 characters** for a TD3 (passport) document.

---

## Input Data

| Field            | Value        |
|------------------|--------------|
| Surname          | TEST         |
| Given names      | MARK         |
| Passport number  | KE1234567    |
| Date of birth    | 16.05.1995   |
| Sex              | M            |
| Expiry date      | 13.06.2028   |
| Nationality      | EST          |
| Issuing country  | EST          |
| Personal code    | 39505165587  |

---

## Generated MRZ

```
P<ESTTEST<<MARK<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
KE12345670EST9505162M280613639505165587<<<88
```

### Field breakdown

**Line 1**

| Chars | Value                                     | Meaning                    |
|-------|-------------------------------------------|----------------------------|
| 1–2   | `P<`                                      | Document type (passport)   |
| 3–5   | `EST`                                     | Issuing country            |
| 6–44  | `TEST<<MARK<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<`| Surname `<<` Given names   |

**Line 2**

| Chars | Value         | Meaning                    |
|-------|---------------|----------------------------|
| 1–9   | `KE1234567`   | Passport number            |
| 10    | `0`           | Check digit (passport no)  |
| 11–13 | `EST`         | Nationality                |
| 14–19 | `950516`      | Date of birth (YYMMDD)     |
| 20    | `2`           | Check digit (DOB)          |
| 21    | `M`           | Sex                        |
| 22–27 | `280613`      | Expiry date (YYMMDD)       |
| 28    | `6`           | Check digit (expiry)       |
| 29–42 | `39505165587<<<` | Personal code + filler  |
| 43    | `8`           | Check digit (personal no)  |
| 44    | `8`           | Overall composite check digit |

---

## Check Digit Algorithm (ICAO 9303 §4.9)

Character values: `0–9` → 0–9, `A–Z` → 10–35, `<` → 0.  
Weights cycle: `7, 3, 1, 7, 3, 1, …`  
Check digit = (weighted sum) mod 10.

---

## Usage

```bash
python3 mrz_generator.py
```
