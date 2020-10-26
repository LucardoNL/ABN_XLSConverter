import pandas as pd
import os

def main():
    for file in os.listdir('./files te converteren/'):
        if file.endswith(".xls"):
            file = ('./files te converteren/' + file)
            excel = pd.read_excel(file)

            excel.Transactiedatum = pd.to_datetime(excel.Transactiedatum, format='%Y%m%d')
            excel.Transactiedatum = excel.Transactiedatum.dt.strftime('%d/%m/%Y')

            excel['Memo'] = excel['Omschrijving']
            excel = excel[['Transactiedatum', 'Omschrijving', 'Memo', 'Transactiebedrag']]

            BEA = excel.Omschrijving.str.startswith('BEA')
            SEPA = excel.Omschrijving.str.startswith('SEPA')
            TRTP = excel.Omschrijving.str.startswith('/TRTP')
            excel.Omschrijving[BEA] = excel.Omschrijving[BEA].str[33:60]
            excel.Omschrijving[SEPA] = excel.Omschrijving[SEPA].str.split('Naam: ').str[1]
            excel.Omschrijving[SEPA] = excel.Omschrijving[SEPA].str.split('Omschrijving: ').str[0]
            excel.Omschrijving[TRTP] = excel.Omschrijving[TRTP].str.split('NAME/').str[1]
            excel.Omschrijving[TRTP] = excel.Omschrijving[TRTP].str.split('/').str[0]
            print(excel['Omschrijving'].head)

            excel.rename(columns = {'Transactiedatum' : 'Date', 'Omschrijving' : 'Payee', 'Transactiebedrag' : 'Amount'}, inplace = True)
            excel.to_csv(file[:-4] + '.csv', index=False)

main()