import os


def create_file_path(file_name):
    # Create the file path to a file, which is in the same folder as the program
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)


def load_hexa_decode_dict(file_name):
    # Load the dict, which decodes the hexadecimal string into four bits of binary
    decode_dict = {}

    with open(create_file_path(file_name), "r", encoding="utf-8") as file_decode:
        for line in file_decode.read().split("\n"):
            key, value = line.split(" = ")
            decode_dict[key] = value

    return decode_dict


def load_hexa_transmission(file_name):
    # Load the hexadecimal transmission into a single string
    hexa_message = ""

    with open(create_file_path(file_name), "r", encoding="utf-8") as file_hexa:
        hexa_message = file_hexa.readline()

    return hexa_message


def decode_hexa_into_binary(hexa_message):
    # Decode the hexadecimal string into a binary code
    decode_dict = load_hexa_decode_dict("day_16_hexadecimal_decode.txt")
    binary_string = ""

    for hexa_char in hexa_message:
        binary_string += decode_dict[hexa_char]

    return binary_string


def decode_literal_value(binary_string, length):
    # Packet represents literal value. While the five bit packet, which is stored in
    # packet_literal, starts with a 1, the four bits after the 1 are added to the
    # binary literal string. Then the binary_string is stripped of the first 5 bits
    # and the next five bits are added to packet_literal. If the first bit is a 0,
    # this procedure is done one last time and the final literal value can be converted
    # into a decimal number (literal_value).
    binary_literal = ""
    packet_literal = binary_string[:5]

    while packet_literal[0] == "1":
        binary_literal += packet_literal[1:5]
        binary_string = binary_string[5:]
        packet_literal = binary_string[:5]
        length += 5

    # Intercept case literal_packet start with 0
    binary_literal += packet_literal[1:5]
    binary_string = binary_string[5:]
    length += 5

    literal_value = int(binary_literal, 2)

    return (
        binary_string,
        length,
        literal_value,
    )


def sum_of_packets(literal_values):
    # Returns the sum of the sub-packets
    return sum(literal_values)


def product_of_packets(literal_values):
    # Returns the product of the sub-packets
    resulting_value = 1
    for literal_value in literal_values:
        resulting_value *= literal_value

    return resulting_value


def minimum_of_packets(literal_values):
    # Returns the smallest value of the sub-packets
    return min(literal_values)


def maximum_of_packets(literal_values):
    # Returns the biggest value of the sub-packets
    return max(literal_values)


def greater_than_packets(literal_values):
    # Returns 1 if value of first sub-packet is greater
    # than the second one. Otherwise returns 0.

    if literal_values[0] > literal_values[1]:
        resulting_value = 1
    else:
        resulting_value = 0

    return resulting_value


def less_than_packets(literal_values):
    # Returns 1 if value of first sub-packet is smaller
    # than the second one. Otherwise returns 0.

    if literal_values[0] < literal_values[1]:
        resulting_value = 1
    else:
        resulting_value = 0

    return resulting_value


def equal_to_packets(literal_values):
    # Returns 1 if value of first sub-packet is
    # euqal to the second one. Otherwise returns 0.

    if literal_values[0] == literal_values[1]:
        resulting_value = 1
    else:
        resulting_value = 0

    return resulting_value


def decode_binary(binary_string, length=0):
    # The needed parts of the binary_string are sliced of, until all packets are decoded.
    # The tailing zeros of the outermost packet can be ignored, because the length of each
    # sub-packet can be taken from the sub-packet itself. In the first run of the function,
    # the type ID of the outermost packet is determined. After that the sub-packets are de-
    # coded for their literal values (type ID = 4). If a sub-packet contains at least one
    # more sub-packet (type ID != 4), the function is called recursively. To track the length
    # of a sub-packet, the current position in the binary_string is tracked with the variable
    # "length". Once the deepest level of the sub-packet is reached (type ID = 4), the decoded
    # values are stored in a list (literal_values) and the values are processed according to
    # the type ID (type ID != 4). The function then goes back one level and either processes
    # the next sub-packet or goes one level higher, until all sub-packets are decoded. Then
    # the value of the outermost packet is determined according to the type ID, which was
    # determined in the beginning, and is stored in resulting_value and returned.

    packet_version, type_id = int(binary_string[:3], 2), int(binary_string[3:6], 2)
    binary_string = binary_string[6:]
    length += 6

    # Track the length of the sub-packet in bits in length_sub_packet, if the length type ID
    # is equal to 0. If is is equal to 1, the number of sub-packets contained in the packet
    # is tracked with sub_packet_count. The values found in the sub-packets are stored in
    # literal_values.
    length_sub_packet = 0
    sub_packet_count = 0
    literal_values = []

    if type_id == 4:
        # Packet represents a literal value
        binary_string, length, literal_value = decode_literal_value(
            binary_string, length
        )

    else:
        # Packet represents an operator, so the length type ID has to be determined
        length_type_id = int(binary_string[0], 2)
        binary_string = binary_string[1:]
        length += 1

        if length_type_id == 0:
            # Any number of sub-packets are stored in the next x bits, where x is stored in
            # total_length_int. To track the current position in the packet, the length of
            # each sub-packet contained in the packet with total_length_int is tracked in
            # length_sub_packet. Each value found in the sub-packets is added to the list of
            # literal_values. When the total length of the sub-packet is reached, the length
            # of the whole packet is added to the length in the binary_string.
            total_length_int = int(binary_string[:15], 2)
            binary_string = binary_string[15:]
            length += 15

            while length_sub_packet != total_length_int:
                binary_string, length_sub_packet, literal_value = decode_binary(
                    binary_string, length_sub_packet
                )
                literal_values.append(literal_value)

            length += length_sub_packet

        elif length_type_id == 1:
            # x sub-packets are stored in the packet, where x is stored in num_of_packets_int.
            # Each value found in a sub-packet is added to the list of literal_values. If all
            # sub-packets are decoded, the length of the whole packet is added to length.
            num_sub_packets_int = int(binary_string[:11], 2)
            binary_string = binary_string[11:]
            length += 11

            while sub_packet_count < num_sub_packets_int:
                binary_string, length_sub_packet, literal_value = decode_binary(
                    binary_string, length_sub_packet
                )
                literal_values.append(literal_value)
                sub_packet_count += 1

            length += length_sub_packet

        # Determine the value of a packet according to the type ID. The
        # resulitng_value is then given to literal_value and returned.
        if type_id == 0:
            resulting_value = sum_of_packets(literal_values)

        elif type_id == 1:
            resulting_value = product_of_packets(literal_values)

        elif type_id == 2:
            resulting_value = minimum_of_packets(literal_values)

        elif type_id == 3:
            resulting_value = maximum_of_packets(literal_values)

        elif type_id == 5:
            resulting_value = greater_than_packets(literal_values)

        elif type_id == 6:
            resulting_value = less_than_packets(literal_values)

        elif type_id == 7:
            resulting_value = equal_to_packets(literal_values)

        literal_value = resulting_value

    return binary_string, length, literal_value


def main():
    hexa_message = load_hexa_transmission("day_16_input.txt")
    binary_string = decode_hexa_into_binary(hexa_message)
    resulting_value = decode_binary(binary_string)[2]

    print(f"The value of the outer most packet is: {resulting_value}")


if __name__ == "__main__":
    main()
