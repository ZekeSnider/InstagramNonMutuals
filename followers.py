from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time 
import json
import pyotp

with open('config.json') as config_file:
	config = json.load(config_file)

MODAL_ELEMENT = "//li/../../.."
MODAL_SUBELEMENT = "//li/.."
FOLLOWERS_LINK = 'a[href="/' + config["username"] + '/followers/"]'
FOLLOWING_LINK = 'a[href="/' + config["username"] + '/following/"]'
CLOSE_BUTTON = "/html/body/div[3]/div/div/div[1]/div/div[2]/button"

driver = webdriver.Chrome()
driver.get("https://www.instagram.com/" + config["username"] + "/following/")

def get_list(include_verified):
	while 1:
		if len(driver.find_elements_by_xpath(MODAL_ELEMENT)) == 4:
			break
		else:
			time.sleep(0.2)
	scroll_div = driver.find_elements_by_xpath(MODAL_ELEMENT)[3]
	parent_div = driver.find_elements_by_xpath(MODAL_SUBELEMENT)[3]

	list = None
	last_length = 0
	diff = 1

	driver.execute_script('arguments[0].scrollTop = 250', scroll_div)
	time.sleep(2)

	# Keep scrolling to bottom of the div while the number of entries is increasing
	# (loading from the server, haven't reached the end yet)
	while diff!=0:
		driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scroll_div)
		time.sleep(1)

	 	list = parent_div.find_elements_by_tag_name("li")
	 	diff = len(list) - last_length
	 	last_length = len(list)


	followers = []
	for item in list:
		person = item.find_element_by_css_selector("div:first-child div:first-child div:first-child div:first-child div:first-child a").get_attribute("href")
		verified = item.find_elements_by_class_name("coreSpriteVerifiedBadge")

		if len(verified) == 0 or include_verified:
			person = person.replace("https://www.instagram.com/", "")
			person = person.replace("/", "")
			followers.append(person)

	print(followers)
	return followers
	

def closeModule():
	driver.find_element_by_xpath(CLOSE_BUTTON).click()


input_fields = driver.find_elements_by_tag_name('input')

input_fields[0].send_keys(config["email"])
input_fields[1].send_keys(config["password"])

input_fields[1].send_keys(Keys.ENTER)

if config["2factorEnabled"] or (config["OTPEnabled"] and config["OTPHash"] == ""):
	confirmation_code = raw_input("Enter the SMS/OTP verification code: ")
	input_fields = driver.find_elements_by_tag_name('input')
	input_fields[0].send_keys(confirmation_code)
	input_fields[0].send_keys(Keys.ENTER)
elif config["OTPEnabled"]:
	time.sleep(0.8)
	confirmation_code = pyotp.TOTP(config["OTPHash"]).now()
	input_fields = driver.find_elements_by_tag_name('input')
	input_fields[0].send_keys(confirmation_code)
	input_fields[0].send_keys(Keys.ENTER)

while 1:
	if len(driver.find_elements_by_css_selector(FOLLOWERS_LINK)) == 1:
		break
	else:
		time.sleep(0.2)

followers_button = driver.find_element_by_css_selector(FOLLOWERS_LINK)
followers_button.click()
followers_list = get_list(config["includeVerified"])

closeModule()

following_button = driver.find_element_by_css_selector(FOLLOWING_LINK)
following_button.click()
following_list = get_list(config["includeVerified"])

driver.close()

non_mutual_follows = list(set(following_list) - set(followers_list))

with open('following.json', 'w') as follow_file, open('followers.json', 'w') as follower_file, open("nonmutual.json", 'w') as non_mutual_file:
	json.dump(followers_list, follower_file, indent=4)
	json.dump(following_list, follow_file, indent=4)
	json.dump(non_mutual_follows, non_mutual_file, indent=4)

print("Follower information written to files.")

print("The following accounts are non-mutual follows: " + unicode(non_mutual_follows))
