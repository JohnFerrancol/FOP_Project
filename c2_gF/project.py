from tabulate import tabulate
import time
from copy import deepcopy
import requests


# Done By Tan Xin Yu: Used to import the data from the csv file and store it a s a 2D Listz
def importFile():
    file = open("portfolioStock.csv", "r")
    fileRead = file.readlines()
    stockList = []
    stocks = []

    for i in fileRead:
        element = str(i)
        # Removes the \n from the element
        lineremoval = element.replace("\n", "")
        stockList.append(lineremoval)
    for x in stockList:
        # For each string, x,  in the stockList, convert the string into a list
        y = x.split(",")
        stocks.append(y)

    file.close()
    return stocks


dataArray = importFile()


# Done by John Gabriel : Function Used to validate any numerical inputs
def numericalInputValidation(prompt):

    while True:

        # The user will input something using the prompt given in the parameter
        value = input(prompt)

        try:

            # Try to convert the value into an integer
            value = int(value)

            # If the value given is negative, throw an error to the user
            if value < 0:
                print("Value should be more than 0! Try Again! ")
                continue

            # If there is no error, return the value
            else:
                return value

        # If the value is unable to be turned into an integer, throw an error
        except:
            print("Value should be an integer!")


# Done by John Gabriel : Function Used to validate any company name inputs
def nameValidation(prompt):

    namesArray = []

    # Add all of the company names inside the namesArray
    for data in dataArray[1:]:
        namesArray.append(data[0])

    while True:

        # The user will input something using the prompt given in the parameter
        companyName = input(prompt)

        # If the company name is not inside dataArray, return the companyName
        if companyName not in namesArray:
            return companyName

        # Else, throw an error
        else:
            print("Company Name already taken! Try Again!")


# Done by John Gabriel : Function Used to validate any capitalisation inputs
def capitalizationValidation(prompt):

    while True:

        # The user will input something using the prompt given in the parameter
        marketCapitalization = input(prompt)

        # If the input is either of the following, return the input value
        if (marketCapitalization == "Mega" or marketCapitalization == "Large" or marketCapitalization == "Mid"):
            return marketCapitalization

        # Else, throw an error
        else:
            print("Invalid market capitalization! Try Again!")


# Done by John Gabriel : Function USed to validate any choice related inputs
def choiceValidation(prompt, lowerLimit, upperLimit):

    while True:

        # The user will input something using the prompt given in the parameter
        choice = input(prompt)

        if choice == "E" or choice == "e":
            return choice
        else:
            try:

                # Try to convert the input value to an integer
                choice = int(choice)

                # If the choice variable is out the range, where range is defined from the lowerLimit and upperLimit parameters, throw an error
                if choice < lowerLimit or choice > upperLimit:
                    print("Error! Integer entered exceeds the choice range!")

                # Else, return the value
                else:
                    return int(choice)

             # If the value is unable to be turned into an integer, throw an error
            except ValueError:
                print("Error! Input should be an integer")


# Done by Tan Xin Yu: Used to display all of the stocks in the csv file
def displayStocks():

    print("    ----------------------- Display Stocks -----------------------")
    displayHeadersArray = ["No"] + dataArray[0]

    # Tabulate is used to present tabular data
    # Using tabulate function: https://pypi.org/project/tabulate/
    print(tabulate(dataArray[1:], headers=displayHeadersArray,
          showindex=range(1, len(dataArray)), tablefmt="fancy_grid"))


# Done by John Gabriel: Used to add a stock into the data 2D List
def addStock():

    print("    ----------------------- Add Stocks -----------------------")

    # Call the various input validation functions to validate the inputs given by the user and obtain the values returned from the following function
    companyName = nameValidation("Enter Company Name: ")
    marketCapitalization = capitalizationValidation(
        "Enter market capitalization of company: Mega, Large or Mid: ")
    qty = numericalInputValidation("Enter Number of Stock Bought = ")
    boughtPrice = numericalInputValidation("Enter Price of Stock Bought = ")
    marketPrice = numericalInputValidation("Enter Market Price of Stock = ")

    # Append the new company added to the dataArray 2D List
    dataArray.append([companyName,
                     marketCapitalization, str(qty), str(boughtPrice), str(marketPrice)])

    # Display to the user that the stock has been added to the data 2D List
    print()
    print(
        f"----------------------- Added {companyName} Successfully -----------------------")


