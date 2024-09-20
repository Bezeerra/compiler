import sys
# sys.path.append('/home/bezerra/Desktop/Estudos/SAM-Compiler')
#
# from SAMCompile.main_sam import sam_compiler


class SamHandler:
    def __init__(self):
        pass
    # def call_sam_compiler(self, file):
    #     try:
    #         result, memory = sam_compiler(file)
    #         print("Memory: ", memory)
    #     except Exception as error:
    #         print("Error calling SAM: ", error)
            
    def write_sam_file(self, functions):
        with open('sam_code.sam', 'w') as file:
            for function in functions:
                file.write(f"{function}\n")
        # self.call_sam_compiler('sam_code.sam')
        




