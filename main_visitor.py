# ===== DILI PWEDI PALITAN ANG PANGALAN SA UBOS NGA MGA FILE =====
# Kung i-rename nimo ang "vis_db.py", palitan usab ang "vis_db" sa import sa ubos
# Kung i-rename nimo ang "vis_ops.py", palitan usab ang "vis_ops" sa import sa ubos
import vis_db
import vis_ops


def menu():
    print("\n" + "="*42)
    print("   VISITOR LOGBOOK - PAG-REKORD NG MGA BISITA")
    print("="*42)
    print("  [1] I-sign in ang bagong bisita")
    print("  [2] Tingnan ang buong tala ng mga bisita")
    print("  [3] Hanapin ang rekord ng isang bisita")
    print("  [4] I-sign out ang bisita")
    print("  [5] Tanggalin ang isang rekord")
    print("  [6] Tanggalin ang LAHAT ng rekord")
    print("  [0] Lumabas")
    print("="*42)


def main():
    ok, msg = vis_db.test_connection()
    print(f"\n  {msg}")
    if not ok:
        print("  Paki-import muna ang 'schema_visitor.sql' sa XAMPP/MySQL.")
        return
    while True:
        menu()
        ch = input("\n  Ano'ng aksyon ang gagawin? : ").strip()
        if ch == "1":
            vis_ops.pumasok()
        elif ch == "2":
            vis_ops.tala_bisita()
        elif ch == "3":
            vis_ops.hanapin_bisita()
        elif ch == "4":
            vis_ops.lumabas()
        elif ch == "5":
            vis_ops.tanggalin()
        elif ch == "6":
            vis_ops.tanggalin_lahat()
        elif ch == "0":
            print("\n  Sige, paalam!")
            break
        else:
            print("\n  * Hindi tamang pagpili.")
if __name__ == "__main__":
    main()
#pwedi alidan name files