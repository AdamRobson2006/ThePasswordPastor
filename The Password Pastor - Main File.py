# Modules are imported here

from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import mysql.connector
import base64

# Here is the code that defines the login window within the program.
# This will need to start up automatically when the program is run, otherwise the user will not be able to get in.
# I have defined this as loginWindow and have given it the title "The Password Pastor Login".
# The initial window size has been set to 1000x500 pixels however I am giving the user the
# option to resize it in case that the window is too small for them specifically.
# This is why the .resizable() has been set to true on both the x and y axis.
# The configure() function changes the background colour of the loginWindow. 
# Using minsize() means that the window layout doesn't become disfigured when the size is made smaller.


loginWindow =Tk()
loginWindow.title("The Password Pastor Login")
loginWindow.geometry("820x550")
loginWindow.resizable(True, True)
loginWindow.configure(background="light blue")
loginWindow.minsize(width=820, height=550)

# Further along in the code, I am going to need the customisable font variables so they can be interchangeable.
# For now, I have set their sizes as permenant values but this can be changed at a later date. In future, it may
# be wise to address font size, type and boldness in seperate categories to simplify the accessability
# functionality

defaultFont = ("Arial", 10 ,"bold")
defaultFont2 = ("Arial", 15 ,"bold")


# Defined here is the topbarFrame that will contain the loginWindowTitle. This will dynamically change according to
# the window size. columnconfigure() is what allows the column's size to change. 

loginTopbarFrame = Frame(loginWindow, bg='RoyalBlue1', relief="solid", borderwidth=3)
loginTopbarFrame.grid(row=0, column=0, columnspan=3, sticky=W+E)

# Here is the window title for The Password Pastor Login Screen.
# This is what appears when it is hovered over in the taskbar, and is what appears on the left of the minimise and close buttons.
# Because the entire program is part of The Password Pastor, it shares the same name as the main window. 

loginWindowTitle = Label(loginTopbarFrame, text="The Password Pastor", height=5, width=20, bg="LightBlue1", relief="solid", borderwidth=2, font=defaultFont)
loginWindowTitle.pack(expand=True, pady=5)

# Here are the column configurations for the login window. These keep the widget spacing in order within the grid that organises
# the image, login entrys and submit button. 

loginWindow.columnconfigure(0, weight=1)
loginWindow.columnconfigure(1, weight=1)
loginWindow.columnconfigure(2, weight=1)

# This is the code which inserts the images stored on the device from their file locations. 
# The images are resized so they can better fit the window
# and the logo image is gridded in the login window. The other image will be used in the main window later in the program

logoFile = r"C:\Users\adamr\OneDrive\Documents\Quick Access Folder\Work\Computer Science\Computer Science - A Level\Programming\Project Logo --- The Password Pastor --- Compressed.jpg"
logoData = Image.open(logoFile)

width = 80
height = 80
resizedLogo = logoData.resize((width, height))

clipboardFile = r"C:\Users\adamr\OneDrive\Documents\Quick Access Folder\Work\Computer Science\Computer Science - A Level\Programming\Clipboard Symbol.png"
clipboardData = Image.open(clipboardFile)

width = 25
height = 25
resizedClipboard = clipboardData.resize((width,height))


logoInfo = ImageTk.PhotoImage(logoData)
loginImage = Label(loginWindow, image=logoInfo, borderwidth=5, relief="solid")
loginImage.grid(row = 2, column = 0, padx=(20, 0),pady=20, sticky=W)

# Defined here are the frames that the entry windows and labels are going to be stored within. 


loginboxFrame = Frame(loginWindow, bg='white', relief="solid", borderwidth=2)
loginboxFrame.grid(row=2, column=1, padx=(0,20),pady=20,sticky=E)

usernameFrame = Frame(loginboxFrame, bg='RoyalBlue1', relief="solid", borderwidth=1, width=30)
usernameFrame.grid(row=1,column=1, sticky=N, padx=10, pady=10)

passwordFrame = Frame(loginboxFrame, bg='RoyalBlue1', relief="solid", borderwidth=1, width=30)
passwordFrame.grid(row=3,column=1, sticky=S, padx=10, pady=10)

# Defined below are the details relating to the username input. 

usernameLabel = Label(usernameFrame, bg='RoyalBlue1', fg="white", font=defaultFont,text="Enter your Username:", height=2)
usernameLabel.grid(row=1, column=1, padx=10, pady=5, sticky=E)

usernameReference = StringVar()

usernameEntry = Entry(usernameFrame, textvariable=usernameReference)
usernameEntry.grid(row=1, column=2, padx=10, pady=5, sticky=W)


# Defined here are the details relating to the password input

passwordLabel = Label(passwordFrame, bg='RoyalBlue1', fg="white", font=defaultFont, text="Enter your Password:", height=2)
passwordLabel.grid(row=2, column=1, padx=10, pady=5, sticky=E)

passwordReference = StringVar()

passwordEntry = Entry(passwordFrame, textvariable=passwordReference)
passwordEntry.grid(row=2, column=2, padx=10, pady=5, sticky=W)

# Here is the value that we will be changed if the user's details are correct. In the program's current state,
# this does nothing and was initially implemented so I could keep track of whether or not the user had been
# authenticated. If this were to be elaborated on, the correct way to develop this would be to use an index
# value instead of setting the value permenantly each time.

