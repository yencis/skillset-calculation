from io import StringIO

def write_list_to_file(input_list, filename="output.txt"):
    with open(filename, 'w') as f:
        for item in input_list:
            f.write(str(item)+"\n")
        f.write("\n")

def text_to_file(text):
    """
    String of text (usually the contents of a .osu file as string)
    converted to a Python File object
    """
    return StringIO(text)