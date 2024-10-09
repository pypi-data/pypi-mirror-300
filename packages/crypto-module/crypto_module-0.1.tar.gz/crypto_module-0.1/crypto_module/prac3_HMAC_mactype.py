import hmac
message = "welcome to TYCS"
key = "INS"

hmac1 = hmac.new(key=key.encode(),msg=message.encode(),digestmod="sha1")
message_digest1 = hmac1.digest()
print("Message Digest 1:",hmac1.name,message_digest1)

hmac2=hmac.new(key=key.encode(),digestmod="sha1")
hmac2.update(bytes(message,encoding="utf-8"))
message_digest2 = hmac2.digest()
print("Message Digest 2:",hmac2.name,message_digest2)

hmac3=hmac.new(key=key.encode(),digestmod="sha1")
hmac3.update(bytes("Welcome to",encoding="utf-8"))
hmac3.update(bytes("CoderzColumn.",encoding="utf-8"))
message_digest3 = hmac3.digest()
print("Message Digest 3:",hmac3.name,message_digest3)

print("Message Digest 3:",hmac3.name,message_digest3)

print("\nMessage Digest Size for1 : {}, 2: {} and 3:{}".
      format(hmac1.digest_size,hmac2.digest_size,hmac3.digest_size,))
print("\nMessage Block Size for1 : {}, 2: {} and 3:{}".
      format(hmac1.block_size,hmac2.block_size,hmac3.block_size,))