Authenticated = False

# This is the beginning of the login function; we are declaring openMainWindow as the global function
# that we are using so that it can be called when the login is found to be correct. 

def login():
    
    global openMainWindow


# Defined here are the outputs for when the user submits their details through the later defined button. These will be compared with the values within the table.

    inputUsername = usernameEntry.get()
    inputPassword = passwordEntry.get()

# dbConfig encompasses the data relating to the SQL Connection. This includes the host, the login details and the name of the database.

    dbConfig = {
        "host": "localhost",
        "user": "root",
        "password": "root",
        "database": "thepasswordpastor"}

# conn uses the mysql.connector library to connect the Python code to the SQL Database that I have set up.
# It references the previously mentioned dbConfig so it can connect to the correct database. Without conn,
# the python program and SQL Database remain isolated from one another. The cursor is what utilises conn
# by allowing interaction. Using try for the statement allows for exceptions.

    try:
        conn = mysql.connector.connect(**dbConfig)
        cursor = conn.cursor()

# query is the variable that the mysql.connector will be using as the query when interacting with thepasswordpastor database. 
# Here, the query will search the database for data that matches the placeholders. The use of AND means that both username and password
# are considered within the search; returning the count for this means that a True or False value can be applied to the output

        query = """ SELECT COUNT(*) FROM login_details WHERE username = %s AND password = %s """

# cursor.execute() is what runs the the specified query when the program is run. The query will be run and will fill the placeholder variables with the username and password
# that the user has input. The except will classify the outliers and return errors to address them. Ordinary running of the program should execute the 
# query, and if the data is found, the count value is incremented by one, as is the global variable that will open the main program when it's value becomes True. 

        cursor.execute(query, (inputUsername, inputPassword))

        count = cursor.fetchone()[0]

        if count > 0:
            print("Found")
            Authenticated == True
            loginWindow.destroy()
            openMainWindow()

        else:
            print("Not Found")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

# The connection has to be closed after the query has been run, and the below code will do that. Failure to do so means that other cursors
# cannot be opened.

    conn.commit()
    conn.close()
    cursor.close()

# Here is the code detailing the login button itself; attached to this is the validation function. This means that when the window is pressed, the validation
# process will take place and the login window will destroy itself if the details are correct. 

submitLogin = Button(loginboxFrame, text="Submit\n Details", cursor = "crosshair", bd=2, height = 3, width = 10, bg="LightBlue1", relief="solid", command= lambda:login())
submitLogin.grid(row=4, columnspan=2, padx=5, pady=5,  sticky=N)

# This is the function that will open the main window for the program after the user has succesfully been able to login

def openMainWindow():

    # Global Variables are declared up here; these include the images for the clipboard and the logo.

    global logoInfo, resizedLogo, clipboardInfo, resizedClipboard


# This function would have adjusted the fonts that were seen on screen, however this method did not work as fonts implemented
# in other sections of the program would not change after this had been done.

    def changetoArial():

        global fontType

        fontType = ("Arial")
        selectedFont = (fontType, fontSize, "bold")
        mainWindowTitle.config(font=selectedFont)
        accessabilityButton.config(font=selectedFont)
        critiqueButton.config(font=selectedFont)       
        encryptionButton.config(font=selectedFont)
        storageButton.config(font=selectedFont)

# This function failed for the same reason as the previous.

    def changetoHelvetica():

        global fontType

        fontType = ("Comic Sans")
        selectedFont = (fontType, fontSize, "bold")
        mainWindowTitle.config(font=selectedFont)
        accessabilityButton.config(font=selectedFont)
        critiqueButton.config(font=selectedFont)       
        encryptionButton.config(font=selectedFont)
        storageButton.config(font=selectedFont) 

