import win32com.client
import pandas as pd

att1 = 'C:/Users/zacharywe/Documents/T&C/AH4R - Terms and Conditions Addendum to Real Estate Purchase Agreement 08.09.2021.docx'
att2 = 'C:/Users/zacharywe/Documents/T&C/Atlas - Terms and Conditions Addendum to Real Estate Purchase Agreement 6.3.21.docx'
att3 = 'C:/Users/zacharywe/Documents/T&C/Divvy - Terms and Conditions Addendum to Real Estate Purchase Agreement 5.25.21.docx'
att4 = 'C:/Users/zacharywe/Documents/T&C/Tricon - Terms and Conditions Addendum to Real Estate Purchase Agreement 10.30.2019.docx'
att5 = 'C:/Users/zacharywe/Documents/T&C/Hudson Homes - Terms and Conditions Addendum to Real Estate Purchase Agreement 2.16.21.docx'
att6 = 'C:/Users/zacharywe/Documents/T&C/Invitation Homes - Terms and Conditions Addendum to Real Estate Purchase Agreement [12.8.2020].docx'
att7 = 'C:/Users/zacharywe/Documents/T&C/MCH - Terms and Conditions Addendum to Real Estate Purchase Agreement 06.16.2021.docx'
att8 = 'C:/Users/zacharywe/Documents/T&C/Open House - Terms and Conditions Addendum to Real Estate Purchase Agreement [05.25.21].docx'
att9 = 'C:/Users/zacharywe/Documents/T&C/Progress - Terms and Conditions Addendum to Real Estate Purchase Agreement [12.11.20].docx'
att10 = 'C:/Users/zacharywe/Documents/T&C/Second Avenue - Terms and Conditions Addendum to Real Estate Purchase Agreement 4.12.21.docx'
att11 = 'C:/Users/zacharywe/Documents/T&C/Sparrow - Terms and Conditions Addendum to Real Estate Purchase Agreement 5.25.21.docx'
att12 = 'C:/Users/zacharywe/Documents/T&C/Sylvan Road - Terms and Conditions Addendum to Real Estate Purchase Agreement 03.27.20 .docx'
att13 = 'C:/Users/zacharywe/Documents/T&C/Starwood (Tiber) - Terms and Conditions Addendum to Real Estate Purchase Agreement 12.14.21 [Georgia, North Carolina, Florida, Tennessee].docx'
att14 = 'C:/Users/zacharywe/Documents/T&C/Starwood (Roofstock) - Terms and Conditions Addendum to Resale Agreement 12.14.21 [Texas, Nevada, Colorado].docx'
att15 = 'C:/Users/zacharywe/Documents/T&C/Westport Capital - Terms and Conditions to Real Estate Purchase Agreement 12.12.21.docx'

file = pd.ExcelFile('MCH_011022.xlsx')
df = file.parse('Summary')

for index, row in df.iterrows(): 
    email = (row['Email Addresses']) 
    cc = (row['CC'])
    subject = (row['Subject'])
    body = (row['Email HTML Body']) 
    buyer = (row['Buyer']) 
    
    if (pd.isnull(email) or pd.isnull(subject) or pd.isnull(body)): 
        continue
    
    olMailItem = 0x0 
    obj = win32com.client.Dispatch("Outlook.Application") 
    newMail = obj.CreateItem(olMailItem) 
    newMail.Subject = subject 
    newMail.GetInspector 
    newMail.body = body 

    for j in df.iteritems():
        if str(row['Buyer']) == 'AH4R':
            newMail.Attachments.Add(att1)
            break
        if str(row['Buyer']) == 'Atlas':
            newMail.Attachments.Add(att2)
            break
        if str(row['Buyer']) == 'Divvy':
            newMail.Attachments.Add(att3)
            break
        if str(row['Buyer']) == 'Tricon':
            newMail.Attachments.Add(att4)
            break
        if str(row['Buyer']) == 'Hudson Homes':
            newMail.Attachments.Add(att5)
            break
        if str(row['Buyer']) == 'Invitation':
            newMail.Attachments.Add(att6)
            break
        if str(row['Buyer']) == "MCH":
            newMail.Attachments.Add(att7)
            break
        if str(row['Buyer']) == "Open House":
            newMail.Attachments.Add(att8)
            break
        if (str(row['Buyer']) == "Progress" or str(row['Buyer']) == "Cerberus"):
            newMail.Attachments.Add(att9)
            break
        if str(row['Buyer']) == "Second Avenue":
            newMail.Attachments.Add(att10)
            break
        if str(row['Buyer']) == "Sparrow":
            newMail.Attachments.Add(att11)
            break   
        if str(row['Buyer']) == "Sylvan Road":
            newMail.Attachments.Add(att12)
            break
        if str(row['Buyer']) == "Starwood":
            newMail.Attachments.Add(att13)
            break
        if str(row['Buyer']) == "Starwood (Roofstock)":
            newMail.Attachments.Add(att14)
            break
        if str(row['Buyer']) == "Westport Capital":
            newMail.Attachments.Add(att15)
            break
        
    newMail.To = email 
    newMail.CC = cc
    newMail.display()
    newMail.send()
