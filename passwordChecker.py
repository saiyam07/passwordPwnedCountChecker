import requests
import sys
import hashlib
from pathlib import Path

apiEndPoint = 'https://api.pwnedpasswords.com/range/'

def request_password_data(pwHead):
    response = requests.get(apiEndPoint+'/'+pwHead)
    if response.status_code == 200:
        return response
    else:
        raise RuntimeError('There is some issue with the API call please check')

def get_password_leakCount(pw_hash_to_check, pw_hashes_recieved):
    pw_hashes_recieved = (a_pw_hash.split(':') for a_pw_hash in pw_hashes_recieved.splitlines())  
    for aHash,attackCount in pw_hashes_recieved:
        if aHash == pw_hash_to_check:
            return attackCount
    return 0

def passwordAttackCheck(passwordToCheck):
    hashedPassword = hashlib.sha1(passwordToCheck.encode("UTF-8")).hexdigest().upper()
    pwHead,pwTail = hashedPassword[:5], hashedPassword[5:]
    pw_API_Response = request_password_data(pwHead)
    return get_password_leakCount(pwTail, pw_API_Response.text)


def main(passwordsToCheck):
    i = 1
    for aPassword in passwordsToCheck:
        count = passwordAttackCheck(aPassword) 
        if count :
            print(f'The password at position {i} has been attcked {count} times, you should pobably change it if used')
        else:
            print(f'The password at position {i} is secure, continue using it')
        i+=1





if __name__ == '__main__':
    pwFile = Path('./pw/passwords.txt')
    if pwFile.stat().st_size > 0:
        passwordsToCheck = [aPassword for aPassword in pwFile.read_text().split(' ')]
        sys.exit(main(passwordsToCheck))
    else:
        raise RuntimeError('There are no passwords to verify') 
    


    