# Function done by John Gabriel : To choose the company they want to either edit or delete
def chooseCompany():

    print("    ----------------------- Choose Company -----------------------")
    print("No - Company")
    print("----------------------------")

    # Iterate over the dataArray List, skipping over the header which is the first list in the 2D List and display all of the companies and their following indexes
    for i in range(1, len(dataArray)):
        print(i, " - ", dataArray[i][0])

    print("----------------------------")

    maxIndex = len(dataArray) - 1

    # Call the choice validation function with the maxIndex and 0 as the upperLimit and lowerLimit parameters repectively
    choice = choiceValidation(
        f"Enter 1 to {maxIndex} for your selection or E to exit: ", 1, maxIndex)

    # Return the index of the company from the dataArray
    return choice


# Done by Tan Xin Yu: Used to update an information about the stock that the user chose from the chooseCompany function
def updateStock(companyNo):

    print("    ----------------------- Update Stocks -----------------------")

    # Get the company from their index
    company = dataArray[companyNo]

    # Obtain the header of the csv file
    headersArray = dataArray[0]

    # ljust is to give n spaces to the left of the string, where n is the argument that needs to be inputed
    # ljust method : https://www.w3schools.com/python/ref_string_ljust.asp
    print("Index:".ljust(20), companyNo)

    # Iterate over the company and show the information of the company, its name, capitalisation, qty, bought and market price
    for i in range(len(company)):
        print(f"{i + 1}. {headersArray[i]}:".ljust(20), company[i])
    print("E. Edit Completed. Exit")

    # Call the choice validation function with 1 and 5 being the lowerLimit and upperLimit respectively
    choice = choiceValidation("What do you want to edit or E to exit: ", 1, 5)

    print()
    if choice == "E" or choice == "e":
        print("Returning to Main Menu...")

    # Prompt the user for the new information about the stock and update accordingly
    # Call the respective validation input functions
    # We -1 to the index for each information as the choice given is not the index of the information in the dataArray
    elif choice == 1:
        newName = nameValidation("(1) Enter new Company Name: ")
        company[choice - 1] = newName
    elif choice == 2:
        newCapitalization = capitalizationValidation(
            "(2) Enter new Capitalization: ")
        company[choice - 1] = newCapitalization
    else:
        newValue = numericalInputValidation(
            f"({choice}) Enter new {headersArray[choice - 1]} : ")
        company[choice - 1] = str(newValue)

    print()
    print(
        f"----------------------- Updated {company[0]} Successfully -----------------------")


# Done By John Gabriel: Used to remove the stock the user chose from the chooseCompany function from the dataArray 2D List
def removeStock(companyNo):

    # Obtain the name of the company before removing it
    companyName = dataArray[companyNo][0]

    # Remove the company from the dataArray by using the pop method, which gets the index of the company in the dataArray
    dataArray.pop(companyNo)

    print(
        f"---------------------- Removed {companyName} Successfully -----------------------")