# This is redundant. Nothing is done with this variable and it can be deleted.

    fontSize = 10

    # In this section of the program, the main window is defined. Within this definition,
    # the window is first defined, the title is added, the geometry is specified, the minimum
    # sizing is specified too, and the background colour is in addition. The resizable function
    # has been implemented again so that the window can be reshaped. 

    mainWindow =Tk()
    mainWindow.title("The Password Pastor")
    mainWindow.geometry("1050x600")
    mainWindow.resizable(True, True)
    mainWindow.configure(background="LightBlue1")
    mainWindow.minsize(width=1050, height=600)

    # Frame and column weights are defined for the same reasons as before. The topbar frame is also defined here, and this is
    # what will contain the butttons and logo inside the main window. This will be present throughout the whole running of the
    # program.

    mainWindow.columnconfigure(0, weight=1)
    mainWindow.columnconfigure(1, weight=0)
    mainWindow.columnconfigure(2, weight=1)
    mainWindow.columnconfigure(4, weight=1)
    mainWindow.columnconfigure(5, weight=1)
    mainWindow.columnconfigure(6, weight=1)

    topbarFrame = Frame(mainWindow, bg='RoyalBlue1', relief="solid", borderwidth=3)
    topbarFrame.grid(row=0, column=0, columnspan=7, sticky=W+E)

    topbarFrame.columnconfigure(0, weight=1)
    topbarFrame.columnconfigure(1, weight=0)
    topbarFrame.columnconfigure(2, weight=1)
    topbarFrame.columnconfigure(3, weight=1)
    topbarFrame.columnconfigure(4, weight=1)
    topbarFrame.columnconfigure(5, weight=1)
    topbarFrame.columnconfigure(6, weight=1)

    # The first button defines the window name; this is not to be confused with the window title, seen in the taskbar. The second button is for the
    # accessability feature, the third is for the critique feature, the fourth is for the critique frature, and the fifth is for the storage feature.
    # The functions themselves are defined later in the code, and are bound to the button using lambda. This means that the function only runs once upon
    # the button press. 

    mainWindowTitle = Button(topbarFrame, text="The Password Pastor", height=5, width=20, bg="LightBlue1", relief="solid", borderwidth=2, font=defaultFont)
    mainWindowTitle.grid(row=0, column=2, padx=5, pady=5, sticky=W)

    accessabilityButton = Button(topbarFrame, text="Accessability", height=5, width=20, bg="White", relief="solid", borderwidth=2, font=defaultFont, command=lambda:openAccessability())
    accessabilityButton.grid(row=0, column=3, padx=5, pady=5, sticky=W)

    critiqueButton = Button(topbarFrame, text="Critique", height=5, width=20, bg="White", relief="solid", borderwidth=2, font=defaultFont, command=lambda:openCritique())
    critiqueButton.grid(row=0, column=4, padx=(5,5), pady=5, sticky=W)

    encryptionButton = Button(topbarFrame, text="Encryption", height=5, width=20, bg="White", relief="solid", borderwidth=2, font=defaultFont, command=lambda:openEncryption())
    encryptionButton.grid(row=0, column=5, padx=5, pady=5, sticky=W)

    storageButton = Button(topbarFrame, text="Storage", height=5, width=20, bg="White", relief="solid", borderwidth=2, font=defaultFont, command=lambda:openStorage())
    storageButton.grid(row=0, column=6, padx=(5,0), pady=5, sticky=W)

    logoInfo = ImageTk.PhotoImage(resizedLogo)
    finalLogo = Label(topbarFrame, image=logoInfo, borderwidth=3, relief="solid")
    finalLogo.grid(row = 0, column = 1, padx=5, pady=5, sticky=W+E)

    # Permenant frame definitions can be found here. These frames remain throughout the program's running, and house the clipboard feature and the window for
    # the other functions to output into. These do not change size.

    widgetFrame = Frame(mainWindow, bg="LightBlue1", height=400, width=1000)
    widgetFrame.grid(row=1, column=0, columnspan=7)

    functionFrame = Frame(widgetFrame, bg='white', relief='solid', borderwidth=3, height=455, width=650)
    functionFrame.grid_propagate(False)
    functionFrame.grid(row=1, column=1, columnspan=3, padx=0, pady=5, sticky=W+N)

    clipboardFrame = Frame(widgetFrame, bg='white', relief='solid', borderwidth=3, height=460, width=300)
    clipboardFrame.grid(row=1, column=6, padx=5, pady=5, sticky=E+N)

    clipboardFrame.columnconfigure(0, weight=1)
    clipboardFrame.columnconfigure(1, weight=1)

# This is yet another value that is not neccesary to the program's running and can be removed.

    submitted = False

# While I have managed to program in the wireframe for the accessability feature, I was not able to program the features.
# The failed attempts were functions further up in the code, and those can be deleted. This section can be dropped too
# provided that accessability wouldn't be developed further.

    def openAccessability():

        accessabilityFrame = Frame(widgetFrame, bg='white', relief='solid', borderwidth=3, height=455, width=650)
        accessabilityFrame.grid_propagate(False)
        accessabilityFrame.grid(row=1, column=1, padx=0, pady=5, sticky="nsew")

        accessabilityFrame.columnconfigure(0, weight=0)
        accessabilityFrame.columnconfigure(1, weight=1)
        accessabilityFrame.columnconfigure(2, weight=1)

        accessabilityFrame.rowconfigure(0, weight=0)
        accessabilityFrame.rowconfigure(1, weight=1)
        accessabilityFrame.rowconfigure(2, weight=1)
        accessabilityFrame.rowconfigure(3, weight=1)
        accessabilityFrame.rowconfigure(4, weight=0)

#

        textSizeFrame = Frame(accessabilityFrame, height=100, width=620, bg='RoyalBlue1', relief="solid", borderwidth=1, )
        textSizeFrame.grid(row=1,column=2, rowspan=1, columnspan=3, sticky=N, padx=10, pady=10)
        textSizeFrame.grid_propagate(False)

        textSizeFrame.columnconfigure(0, weight=0)
        textSizeFrame.columnconfigure(1, weight=1)
        textSizeFrame.columnconfigure(2, weight=1)
        textSizeFrame.columnconfigure(3, weight=1)
        textSizeFrame.columnconfigure(4, weight=1)
        
        sizeLabel = Label(textSizeFrame, bg='RoyalBlue1', fg="white", font=defaultFont2, text="Font Sizes:", height=2)
        sizeLabel.grid(row=1, column=0, padx=10, pady=5, sticky=N)

        fontSizeUp = Button(textSizeFrame, bg='white', height=5, width=20, relief="solid", text="Increase Font Size", bd=3)
        fontSizeUp.grid(row=1, column=3, padx=20, pady=5, sticky=E)

        fontSizeDown = Button(textSizeFrame, bg='white', height=5, width=20, relief="solid", text="Decrease Font Size", bd=3)
        fontSizeDown.grid(row=1, column=4, padx=20, pady=5, sticky=E)

