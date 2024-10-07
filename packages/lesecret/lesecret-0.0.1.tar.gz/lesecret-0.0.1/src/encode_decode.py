import numpy as np
from PIL import Image

END_OF_TEXT = '1111111111111110'
ENCODING = 'utf-8'

image = Image.open('/Users/jerry/Documents/_03_Development/_01_Projects/the-secret/test.jpg')
image_data = np.array(image)
image_capacity = image_data.size
print(image_data.shape)

print(f'This image can store {image_capacity // 8} bytes of data')

text = 'test string to encode 測試'

binary_message = ''.join(format(byte, '08b') for byte in text.encode(ENCODING))
binary_message += END_OF_TEXT

print(f'{binary_message=}')

data_flat = image_data.flatten()
print(f"{data_flat=}")

for i, bit in enumerate(binary_message):
    data_flat[i] = (data_flat[i] & ~1) | int(bit)

print(f"{data_flat=}")

image_data = data_flat.reshape(image_data.shape)
# print(f"{image_data=}")
encoded_image = Image.fromarray(image_data)
encoded_image.save('/Users/jerry/Documents/_03_Development/_01_Projects/the-secret/test-encode.png')

####### decoding phase

image = Image.open('/Users/jerry/Documents/_03_Development/_01_Projects/the-secret/test-encode.png')
image_data = np.array(image)
# print(f"{image_data=}")

data_flat = image_data.flatten()
print(f"{data_flat=}")

lsb_array = data_flat & 1
binary_message = ''.join(lsb_array.astype(str))

end_marker = binary_message.find(END_OF_TEXT)

decoded_binary_message = binary_message[:end_marker]
print(f"{decoded_binary_message=}")
byte_chunks = [decoded_binary_message[i : i + 8] for i in range(0, len(decoded_binary_message), 8)]
byte_array = bytearray(int(byte, 2) for byte in byte_chunks)

print(byte_array.decode(ENCODING))
