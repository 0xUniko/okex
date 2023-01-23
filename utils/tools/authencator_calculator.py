import hmac, base64, struct, hashlib, time


def calGoogleCode(secret_key):
    """
    基于时间的算法
    :param secret_key:
    :return:
    """
    # 密钥长度非8倍数，用'='补足
    # lens = len(secret_key)
    # lenx = 8 - (lens % 4 if lens % 4 else 4)
    # secret_key += lenx * '='
    # print(secret_key)

    decode_secret = base64.b32decode(secret_key, True)
    # 解码 Base32 编码过的 bytes-like object 或 ASCII 字符串 s 并返回解码过的 bytes。

    interval_number = int(time.time() // 30)

    message = struct.pack(">Q", interval_number)
    digest = hmac.new(decode_secret, message, hashlib.sha1).digest()
    index = ord(chr(digest[19])) % 16  # 注：网上材料有的没加chr，会报错
    google_code = (struct.unpack(">I", digest[index:index + 4])[0]
                   & 0x7fffffff) % 1000000

    return "%06d" % google_code