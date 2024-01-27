# BizCardX-Extracting-Business-Card-Data-with-OCR
This project aimed to develop a Streamlit application that allows users to upload an image of a business card and extract relevant information from it using EasyOCR and the extracted information had to save into a database along with the uploaded business card image, and require to make changes in database data as required.

## About EasyOCR
In today's fast-paced business environment, efficiently managing and organizing contact information is crucial for successful networking and communication. With the advent of digital tools and technologies, manual entry of business card details into a database can be time-consuming and prone to errors. To overcome these challenges, developers can leverage the power of optical character recognition (OCR) and databases to automate the process of extracting relevant information from business cards and storing it for easy access.

One powerful OCR library that facilitates the extraction of text from images is EasyOCR. EasyOCR is an open-source Python library that utilizes deep learning models to accurately recognize and extract text from various languages. By integrating EasyOCR with a PostgreSQL database, developers can streamline the process of capturing business card data and storing it in a structured and organized manner.

- The dependencies on the EasyOCR package are minimal, making it easy to configure your OCR development environment.
- The EasyOCR package can be installed with a single pip command.
- Once EasyOCR is installed, only one import statement is required to import the package into your project.
- From there, all you need is two lines of code to perform OCR — one to initialize the Reader class and then another to OCR the image via the readtext function.

## About Project
This project is a user-friendly tool for extracting information from business cards. The tool uses OCR technology to recognize text on business cards and extracts the data into a SQL database after classification using regular expressions. Users can access the extracted information using a GUI built using streamlit. The BizCardX application is a simple and intuitive user interface that guides users through the process of uploading the business card image and extracting its information. The extracted information would be displayed in a clean and organized manner, and users would be able to easily add it to the database with the click of a button in streamlit UI. Further the data stored in database can be easily read, updated and deleted by user as per the requirement from streamlit UI.

## Technologies Used
1. Streamlit GUI : Framework for creating interactive web applications with Python.
2. EasyOCR : Python library for optical character recognition.
3. PostgreSQL : Database management system for storing extracted business card information.
4. Pandas : To Create a DataFrame with the scraped data
5. OpenCV as CV2 : It is library used for processing image
6. Matplotlib.pyplot : It is the library used for displaying images using plot
7. Regular expressions : It is the library used to search the required texts.

## Workflow

- Install the required libraries Python, Streamlit, EasyOCR, and a database system like PostgreSQL using the pip install command.
  
- Design a user-friendly interface with Streamlit allowing users to upload business card images and extract their information using widgets like file uploaders and buttons, I have created the app with three menu options namely HOME, UPLOAD & EXTRACT, Alter or delete where user has the option to upload the respective Business Card whose information has to be extracted, stored, updated or deleted if needed.
  
- Once user uploads a business card, the text present in the card is extracted by easyocr library.
  
- The extracted text is sent to get_data() function for respective text classification as company name, card holder name, designation, mobile number, email address, website URL, area, city, state, and pin code using loops and some regular expression.
  
- Presenting the extracted information in a structured manner within the Streamlit GUI using tables, text boxes, and labels.
  
- On Clicking Upload to Database Button the data gets stored in the PostgreSQL Database.
  
- Further with the help of Alter or Delete menu the uploaded data’s in SQL Database can be accessed for Read, Update and Delete Operations.

## Result
The final application will be a Streamlit-based tool that allows users to upload business card images and extract relevant information using easyOCR. Extracted details will include company name, cardholder name, designation, contact information, and address details, displayed in an organized manner within the application's GUI.

Users can store this extracted information in a database along with the uploaded images. The database can manage multiple entries, providing a repository for efficiently managing business card information.

Overall, this application is designed to efficiently manage business card information, serving the needs of both businesses and individuals.
