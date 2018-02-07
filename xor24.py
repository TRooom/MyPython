encrypted = open("encrypted_text", mode="rb").read()


def generate_bytes():
    b = []
    for x in range(256):
        b.append(x)
    return b


def pick_byte(pos):
    all_bs = generate_bytes()
    for x in range(pos, len(encrypted), 24):
        if x >= len(encrypted):
            break
        enc = int(encrypted[x])
        new_bs = []
        for b in all_bs:
            if chr(enc^b) in "qwertyuiopasdfghjklzxcvbnm_":
                new_bs.append(b)
        if len(new_bs) == 1:
            return new_bs[0]
        all_bs = new_bs

def pick_key():
    key = []
    for x in range(24):
        k = pick_byte(x)
        key.append(k)
    return key

def decript():
    key = pick_key()

    decripted = []
    for x in range(len(encrypted)):
        dec = key[x%24] ^ int(encrypted[x])
        decripted.append(dec)
    d = bytes(decripted)
    open("decripted",mode="wb").write(d)
    key = [chr(x) for x in key]
    key = "".join(key)
    print(key)

decript()