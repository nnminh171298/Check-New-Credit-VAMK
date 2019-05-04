# CSS selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display

# mail
import smtplib
from email.message import EmailMessage

import time

def mail(data, mailUser, mailPass):
	# draft the email
	msg = EmailMessage()
	msg.set_content(data)
	msg['Subject'] = 'Winha grades'
	msg['From'] = mailUser
	msg['To'] = mailUser

	# send
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.login(mailUser, mailPass)
	server.send_message(msg)
	server.quit()
	
def wait_element(driver, locate_by, location_text):
	try:
		delay = 10
		element = wait(driver, delay).until(EC.presence_of_element_located((locate_by, location_text)))
		return element
	except:
		raise SystemExit
	
def get_grade(line_list, vamkUser, vamkPass):
	firefox_options = webdriver.FirefoxOptions()
	firefox_options.headless = True
	firefox_options.add_argument("--incognito")

	# Open page
	driver = webdriver.Firefox(options = firefox_options)
	driver.get("https://secure.puv.fi/wille/wille.asp")
	
	# Login alert (only from outside intranet)
	try:
		driver.switch_to.alert.send_keys(vamkUser + Keys.TAB + vamkPass)
		driver.switch_to.alert.accept()
	except:
		pass

	# English
	element = wait_element(driver, By.CSS_SELECTOR, 'a:nth-child(3) img')
	element.click()

	# Login (again)
	element = wait_element(driver, By.CSS_SELECTOR, 'tr:nth-child(1) .InputBox')
	element.send_keys(vamkUser + Keys.TAB + vamkPass)
	driver.find_element_by_css_selector('.InputButton').click()

	# ISP
	element = wait_element(driver, By.XPATH, '/html/frameset/frame[1]')
	driver.switch_to.frame(element)
	element = wait_element(driver, By.CSS_SELECTOR, 'a[href="eHopshae.Asp"]')
	element.click()
	driver.switch_to.default_content()

	# Completions
	element = wait_element(driver, By.XPATH, '/html/frameset/frame[2]')
	driver.switch_to.frame(element)
	element = wait_element(driver, By.CSS_SELECTOR, '.tblBgColor > tbody:nth-child(1) > tr:nth-child(6) > td:nth-child(3) > input:nth-child(1)')
	element.click()
	driver.find_element_by_css_selector('.InputButton').click()

	# Date of assessment
	element = wait_element(driver, By.CSS_SELECTOR, 'tr.pageHeader > td:nth-child(10) > a:nth-child(1)')
	element.click()
	time.sleep(10)

	# Get course-grade-date
	index = 3;
	if last_line == '':
		new_data_flag = True
	else:
		new_data_flag = False
	new_data = []
	grade_sum = 0;
	count = 0;
	while True:
		try:
			row = '#DataGrid1 > tbody:nth-child(1) > tr:nth-child(' + str(index) + ') > '
			course_name = driver.find_element_by_css_selector(row + 'td:nth-child(2) > a:nth-child(1)')
			grade = driver.find_element_by_css_selector(row + 'td:nth-child(8)')
			date = driver.find_element_by_css_selector(row + 'td:nth-child(10) > a:nth-child(1)')

			line = grade.text + '\t' + date.text + '\t' + course_name.text
			if(new_data_flag):
				new_data.append(line)
			if(last_line == line):
				new_data_flag = True

			try:
				grade_sum = grade_sum + int(grade.text)
				count = count + 1
			except ValueError:
				pass

			index = index + 2
		except:
			if(new_data == []):
				new_data_flag = False
			if(count != 0):
				cgpa_line = str("\nCGPA = %.2f" % (grade_sum/count))
			else:
				cgpa_line = ''
			seperator = '\n'
			write_data = seperator.join(new_data) + seperator
			return [new_data_flag, write_data, cgpa_line]

if __name__=="__main__":
	id_gmail_app_file = 'IdGmailApp.txt'
	id_vamk_file = 'IdVamk.txt'
	grade_file = 'grades.txt'

	# look for mail app ID
	try:
		fh = open(id_gmail_app_file, 'r')
		[mailUser, mailPass] = fh.read().splitlines()
		fh.close()
	except FileNotFoundError:
		print('Save Gmail app username and password to "IdGmailApp.txt" in the same folder to continue.')
		raise SystemExit

	# look for VAMK ID
	try:
		fh = open(id_vamk_file, 'r')
		[vamkUser, vamkPass] = fh.read().splitlines()
		fh.close()
	except FileNotFoundError:
		print('Save VAMK ID in "IdVamk.txt" to the same folder to continue.')
		raise SystemExit
	
	# look for saved grades
	try:
		fh = open(grade_file, 'r')
		line_list = fh.read().splitlines()
		last_line = line_list[-1]
	except:
		last_line = ''
	fh.close()
	
	display = Display(visible=0, size=(800, 600))
	display.start()
	[new_data_flag, write_data, cgpa_line] = get_grade(last_line, vamkUser, vamkPass)
	if new_data_flag:
		fh = open(grade_file, 'a')
		fh.write(write_data)
		fh.close()
		mail(write_data + cgpa_line, mailUser, mailPass)
