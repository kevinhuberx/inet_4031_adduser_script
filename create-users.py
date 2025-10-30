#!/usr/bin/python3

# INET4031
# Kevin Huber
# 10/30/25
# Date Last Modified


import os # To execute system-level commands 
import re # Regular expression (re) to detect commented out lines in input files 
import sys # To read input from standard input 


def main():
    for line in sys.stdin:

        # This regular expression checks if the line begins with a '#'
        # Lines starting with '#' are treated as comments in the input file and are skipped.
        match = re.match("^#",line)
        print("The contents of the match variable: ", match)
        
        # Split the current line into parts separated by colons.
        # These parts represent the username, password, last name, first name, and the list of groups the user belongs to.
        fields = line.strip().split(':')
        print("length of fields: ", len(fields))

        #REPLACE THESE COMMENTS with a single comment describing the logic of the IF
        #what would an appropriate comment be for describing what this IF statement is checking for?
        #what happens if the IF statement evaluates to true?
        #how does this IF statement rely on what happened in the prior two lines of code? The match and fields lines.
        #the code clearly shows that the variables match and the length of fields is being checked for being != 5  so why is it doing that?

        # This checks whether the current line should be skipped or read
        # 
        # If the line starts with a # or does not contain exactly 5 fields, it is ignored for error handling
        
        if match or len(fields) != 5:
            continue

        print("Processing line:", line.strip())
        print("Split fields:", fields)
        # Extract the username and password from the first two fields of the line 
        # gecos combines the two fields into the format expected for the /etc/passwd file 
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3],fields[2])

        #Split the fifth field by commas to obtain the list of groups the user should be added to 
        # This allows for handling multiple groups for a single user 
        groups = fields[4].split(',')

        # Alert the user that an account is being created for a specific username
        print("==> Creating account for %s..." % (username))
        
        # Build the command to create the new user account 
        # --disabled-password prevents the account from having a password until it is set 
        # --gecos sets the user information, such as first name, last name 
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos,username)
        print("User creation cmd", cmd)

        # These statements will execute the adduser command, for a dry run, leave these commented out.
        #print cmd
        #os.system(cmd)

        # Alert the user that the script is about to set the password for the specific user 
        print("==> Setting the password for %s..." % (username))

        # Creates the command to set the user;s password 
        # Uses echo to send the password twice to the command 
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password,password,username)
        print("Password command:", cmd)
        
        # These statements will execute the adduser command, for a dry run, leave these commented out.
        #print cmd
        #os.system(cmd)

        for group in groups:
            #Check if the group is valid or if the user does not belong to one 
            # if it is a valid group, add the user to thar group
            # Prevents adding users to groups that are empty or do no exist. 
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username,group))
                cmd = "/usr/sbin/adduser %s %s" % (username,group)
                print("Group Command:", cmd)
                print("=" * 50)
                #print cmd
                #os.system(cmd)

if __name__ == '__main__':
    main()