#

        fontFrame = Frame(accessabilityFrame, height=100, width=620, bg='RoyalBlue1', relief="solid", borderwidth=1)
        fontFrame.grid(row=2,column=2, rowspan=1, columnspan=3, sticky=N, padx=10, pady=10)
        fontFrame.grid_propagate(False)

        fontFrame.columnconfigure(0, weight=0)
        fontFrame.columnconfigure(1, weight=1)
        fontFrame.columnconfigure(2, weight=1)
        fontFrame.columnconfigure(3, weight=1)
        fontFrame.columnconfigure(4, weight=1)

        fontLabel = Label(fontFrame, bg='RoyalBlue1', fg="white", font=defaultFont2, text="Font Types:", height=2)
        fontLabel.grid(row=1, column=0, padx=10, pady=5, sticky=N)
        
        arialSelect = Button(fontFrame, bg='white', height=5, width=20, relief="solid", text="Change to Arial", bd=3, command=lambda:changetoArial())
        arialSelect.grid(row=1, column=3, padx=20, pady=5, sticky=E)

        helveticaSelect = Button(fontFrame, bg='white', height=5, width=20, relief="solid", text="Change to Helvetica", bd=3, command=lambda:changetoHelvetica())
        helveticaSelect.grid(row=1, column=4, padx=20, pady=5, sticky=E)

#

        colourSchemeFrame = Frame(accessabilityFrame, height=100, width=620, bg='RoyalBlue1', relief="solid", borderwidth=1)
        colourSchemeFrame.grid(row=3,column=2, rowspan=1, columnspan=3, sticky=N, padx=10, pady=10)
        colourSchemeFrame.grid_propagate(False)

        colourSchemeFrame.columnconfigure(0, weight=0)
        colourSchemeFrame.columnconfigure(1, weight=1)
        colourSchemeFrame.columnconfigure(2, weight=1)
        colourSchemeFrame.columnconfigure(3, weight=1)
        colourSchemeFrame.columnconfigure(4, weight=1)

        colourSchemeLabel = Label(colourSchemeFrame, bg='RoyalBlue1', fg="white", font=defaultFont2, text="Colour Scheme:", height=2)
        colourSchemeLabel.grid(row=1, column=0, padx=10, pady=5, sticky=N)
        
        lightMode = Button(colourSchemeFrame, bg='white', height=5, width=20, relief="solid", text="Change to Light Mode", bd=3)
        lightMode.grid(row=1, column=3, padx=20, pady=5, sticky=E)

        darkMode = Button(colourSchemeFrame, bg='white', height=5, width=20, relief="solid", text="Change to Dark Mode", bd=3)
        darkMode.grid(row=1, column=4, padx=20, pady=5, sticky=E)

#

        saveChangesFrame = Frame(accessabilityFrame, bg='white', relief='solid', borderwidth=0, bd=2)
        saveChangesFrame.grid_propagate(True)
        saveChangesFrame.grid(row=4, column=1, columnspan=3, sticky="nsew")

        
        saveChanges = Button(saveChangesFrame, height=3, width=10, text="Save\nChanges ", bd=3)
        saveChanges.pack()

        def fontSize():
            print("s")

# Here is the function that will be bound to the clipboard's copy button. This works by retrieving the text entered and then 
# appending it to the clipboard using Tkinter's built in compatibility. The clipboard is first cleared so that no other content
# is pasted once the text is copied. After the functionality is defined, the button can be found below.

    def copy():     
            
        textToCopy = clipboardText.get("1.0", "end-1c")
        clipboardFrame.clipboard_clear()
        clipboardFrame.clipboard_append(textToCopy)
        
    clipboardText = Text(clipboardFrame, height=26, width=30)
    clipboardText.grid(row=1,column=1)

    clipboardInfo = ImageTk.PhotoImage(resizedClipboard)
    clipboardCopyButton = Button(clipboardFrame, image=clipboardInfo, borderwidth=0, command=lambda:copy())
    clipboardCopyButton.grid(row=0, column=2)

    def openCritique():

# For the critique function, a frame identical to the initial function frame is built in place of the old one, and this eradicates
# any conflicts that were present before. The input password feature takes up the entire frame so that the space is used optimally.
# The submit frame works in a similiar way to the topbar frame, and is placed at the bottom of the function frame when the input
# feature is still open.

        functionFrame.destroy
        
        functionFrame2 = Frame(widgetFrame, bg='white', relief='solid', borderwidth=3, height=455, width=650)
        functionFrame2.grid_propagate(False)
        functionFrame2.grid(row=1, column=1, columnspan=3, padx=0, pady=5, sticky=W+N)

        critiqueFrameIn = Frame(widgetFrame, bg='white', relief='solid', borderwidth=3, height=455, width=650)
        critiqueFrameIn.grid_propagate(False)
        critiqueFrameIn.grid(row=1, column=1, padx=0, pady=5, sticky="nsew")

        inputPassword = Text(critiqueFrameIn)
        inputPassword.grid(row=1, column=1, rowspan=5, columnspan=3, sticky="nsew")

        submitFrame = Frame(critiqueFrameIn, bg='white', relief='solid', borderwidth=0, bd=2)
        submitFrame.grid_propagate(True)
        submitFrame.grid(row=6, column=1, columnspan=3, sticky="nsew")

        submitPassword = Button(submitFrame, height=3, width=10, text="Submit", bd=3, command=lambda:passwordCheck())
        submitPassword.pack()


        def passwordCheck():

            passwordToCheck = inputPassword.get("1.0", "end-1c")

            critiqueFrameIn.destroy()

            critiqueFrameOut = Frame((functionFrame2), bg='white', relief='solid')
            critiqueFrameOut.grid_propagate(False)
            critiqueFrameOut.grid(row=1, column=1, padx=0, pady=5, sticky="nsew")

