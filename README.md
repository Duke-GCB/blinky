# blinky
Tools and scripts for Grouper management

## Setup
Create config file
```
cp example_blinky.cfg ~/.blinky.cfg
```
Edit `~/.blinky.cfg` filling in 
- `account_id` -  your user's Duke Unique ID (a number)
- `account_password` - your user's password

Create environment, activate it and install requirements
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

## Run
List a groups a user is in based on that users netid.
```
python blinky_go.py member_groups jpb67
```
