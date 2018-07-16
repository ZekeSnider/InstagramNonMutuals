from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time 
import json

with open('config.json') as config_file:
	config = json.load(config_file)

driver = webdriver.Chrome()
driver.get("https://www.instagram.com/" + config["username"] + "/following/")

def getList():
	time.sleep(2)
	scroll_div = driver.find_elements_by_xpath("//li/../../..")[3]
	parent_div = driver.find_elements_by_xpath("//li/..")[3]

	list = None
	last_length = 0
	diff = 1

	scroll_id = scroll_div.get_attribute("class")
	while diff!=0:
		driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scroll_div)
	 	list = parent_div.find_elements_by_tag_name("li")
	 	diff = len(list) - last_length
	 	last_length = len(list)
	 	time.sleep(0.3)

	followers = []
	for item in list:
		person = item.find_element_by_css_selector("div:first-child div:first-child div:first-child div:first-child div:first-child a").get_attribute("href")
		person = person.replace("https://www.instagram.com/", "")
		person = person.replace("/", "")
		followers.append(person)

	print(followers)
	return followers
	

def closeModule():
	driver.find_element_by_xpath("//button[contains(text(),'Close')]").click()


inputFields = driver.find_elements_by_tag_name('input')

inputFields[0].send_keys(config["email"])
inputFields[1].send_keys(config["password"])

inputFields[1].send_keys(Keys.ENTER)

#confirmation_code = raw_input("Enter the SMS verification code: ")
#inputFields = driver.find_elements_by_tag_name('input')
##inputFields[0].send_keys(confirmation_code)
#inputFields[0].send_keys(Keys.ENTER)


#driver.explicity_wait(3)
time.sleep(2)

followersButton = driver.find_element_by_css_selector('a[href="/' + config["username"] + '/followers/"]')
followersButton.click()
followerList = getList()

closeModule()

followingButton = driver.find_element_by_css_selector('a[href="/' + config["username"] + '/following/"]')
followingButton.click()
followingList = getList()

driver.close()

non_mutual_follows = list(set(followingList) - set(followerList))

with open('following.json', 'w') as follow_file, open('followers.json', 'w') as follower_file, open("nonmutual.json", 'w') as non_mutual_file:
	json.dump(followerList, follower_file, indent=4)
	json.dump(followingList, follow_file, indent=4)
	json.dump(non_mutual_follows, non_mutual_file, indent=4)

print("Follower information written to files.")

print("The following accounts are non-mutual follows: " + unicode(non_mutual_follows))
