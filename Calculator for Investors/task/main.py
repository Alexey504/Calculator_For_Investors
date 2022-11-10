import csv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, MetaData, Table
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Query
import os


Base = declarative_base()


class Companies(Base):
    __tablename__ = 'companies'

    ticker = Column(String, primary_key=True)
    name = Column(String)
    sector = Column(String)


class Financial(Base):
    __tablename__ = 'financial'

    ticker = Column(String, primary_key=True)
    ebitda = Column(Float)
    sales = Column(Float)
    net_profit = Column(Float)
    market_price = Column(Float)
    net_debt = Column(Float)
    assets = Column(Float)
    equity = Column(Float)
    cash_equivalents = Column(Float)
    liabilities = Column(Float)


def first_step():
    print("Not implemented!")


def exit_():
    print("Have a nice day!")


def company_options():
    ticker = input("Enter ticker (in the format 'MOON'):\n")
    name = input("Enter company (in the format 'Moon Corp'):\n")
    sector = input("Enter industries (in the format 'Technology'):\n")
    ebitda = float(input("Enter ebitda (in the format '987654321'):\n"))
    sales = float(input("Enter sales (in the format '987654321'):\n"))
    net_profit = float(input("Enter net profit (in the format '987654321'):\n"))
    market_price = float(input("Enter market price (in the format '987654321'):\n"))
    net_debt = float(input("Enter net debt (in the format '987654321'):\n"))
    assets = float(input("Enter assets (in the format '987654321'):\n"))
    equity = float(input("Enter equity (in the format '987654321'):\n"))
    cash_equivalents = float(input("Enter cash equivalents (in the format '987654321'):\n"))
    liabilities = float(input("Enter liabilities (in the format '987654321'):\n"))
    return ticker, name, sector, ebitda, sales, net_profit,\
           market_price, net_debt, assets, equity, cash_equivalents, liabilities


def update_options():
    ebitda = float(input("Enter ebitda (in the format '987654321'):\n"))
    sales = float(input("Enter sales (in the format '987654321'):\n"))
    net_profit = float(input("Enter net profit (in the format '987654321'):\n"))
    market_price = float(input("Enter market price (in the format '987654321'):\n"))
    net_debt = float(input("Enter net debt (in the format '987654321'):\n"))
    assets = float(input("Enter assets (in the format '987654321'):\n"))
    equity = float(input("Enter equity (in the format '987654321'):\n"))
    cash_equivalents = float(input("Enter cash equivalents (in the format '987654321'):\n"))
    liabilities = float(input("Enter liabilities (in the format '987654321'):\n"))
    return ebitda, sales, net_profit, market_price, net_debt, assets, equity, cash_equivalents, liabilities


def create_company():

    engine = create_engine('sqlite:///investor.db')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()

    ticker, name, sector, ebitda, sales, net_profit, \
    market_price, net_debt, assets, equity, cash_equivalents, liabilities = company_options()

    session.add(Companies(ticker=ticker, name=name, sector=sector))
    session.add(Financial(ticker=ticker, ebitda=ebitda, sales=sales, net_profit=net_profit, market_price=market_price,
                          net_debt=net_debt, assets=assets, equity=equity, cash_equivalents=cash_equivalents,
                          liabilities=liabilities))
    session.commit()
    print('Company created successfully!')


def read_company():

    engine = create_engine('sqlite:///investor.db')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()

    user_input_name = input("Enter company name:\n")
    query = Query(Companies, session)
    query_fin = Query(Financial, session)

    list_companies = {}
    cnt = 0

    def division(a, b):
        if a is None or b is None:
            return
        return round(a / b, 2)

    for row in query.filter(Companies.name.contains(user_input_name)):
        list_companies[cnt] = row.name
        cnt += 1
    if not list_companies:
        print("Company not found!")
    else:
        for i, comp in list_companies.items():
            print(i, comp)
        user_input_number = int(input("Enter company number:\n"))
        company_name = list_companies[user_input_number]
        for row in query.filter(Companies.name == company_name):
            tk = row.ticker
            print(row.ticker, row.name)
        for cmp in query_fin.filter(Financial.ticker == tk):

            pe = division(cmp.market_price, cmp.net_profit)
            ps = division(cmp.market_price, cmp.sales)
            pb = division(cmp.market_price, cmp.assets)
            ne = division(cmp.net_debt, cmp.ebitda)
            roe = division(cmp.net_profit, cmp.equity)
            roa = division(cmp.net_profit, cmp.assets)
            la = division(cmp.liabilities, cmp.assets)

            print(f'P/E = {pe}\nP/S = {ps}\nP/B = {pb}\nND/EBITDA = {ne}\nROE = {roe}\nROA = {roa}\nL/A = {la}\n')


def update_company():
    engine = create_engine('sqlite:///investor.db')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()

    user_input_name = input("Enter company name:\n")

    query = Query(Companies, session)
    query_fin = Query(Financial, session)

    list_companies = {}
    cnt = 0

    for row in query.filter(Companies.name.contains(user_input_name)):
        list_companies[cnt] = row.name
        cnt += 1
    if not list_companies:
        print("Company not found!")
    else:
        for i, comp in list_companies.items():
            print(i, comp)
        user_input_number = int(input("Enter company number:\n"))
        company_name = list_companies[user_input_number]
        for row in query.filter(Companies.name == company_name):
            tk = row.ticker
        comp_filter = query_fin.filter(Financial.ticker == tk)
        ebitda, sales, net_profit, \
        market_price, net_debt, assets, equity, cash_equivalents, liabilities = update_options()

        comp_filter.update({
            "ebitda": ebitda,
            "sales": sales,
            "net_profit": net_profit,
            "market_price": market_price,
            "net_debt": net_debt,
            "assets": assets,
            "equity": equity,
            "cash_equivalents": cash_equivalents,
            "liabilities": liabilities
        })
        session.commit()

        print("Company updated successfully!")


