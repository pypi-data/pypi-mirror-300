def to_lowercase(text):
    return text.lower()

def remove_spaces(text):
    return text.replace(" ", "")

def create_diagraphs(text):
    diagraphs = []
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i] == text[i + 1]:
            diagraphs.append(text[i] + 'x')
            i += 1
        else:
            if i + 1 < len(text):
                diagraphs.append(text[i] + text[i + 1])
                i += 2
            else:
                diagraphs.append(text[i] + 'x')
                i += 1
    return diagraphs

def prepare_text(text):
    text = remove_spaces(to_lowercase(text))
    return create_diagraphs(text)

def generate_key_table(keyword):
    alphabet = 'abcdefghiklmnopqrstuvwxyz'  # 'j' is omitted
    key = ''.join(sorted(set(keyword), key=lambda x: keyword.index(x)))  # Remove duplicates while preserving order
    key += ''.join([c for c in alphabet if c not in key])  # Append remaining letters

    return [list(key[i:i + 5]) for i in range(0, len(key), 5)]

def find_position(matrix, char):
    for i, row in enumerate(matrix):
        if char in row:
            return (i, row.index(char))
    return (None, None)

def playfair_encrypt(matrix, diagraph):
    r1, c1 = find_position(matrix, diagraph[0])
    r2, c2 = find_position(matrix, diagraph[1])

    if r1 is None or r2 is None:
        raise ValueError(f"Character not found in matrix: {diagraph}")

    if r1 == r2:
        return matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
    elif c1 == c2:
        return matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]
    else:
        return matrix[r1][c2] + matrix[r2][c1]

def encrypt_playfair(text, key):
    matrix = generate_key_table(key)
    diagraphs = prepare_text(text)
    encrypted_text = ''.join(playfair_encrypt(matrix, diagraph) for diagraph in diagraphs)
    return encrypted_text

# Main execution
text_plain = 'instruments'
key = 'HelloTYCS'

print("Key text:", key)
print("Plain Text:", text_plain)

cipher_text = encrypt_playfair(text_plain, key)
print("CipherText:", cipher_text)