# Done By John Gabriel: Used to display the following portfolio statement required
def portfolioStatement():

    # Deepcopy is used to create a copy of the dataArray in a seperate location in memory
    tempArray = deepcopy(dataArray)

    # Create a new headersArray and extend the headersArray with additional headers and remove capitalization from headersArray
    tempHeadersArray = ['No'] + tempArray[0]
    tempHeadersArray.extend(["Total Invested", "Invested Portfolio Size",
                             "Total Market Value", "Profit/Loss", "Market Portfolio Size"])
    tempHeadersArray.remove("Capitalization")

    totalInvestmentValue = 0
    totalMarketValue = 0
    totalProfit = 0

    # Iterate over the temporary data array, skipping the header and calculate the totalInvestmentValue, totalMarketValue and totalProfit
    for company in tempArray[1:]:

        # Obtain the qty, boughtPrice and marketPrice of the follwing stock/ company
        qty = float(company[2])
        boughtPrice = float(company[3])
        marketPrice = float(company[4])

        # Calculate the profit
        profit = (marketPrice - boughtPrice)

        # Increment the totalInvestmentValue, totalMarketValue and totalProfit accordingly
        totalInvestmentValue += boughtPrice * qty
        totalMarketValue += marketPrice * qty
        totalProfit += profit * qty

    # Iterate over the temporary data array, skipping the header and calculate the investedPortfolioSize, marketPortfolioSize, profit
    for company in tempArray[1:]:

        qty = float(company[2])
        boughtPrice = float(company[3])
        marketPrice = float(company[4])

        # Calculate the following investedPortfolioSize
        totalInvested = qty * boughtPrice
        investedPortfolioSize = round(
            totalInvested / totalInvestmentValue * 100)

        # Calculate the following marketPortfolioSize
        totalMarket = qty * marketPrice
        marketPortfolioSize = round(totalMarket / totalMarketValue * 100)

        profit = (marketPrice - boughtPrice) * qty

        # Append the following details to the respective company
        company.extend([totalInvested, investedPortfolioSize,
                       totalMarket, profit, marketPortfolioSize])

        # Remove the capitalization as it is not needed for the portfolio statement
        company.remove(company[1])

    print("----------------------- Portfolio Statement -----------------------".rjust(110))

    # Tabulate the following data into the table, display the total invested, total market value and total profit
    print(tabulate(tempArray[1:],
          headers=tempHeadersArray, showindex=range(1, len(dataArray)), tablefmt="fancy_grid"))
    print("Total Invested: ", totalInvestmentValue)
    print("Total Market Value: ", totalMarketValue)
    print("Total Profit: ", totalProfit)


# Done By John Gabriel: Used to export the the dataArray 2D List to csv file
def exportFile():

    with open("portfolioStock.csv", "w") as file:

        # Iterate over the dataArray
        for line in dataArray:

            # For each list in the 2D List, use the join method to join the list into a string with commas seperating them
            # Join method python: https://www.w3schools.com/python/ref_string_join.asp
            combinedString = ",".join(line) + "\n"
            file.write(combinedString)

    print()
    print("---------------------- Exported 2D List to portfolioStock.csv! ----------------------")


# Done By Tan Xin Yu: Function used to get customer feedback
def feedbackForm():

    file = open('feedback.txt', 'a')

    # Call the choice validation function with 1 and 5 as the lowerLimit and upperLimit respectively
    programAccessibility = choiceValidation(
        "On a scale of 1 to 5 (1=Very Difficult, 5=Very Easy), please rate your difficulty of navigating this program : ", 1, 5)
    satisfactoryLevel = choiceValidation(
        "On a scale of 1 to 5 (1=Least Satisfactory, 5=Most Satisfactory), please rate your satisfactory level with this program : ", 1, 5)

    # Prompt user for program strengths, weaknesses and improvements
    programStrengths = input("What do you like about this program? :\n")
    programWeaknesses = input("What do you dislike about this program? :\n")
    programImprovements = input(
        "What do you think can be improved for this program? :\n")

    print()
    print("----Thank you for your time in filling up the feedback form! We hope that you have a nice day!----")

    feedback = [str(satisfactoryLevel), str(programAccessibility),
                programStrengths, programWeaknesses, programImprovements]

    # Combine the feedback list into a comma-separated string
    combinedString = ",".join(feedback) + "\n"
    file.write(combinedString)

    file.close()


