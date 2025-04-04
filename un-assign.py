from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import csv


"""
Feed the script a set of serial numbers to un-assign in JAMF

REQ: CSV file must have a single Serial number per cell and line
I.e: *****,
	 *****,
	 *****,


1. Move CSV file to folder, or change input file directory in "Parse_Serial_Number()" function
2. Run script through terminal "python3 un-assign.py"

"""


driver = webdriver.Chrome()
#Change to companys Jamf URL
driver.get("url-to-jamf")
wait = WebDriverWait(driver, 30)



def login(): #Navigate through login
	
	#input your user
	user = wait.until(EC.presence_of_element_located((By.ID, "input28"))).send_keys("")
	#input your pass
	pass_word = wait.until(EC.presence_of_element_located((By.ID, "input36"))).send_keys("")


	sighn_in_butt = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Sign in']"))).click()

	wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Select")))
	select_butts = driver.find_elements(By.LINK_TEXT, "Select") 
	
	select_butts[1].click()





def navigate():

	save_arr = []

	serial_numbs = parse_serial_numb()

	computers_butt = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='computers.html']"))).click()
	prestage_butt = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='computerEnrollmentPrestage.html']"))).click()
	"""
	DEP_US = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='computerEnrollmentPrestage.html?id=1&o=r']")))
	"""


	#DEP_US = driver.find_element(By.XPATH, "//a[@href='computerEnrollmentPrestage.html?id=1&o=r']")
	driver.get("")



	iframe = wait.until(EC.presence_of_element_located((By.XPATH ,"//iframe[@src='legacy/computerEnrollmentPrestage.html?id=1&o=r']")))
	driver.switch_to.frame(iframe)


	edit_button = wait.until(EC.element_to_be_clickable((By.ID, "edit-button"))).click()		



	a_tags = driver.find_elements(By.TAG_NAME, 'a')
	time.sleep(2)
	scope_tag = a_tags[1]


	scope_tag.click()

	#search_button = driver.find_elements(By.TAG_NAME, 'input')
	search_button = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Filter Results']")))

	count = 0
	max_count = len(serial_numbs)
	for serial in serial_numbs:
		print(f"{count} out of {max_count} un-assigned")
		count += 1
		for i in range(20):
			search_button.send_keys(Keys.BACK_SPACE)

		search_button.send_keys(serial)

		status = driver.find_elements(By.TAG_NAME, "td")

		text = []

		for word in status[2800:]:
			if(word.text):
				text += [word.text]

		for word in text:
			if word == "Not Assigned":
				break
			elif word == "Assigned":
				check_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='"+ serial +"']"))).click()
				break

	
	print("Type Save -or- Cancel")
	user_option = input("Enter Option: ")
	
	while(True):
		if user_option == 'Save':
			save_button = wait.until(EC.element_to_be_clickable((By.ID, "save-button"))).click()
			find_buttons = driver.find_elements(By.TAG_NAME, 'button')

			for obj in find_buttons[800:]:
				if obj.get_attribute("class") == "jamf-button  primary  ok":
					obj.click()
					time.sleep(5) #Sleep to allow synv time after save


			print(final_save.get_attribute("class"))


			


			#final_save.click()
			time.sleep(3)
			break


		elif user_option == "Cancel":
			cancel_button = wait.until(EC.element_to_be_clickable((By.ID, 'cancel-button'))).click()
			break

		else:
			print("\nInvalid Option")


def parse_serial_numb():
	serial_numbs = []
	with open('New_un-assign - Sheet1.csv', 'r' ,newline='') as csvfile:
	    user_csv = csv.reader(csvfile, delimiter=',', quotechar='|')
	    for row in user_csv:
	    	serial_numbs += row


	csvfile.close()
	return serial_numbs
	

			
login()
navigate()




driver.quit()
driver.close() 


