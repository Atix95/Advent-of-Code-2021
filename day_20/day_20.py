import os

COLORS_TURQOISE = "\x1b[38;5;80m"
COLOR_RESET = "\x1b[0m"


class TrenchMap:
    """
    Class that represents a trench map. It can load the input, convert it to binary
    and apply the enhancement algorithm. It can also count the number of pixels that
    are on.
    """

    def __init__(self):
        self.input_image = []
        self.image = []
        self.input_enhancement_algorithm = ""
        self.enhancement_algorithm = None

    def __str__(self) -> str:
        """
        Representation of the image in the same way the image is represented in the
        input.
        """
        return self.input_representation()

    def get_input_image(self) -> list[str]:
        """Input image as it is represented in the input."""
        return self.input_image

    def get_image(self) -> list[str]:
        """Image represented as binary."""
        return self.image

    def get_input_enhancement_algorithm(self) -> str:
        """Enhancement algorithm as it is represented in the input."""
        return self.input_enhancement_algorithm

    def get_enhancement_algorithm(self) -> int:
        """ "Enhancement algorithm as binary."""
        return self.enhancement_algorithm

    def input_representation(self) -> str:
        """
        Representation of the image in the same way the image is represented in the
        input.
        """
        output = ""

        for line in self.input_image:
            for character in line:
                if character == ".":
                    output += character
                elif character == "#":
                    output += COLORS_TURQOISE + character + COLOR_RESET
            output += "\n"

        return output

    def binary_representation(self) -> str:
        """Representation of the image as binary."""
        output = ""

        for line in self.image:
            for bite in line:
                if bite == "0":
                    output += bite
                elif bite == "1":
                    output += COLORS_TURQOISE + bite + COLOR_RESET
            output += "\n"

        return output

    def load_input(self, file_name: str) -> None:
        """
        Loading the input from the file and converting the image and the algorithm to
        binary.
        """
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), file_name))

        with open(file_path, "r") as input_file:
            lines = input_file.read().splitlines()

        self.input_enhancement_algorithm = lines[0]
        self.input_image = lines[2:]

        self.convert_enhancement_algorithm_to_binary()
        self.convert_image_to_binary()

    def binary_conversion(self, binary_number: int, idx_of_char: int, char: str) -> int:
        """
        Converting the image and the algorithm to binary
        """
        if idx_of_char == 0:
            if char == ".":
                binary_number = format(0, "b")
            elif char == "#":
                binary_number = format(1, "b")
        else:
            if char == ".":
                binary_number += format(0, "b")
            elif char == "#":
                binary_number += format(1, "b")

        return binary_number

    def convert_enhancement_algorithm_to_binary(self) -> None:
        """Converting the algorithm to binary."""
        for index, character in enumerate(self.input_enhancement_algorithm):
            self.enhancement_algorithm = self.binary_conversion(
                self.enhancement_algorithm, index, character
            )

    def convert_image_to_binary(self) -> None:
        """Coverting the image to binary."""
        self.image = []
        for line in self.input_image:
            number = None
            for index, character in enumerate(line):
                number = self.binary_conversion(number, index, character)
            self.image.append(number)

    def expand_images(self) -> None:
        """Expanding the image by 5 pixels in each direction."""
        additional_pixels = 5

        for index, line in enumerate(self.input_image):
            self.input_image[index] = (
                "." * additional_pixels + line + "." * additional_pixels
            )
        self.input_image = (
            ["." * len(self.input_image[0])] * additional_pixels
            + self.input_image
            + ["." * len(self.input_image[0])] * additional_pixels
        )
        self.convert_image_to_binary()

    def apply_enhancement_algorithm(self, number_of_applications: int = 2) -> None:
        """
        Recursive application of the enhancement algorithm. The number of applications
        is 2 by default. The image is expanded by 5 pixels in each direction before
        the algorithm is applied. After enhancing the image is then cropped by 1 pixel
        in each direction to cut off the edges of the image that were not turned on
        during an odd number of applications. For odd number of applications the image
        is cropped by 6 pixels in each direction to cut off the edges of the image that
        were turned on.
        """
        if number_of_applications == 0:
            return

        self.expand_images()

        number_of_lines = len(self.image)
        bite_size = len(self.image[0])

        enhanced_image = []

        for x, line in enumerate(self.image):
            enhanced_line = ""
            if x == 0 or x == number_of_lines - 1:
                enhanced_image.append(self.input_image[x])
                continue

            for y, bite in enumerate(line):
                if y == 0 or y == bite_size - 1:
                    enhanced_line += self.input_image[x][y]
                    continue
                bite_in_algorithm = int(
                    self.image[x - 1][y - 1 : y + 2]
                    + self.image[x][y - 1 : y + 2]
                    + self.image[x + 1][y - 1 : y + 2],
                    2,
                )
                assert bite_in_algorithm in range(512)
                enhanced_line += self.input_enhancement_algorithm[bite_in_algorithm]

            enhanced_image.append(enhanced_line)

        self.input_image = [line[1:-1] for line in enhanced_image[1:-1]]
        if number_of_applications % 2 == 1:
            self.input_image = [line[6:-6] for line in enhanced_image[6:-6]]
        self.convert_image_to_binary()
        self.apply_enhancement_algorithm(number_of_applications - 1)

    def number_of_pixels_on(self) -> int:
        """
        The number of pixels that are on. The image is cropped by 5 pixels in each
        direction before counting the number of pixels that are on as the edges of the
        image do not count towards the relevant pixels.
        """
        return sum([line.count("#") for line in self.input_image])

    def crop_image_after_multiple_enhancements(self) -> None:
        """
        Cropping the image by 25 pixels in each direction to cut off the edges of the
        image that were not turned on during an even number of applications.
        """
        self.input_image = [line[25:-25] for line in self.input_image[25:-25]]
        self.convert_image_to_binary()


def main():
    map = TrenchMap()
    map.load_input("day_20_input.txt")
    map.apply_enhancement_algorithm(number_of_applications=2)
    print(map.input_representation())
    print(
        f"The number of pixels that are on after 2 applications is:",
        map.number_of_pixels_on(),
    )
    map.apply_enhancement_algorithm(number_of_applications=48)
    map.crop_image_after_multiple_enhancements()
    print(map.input_representation())
    print(
        f"The number of pixels that are on after 50 applications is:",
        map.number_of_pixels_on(),
    )


if __name__ == "__main__":
    main()