# Here, the special symbols are defined for the critique system. These will be referenced when the special characters function
# is run during the checking process.

            SpecialSym =['$', '@', '#', '%', '!', '|','#','.',"?"]
            val = True

            # The password too short check uses the len() function to check how long the password is. If the character length is under or equal to 5,
            # the function will recognise that the password is too short and highlight that to the user

            if len(passwordToCheck) <= 5:
                a = "Your password length should be 6 long at the very least..."
                Label(critiqueFrameOut, text=a, borderwidth=2, font=defaultFont, relief="solid").pack(padx=5, pady=5, anchor="e")
                val = False

            # The password too long check uses the len() function in conjunction with the greater than operator. If the given value is above or equal to
            # 20 characters, a message is shown to the user informing them to make their password shorter

            if len(passwordToCheck) >= 20:
                b = "\n This password is too long. How are you supposed to remember this? "
                Label(critiqueFrameOut, text=b,font=defaultFont, borderwidth=2, relief="solid").pack(padx=5, pady=5, anchor="e")
                val = False
            
            # The number check uses the isdigit function to check for numbers within the passwordToCheck string. isdigit looks at each character in the string
            # and as implied by the name, can deduce whether or not a character is a number or not, and this is done through a linear search. If there is no
            # number, the function will return the statement telling the user to add one, and concatenate 123 onto the password input
        
            if not any(char.isdigit() for char in passwordToCheck):
                c = "Your password should have at least one number. Try " + passwordToCheck + "123"
                Label(critiqueFrameOut, text=c,font=defaultFont, borderwidth=2, relief="solid").pack(padx=5, pady=5, anchor="e")
                val = False

            # This password check will capitalise the first letter of the given password and create the capitalPassword variable. This will be added to the 
            # recommendation if there is not an uppercase character detected within the string given by the user
            
            capitalPassword = passwordToCheck.capitalize()  

            if not any(char.isupper() for char in passwordToCheck):
                d = "Your password should have at least one uppercase letter. Try " + capitalPassword
                Label(critiqueFrameOut, text=d,font=defaultFont, borderwidth=2, relief="solid").pack(padx=5, pady=5, anchor="e")
                val = False


            # This check loops through the string and checks each character to see if a lowercase character appears. This improvement does not give a suggestion
            # but will still be shown with the rest of the improvements

            if not any(char.islower() for char in passwordToCheck):
                e = "Your password should have at least one lowercase letter."
                Label(critiqueFrameOut, text=e,font=defaultFont, borderwidth=2, relief="solid").pack(padx=5, pady=5, anchor="e")
                val = False

            # This check references the special characters seen earlier in the program code. If any of the characters contained within the special characters list
            # are not found within the password given by the user, an exclamation mark will be appended onto the user's password. Checking for this special character
            # is done using the same linear search as the other checks
                    
            if not any(char in SpecialSym for char in passwordToCheck):
                f = "Your password should have at least one of the symbols: $@#%!|?. Try " + passwordToCheck + "!"
                Label(critiqueFrameOut, text=f,font=defaultFont, borderwidth=2, relief="solid").pack(padx=5, pady=5, anchor="e")
                val = False

            # This if statement considers the results of all the checks that have taken place. For the previous statements, if the improvement needs to be suggested, 
            # that means that the value returned is False. This means that all the values are returned to the user that have come back false, and this creates the 
            # messages within the window

            if val:
                return val


    def openEncryption():

        # Here is the frame that is gridded inside the function frame when the encryption feature is opened. Creation of a new frame reduces the amount
        # of conflicts within the program. Akin to the other functions within the program, the rows and columns need to be configured first. 

        encryptionFrame = Frame(widgetFrame, bg='white', relief='solid', borderwidth=3, height=455, width=650)
        encryptionFrame.grid_propagate(False)
        encryptionFrame.grid(row=1, column=1, padx=0, pady=5, sticky="nsew")

        encryptionFrame.columnconfigure(0, weight=0)
        encryptionFrame.columnconfigure(1, weight=1)
        encryptionFrame.columnconfigure(2, weight=1)

        encryptionFrame.rowconfigure(0, weight=0)
        encryptionFrame.rowconfigure(1, weight=1)
        encryptionFrame.rowconfigure(2, weight=1)
        encryptionFrame.rowconfigure(3, weight=1)
        encryptionFrame.rowconfigure(4, weight=0)

        # Here is the code relevant to the password input feature for the user. This section below contains the frame, label and text input.

        inputPasswordFrame = Frame(encryptionFrame, height=100, width=620, bg='RoyalBlue1', relief="solid", borderwidth=1)
        inputPasswordFrame.grid(row=1,column=2, rowspan=1, columnspan=3, sticky=N, padx=10, pady=10)
        inputPasswordFrame.grid_propagate(False)

        inputPasswordFrame.columnconfigure(0, weight=0)
        inputPasswordFrame.columnconfigure(1, weight=1)
        inputPasswordFrame.columnconfigure(2, weight=1)
        inputPasswordFrame.columnconfigure(3, weight=1)
        inputPasswordFrame.columnconfigure(4, weight=1)

        inputPasswordFrame.rowconfigure(0, weight=0)
        inputPasswordFrame.rowconfigure(1, weight=1)
        inputPasswordFrame.rowconfigure(2, weight=1)

        inputPasswordLabel = Label(inputPasswordFrame, bg='RoyalBlue1', fg="white", font=defaultFont2, text="Enter your Password:")
        inputPasswordLabel.grid(row=1, column=1, rowspan=2, padx=10, pady=5, sticky="nsew")

        # StringVar ensures data is valid

        passwordReference = StringVar()

        passwordEntry = Entry(inputPasswordFrame, textvariable=passwordReference, font=defaultFont2, width=30)
        passwordEntry.grid(row=1, column=2, rowspan=2, padx=10, pady=5, sticky="nsew")

        # Here is the code relevant to the key input feature for the user. This section below contains the frame, label and text input.

        inputKeyFrame = Frame(encryptionFrame, height=100, width=620, bg='RoyalBlue1', relief="solid", borderwidth=1)
        inputKeyFrame.grid(row=2,column=2, rowspan=1, columnspan=3, sticky=N, padx=10, pady=10)
        inputKeyFrame.grid_propagate(False)

        inputKeyFrame.columnconfigure(0, weight=0)
        inputKeyFrame.columnconfigure(1, weight=1)
        inputKeyFrame.columnconfigure(2, weight=1)
        inputKeyFrame.columnconfigure(3, weight=1)
        inputKeyFrame.columnconfigure(4, weight=1)

        inputKeyFrame.rowconfigure(0, weight=0)
        inputKeyFrame.rowconfigure(1, weight=1)
        inputKeyFrame.rowconfigure(2, weight=1)

        inputKeyLabel = Label(inputKeyFrame, bg='RoyalBlue1', fg="white", font=defaultFont2, text="Enter your Custom Key:")
        inputKeyLabel.grid(row=1, column=1, rowspan=2, padx=10, pady=5, sticky="nsew")

        # StringVar ensures data is valid

        keyReference = StringVar()

        keyEntry = Entry(inputKeyFrame, textvariable=keyReference, font=defaultFont2, width=30)
        keyEntry.grid(row=1, column=2, rowspan=2, padx=10, pady=5, sticky="nsew")

        # Here is the code relevant to the output encrypted password. A placeholder is present until the password is output, and this 
        # means that the container doesn't change size when the encrypted password is output into the cell. 

        outputPasswordOuterFrame = Frame(encryptionFrame, height=100, width=620, bg='RoyalBlue1', relief="solid", borderwidth=1)
        outputPasswordOuterFrame.grid(row=3,column=2, rowspan=1, columnspan=3, sticky=N, padx=10, pady=10)
        outputPasswordOuterFrame.grid_propagate(False)

        outputPasswordOuterFrame.columnconfigure(0, weight=0)
        outputPasswordOuterFrame.columnconfigure(1, weight=1)
        outputPasswordOuterFrame.columnconfigure(2, weight=1)
        outputPasswordOuterFrame.columnconfigure(3, weight=1)
        outputPasswordOuterFrame.columnconfigure(4, weight=0)

        outputPasswordOuterFrame.rowconfigure(0, weight=0)
        outputPasswordOuterFrame.rowconfigure(1, weight=1)
        outputPasswordOuterFrame.rowconfigure(2, weight=1)

        outputPasswordLabel = Label(outputPasswordOuterFrame, bg='RoyalBlue1', fg="white", font=defaultFont2, text="Your Encrypted Password:")
        outputPasswordLabel.grid(row=1, column=1, rowspan=2, padx=10, pady=5, sticky=N+S+W)



        outputPasswordInnerFrame = Frame(outputPasswordOuterFrame, width=30)
        outputPasswordInnerFrame.grid(row=1, column=2, rowspan=2, columnspan=3, padx=(0, 25), pady=5, sticky="nsew")
        
        outputPasswordFiller = Label(outputPasswordInnerFrame, width=28, text="        ", fg="black")
        outputPasswordFiller.grid(row=1, column=1, rowspan=2, columnspan=2, sticky="nsew")
        
        outputPasswordInnerFrame.columnconfigure(0, weight=1)
        outputPasswordInnerFrame.columnconfigure(1, weight=1)

        # The code presented here is the submit button for the user's password so that they are able to encrypt it

        saveFrame = Frame(encryptionFrame, height=75, bg='white', relief='solid', borderwidth=0, bd=2)
        saveFrame.grid_propagate(True)
        saveFrame.grid(row=4, column=1, columnspan=3, sticky="nsew", pady=(20,0))

        submitPassword = Button(saveFrame, height=3, width=10, text="Submit", bd=3, command=lambda:encrypt())
        submitPassword.pack()

        # Here is the encryption function that is run when the submit button, seen above, is pressed. When this function is run, the password 
        # and key are input as placeholders for the encryption algorithm. The two results are joined together in a string, the characters are 
        # reordered multiple times and then converted into base64. The placeholder is then destroyed and the output password is put in it's 
        # place

        def encrypt():

            inputPassword = passwordReference.get()
            inputKey = keyReference.get()

            preEncrypt = ''.join(chr(ord(char) ^ ord(key_char)) for char, key_char in zip(inputPassword, inputKey))
            postEncrypt = preEncrypt.encode()
            postEncrypt64 = base64.b64encode(postEncrypt).decode('utf-8')

            print("Encrypted Password is:", postEncrypt64)

            outputPasswordFiller.destroy()

            outputPassword = Label(outputPasswordInnerFrame, text=postEncrypt64, font=defaultFont2, width=28, fg="black")
            outputPassword.grid(row=1, column=1, rowspan=1, columnspan=2, pady=(30,0), sticky=W)


    def openStorage():

        # This is the frame that will be created inside of the function frame. Columnn and row weights are defined again. 

        storageFrame = Frame(widgetFrame, bg='white', relief='solid', borderwidth=3, height=455, width=650)
        storageFrame.grid_propagate(False)
        storageFrame.grid(row=1, column=1, padx=0, pady=5, sticky="nsew")

        storageFrame.columnconfigure(0, weight=0)
        storageFrame.columnconfigure(1, weight=1)
        storageFrame.columnconfigure(2, weight=1)

        storageFrame.rowconfigure(0, weight=0)
        storageFrame.rowconfigure(1, weight=1)
        storageFrame.rowconfigure(2, weight=1)
        storageFrame.rowconfigure(3, weight=1)
        storageFrame.rowconfigure(4, weight=0)

        # The select options section below is what allows the user to switch in between saving their passwords and retrieving their
        # passwords. The Save button and Retrieve button run the functions that build their respective function interfaces; 

        selectOptions = Frame(storageFrame, height=100, width=620, bg='RoyalBlue1', relief="solid", borderwidth=1)
        selectOptions.grid(row=1,column=2, rowspan=1, columnspan=3, sticky=N, padx=10, pady=10)
        selectOptions.grid_propagate(False)

        selectOptions.columnconfigure(0, weight=0)
        selectOptions.columnconfigure(1, weight=1)
        selectOptions.columnconfigure(2, weight=1)
        selectOptions.columnconfigure(3, weight=1)
        selectOptions.columnconfigure(4, weight=1)

        SROptionsLabel = Label(selectOptions, bg='RoyalBlue1', fg="white", font=defaultFont2, text="Select Option:", height=2)
        SROptionsLabel.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        SavePasswordSelect = Button(selectOptions, bg='white', height=5, width=20, relief="solid", text="Save Password", bd=3, command=lambda:switchToSave())
        SavePasswordSelect.grid(row=1, column=3, padx=20, pady=5, sticky=E)

        RetrievePasswordSelect = Button(selectOptions, bg='white', height=5, width=20, relief="solid", text="Retrieve Password", bd=3, command=lambda:switchToRetrieval())
        RetrievePasswordSelect.grid(row=1, column=4, padx=20, pady=5, sticky=E)

        # Defined below is the first input for the retrieval process. This is referenced in both Save and Retrieve. It is important 
        # to note that this reference remains even if it is the value being input is the service relating to the password

        inputPasswordFrame = Frame(storageFrame, height=100, width=620, bg='RoyalBlue1', relief="solid", borderwidth=1)
        inputPasswordFrame.grid(row=2,column=2, rowspan=1, columnspan=3, sticky=N, padx=10, pady=10)
        inputPasswordFrame.grid_propagate(False)

        inputPasswordFrame.columnconfigure(0, weight=0)
        inputPasswordFrame.columnconfigure(1, weight=1)
        inputPasswordFrame.columnconfigure(2, weight=1)
        inputPasswordFrame.columnconfigure(3, weight=1)
        inputPasswordFrame.columnconfigure(4, weight=1)

        inputPasswordFrame.rowconfigure(0, weight=0)
        inputPasswordFrame.rowconfigure(1, weight=1)
        inputPasswordFrame.rowconfigure(2, weight=1)

        inputPasswordLabel = Label(inputPasswordFrame, bg='RoyalBlue1', fg="white", font=defaultFont2, text="Enter your Password:")
        inputPasswordLabel.grid(row=1, column=1, rowspan=2, padx=10, pady=5, sticky="nsew")

        # Validation

        passwordReference = StringVar()

        passwordEntry = Entry(inputPasswordFrame, textvariable=passwordReference, font=defaultFont2, width=30)
        passwordEntry.grid(row=1, column=2, rowspan=2, padx=10, pady=5, sticky="nsew")

        # Defined below is the password output space; this is where the retrieved data will be placed once the query has been run.
        # An index value is used to deviate between Retrieval and Saved, meaning that conflicts are not created when building the
        # new widgets

        outputPasswordOuterFrame = Frame(storageFrame, height=100, width=620, bg='RoyalBlue1', relief="solid", borderwidth=1)
        outputPasswordOuterFrame.grid(row=3,column=2, rowspan=1, columnspan=3, sticky=N, padx=10, pady=10)
        outputPasswordOuterFrame.grid_propagate(False)

        outputPasswordOuterFrame.columnconfigure(0, weight=0)
        outputPasswordOuterFrame.columnconfigure(1, weight=1)
        outputPasswordOuterFrame.columnconfigure(2, weight=1)
        outputPasswordOuterFrame.columnconfigure(3, weight=1)
        outputPasswordOuterFrame.columnconfigure(4, weight=0)

        outputPasswordOuterFrame.rowconfigure(0, weight=0)
        outputPasswordOuterFrame.rowconfigure(1, weight=1)
        outputPasswordOuterFrame.rowconfigure(2, weight=1)

        outputPasswordLabel = Label(outputPasswordOuterFrame, bg='RoyalBlue1', fg="white", font=defaultFont2, text="Your Password is:")
        outputPasswordLabel.grid(row=1, column=1, rowspan=2, padx=10, pady=5, sticky=N+S+W)

        outputPasswordInnerFrame = Frame(outputPasswordOuterFrame, width=30)
        outputPasswordInnerFrame.grid(row=1, column=2, rowspan=2, columnspan=3, padx=(0, 25), pady=5, sticky="nsew")

        outputPasswordInnerFrame.columnconfigure(0, weight=0)
        outputPasswordInnerFrame.columnconfigure(1, weight=1)

        outputPasswordFiller = Label(outputPasswordInnerFrame, width=28, fg="black")
        outputPasswordFiller.grid(row=1, column=1, rowspan=3, columnspan=1, sticky="nsew")

        # Save Button

        saveFrame = Frame(storageFrame, height=75, bg='white', relief='solid', borderwidth=0, bd=2)
        saveFrame.grid_propagate(True)
        saveFrame.grid(row=4, column=1, columnspan=3, sticky="nsew", pady=(20,0))

        submitPassword = Button(saveFrame, height=3, width=10, text="Submit", bd=3)
        submitPassword.pack()

        Retrieval = {"value": False}


        # This function is what is run to change the input fields to suit the retrieval process. This is done using config
        # so they can be edited while the window is running. Nested within this function is the retrieve password function,
        # and this gets the user's input and checks the database for if the service has a connected password login. This is
        # printed to the command line and then output in the corresponding cell in the Tkinter window 

        def switchToRetrieval():

            submitPassword.destroy()

            Retrieval["value"] == False

            inputPasswordLabel.config(text="Enter your Service:")
            outputPasswordLabel.config(text="Your Password is:")

            retrievePassword = Button(saveFrame, height=3, width=10, text="Retrieve", bd=3, command=lambda:retrievePassword())
            retrievePassword.pack()

            def retrievePassword():

                inputService = passwordReference.get()


                dbConfig = {"host": "localhost",
                            "user": "root",
                            "password": "root",
                            "database": "thepasswordpastor"}
               
                try:
                    conn = mysql.connector.connect(**dbConfig)
                    cursor = conn.cursor()

                    retrieveQuery = """ SELECT servicePassword FROM password_storage WHERE serviceName = %s """ 
                    
                    cursor.execute(retrieveQuery, (inputService,))
                    result = cursor.fetchone()
                    print(result)

                    outputPasswordFiller.destroy()

                    outputPassword = Label(outputPasswordInnerFrame, text=result, font=defaultFont2, width=28, fg="black")
                    outputPassword.grid(row=1, column=1, rowspan=1, columnspan=2, pady=(30,0), sticky=S)

                   


                except mysql.connector.Error as err:
                    print(f"Error: {err}")

                conn.commit()
                conn.close()
                cursor.close()


 

        # Akin to the retrieve feature, this function reconfigures the input boxes so the user can save a password. Embedded within this 
        # function is the save password function, and this works by inserting the data taken from the input into a new record within the
        # table. The input data is the service and password, and this should be retrieved if these values are input into the retrieve
        # function.  

        def switchToSave():

            nonlocal Retrieval

            inputPasswordLabel.configure(text="Enter your Password:")
            outputPasswordLabel.configure(text="Enter the Relevant Service:")

            outputPasswordInnerFrame.destroy()

            submitPassword.destroy()

            serviceReference = StringVar()

            serviceEntry = Entry(outputPasswordOuterFrame, textvariable=serviceReference, font=defaultFont2, width=30)
            serviceEntry.grid(row=1, column=2, rowspan=2, padx=10, pady=5, sticky="nsew")

            savePassword = Button(saveFrame, height=3, width=10, text="Submit", bd=3, command=lambda:savePassword())
            savePassword.pack()

            Retrieval["value"] == True

            def savePassword():


                dbConfig = {"host": "localhost",
                    "user": "root",
                    "password": "root",
                    "database": "thepasswordpastor"}
                
                inputService = serviceReference.get()
                inputPassword = passwordReference.get()

                try:
                    conn = mysql.connector.connect(**dbConfig)
                    cursor = conn.cursor()

                    query = """ INSERT INTO password_storage (serviceName, servicePassword) VALUES (%s, %s) """
                    
                    cursor.execute(query, (inputService, inputPassword))

                except mysql.connector.Error as err:
                    print(f"Error: {err}")

                conn.commit()
                conn.close()
                cursor.close()
            
loginWindow.mainloop()