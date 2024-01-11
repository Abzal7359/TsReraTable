import base64
import csv
import re
import time
import requests
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from openpyxl import load_workbook
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_experimental_option("detach", True)
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.implicitly_wait(10)
# ------------------------------------------------------------------------------------------------------------------------------------
driver.get("https://rera.telangana.gov.in/")
window1 = driver.current_window_handle
time.sleep(5)
driver.find_element(By.XPATH, "//a[normalize-space()='Search Registered Projects and Agents']").click()
time.sleep(5)
window2 = None

all_windows = driver.window_handles
# Loop through each window handle
for window in all_windows:
    # Switch to the window that is not the main window
    if window != window1:
        window2 = window

        driver.switch_to.window(window)
        break
#
#
driver.find_element(By.XPATH, "//input[@id='PageSize']").clear()
driver.find_element(By.XPATH, "//input[@id='PageSize']").send_keys(20, Keys.ENTER)

# s = driver.find_element(By.XPATH, "//li[@class='col-md-3 col-sm-2 text-center']").text
# rangee = int(s.split()[-1])
# print(rangee)

for i in range(1):
    # for k in range(7):
    #     driver.find_element(By.XPATH, "//button[@id='btnNext']").click()
    #     time.sleep(5)

    for j in range(8,9):
        sr_no = driver.find_element(By.XPATH, f"(//tr[{j}]//td)[1]").text
        projectname = driver.find_element(By.XPATH, f"(//tr[{j}]//td)[2]").text

        driver.find_element(By.XPATH, f"(//tr[{j}]//td)[5]//a").click()
        all_windows = driver.window_handles
        for window in all_windows:
            if window != window1 and window != window2:
                driver.switch_to.window(window)
        time.sleep(3)
        info_type = driver.find_element(By.XPATH,
                                        "//label[normalize-space()='Information Type']/parent::div/following::div").text
        # Name= None
        # og_type=None
        # past_exp=None
        # reg_in_other_states=None
        # descript_og_type=None
        project_type = driver.find_element(By.XPATH,
                                           "//label[normalize-space()='Project Type']/parent::div/following::div").text
        if info_type == "Other Than Individual":
            # --------code below to add development work---------
            amenities = driver.find_elements(By.XPATH, "//*[@id='DivAmenities']/div[2]/div[2]/table/tbody/tr")
            for ami in range(2, len(amenities) + 1):
                one = driver.find_element(By.XPATH,
                                          f"//*[@id='DivAmenities']/div[2]/div[2]/table/tbody/tr[{ami}]/td[1]").text
                two = driver.find_element(By.XPATH,
                                          f"//*[@id='DivAmenities']/div[2]/div[2]/table/tbody/tr[{ami}]/td[2]").text
                three = driver.find_element(By.XPATH,
                                            f"//*[@id='DivAmenities']/div[2]/div[2]/table/tbody/tr[{ami}]/td[3]").text
                four = driver.find_element(By.XPATH,
                                           f"//*[@id='DivAmenities']/div[2]/div[2]/table/tbody/tr[{ami}]/td[4]").text
                row_two = [sr_no, projectname, one, two, three, four]
                # "C:\Users\abzalhussain\Desktop\Amineties\fac.csv"
                with open("C://Users/abzalhussain/Desktop/Amineties/fac.csv", mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(row_two)

            # below code to add past experience table ----------------
            past_exp = driver.find_elements(By.XPATH, "//*[@id='DivExp']/div/div/div/table/tbody/tr")
            if len(past_exp):
                for exp in range(1, len(past_exp) + 1):
                    serial = driver.find_element(By.XPATH,
                                                 f"//*[@id='DivExp']/div/div/div/table/tbody/tr[{exp}]/td[1]").text
                    PN = driver.find_element(By.XPATH,
                                             f"//*[@id='DivExp']/div/div/div/table/tbody/tr[{exp}]/td[2]").text
                    TP = driver.find_element(By.XPATH,
                                             f"//*[@id='DivExp']/div/div/div/table/tbody/tr[{exp}]/td[3]").text
                    OT = driver.find_element(By.XPATH,
                                             f"//*[@id='DivExp']/div/div/div/table/tbody/tr[{exp}]/td[4]").text
                    LA = driver.find_element(By.XPATH,
                                             f"//*[@id='DivExp']/div/div/div/table/tbody/tr[{exp}]/td[5]").text
                    AD = driver.find_element(By.XPATH,
                                             f"//*[@id='DivExp']/div/div/div/table/tbody/tr[{exp}]/td[6]").text
                    CTS = driver.find_element(By.XPATH,
                                              f"//*[@id='DivExp']/div/div/div/table/tbody/tr[{exp}]/td[7]").text
                    NB = driver.find_element(By.XPATH,
                                             f"//*[@id='DivExp']/div/div/div/table/tbody/tr[{exp}]/td[8]").text
                    NA = driver.find_element(By.XPATH,
                                             f"//*[@id='DivExp']/div/div/div/table/tbody/tr[{exp}]/td[9]").text
                    OD = driver.find_element(By.XPATH,
                                             f"//*[@id='DivExp']/div/div/div/table/tbody/tr[{exp}]/td[10]").text
                    ADC = driver.find_element(By.XPATH,
                                              f"//*[@id='DivExp']/div/div/div/table/tbody/tr[{exp}]/td[11]").text
                    row_four = [sr_no, projectname, serial, PN, TP, OT, LA, AD, CTS, NB, OD, ADC]
                    #"C:\Users\abzalhussain\Desktop\past experience\past.csv"
                    with open("C://Users/abzalhussain/Desktop/past experience/past.csv", mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row_four)

            else:
                pass

            #below code for promoter details-------------------
            Promoter_details=driver.find_elements(By.XPATH,"//*[@id='DivCoPromoter']/div[1]/table/tbody/tr")
            if len(Promoter_details):
                for prom in range(1,len(Promoter_details)+1):
                    if prom % 2 ==0:
                        pn=driver.find_element(By.XPATH,f"//*[@id='DivCoPromoter']/div[1]/table/tbody/tr[{prom}]/td[2]").text
                        PT=driver.find_element(By.XPATH,f"//*[@id='DivCoPromoter']/div[1]/table/tbody/tr[{prom}]/td[3]").text
                        TA=driver.find_element(By.XPATH,f"//*[@id='DivCoPromoter']/div[1]/table/tbody/tr[{prom}]/td[4]").text
                        ON=driver.find_element(By.XPATH,f"//*[@id='DivCoPromoter']/div[1]/table/tbody/tr[{prom}]/td[5]").text
                        OtherDetails=driver.find_element(By.XPATH,f"//*[@id='DivCoPromoter']/div[1]/table/tbody/tr[{prom}]/td[6]").text
                        row_five = [sr_no, projectname,pn,PT,TA,ON,OtherDetails]
                        # "C:\Users\abzalhussain\Desktop\promoter\promoterr.csv"
                        with open("C://Users/abzalhussain/Desktop/promoter/promoterr.csv", mode='a',
                                  newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(row_five)
            else:
                pass



        # below code for plotted table
        if project_type == "Plotted Development":
            ploted_table = driver.find_elements(By.XPATH, "//*[@id='DivBuilding']/table/tbody/tr")
            for plot in range(2, len(ploted_table) + 1):
                first = driver.find_element(By.XPATH, f"//*[@id='DivBuilding']/table/tbody/tr[{plot}]/td[1]").text
                second = driver.find_element(By.XPATH, f"//*[@id='DivBuilding']/table/tbody/tr[{plot}]/td[2]").text
                third = driver.find_element(By.XPATH, f"//*[@id='DivBuilding']/table/tbody/tr[{plot}]/td[3]").text
                fourth = driver.find_element(By.XPATH, f"//*[@id='DivBuilding']/table/tbody/tr[{plot}]/td[4]").text
                row_three = [sr_no, projectname, first, second, third, fourth]
                # "C:\Users\abzalhussain\Desktop\plot Details\plot.csv"
                with open("C://Users/abzalhussain/Desktop/plot Details/plot.csv", mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(row_three)

        if info_type == "Other Than Individual" and project_type != "Plotted Development":

            # ----------------------Land Details-------------------------------------------------------------------------

            Total_units = driver.find_element(By.XPATH,
                                              "//label[normalize-space()='Total Building Units (as per approved plan)']/parent::div/following::div").text

            # //h2[normalize-space()='Building Details']/parent::div/following::table//td[contains(text(),'RAJAPUSHPA SERENE DALE')]/following-sibling::td[9]

            # slab_path = f"//h2[normalize-space()='Building Details']/parent::div/following::table//td[contains(text(),\"{projectname}\")]/following-sibling::td[6]"
            # parking_path = f"//h2[normalize-space()='Building Details']/parent::div/following::table//td[contains(text(),\"{projectname}\")]/following-sibling::td[9]"
            starting_number = 3
            difference = 4

            lll = [starting_number + (i * difference) for i in range(int(Total_units))]
            zzz = [2 + (i * difference) for i in range(int(Total_units))]

            # TABLE_ROWS=f"//div[1]/table[1]/tbody[1]/tr[{zz}]/td[3]/table[1]/tbody[1]/tr"
            for zz in range(int(Total_units)):
                tower_name_path = f"//*[@id='DivBuilding']/div/table/tbody/tr[{zzz[zz]}]/td[3]"

                print(tower_name_path, "path")

                tower_name = driver.find_element(By.XPATH, tower_name_path).text
                print(tower_name, "name")

                # -------below lines to get first line data from table--------
                Proposed_dat = f"//*[@id='DivBuilding']/div/table/tbody/tr[{zzz[zz]}]/td[4]"
                Proposed_date = driver.find_element(By.XPATH, Proposed_dat).text

                num_basement = f"//*[@id='DivBuilding']/div/table/tbody/tr[{zzz[zz]}]/td[5]"
                num_basements = driver.find_element(By.XPATH, num_basement).text

                num_plint = f"//*[@id='DivBuilding']/div/table/tbody/tr[{zzz[zz]}]/td[6]"
                num_plinth = driver.find_element(By.XPATH, num_plint).text

                num_podium = f"//*[@id='DivBuilding']/div/table/tbody/tr[{zzz[zz]}]/td[7]"
                num_podiums = driver.find_element(By.XPATH, num_podium).text

                num_slab_structur = f"//*[@id='DivBuilding']/div/table/tbody/tr[{zzz[zz]}]/td[8]"
                num_slab_structure = driver.find_element(By.XPATH, num_slab_structur).text

                num_stilt = f"//*[@id='DivBuilding']/div/table/tbody/tr[{zzz[zz]}]/td[9]"
                num_stilts = driver.find_element(By.XPATH, num_stilt).text

                num_open_parkin = f"//*[@id='DivBuilding']/div/table/tbody/tr[{zzz[zz]}]/td[10]"
                num_open_parking = driver.find_element(By.XPATH, num_open_parkin).text

                Total_area_par = f"//*[@id='DivBuilding']/div/table/tbody/tr[{zzz[zz]}]/td[11]"
                Total_area_park = driver.find_element(By.XPATH, Total_area_par).text

                row_one = [sr_no, projectname, tower_name, Proposed_date, num_basements, num_plinth,
                           num_podiums, num_slab_structure, num_stilts, num_open_parking, Total_area_park]
                # "C:\Users\abzalhussain\Desktop\first_row\row_one.csv"
                with open("C://Users/abzalhussain/Desktop/first_row/row_one.csv", mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(row_one)

                con = lll[zz]
                TABLE_ROWS = f"//div[1]/table[1]/tbody[1]/tr[{con}]/td[3]/table[1]/tbody[1]/tr"
                print(TABLE_ROWS)
                # if zz == 0:
                #     TABLE_ROWS = f"//div[1]/table[1]/tbody[1]/tr[{con}]/td[3]/table[1]/tbody[1]/tr"
                # else:
                #     con=con+4
                #     print(con)
                #     TABLE_ROWS = f"//div[1]/table[1]/tbody[1]/tr[{con}]/td[3]/table[1]/tbody[1]/tr"
                #     print(TABLE_ROWS)

                lennth = len(driver.find_elements(By.XPATH, TABLE_ROWS))
                print(lennth)
                for kk in range(2, lennth + 1):
                    s_n = f"//div[1]/table[1]/tbody[1]/tr[{con}]/td[3]/table[1]/tbody[1]/tr[{kk}]/td[1]"
                    s_no = driver.find_element(By.XPATH, s_n).text
                    floor_i = f"//div[1]/table[1]/tbody[1]/tr[{con}]/td[3]/table[1]/tbody[1]/tr[{kk}]/td[2]"
                    floor_id = driver.find_element(By.XPATH, floor_i).text
                    Mort_Are = f"//div[1]/table[1]/tbody[1]/tr[{con}]/td[3]/table[1]/tbody[1]/tr[{kk}]/td[3]"
                    Mort_Area = driver.find_element(By.XPATH, Mort_Are).text
                    Ap_Typ = f"//div[1]/table[1]/tbody[1]/tr[{con}]/td[3]/table[1]/tbody[1]/tr[{kk}]/td[4]"
                    Ap_Type = driver.find_element(By.XPATH, Ap_Typ).text
                    sal_are = f"//div[1]/table[1]/tbody[1]/tr[{con}]/td[3]/table[1]/tbody[1]/tr[{kk}]/td[5]"
                    sal_area = driver.find_element(By.XPATH, sal_are).text
                    Numb_Apartmen = f"//div[1]/table[1]/tbody[1]/tr[{con}]/td[3]/table[1]/tbody[1]/tr[{kk}]/td[6]"
                    Numb_Apartment = driver.find_element(By.XPATH, Numb_Apartmen).text
                    Numb_of_booked_Apartmen = f"//div[1]/table[1]/tbody[1]/tr[{con}]/td[3]/table[1]/tbody[1]/tr[{kk}]/td[7]"
                    Numb_of_booked_Apartment = driver.find_element(By.XPATH, Numb_of_booked_Apartmen).text

                    row = [sr_no, projectname, tower_name, s_no, floor_id, Mort_Area, Ap_Type,
                           sal_area, Numb_Apartment, Numb_of_booked_Apartment]

                    # "C:\Users\abzalhussain\Desktop\table details\rera_table.csv"
                    with open("C://Users/abzalhussain/Desktop/table details/rera_table.csv", mode='a',
                              newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row)
                print(projectname, tower_name)

            driver.close()
            driver.switch_to.window(window2)
            time.sleep(1)
        else:
            print(info_type)
            print("not plotted development")
            driver.close()
            driver.switch_to.window(window2)
            time.sleep(1)
