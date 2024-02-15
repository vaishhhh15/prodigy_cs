def encrypt_image(image_path, key):
    with open(image_path, 'rb') as file:
        # Read image data as bytes
        image_data = bytearray(file.read())

    # Apply a simple bitwise XOR operation to each byte based on the key
    encrypted_data = bytes([byte ^ key for byte in image_data])

    # Save the encrypted image
    with open("encrypted_image.png", 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

def decrypt_image(encrypted_image_path, key):
    with open(encrypted_image_path, 'rb') as encrypted_file:
        # Read encrypted image data as bytes
        encrypted_data = bytearray(encrypted_file.read())

    # Reverse the operation using the same key to decrypt
    decrypted_data = bytes([byte ^ key for byte in encrypted_data])

    # Save the decrypted image
    with open("decrypted_image.png", 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

def main():
    # Replace 'your_image.png' with the path to your input image
    image_path = 'your_image.png'

    # Set a key for encryption
    encryption_key = 123

    # Encrypt the image
    encrypt_image(image_path, encryption_key)
    print("Image encrypted successfully.")

    # Decrypt the image
    encrypted_image_path = 'encrypted_image.png'
    decrypt_image(encrypted_image_path, encryption_key)
    print("Image decrypted successfully.")

if __name__ == "__main__":
    main()
