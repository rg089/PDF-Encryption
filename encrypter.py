"""
Encrypt PDF's using Python.
"""

import PyPDF2
import os


def yes_no_input(qn):
    """
    Parameters: qn -> The question asked in string form.
    Returns: True if answer is yes, else False.
    """
    ans = ""
    while not (ans == "y" or ans == "yes" or ans == "n" or ans == "no"):
        ans = input(qn).lower()
    if ans == "yes" or ans == "y":
        return True
    return False


def positive_int_input(qn, n):
    """
    Take integer input > 0.
    Parameters: qn -> The question asked in string form.
    Returns: The integer input.
    """
    ans = -1
    while ans < 1:
        try:
            ans = int(input(qn))
        except:
            print("Please enter an integer from 1 to {}.".format(n))
    return ans


def receivePassword():
    """
    Takes the password input and validates it.
    :return: The Entered Password
    """
    password1 = input("Please Enter the Password: ")
    while len(password1) < 3:
        print("The length should be at least 3 characters.")
        password1 = input("Please enter a longer password: ")
    pw = input("Please Re-Enter the Password to Confirm: ")
    wrongTries = 0
    while pw != password1:
        wrongTries += 1
        print("Error: Passwords Don't Match! {} Tries Left.".format(3 - wrongTries))
        if wrongTries == 3:
            print("Resetting the Password...\n")
            return ""
        pw = input("Enter the correct Password: ")
    print("Success! Password Set Successfully!")
    return password1


def getPath():
    path = input("Please enter the path to the location of the PDF File including the file itself (Please use \\ "
                 "instead of /) : ")
    if not os.path.exists(path) or not path.endswith(".pdf"):
        print("Please enter a valid path to the PDF. The path should include the PDF itself, i.e. it should end with "
              ".pdf")
        path = input("Please enter the valid path: ")
    return path


def findPDF():
    """
    Finds and selects the PDF in either the current directory or the specified path
    :return: Path of the PDF File.
    """
    print("If the PDF document is not in the current directory ({}), please answer 'no' to the below question.".format(
        os.getcwd()))
    sameDirectory = yes_no_input("Is the file in this directory? (y/n): ")
    if not sameDirectory:
        return getPath()
    possiblePDFs = [file for file in os.listdir() if file.endswith(".pdf")]
    if len(possiblePDFs) == 0:
        print("No PDF found in the current directory.")
        return getPath()
    if len(possiblePDFs) == 1:
        print("PDF Found!\nName - {}".format(possiblePDFs[0]))
        return possiblePDFs[0]
    print("Please chose the PDF you want to convert.")
    for i in range(1, len(possiblePDFs) + 1):
        print("{}. {}".format(i, possiblePDFs[i - 1]))
    pdfNum = positive_int_input("Please enter the number at which your PDF falls: ", len(possiblePDFs))
    return possiblePDFs[pdfNum - 1]


def extractName(path):
    """
    Given the path of the PDF, extracts its name.
    :param path: Path of the given PDF.
    :return: Name of the PDF
    """
    words = path.split("\\")
    name = words[-1]
    index = name.find(".pdf")
    if index == -1:
        print("There was a problem in finding the name of the PDF.")
        return ""
    else:
        return name[:index]


def savePassword(name: str, password: str):
    """
    Saves the password in the text file.
    :param name: Name of the encrypted PDF.
    :param password: The password used for encryption.
    :return: None.
    """
    with open("PasswordBank.txt", "a+") as f:
        f.write("{}_encrypted.pdf : {}\n".format(name, password))
    print("Password Successfully Saved in PasswordBank!")


def createEncrypted(path: str, name: str, password: str):
    """
    Creates the encrypted PDF with the given Password.
    :param path: The path of the PDF to encrypt.
    :param name: The name of the PDF to encrypt
    :param password: The encryption password.
    :return: None.
    """
    print ("Generating Encryption.....")
    input_pdf = PyPDF2.PdfFileReader(path)
    output_pdf = PyPDF2.PdfFileWriter()
    if input_pdf.isEncrypted:
        print("Given PDF is already encrypted.\nAborting ...")
        return
    output_pdf.appendPagesFromReader(input_pdf)
    output_pdf.encrypt(password)
    with open("{}_encrypted.pdf".format(name), "wb") as f:
        output_pdf.write(f)
    print("Successful Generation of the Encrypted PDF.")
    print("Name of the encrypted PDF - {}_encrypted.pdf".format(name))
    print("Location - Current Directory ({})".format(os.getcwd()))
    save = yes_no_input("Do you want to save the password? (y/n): ")
    if save:
        savePassword(name, password)


if __name__ == '__main__':
    print("Starting PDF Encryption....\nPlease follow the instructions and provide the required details.\n")
    path = findPDF()
    password = receivePassword()
    while password == "":
        password = receivePassword()
    name = extractName(path)
    createEncrypted(path, name, password)
