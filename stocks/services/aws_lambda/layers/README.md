# BeautifulSoup and Requests - AWS Lambda Layers

This repository contains pre-packaged Python dependencies to be used as AWS Lambda Layers. These layers provide the libraries **BeautifulSoup4 (bs4)** and **requests** for web scraping and HTTP requests, respectively.

## **What Are Lambda Layers?**

AWS Lambda Layers allow you to externalize dependencies, making your Lambda functions lightweight and faster to deploy.

## **Dependencies Included**

### **1. BeautifulSoup4 (bs4)**

- **Purpose**: Parses and extracts data from HTML or XML documents.
- **Usage**:
  - Web scraping
  - Processing HTML content efficiently

### **2. Requests**

- **Purpose**: Simplifies making HTTP requests in Python.
- **Usage**:
  - Fetching data from APIs
  - Making GET, POST, and other HTTP requests


## **Lambdas Using These Layers**

### **1. marketwatch_data Lambda**
- **Description**: Scrapes performance data and competitors' information for a given stock symbol from MarketWatch.
- **Libraries Used**:
  - `requests`: For fetching HTML content.
  - `BeautifulSoup4`: For parsing and extracting the required data from the MarketWatch page.

### **2. polygon_data Lambda**
- **Description**: Get Stock values from the Polygon API for a given stock symbol and date.
- **Libraries Used**:
  - `requests`: For fetching HTML content.
