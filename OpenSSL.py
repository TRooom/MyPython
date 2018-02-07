import os





def create_command(k, input, output):
    key = k.split(" ")[1]
    f = k.split(" ")[0]
    command = "openssl enc -d {0} -md md5 -k {1} -in {2} -out {3} ".format(f, key, input, output)
    return command

def pick_key(input,output,keys):
    for k in keys:
        com = create_command(k, input, output)
        code = os.system(com)
        if code == 0:
            keys.remove(k)
            break

def decrypt():
    input = "openssl/ciphertext0"
    output = "openssl/ciphertext1"
    numder = 1
    keys = ["-rc2 4f0c6a3e90401fa7bc51a5ae9982845c",
            "-cast5-cfb 6fbdbcb790138cc054556b45dfaff777",
            "-aes-192-ecb 4befaa7b927a349af5d9f7c321419c8c",
            "-desx 296c5b3207bf00fa3271287447b5e53a",
            "-des-ecb acc6cccd9ee0df92e1f329151ac28a9d",
            "-des3 5324a480df9a59e444f4b82aa1e29b30",
            "-aes-128-cbc e11f3ce8443d192bb376d1d025de2540",
            "-camellia128 617223fdcaf2532a633b2dc0675b9663",
            "-seed e1930b4927e6b6d92d120c7c1bba3421",
            "-aes-256-cbc 146983842e420321011e74145a59aa48",
            "-bf ae9d5595593d62eefa1687551497db39",
            "-des-ede 5f6b93462201020193c8664c600e3faa",
            "-aes256 df2240f7fd137880c89f375a81728256"]

    for _ in range(13):
        pick_key(input,output,keys)
        numder+=1
        input = output
        output = input[:18] + str(numder)


decrypt()