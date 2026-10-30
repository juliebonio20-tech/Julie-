import re
from datetime import datetime

import mysql.connector

# ===== DILI PWEDI PALITAN ANG PANGALAN SA "vis_db.py" =====
# Kung i-rename nimo ang vis_db.py, kinahanglan palitan usab nimo ni nga import ug ang file name
import vis_db


def req(msg):
    while True:
        v = input(msg).strip()
        if v == "":
            print("  * Hindi puwede blangko.")
            continue
        return v


def nowtime(label):
    print(f"  [{label}] ENTER kung ngayon na, o ilagay ang HH:MM")
    a = input("    >> ").strip()
    if a == "":
        return datetime.now().strftime("%H:%M")
    if re.match(r"^([01]\d|2[0-3]):([0-5]\d)$", a):
        return a
    print("  * Mali ang format.")
    return nowtime(label)


def card(r):
    print("\n" + "="*40)
    print(f"  VISITOR #: {r['visitor_no']}")
    print("="*40)
    print(f"  Buong Pangalan  : {r['full_name']}")
    print(f"  Opisina/Kompan... : {r['company_office'] or '-'}")
    print(f"  ID na Ipinasa   : {r['id_type']} #{r['id_no']}")
    print(f"  Layunin         : {r['purpose']}")
    print(f"  Kakausapin      : {r['person_to_visit']}")
    print(f"  Contact #       : {r['contact_no'] or '-'}")
    print(f"  Oras ng Pagpasok: {r['time_in']}")
    print(f"  Oras ng Paglabas: {r['time_out'] or '--- NASA LOOB PA ---'}")
    print(f"  Bantay sa Gate   : {r['guard_on_duty']}")
    print(f"  Kalagayan       : {r['status']}")
    if r['remarks']:
        print(f"  Tala            : {r['remarks']}")
    print("="*40)


def pumasok():
    print("\n--- PAG-REGISTER NG BISITA (SIGN-IN) ---")
    vno = vis_db.next_vno()
    print(f"  Visitor #: {vno}\n")
    name = req("  Buong pangalan: ")
    comp = input("  Opisina/Institusyon (opsyonal): ").strip() or None
    print("  Uri ng ID: [1] School ID [2] Government ID [3] Company ID [4] Iba pa")
    c = input("    Pumili: ").strip()
    if c == "1":
        idt = "School ID"
    elif c == "2":
        idt = "Government ID"
    elif c == "3":
        idt = "Company ID"
    elif c == "4":
        idt = req("    Tukuyin ang uri ng ID: ")
    else:
        idt = "Iba pa"
    idn = req("  Numero ng ID: ")
    purp = req("  Layunin ng pagbisita: ")
    pvisit = req("  Taong kakausapin: ")
    cnum = input("  Contact Number (nimo): ").strip() or None
    tin = nowtime("Oras ng pagpasok")
    guard = req("  Pangalan ng Guard on Duty: ")
    rec = {
        "visitor_no": vno,
        "full_name": name,
        "company_office": comp,
        "id_type": idt,
        "id_no": idn,
        "purpose": purp,
        "person_to_visit": pvisit,
        "contact_no": cnum,
        "time_in": tin,
        "time_out": None,
        "guard_on_duty": guard,
        "remarks": None,
        "status": "Nasa Loob",
    }
    try:
        vis_db.sign_in(rec)
        print("\n  [TAPOS NA] Na-sign-in na ang bisita.")
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")


def tala_bisita():
    try:
        rows = vis_db.list_all()
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not rows:
        print("\n  Wala pang naitalang bisita sa araw na ito.")
        return
    print("\n--- MGA BISITA SA LOGBOOK ---")
    for r in rows:
        tout = r['time_out'] or 'NASA LOOB PA'
        print(f"  [{r['visitor_no']}] {r['full_name']} | Pasok:{r['time_in']} | Labas:{tout} | Kakausapin:{r['person_to_visit']} | {r['status']}")


def hanapin_bisita():
    vno = req("  Visitor #: ").upper()
    try:
        r = vis_db.find_visitor(vno)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not r:
        print("  [WALA] Hindi matagpuan ang bisita.")
        return
    card(r)


def lumabas():
    vno = req("  Visitor # na magpapalabas: ").upper()
    try:
        r = vis_db.find_visitor(vno)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not r:
        print("  [WALA] Hindi matagpuan.")
        return
    if r['status'] == 'Umalis na':
        print("  [PAALALA] Umalis na ang bisita.")
        card(r)
        return
    card(r)
    tout = nowtime("Oras ng paglabas")
    try:
        ok = vis_db.sign_out(vno, tout)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if ok:
        print("  [TAPOS NA] Na-sign-out na ang bisita.")
    else:
        print("  [MALI] Hindi nagtagumpay ang pag-sign-out.")


def tanggalin():
    vno = req("  Visitor # na tatanggalin: ").upper()
    try:
        r = vis_db.find_visitor(vno)
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
        return
    if not r:
        print("  [WALA] Hindi matagpuan.")
        return
    card(r)
    konf = input("  Sigurado ka bang tanggalin ito? (oo/hindi): ").strip().lower()
    if konf not in ("oo", "o", "yes", "y"):
        print("  Kinansela.")
        return
    try:
        vis_db.delete_visitor(vno)
        print("  [TINANGGAL] Natanggal na ang rekord sa logbook.")
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")


def tanggalin_lahat():
    print("\n--- PAGTANGGAL NG LAHAT NG REKORD ---")
    konf = input("  Sigurado ka bang tanggalin LAHAT ng rekord? (oo/hindi): ").strip().lower()
    if konf not in ("oo", "o", "yes", "y"):
        print("  Kinansela.")
        return
    try:
        count = vis_db.clear_log()
        print(f"  [TINANGGAL] Natanggal ang {count} rekord sa logbook.")
    except mysql.connector.Error as e:
        print(f"  [MALI] {e}")
