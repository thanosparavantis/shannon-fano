import numpy as np
from PIL import Image
import base64
import json

def main():
    # https://github.com/DanonOfficial/Huffman-Shannon-Fano-Coding/blob/master/png.py
    # https://stackoverflow.com/questions/8863917/importerror-no-module-named-pil
    # https://stackoverflow.com/questions/25102461/python-rgb-matrix-of-an-image
    # https://stackoverflow.com/questions/13730468/from-nd-to-1d-arrays

    code_size   = 0     # To be filled
    noise       = 0     # To be filled

    # Load image from file
    image = Image.open("image.jpg")
    print("Format: {}, Size: {}, Mode: {}".format(image.format, image.size, image.mode))

    width = image.size[0]
    height = image.size[1]
    pixel_array = image.load()

    # Extract RGB values from all pixels
    array_4d = np.array(image)

    # Convert 4d array to 1d
    array_1d = np.ravel(array_4d)

    print("RGB array:\n" + str(array_1d))
    print()

    linear_compression(width, height, array_1d)


def linear_compression(width, height, rgb_array, n=10, k=8):
    # Σελίδα 152
    # https://www.youtube.com/watch?v=oYONDEX2sh8
    # https://www.youtube.com/watch?v=z4WE2qpvaF8

    # C => Κώδικας
    # G => Γεννήτορας πίνακας => [ Ι_k | P ] => διάσταση (n * k)
    # P => Αυθαίρετος πίνακας => διάσταση (k * (n - k))
    # D => Διάνυσμα της λέξης
    # H => Πίνακας ισοτιμίας => [ transpose P | I_(n-k) ] => διάσταση (n * (n - k))

    # C = D * G

    # Παίρνουμε τη πληροφορία και τη χωρίζουμε σε k διαδοχικά τμήματα
    # Κωδικοποιούμε το καθένα σε μήκος n σύμφωνα με ένα σύνολο κανόνων
    # Τα n-k ψηφία ελέγχου προκύπτουν από τους γραμμικούς συνδιασμούς των ψηφίων πληροφορίας

    # ==========================================================
    # Convert all RGB values to binary digits
    # ==========================================================

    rgb_bin_array = []

    for num in rgb_array:
        binary = bin(num)[2:].zfill(k)
        rgb_bin_array.append([int(bit) for bit in list(binary)])

    rgb_bin_array = np.array(rgb_bin_array)

    # ==========================================================
    # Setup matrices I, P and G
    # ==========================================================

    I = np.eye(k, dtype=int)
    P = np.random.randint(low=0, high=2, size=(k, n-k), dtype=int)
    G = np.concatenate((I, P), axis=1)

    print("RGB bin array:\n" + str(rgb_bin_array))
    print()
    print("I:\n" + str(I))
    print()
    print("P:\n" + str(P))
    print()
    print("G:\n" + str(G))

    print()
    print()

    # ==========================================================
    # Setup array of encoded RGB binary values
    # ==========================================================

    c = []

    for bits in rgb_bin_array:
        encoded = np.mod(bits.dot(G), np.array([2])) # Apply mod 2 to limit values on 0-1
        c.append(encoded)

    c = np.array(c)
    print("c:\n" + str(c))

    # ==========================================================
    # Append all encoded bits into one string
    # ==========================================================

    raw_encoded = ""
    for bits in c:
        raw_encoded += "".join([ str(bit) for bit in bits ])

    print()
    print(raw_encoded)
    print()

    # Base64 encoding

    base64_encoded = base64.b64encode(raw_encoded.encode())

    # ==========================================================
    # JSON data
    # ==========================================================

    data = {
        "data": base64_encoded.decode(),
        "error": 0,
        "width": width,
        "height": height,
        "n": n,
        "k": k
    }
    print(json.dumps(data))


if __name__ == "__main__":
    main()
