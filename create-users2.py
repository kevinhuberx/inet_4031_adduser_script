#!/usr/bin/python3

# INET4031
# Kevin Huber
# 10/30/25
# 10/30/25


import os # To execute system-level commands
import re # Regular expression (re) to detect commented out lines in input files
import sys # To read input from standard input


def main():
    # Ask the user if they would like to perform a Dry-Run
    run_option = input("Do you want to perform a Dry-Run? (Y/N): ")

    # Set the dry run variable according to the user input
    if run_option.strip().upper() == "Y":
        dry_run = True
    else:
        dry_run = False

    # Check if the user provided an input file as a command-line argument
    if len(sys.argv) < 2:
        print("Error: You must provide an input file as an argument.")
        sys.exit(1)

    # Open the input file provided as the first command-line argument
    input_file = sys.argv[1]
    with open(input_file) as f:
        for line in f:

            # This regular expression checks if the line begins with a '#'
            # Lines starting with '#' are treated as comments in the input file and are skipped.
            match = re.match("^#",line)
            # Dry Run Debug Print Statement
            #print("The contents of the match variable: ", match)

            # Split the current line into parts separated by colons.
            # These parts represent the username, password, last name, first name, and the list of groups the user belongs to.
            fields = line.strip().split(':')
            # Dry Run Debug Print Statement
            #print("length of fields: ", len(fields))

            # This IF statement checks two conditions:
            # If the line starts with a '#' (match is not None), meaning it is a comment and should be skipped.
            # If the line does not have exactly 5 fields after splitting by ':' (len(fields) != 5), meaning it is incomplete or malformed.
            # If either condition is true, the 'continue' statement skips processing this line and moves to the next one.
            if match or len(fields) != 5:
                if dry_run:
                    if match:
                        print("Dry Run: Skipping commented line:", line.strip())
                    elif len(fields) != 5:
                        print("Dry Run: Invalid line, not enough fields:", line.strip())
                continue

            # Dry Run Debug Print Statement
            #print("Processing line:", line.strip())
            #print("Split fields:", fields)

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
            # Dry Run Debug Print Statement
            if dry_run:
                print("Dry Run: User creation cmd", cmd)
            else:
                # These statements will execute the adduser command
                os.system(cmd)

            # Alert the user that the script is about to set the password for the specific user
            print("==> Setting the password for %s..." % (username))

            # Creates the command to set the user's password
            # Uses echo to send the password twice to the command
            cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password,password,username)
            if dry_run:
                print("Dry Run: Password command:", cmd)
            else:
                # These statements will execute the adduser command
                os.system(cmd)

            for group in groups:
                #Check if the group is valid or if the user does not belong to one
                # if it is a valid group, add the user to that group
                # Prevents adding users to groups that are empty or do not exist.
                if group != '-':
                    print("==> Assigning %s to the %s group..." % (username,group))
                    cmd = "/usr/sbin/adduser %s %s" % (username,group)

                    # Dry Run Debug Print Statement
                    if dry_run:
                        print("Dry Run: Group Command:", cmd)
                        print("=" * 50)
                    else:
                        # These statements will execute the adduser command
                        os.system(cmd)


if __name__ == '__main__':
    main()
