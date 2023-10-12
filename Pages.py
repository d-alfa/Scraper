
# Returns "juodoji-arbata" pages and puts them inside a list
j_a_pages = []
def juodoji_arbata_pages():
    pages_sk = 1
    while pages_sk <= 3:
        url = f"https://www.skonis-kvapas.lt/arbata/juodoji-arbata?page={pages_sk}"
        pages_sk = pages_sk + 1
        j_a_pages.append(url)
    return j_a_pages