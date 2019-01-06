# Instagram Non-Mutuals

This is a script that scrapes Instagram using Chrome Driver and Selenium to determine a list of non-mutual follows for your account. These are accounts that you follow, but they do not follow you back. It also saves lists of your complete following/followers lists, in case it is useful.


## Usage

### Prerequisites

+ You must have Python 2.x installed.
+ You must have chrome driver installed. On macOS, you can install simply via `brew cask install chromedriver`
+ You must have selenium installed. `pip install selenium` or `pip install -r requirements.txt`
+ You must copy the file `config.json.template` to `config.json`, and fill in the configuration details. The `includeVerified` option allows you to optionally hide all verified accounts from the lists.

### Running
Use `python followers.py`. If you have 2 factor enabled, you will be prompted for the verification code, or if you use TOTP, you can configure the `OTPHash` in `config.json`.

The resulting files are saved to `followers.json`, `following.json`, and `nonmutual.json`.