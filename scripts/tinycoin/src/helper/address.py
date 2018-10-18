import blocksmith
from blocksmith import BitcoinWallet
import codecs
import hashlib
import uuid


def public_to_address(public_key):
    print("Public key: ", public_key)
    public_key_bytes = codecs.decode(public_key, 'hex')
    # Run SHA256 for the public key
    sha256_bpk = hashlib.sha256(public_key_bytes)
    sha256_bpk_digest = sha256_bpk.digest()
    # Run ripemd160 for the SHA256
    ripemd160_bpk = hashlib.new('ripemd160')
    ripemd160_bpk.update(sha256_bpk_digest)
    ripemd160_bpk_digest = ripemd160_bpk.digest()
    ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest, 'hex')
    # Add network byte
    network_byte = b'00'
    network_bitcoin_public_key = network_byte + ripemd160_bpk_hex
    network_bitcoin_public_key_bytes = codecs.decode(network_bitcoin_public_key, 'hex')
    # Double SHA256 to get checksum
    sha256_nbpk = hashlib.sha256(network_bitcoin_public_key_bytes)
    sha256_nbpk_digest = sha256_nbpk.digest()
    print("first sha: ", codecs.encode(sha256_nbpk_digest, 'hex'))
    sha256_2_nbpk = hashlib.sha256(sha256_nbpk_digest)
    sha256_2_nbpk_digest = sha256_2_nbpk.digest()
    sha256_2_hex = codecs.encode(sha256_2_nbpk_digest, 'hex')
    print("second sha: ", sha256_2_hex)
    checksum = sha256_2_hex[:8]
    print("checksum: ", checksum)
    # Concatenate public key and checksum to get the address
    address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')
    wallet = base58(address_hex)
    return wallet


def base58(address_hex):
    print("address hex: ", address_hex)
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    b58_string = ''
    # Get the number of leading zeros and convert hex to decimal
    leading_zeros = len(address_hex) - len(address_hex.lstrip('0'))
    # Convert hex to decimal
    address_int = int(address_hex, 16)
    # Append digits to the start of string
    while address_int > 0:
        digit = address_int % 58
        # print("digit: ", digit)
        digit_char = alphabet[digit]
        # print("digit char: ", digit_char)
        b58_string = digit_char + b58_string
        address_int //= 58

    # print("address_int: ", address_int)
    # Add '1' for each 2 leading zeros
    ones = leading_zeros // 2
    print("b58string: ", b58_string)
    print("ones: ", ones)
    for one in range(ones):
        print("bitc: ", '1' + b58_string)
        b58_string = 'C' + b58_string

    return b58_string


def generate_address():
    kg = blocksmith.KeyGenerator()
    kg.seed_input(str(uuid.uuid4()))
    key = kg.generate_key()
    print("Private key: ", key)

    btc = BitcoinWallet()

    public_key = btc._BitcoinWallet__private_to_public(key)
    address = public_to_address(public_key)
    return address