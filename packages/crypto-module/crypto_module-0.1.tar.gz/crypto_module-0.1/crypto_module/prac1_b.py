def stringEncryption(text, key):
    cipherText = ""
    cipher = []

    # Ensure that text and key lengths are the same
    if len(text) != len(key):
        raise ValueError("Text and key must be of the same length.")

    # Calculate cipher values
    for i in range(len(key)):
        value = (ord(text[i]) - ord('A') + ord(key[i]) - ord('A')) % 26
        cipher.append(value)

    # Convert numeric values to characters
    for value in cipher:
        x = value + ord('A')
        cipherText += chr(x)

    return cipherText

plainText = "HelloTYCS"
key = "MONEYBANK"

# Ensure both plainText and key are in uppercase
plainText = plainText.upper()
key = key.upper()

# Encrypt the plainText
encryptedText = stringEncryption(plainText, key)
print("Cipher Text - " + encryptedText)
