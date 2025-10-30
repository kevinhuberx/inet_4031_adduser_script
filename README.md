# INET4031 Add Users Script and User List

## Program Description
This Python script provides an automated way to add multiple users to a Linux system using a structured input file, removing the need to manually type each command for every user.

This program will handle the same commands automatically:
sudo adduser username – to create a new account.
sudo passwd username – to set the user’s password.
sudo adduser username groupname – to add the user to one or more groups.

The script combines all of these steps into a single automated process. By reading a formatted input file that contains the username, password, full name, and group memberships for each user, the script constructs and executes the necessary Linux commands for each entry. This ensures consistency, reduces human error, and saves time when managing multiple users.

### Program User Operation

This script automates the process of adding users to a Linux system using a predefined input file. The user prepares a text file containing all the required information for each user account, and the script reads this file line by line, generating and optionally executing the appropriate Linux commands to create the users, set their passwords, and assign them to groups.

The code file itself contains more in-depth comments to explain various lines of code and their functions. 

#### Input File Format

The format of the input takes the current format: 
`username:password:last_name:first_name:group1,group2,group3`

To skip a line in the input file, simply add a # at the beginning of the line. The script will detect this and ignore the line, allowing you to temporarily disable certain user entries without deleting them.

If you do not want a new user added to any groups, set the group field to -. The script will check for this and skip any adduser commands for groups when it encounters -.

#### Command Execution

To run the program, you may first need to make the Python script executable:
`chmod +x create-users.py`

Then execute the script with the input file as standard input:
`./create-users.py < create-users.input`

Use `sudo` if the script requires administrative privileges to create users or set passwords.

#### "Dry Run"

The script is preconfigured in a dry run state. All os.system(cmd) commands are commented out, so no actual changes will be made to the system. Optional debug print statements are also included but commented out.

To Perform a Dry-Run:

Uncomment any # Dry Run Debug Print Statement lines in the code to see the values of key variables and the exact commands that would be executed.

Run the script as usual with input redirection:
`./create-users.py < create-users.input`
