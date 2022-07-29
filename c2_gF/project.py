from tabulate import tabulate
import time
from copy import deepcopy
import requests
import matplotlib.pyplot as plt


# Done By Tan Xin Yu
def importFile():
    file = open("portfolioStock.csv", "r")
    Fileread = file.readlines()
    Stocklist = []
    Stocks = []

    for i in Fileread:  # removes \n in lists
        element = str(i)
        lineremoval = element.replace("\n", "")
        Stocklist.append(lineremoval)

    for x in Stocklist:  # converts from a list into a 2D list
        y = x.split(",")
        Stocks.append(y)

    file.close()
    return Stocks


dataArray = importFile()
headersArray = dataArray[0]


# Done by John Gabriel : Function Used to validate any numerical inputs
def numericalInputValidation(prompt):

    while True:
        value = input(prompt)

        try:
            value = int(value)

            if value < 0:
                print("Value should be more than 0! Try Again! ")
                continue
            else:
                return value

        except:
            print("Value should be an integer")


# Done by John Gabriel : Function Used to validate any company name inputs
def nameValidation(prompt):

    namesArray = []

    for data in dataArray[1:]:
        namesArray.append(data[0])

    while True:
        companyName = input(prompt)

        if companyName not in namesArray:
            return companyName
        else:
            print("Company Name already taken! Try Again!")


# Done by John Gabriel : Function Used to validate any capitalisation inputs
def capitalizationValidation(prompt):
    while True:
        marketCapitalization = input(prompt)

        if (marketCapitalization == "Mega" or marketCapitalization == "Large" or marketCapitalization == "Mid"):
            return marketCapitalization
        else:
            print("Invalid market capitalization! Try Again!")


# Done by John Gabriel : Function USed to validate any choice related inputs
def choiceValidation(prompt, lowerLimit, upperLimit):

    while True:
        choice = input(prompt)

        if choice == "E" or choice == "e":
            return choice
        else:
            try:
                choice = int(choice)

                if choice < lowerLimit or choice > upperLimit:
                    print("Error! Integer entered exceeds the choice range!")
                else:
                    return int(choice)
            except ValueError:
                print("Error! Input should be an integer")


# Function done by John Gabriel : To choose the company they want to either edit or delete
def chooseCompany():
    print("No - Company")
    print("----------------------------")

    for i in range(1, len(dataArray)):
        print(i, " - ", dataArray[i][0])

    print("----------------------------")

    maxIndex = len(dataArray) - 1
    choice = choiceValidation(
        f"Enter 0 to {maxIndex} for your selection or E to exit: ", 0, maxIndex)

    return choice


# Done by Tan Xin Yu
def displayStocks():

    displayHeadersArray = ["No"] + dataArray[0]

    print(tabulate(dataArray[1:], headers=displayHeadersArray,
          showindex=range(1, len(dataArray)), tablefmt="fancy_grid"))


# Done by John Gabriel
def addStock():

    companyName = nameValidation("Enter Company Name: ")
    marketCapitalization = capitalizationValidation(
        "Enter market capitalization of company: Mega, Large or Mid: ")

    qty = numericalInputValidation("Enter Number of Stock Bought = ")
    boughtPrice = numericalInputValidation("Enter Price of Stock Bought = ")
    marketPrice = numericalInputValidation("Enter Market Price of Stock = ")

    dataArray.append([companyName,
                     marketCapitalization, str(qty), str(boughtPrice), str(marketPrice)])


# Done by Tan Xin Yu
def updateStock(companyNo):

    company = dataArray[companyNo]

    print("Index:".ljust(20), companyNo)

    for i in range(len(company)):
        print(f"{i + 1}. {headersArray[i]}:".ljust(20), company[i])
    print("E. Edit Completed. Exit")

    choice = choiceValidation("What do you want to edit or E to exit: ", 1, 5)

    if choice == "E" or choice == "e":
        print("Returning to Main Menu")
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


# Done By John Gabriel
def removeStock(companyNo):
    dataArray.pop(companyNo)

    print(f"Removed {dataArray[companyNo - 1][0]}....")


