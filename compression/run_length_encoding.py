from dip import *

class Rle:
    def __init__(self):
        pass

    def encode_image(self,binary_image):
        """
        Compress the image
        takes as input:
        image: binary_image
        returns run length code
        """

        rle_code = []
        for row in binary_image:
            reference_pixel = row[0]
            run_counter = 1

            for pixel in row[1:]:
                if pixel == reference_pixel:
                    run_counter += 1
                else:
                    rle_code.append((run_counter, reference_pixel))
                    reference_pixel = pixel
                    run_counter = 1

            rle_code.append((run_counter, reference_pixel))

        return rle_code
        

    def decode_image(self, rle_code, height , width):
        """
        Get original image from the rle_code
        takes as input:
        rle_code: the run length code to be decoded
        Height, width: height and width of the original image
        returns decoded binary image
        """

        decoded_image = zeros((height, width), uint8)
        current_row = 0
        current_col = 0

        for run in rle_code:
            run_length, pixel_value = run
            for _ in range(run_length):
                decoded_image[current_row, current_col] = pixel_value
                current_col += 1
                if current_col >= width:
                    current_col = 0
                    current_row += 1
                    if current_row >= height:
                        break

        return decoded_image
