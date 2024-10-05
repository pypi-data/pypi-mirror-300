# Python interface for invoice generation
Simple utility for PDF invoice generation in Python

## Setup
1. Install the module
2. Copy ```config/config.example.yaml``` from the repository to ```config/config.yaml``` and update parameter values as desired
3. Optionally configure terms by creating a ```translations/terms.[language].yaml``` file, check out the example file ```config/terms.example.yaml```

## Usage
1. Generate an invoice object eg. ```invoice = Invoice(invoice_id, invoice_date <YY-mm-dd>, customer_id, customer_name, customer_address, customer_postal_code, customer_city, customer_country, customer_vat_registered_number, vat_percentage)```
2. Set article lines by using the ```set_articles()``` method on the invoice object. Example ```[{'name': 'Pizza margherita', 'price': 9.99, 'amount': 1}, {'name': 'Pizza fungi', 'price': 11.99, 'amount': 1}]```
3. Generate an InvoicePDF object eg. ```pdf = InvoicePDF(invoice <the invoice object>, invoice_language <the desired print language>)```
4. Generate the PDF by running the ```generate_document()``` method on the invoicepdf object

## Translations
Translations can be overwritten by copying the translation file into /translations folder

## Contribution
Feel free or make proposals for code contributions and the addition of translation files for additional language support in this repository

## Credits
Big thanks to Pluralsight (https://www.pluralsight.com) and Chart Explorers (https://www.youtube.com/@ChartExplorers) for the detailed descriptions on working with the used techniques