# Done By John Gabriel
def portfolioStatementCalculation():
    tempArray = deepcopy(dataArray)
    tempHeadersArray = ['No'] + tempArray[0]
    tempHeadersArray.extend(["Total Invested", "Invested Portfolio Size",
                             "Total Market Value", "Profit/Loss", "Market Portfolio Size"])

    totalInvestmentValue = 0
    totalMarketValue = 0
    totalProfit = 0

    for company in tempArray[1:]:
        qty = float(company[2])
        boughtPrice = float(company[3])
        marketPrice = float(company[4])

        profit = (marketPrice - boughtPrice)

        totalInvestmentValue += boughtPrice * qty
        totalMarketValue += marketPrice * qty
        totalProfit += profit * qty

    for company in tempArray[1:]:

        qty = float(company[2])
        boughtPrice = float(company[3])
        marketPrice = float(company[4])

        totalInvested = qty * boughtPrice
        investedPortfolioSize = round(
            totalInvested / totalInvestmentValue * 100)

        totalMarket = qty * marketPrice
        marketPortfolioSize = round(totalMarket / totalMarketValue * 100)

        profit = (marketPrice - boughtPrice) * qty

        company.extend([totalInvested, investedPortfolioSize,
                       totalMarket, profit, marketPortfolioSize])

    return tempArray, tempHeadersArray, totalInvestmentValue, totalMarketValue, totalProfit


# Done By John Gabriel
def portfolioStatement():

    tempArray, tempHeadersArray, totalInvestmentValue, totalMarketValue, totalProfit = portfolioStatementCalculation()
    print(tabulate(tempArray[1:],
          headers=tempHeadersArray, showindex=range(1, len(dataArray)), tablefmt="fancy_grid"))
    print("Total Invested: ", totalInvestmentValue)
    print("Total Market Value: ", totalMarketValue)
    print("Total Profit: ", totalProfit)


# Done By John Gabriel
def exportFile():

    with open("portfolioStock.csv", "w") as file:
        for line in dataArray:
            combinedString = ",".join(line) + "\n"
            file.write(combinedString)

    print("Exported 2D List to portfolioStock.csv! ")


# Done By John Gabriel to look up the stock using the IEX API
def lookUpStock():

    print("------ Look up a stock from the IEX API ------")

    stock = input("Type in the symbol of the stock you want to look up: ")

    try:
        iex_api_key = 'pk_d2cf149ae68b4b748b6dbf4723c2019a'
        api_url = f'https://cloud.iexapis.com/stable/stock/{stock}/quote?token={iex_api_key}'

        # Extracting data from the IEX API: https://medium.com/codex/pulling-stock-data-from-iex-cloud-with-python-d44f63bb82e0
        # Thsi stores data in an form of json: JavaScript Object Notation, similar to a dictionary in python
        api_data = requests.get(api_url).json()

        # Obtain the companyName and the lastestPrice key from the json or dictionary obtained
        companyName = api_data['companyName']
        latestPrice = api_data['latestPrice']

        print(f"The share of {companyName} is ${latestPrice}")
        isBuying = input(
            "Do you want to buy the stock? Type Y for yes or N for No: ")

        if (isBuying.upper() == 'Y'):
            addStock()
        else:
            print("Exiting Look Up Stock...")

    # This error runs when stock does not exist when findingg the stock symbol in the API
    except requests.exceptions.JSONDecodeError:
        print("Stock does not exist")


def portfolioDistribution():

    tempArray, tempHeadersArray, totalInvestmentValue, totalMarketValue, totalProfit = portfolioStatementCalculation()

    investedArray = []
    marketArray = []
    companyArray = []

    for data in tempArray[1:]:
        companyArray.append(data[0])
        investedArray.append(data[6])
        marketArray.append(data[9])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(
        10, 10))  # ax1,ax2 refer to your two pies
    # Pie Chart
    ax1.pie(investedArray, labels=companyArray,
            autopct='%1.1f%%', pctdistance=0.85)
    ax1.set_title('Invested Stock Distribution')
    ax2.pie(marketArray, labels=companyArray,
            autopct='%1.1f%%', pctdistance=0.85)
    ax2.set_title('Market Stock Distribution')

    plt.show()


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
    print("8. Proposed Function - View Portfolio Distribution     - (by student 1)")
    print("9. Proposed Function - Look Up Stock from IEX API      - (by student 2)")
    print("E. Exit Main Menu")
    print("-----------------------------------------------------------------------")

    choice = choiceValidation("    Select an option: ", 1, 9)

    if choice == "E" or choice == "e":
        print("Exiting program...")
        break
    elif choice == 1:
        displayStocks()
    elif choice == 2:
        addStock()
    elif choice == 3:
        companyNo = chooseCompany()
        if companyNo == "E" or companyNo == "e":
            continue
        updateStock(companyNo)
    elif choice == 4:
        companyNo = chooseCompany()
        if companyNo == "E" or companyNo == "e":
            continue
        removeStock(companyNo)
    elif choice == 5:
        portfolioStatement()
    elif choice == 6:
        importFile()
    elif choice == 7:
        exportFile()
    elif choice == 8:
        portfolioDistribution()
    elif choice == 9:
        lookUpStock()

    # Pause the program for 2 seconds before looping again
    time.sleep(2)