# Done By John Gabriel: Look up the stock using the IEX API
def lookUpStock():

    print("    ----------------------- Look up Stocks -----------------------")

    stock = input("Type in the symbol of the stock you want to look up: ")

    try:
        iexApiKey = 'pk_d2cf149ae68b4b748b6dbf4723c2019a'
        apiUrl = f'https://cloud.iexapis.com/stable/stock/{stock}/quote?token={iexApiKey}'

        # Extracting data from the IEX API: https://medium.com/codex/pulling-stock-data-from-iex-cloud-with-python-d44f63bb82e0
        # This stores data in an form of json: JavaScript Object Notation, similar to a dictionary in python
        apiData = requests.get(apiUrl).json()

        # Obtain the companyName and the lastestPrice key from the json or dictionary obtained
        companyName = apiData['companyName']
        latestPrice = apiData['latestPrice']

        # Prompt the user if they want to add the following stock
        print(f"The share of {companyName} is ${latestPrice}")
        isBuying = input(
            "Do you want to add the stock? Type Y for yes or N for No: ")

        print()

        # If the user wants to add the stock, redirect them to the addStock function
        if (isBuying.upper() == 'Y'):
            addStock()

        # Else, exit the function to the main menu
        else:
            print(
                "---------------------- Exiting Look Up Stock ----------------------")

    # This error runs when stock does not exist when findingg the stock symbol in the API
    except requests.exceptions.JSONDecodeError:
        print()
        print("---------------------- Stock does not exist ----------------------")


# Display the main menu as well as run one of the following functions chosen by the user for each iteration of the loop until an 'e' or 'E' has been inputted by the user
while True:
    print("=======================================================================")
    print(" Class    SN      Student Name")
    print("=======  ====    ===============================")
    print("  02      01      John Gabriel Gamoba Ferrancol")
    print("          11      Tan Xin Yu")
    print("-----------------------------------------------------------------------")
    print("          Portfolio Application Main Menu")
    print("-----------------------------------------------------------------------")
    print("1. Display All Stocks")
    print("2. Add Stock")
    print("3. Update Stock")
    print("4. Remove Stock")
    print("5. Portfolio Statement")
    print("6. Import portfolio file (csv/txt) into 2D List Stocks - (by student 1)")
    print("7. Export 2D List Stocks to portfolio file (csv/txt)   - (by student 2)")
    print("8. Proposed Function - Feedback form                   - (by student 1)")
    print("9. Proposed Function - Look Up Stock from IEX API      - (by student 2)")
    print("E. Exit Main Menu")
    print("-----------------------------------------------------------------------")

    # Prompt the user which function they want to run from the program
    # Call the choiceValidation function to validate the input of the user, with 1 and 9 being the lowerLimit and upperLimit respectively
    choice = choiceValidation("    Select an option: ", 1, 9)

    print()

    # Run the following function depending on what the user inputs as the choice
    if choice == "E" or choice == "e":
        print("Exiting program...")
        break
    elif choice == 1:
        displayStocks()
    elif choice == 2:
        addStock()
    elif choice == 3:
        # Run the chooseCompany to allow the user to choose the company he/she wants to edit
        companyNo = chooseCompany()
        print()

        # If the user chooses to exit the function, continue to the top of the while loop
        if companyNo == "E" or companyNo == "e":
            continue

        # Run the updateStock function with the index of the company in the dataArray they want to update as the argument
        updateStock(companyNo)
    elif choice == 4:
        # Run the chooseCompany to allow the user to choose the company he/she wants to edit
        companyNo = chooseCompany()
        print()

        # If the user chooses to exit the function, continue to the top of the while loop
        if companyNo == "E" or companyNo == "e":
            continue

        # Run the removeStock function with the index of the company in the dataArray they want to remove as the argument
        removeStock(companyNo)
    elif choice == 5:
        portfolioStatement()
    elif choice == 6:
        importFile()
    elif choice == 7:
        exportFile()
    elif choice == 8:
        feedbackForm()
    elif choice == 9:
        lookUpStock()

    # Pause the program for 2 seconds before looping again
    print()
    time.sleep(2)


