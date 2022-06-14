import os
import numpy as np
import PIL.Image

def encode():
    filename = input("Enter your file name (including file extension): ")
    if os.path.isfile(filename):
        message=input("Type in the message you want to encode: ")
        
        image = PIL.Image.open(filename, "r")
        width, height = image.size
        img_arr = np.array(list(image.getdata()))

        if image.mode == "P":
            print("This image is not supported")
            exit()

        channels = 4 if image.mode == "RGBA" else 3
        pixels = img_arr.size // channels
        END = "$khalid"
        message += END

        bit_message = "".join(f"{ord(i):08b}" for i in message)
        no_of_bits = len(bit_message)

        if no_of_bits > pixels:
            print("message is too large for given image")
        else:
            index = 0
            for i in range(pixels):
                for j in range (0, 3):
                    if index < no_of_bits:
                        img_arr[i][j] = int(bin(img_arr[i][j])[2:-1] + bit_message[index], 2)
                        index+=1

        img_arr = img_arr.reshape((height, width, channels))
        result = PIL.Image.fromarray(img_arr.astype('uint8'), image.mode)
        result.save('encoded.png')
        print("Successfully encoded and written into new image file-'encoded.png':)")
    else:
        print("Path does not exists.")
    
def decode():
    filename = input("Enter your file name (including file extension): ")
    if os.path.isfile(filename):
        image = PIL.Image.open(filename, "r")
        img_arr = np.array(list(image.getdata()))

        channels = 4 if image.mode == "RGBA" else 3
        pixels = img_arr.size // channels

        message_bits = [bin(img_arr[i][j])[-1] for i in range(pixels) for j in range(0, 3)]
        message_bits = "".join(message_bits)
        message_bits = [message_bits[i:i+8] for i in range(0, len(message_bits), 8)]

        message = [chr(int(message_bits[i], 2))for i in range(len(message_bits))]
        message = "".join(message)
        END = "$khalid"

        if END in message:
            print("Successfully decoded the message - '", message[:message.index(END)], "'")
        else:
            print("[ERROR] Couldn't find a message")
    else:
            print("Path does not exists.")

def main():
    ip = int(input("Select any of the option\n1.encode\n2.decode\n"))
    while(ip!=1 and ip!=2):
        print("Enter a valid choice")
        ip = int(input())
    if(ip == 1):
        encode()
    elif(ip == 2):
        decode()

if __name__ =='__main__':
    main()