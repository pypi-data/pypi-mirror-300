
# import markdown as markdown_

class markdown:
    def __init__(self):
        # print("init markdown")
        pass 

    @staticmethod
    def number_lines_in_md(input, output):
        with open(input, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        numbered_lines = []
        numbering = False
        line_number = 1

        for line in lines:
            # Check for start and stop tags
            if "<numbering>" in line:
                line_number = 1
                numbering = True
                continue  # Skip adding the start tag
            elif "</numbering>" in line:
                numbering = False
                continue  # Skip adding the stop tag

            # If numbering is active, number the line
            if numbering:
                if line.strip(): # remove blank lines from list
                    numbered_lines.append(f"{line_number}. {line.strip()}\n")
                    line_number += 1
            else:
                numbered_lines.append(line)

        # Write back to the file or a new file
        with open(output, 'w', encoding='utf-8') as file:
            file.writelines(numbered_lines)