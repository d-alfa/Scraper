
# Funkcija gražinanti visus "juodoji-arbata" puslapius
def visi_puslapiai():
    puslapiu_sk = 1
    puslapiai = []
    while puslapiu_sk <= 3:
        url = f"https://www.skonis-kvapas.lt/arbata/juodoji-arbata?page={puslapiu_sk}"
        puslapiu_sk = puslapiu_sk + 1
        puslapiai.append(url)
    print(puslapiai)

visi_puslapiai()