from PIL import Image
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Load the image
image = Image.open("kermit.png")

# Generate a random secret key
secret_key = get_random_bytes(16)

# Create an AES cipher object
cipher = AES.new(secret_key, AES.MODE_EAX)

# Encrypt the image data
encrypted_data, tag = cipher.encrypt_and_digest(image.tobytes())

# Save the encrypted data
with open("encrypted_image.bin", "wb") as f:
    f.write(cipher.nonce)
    f.write(encrypted_data)
    f.write(tag)

# Load the encrypted data
with open("encrypted_image.bin", "rb") as f:
    nonce = f.read(16)  # IV
    ciphertext = f.read()

# Create a new AES cipher object
cipher = AES.new(secret_key, AES.MODE_EAX, nonce=nonce)

# Decrypt the data
decrypted_data = cipher.decrypt(ciphertext)

# Create an image object from the decrypted data
decrypted_image = Image.frombytes(image.mode, image.size, decrypted_data)

# Convert the image mode to RGB
decrypted_image = decrypted_image.convert("RGB")

# Save the decrypted image
decrypted_image.save("decrypted_kermit.png")
