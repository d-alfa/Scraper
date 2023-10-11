
# Gražinanti visus "juodoji-arbata" puslapius ir talpina juos sąraše
j_a_puslapiai = []
def juodoji_arbata_puslapiai():
    puslapiu_sk = 1
    while puslapiu_sk <= 3:
        url = f"https://www.skonis-kvapas.lt/arbata/juodoji-arbata?page={puslapiu_sk}"
        puslapiu_sk = puslapiu_sk + 1
        j_a_puslapiai.append(url)
    return j_a_puslapiai