def delete_company():
    engine = create_engine('sqlite:///investor.db')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()

    user_input_name = input("Enter company name:\n")
    query = Query(Companies, session)
    query_fin = Query(Financial, session)

    list_companies = {}
    cnt = 0

    for row in query.filter(Companies.name.contains(user_input_name)):
        list_companies[cnt] = row.name
        cnt += 1
    if not list_companies:
        print("Company not found!")
    else:
        for i, comp in list_companies.items():
            print(i, comp)

        user_input_number = int(input("Enter company number:\n"))
        company_name = list_companies[user_input_number]
        for row in query.filter(Companies.name == company_name):
            tk = row.ticker

        query.filter(Companies.name == company_name).delete()
        query_fin.filter(Financial.ticker == tk).delete()
        session.commit()

        print("Company deleted successfully!")


def list_companies():
    engine = create_engine('sqlite:///investor.db')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()

    query = Query(Companies, session)
    all_rows = query.all()

    comp_list = []
    print("COMPANY LIST")
    for row in all_rows:
        comp_list.append((row.ticker, row.name, row.sector))
    comp_list.sort(key=lambda x: x[0])
    for c in comp_list:
        print(*c)


def top_ten_ne():
    engine = create_engine('sqlite:///investor.db')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()

    query_fin = session.query(Financial.ticker, Financial.net_debt, Financial.ebitda)
    list = []
    for t, nd, e in query_fin.filter(Financial.net_debt, Financial.ebitda):
        list.append((t, round(nd / e, 2)))
    list.sort(key=lambda x: x[1], reverse=True)
    print("TICKER ND/EBITDA")
    for pair in list[:10]:
        print(*pair)


def top_ten_roe():
    engine = create_engine('sqlite:///investor.db')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()

    query_fin = session.query(Financial.ticker, Financial.net_profit, Financial.equity)
    list = []
    for t, np, e in query_fin.filter(Financial.net_profit, Financial.equity):
        list.append((t, round(np / e, 2)))
    list.sort(key=lambda x: x[1], reverse=True)
    print("TICKER ROE")
    for pair in list[:10]:
        print(*pair)


def top_ten_roa():
    engine = create_engine('sqlite:///investor.db')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()

    query_fin = session.query(Financial.ticker, Financial.net_profit, Financial.assets)
    list = []
    for t, np, a in query_fin.filter(Financial.net_profit, Financial.assets):
        list.append((t, round(np / a, 2)))
    list.sort(key=lambda x: x[1], reverse=True)
    print("TICKER ROA")
    for pair in list[:10]:
        print(*pair)


def main():
    main_menu = {1: lambda: crud_menu, 2: lambda: top_ten_menu}
    crud_menu = {0: lambda: main_menu, 1: create_company, 2: read_company, 3: update_company,
                 4: delete_company, 5: list_companies}
    top_ten_menu = {0: lambda: main_menu, 1: top_ten_ne, 2: top_ten_roe, 3: top_ten_roa}

    def display_menu(menu, num):
        return menu.get(num)

    main_menu_message = "MAIN MENU\n0 Exit\n1 CRUD operations\n2 Show top ten companies by criteria"
    crud_menu_message = "CRUD MENU\n0 Back\n1 Create a company\n2 Read a company\n3 Update a company\n4 Delete a " \
                        "company\n5 List all companies "
    top_ten_menu_message = "TOP TEN MENU\n0 Back\n1 List by ND/EBITDA\n2 List by ROE\n3 List by ROA"

    print("Welcome to the Investor Program!")
    running = True
    menu_text = main_menu_message
    menu = main_menu
    while running:

        if menu == crud_menu:
            menu_text = crud_menu_message
        elif menu == top_ten_menu:
            menu_text = top_ten_menu_message
        print(menu_text)
        print()

        user_input = input("Enter an option:\n")

        if menu == main_menu and user_input == '0':
            print("Have a nice day!")
            return
        if not user_input.isdigit() or int(user_input) not in menu:
            print("Invalid option!")
            menu = main_menu
            menu_text = main_menu_message
        else:
            if menu == main_menu:
                menu = display_menu(menu, int(user_input))()
            else:
                display_menu(menu, int(user_input))()
                menu = main_menu
                menu_text = main_menu_message
        print()


def create_db():

    engine = create_engine('sqlite:///investor.db')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()

    with open("companies.csv") as companies:
        companies_reader = csv.DictReader(companies, delimiter=",")
        for line in companies_reader:
            for k, v in line.items():
                if not v:
                    line[k] = None
            session.add(Companies(**line))
            session.commit()

    with open("financial.csv") as finance:
        finance_reader = csv.DictReader(finance, delimiter=",")
        for line in finance_reader:
            for k, v in line.items():
                if not v:
                    line[k] = None
            session.add(Financial(**line))
            session.commit()

    # print("Database created successfully!")


if __name__ == "__main__":
    if not os.path.isfile("investor.db"):
        create_db()
    main()
