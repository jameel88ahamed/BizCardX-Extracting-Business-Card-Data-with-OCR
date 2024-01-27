import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import easyocr
import psycopg2
import os
import cv2
import matplotlib.pyplot as plt
import re
import pandas as pd

# SETTING PAGE CONFIGURATIONS
icon = Image.open("icon.png")
st.set_page_config(page_title= "BizCardX: Extracting Business Card Data with OCR | By Jameel",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This Application is created by *Jameel*!"""})
st.markdown("<h1 style='text-align: center; color: #BDF2B2;'>BizCardX: Extracting Business Card Data with OCR</h1>", unsafe_allow_html=True)

# SETTING-UP BACKGROUND IMAGE
def setting_bg():
    st.markdown(f""" <style>.stApp {{
                        background: url("https://th.bing.com/th/id/OIP.o4K4kMt9ZR5-ezi3ps3eDAHaEK?w=289&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7");
                        background-size: cover}}
                     </style>""",unsafe_allow_html=True) 
    
setting_bg()

# CREATING OPTION MENU
with st.sidebar:
    Option = option_menu(None, ["Home","Upload & Extract","Alter or Delete"], 
                        icons=["house","cloud-upload","pencil-square"],
                        default_index=0,
                        styles={"nav-link": {"font-size": "30px", "text-align": "centre", "margin": "0px", "--hover-color": "#404A52"},
                                "icon": {"font-size": "25px"},
                                "container" : {"max-width": "3000px"},
                                "nav-link-selected": {"background-color": "#1D4445"}})
    
# INITIALIZING THE EasyOCR READER
reader = easyocr.Reader(['en'])

#CONNECTING WITH POSTGRESQL DATABASE
mydb = psycopg2.connect(
                        host='localhost',
                        user='postgres',
                        password='Enter your password',
                        database='Bizcardx',
                        port='5432'
)
cursor = mydb.cursor()

# TABLE CREATION
create_query = '''CREATE TABLE IF NOT EXISTS Cards_Data (
                                                        id SERIAL PRIMARY KEY,
                                                        company_name text,
                                                        card_holder text,
                                                        designation text,
                                                        mobile_number Varchar(50),
                                                        email text,
                                                        website text,
                                                        area text,
                                                        city text,
                                                        state text,
                                                        pin_code Varchar(10),
                                                        image BYTEA
                                                    )'''

cursor.execute(create_query)
mydb.commit()

#FUNCTION FOR SAVING CARD TO FILE FOLDER
def save_card(card):
    with open(os.path.join('uploaded_cards', card.name), "wb") as f:
        f.write(card.getbuffer())

#FUNCTION FOR SHOWING THE GRAPHICAL REPRESENTATION OF EXTRACTED IMAGE DETAILS ON IMAGE
def image_text(image,res):
    for(bbox, text, prob) in res:
        #unpacking the bounding box
        (tl, tr, br, bl)=bbox
        tl=(int(tl[0]), int(tl[1]))
        tr=(int(tr[0]), int(tr[1]))
        br=(int(br[0]), int(br[1]))
        bl=(int(bl[0]), int(bl[1]))
        cv2.rectangle(image, tl, br, (255,0,0),2) #Forming Rectangle box to write texts
        cv2.putText(image, text, (tl[0], tl[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,28),2)
        plt.rcParams['figure.figsize']=(15,15)
        plt.axis('off')
        plt.imshow(image)

#FUNCTION FOR CONVERTING IMAGE TO BINARY TO UPLOAD TO SQL DATABASE
def img_to_binary(file):
    with open(file, 'rb') as file:
        binaryData=file.read()
    return binaryData

#STREAMLIT BACKEND
if Option=="Home":
    st.markdown("## :green[**Technologies Used :**] Python,easyOCR, Streamlit, PostgreSQL, Pandas, Matplotlib.pyplot")
    st.markdown("## :green[**Description :**] In this streamlit web application you can upload an image of a business card and extract relevant information from it using easyOCR library. You can view, modify or delete the extracted data in this application. This application would also allow users to save the extracted information into a database along with the uploaded business card image. The database would be able to store multiple entries, each with its own business card image and extracted information.")

elif Option=="Upload & Extract":
    st.markdown("### Upload a Business Card")
    uploaded_card=st.file_uploader("upload here",label_visibility="collapsed",type=["png","jpeg","jpg"])

    if uploaded_card is not None:
        save_card(uploaded_card)

        # DISPLAYING THE UPLOADED CARD
        col1,col2=st.columns(2)
        with col1:
            st.markdown("#     ")
            st.markdown("#     ")
            st.markdown("### You have uploaded the card")
            st.image(uploaded_card)

        # DISPLAYING THE CARD WITH EXTRACTED DATA
        with col2:
            st.markdown("#     ")
            st.markdown("#     ")
            with st.spinner("Please wait processing the image..."):
                st.set_option('deprecation.showPyplotGlobalUse', False)
                img_path=os.getcwd()+ "\\" + "uploaded_cards"+ "\\"+ uploaded_card.name
                image = cv2.imread(img_path) #Reading image
                res = reader.readtext(img_path) #extracting data from image
                st.markdown("### Image Processed and Data Extracted is as shown below")
                st.pyplot(image_text(image,res)) #displaying image preview with extracted information

        #easy OCR
        saved_img = os.getcwd()+ "\\" + "uploaded_cards"+ "\\"+ uploaded_card.name
        result = reader.readtext(saved_img,detail = 0,paragraph=False)

        #FUNCTION FOR COLLECTING ALL DATA FROM CARD
        def get_data(res):
            data = {"company_name" : [],
                    "card_holder" : [],
                    "designation" : [],
                    "mobile_number" :[],
                    'email': [],
                    "website": [],
                    "area" : [],
                    "city" : [],
                    "state" : [],
                    "pin_code" : [],
                    "image": img_to_binary(saved_img)}
            for ind, i in enumerate(res):
              #TO GET WEBSITE  
                if 'www' in i.lower() or "www." in i.lower():
                            data['website'].append(i)
                elif 'WWW' in i:
                    data["website"] = res[4] +"." + res[5]

                # TO GET EMAIL ID
                elif "@" in i:
                    data["email"].append(i)

                #TO GET MOBILE NUMBER
                elif "-" in i:
                    data["mobile_number"].append(i)
                    if len(data["mobile_number"]) ==2:
                        data["mobile_number"] = " & ".join(data["mobile_number"])

                # TO GET COMPANY NAME  
                elif ind == len(res)-1:
                    data["company_name"].append(i)

                # TO GET CARD HOLDER NAME
                elif ind == 0:
                    data["card_holder"].append(i)

                # TO GET DESIGNATION
                elif ind == 1:
                    data["designation"].append(i)

                # TO GET AREA
                if re.findall('^[0-9].+, [a-zA-Z]+',i):
                    data["area"].append(i.split(',')[0])
                elif re.findall('[0-9] [a-zA-Z]+',i):
                    data["area"].append(i)

                # TO GET CITY NAME
                match1 = re.findall('.+St , ([a-zA-Z]+).+', i)
                match2 = re.findall('.+St., ([a-zA-Z]+).+', i)
                match3 = re.findall('^[E].*',i)
                if match1:
                    data["city"].append(match1[0])
                elif match2:
                    data["city"].append(match2[0])
                elif match3:
                    data["city"].append(match3[0])

                # TO GET STATE
                state_match = re.findall('[a-zA-Z]{9} +[0-9]',i)
                if state_match:
                        data["state"].append(i[:9])
                elif re.findall('^[0-9].+, ([a-zA-Z]+);',i):
                    data["state"].append(i.split()[-1])
                if len(data["state"])== 2:
                    data["state"].pop(0)

                # TO GET PINCODE        
                if len(i)>=6 and i.isdigit():
                    data["pin_code"].append(i)
                elif re.findall('[a-zA-Z]{9} +[0-9]',i):
                    data["pin_code"].append(i[10:])
            return data

        overall_data = get_data(result)

        #FUNCTION TO CREATE DATAFRAME
        def create_df(data):
            df = pd.DataFrame(data)
            return df
        
        df = create_df(overall_data)
        st.success("### The Extracted data is shown below")
        st.write(df)

        if st.button("Upload to Database"):
            for index, row in df.iterrows():
                try:
                    insert_query = '''INSERT INTO cards_data(
                                                            company_name,
                                                            card_holder,
                                                            designation,
                                                            mobile_number,
                                                            email,
                                                            website,
                                                            area,
                                                            city,
                                                            state,
                                                            pin_code,
                                                            image
                                                        )
                                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                                                    '''
                    values = (
                            row['company_name'],
                            row['card_holder'],
                            row['designation'],
                            row['mobile_number'],
                            row['email'],
                            row['website'],
                            row['area'],
                            row['city'],
                            row['state'],
                            row['pin_code'],
                            row['image']
                            )
                    cursor.execute(insert_query, values)
                    mydb.commit()
                    st.success("#### Uploaded to the database successfully!")
                except psycopg2.IntegrityError as e:
                    if e.pgcode == '23505':
                        st.write(f"#### Data has already present for the email {row['email']}")
                    else:
                        st.write(f"Error: {e}")

#UPDATE MENU
elif Option=="Alter or Delete":
    col1,col2,col3 = st.columns([2,3,1])
    col2.markdown('<h2 style="color: #BDF2B2;">Update or Delete the data here</h2>', unsafe_allow_html=True)
    column1,column2 = st.columns(2,gap="large")
    try:
        with column1:
            cursor.execute("SELECT card_holder FROM cards_data")
            Names = cursor.fetchall()
            Card_holder_names = {}
            for row in Names:
                Card_holder_names[row[0]] = row[0]
            selected_card = st.selectbox("Select a card holder name to update", list(Card_holder_names.keys()))
            st.markdown("#### Update or modify any data below")
            cursor.execute("select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code from cards_data WHERE card_holder=%s",
                            (selected_card,))
            data1 = cursor.fetchone()

            company_name = st.text_input("Company_Name", data1[0])
            card_holder = st.text_input("Card_Holder", data1[1])
            designation = st.text_input("Designation", data1[2])
            mobile_number = st.text_input("Mobile_Number", data1[3])
            email = st.text_input("Email", data1[4])
            website = st.text_input("Website", data1[5])
            area = st.text_input("Area", data1[6])
            city = st.text_input("City", data1[7])
            state = st.text_input("State", data1[8])
            pin_code = st.text_input("Pin_code", data1[9])

            if st.button("Update the changes to database"):
                update_query = """UPDATE cards_data 
                                    SET 
                                        company_name=%s,
                                        card_holder=%s,
                                        designation=%s,
                                        mobile_number=%s,
                                        email=%s,
                                        website=%s,
                                        area=%s,
                                        city=%s,
                                        state=%s,
                                        pin_code=%s
                                    WHERE 
                                        card_holder=%s
                                """
                values = (
                    company_name, card_holder, designation, mobile_number,
                    email, website, area, city, state, pin_code, selected_card
                )
                cursor.execute(update_query, values)
                mydb.commit()
                st.success("##### Information updated in database successfully.")

        with column2:
            cursor.execute("SELECT card_holder FROM cards_data")
            data2 = cursor.fetchall()
            Card_holder_names = {}
            for row in data2:
                Card_holder_names[row[0]] = row[0]
            selected_card = st.selectbox("Select a card holder name to Delete", list(Card_holder_names.keys()))
            st.write(f"#### Did you want to delete :green[**{selected_card}'s**] card from database?")

            if st.button("Yes Delete this Business Card"):
                cursor.execute(f"DELETE FROM cards_data WHERE card_holder='{selected_card}'")
                mydb.commit()
                st.success("#### Business card information for '{}' deleted from database.".format(selected_card))
    except:
        st.warning("##### There is no data available in the database")

    if st.button("View updated data"):
        cursor.execute("SELECT company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code FROM cards_data")
        updated_data = cursor.fetchall()
        updated_df = pd.DataFrame(updated_data, columns=["Company_Name", "Card_Holder", "Designation", "Mobile_Number", "Email", "Website", "Area", "City", "State", "Pin_Code"])
        st.write(updated_df)
