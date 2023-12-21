# Takekuni Tanemori
# Assembler that reads Assembly procedures and outputs a hexadecimal image file to be read and processed by the CPU


# reads a file and puts each line of the file into a list as a list of each part of the instruction
def create_file_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_lines = []
        for line in file:
            no_comma = line.replace(",", "")
            no_comma = no_comma.replace("[", "")
            no_comma = no_comma.replace("]", "")
            file_lines.append(no_comma.split())
        return file_lines


# prints out each line of the file
def print_file(file_lines):
    for line in file_lines:
        print(line)


# converts decimal to binary
def deci_to_bin(deci):
    bin = ""
    if deci == 0:
        return "0"
    while (deci != 0):
        bin = str(deci % 2) + bin
        deci = deci // 2
    return bin


# pads 0 to binary to be length bits long
def pads(binary, length):
    num_zero = length - len(binary)
    return num_zero * "0" + binary



# reads the instruction type and encode in binary
# bits 0-2 is opcode
def type_to_bin(type):
    if type == "ADD":
        return "000"
    elif type == "SUB":
        return "001"
    elif type == "LDR":
        return "010"
    elif type == "STR":
        return "011"


# checks if instruction contains an immediate value or not and encodes into binary
# bit 3 is immediate/register
def check_imm(last_value):
    try:
        num = int(last_value)
        #print("immediate value, value is " + str(num))
        return ("0", True)
    except ValueError:
        #print("register, it is " + last_value)
        return ("1", False)

# converts register to binary encoding
# bits 4-5 and 6-7 are register 1 and register 2
def reg_to_bin(register):
    deci = int(register[1:])
    bin_string = pads(deci_to_bin(deci), 2)
    return bin_string


# converts immediate value to binary encoding
# bits 8-15 is immediate value (can be register 3)
def imm_to_bin(immediate):
    deci = int(immediate)
    bin_string = pads(deci_to_bin(deci), 8)
    return bin_string








# reads a single instruction and returns value in binary
def read_instruction_line(line):
    binary_encryption = ""

    # adds bits 0-2
    binary_encryption += type_to_bin(line[0])

    # adds bit 3
    imm_bin, imm = check_imm(line[3])
    binary_encryption += imm_bin

    # adds bit 4-5
    binary_encryption += reg_to_bin(line[1])

    # adds bit 6-7
    binary_encryption += reg_to_bin(line[2])

    # adds bit 8-15
    if imm:
        binary_encryption += imm_to_bin(line[3])
    else:
        binary_encryption += "000000"
        binary_encryption += reg_to_bin(line[3])

    return binary_encryption

# encrypts each line into binary
def convert_file_to_binary(file_lines):
    binary_file = []
    for line in file_lines:
        print(read_instruction_line(line))
        binary_file.append(read_instruction_line(line))
    return binary_file

# converts binary to hexadecimal
def convert_to_image_file(binary_file):
    image_file = ["v3.0 hex words addressed\n"]
    count = 0
    total_count = 0
    while total_count != 256:
        if total_count < len(binary_file):
            deci = int(binary_file[total_count], 2)
            hex_val = hex(deci)[2:]

            hex_val = "0" * (4 - len(hex_val)) + hex_val
        else:
            hex_val = "0000"
        if total_count % 16 == 0:
            hex_val = str(hex(count))[2:] + "0: " + hex_val
            count += 1
        if total_count % 16 == 15:
            hex_val += "\n"
        else:
            hex_val += " "
        image_file.append(hex_val)
        total_count += 1
    return image_file


# creates an image file
def create_image_file(hexa_file):
    outputFile = open("image", "x")
    outputFile.writelines(hexa_file)
    outputFile.close()

# splits the file into two lists, text and data segment
def split_file(file_list):
    text = []
    data = []
    is_text = False
    is_data = False
    for line in file_list:
        if line == ".text":
            is_text = True
            continue
        if line == ".data":
            is_data = True
            is_text = False
            continue
        if is_text:
            text.append(line)
        if is_data:
            data.append(line)
    return (text,data)




# runs the program
def run_program():
    file_list = create_file_list('proj2.txt')
    binary = convert_file_to_binary(file_list)
    image = convert_to_image_file(binary)
    create_image_file(image)



run_program()