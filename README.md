# ani-cli
Command line interface for watching anime
This tool scrapes site <a href="https://ogladajanime.pl/">ogladajanime.pl</a><br>
works only on linux
<hr>

## Dependencies:
- mpv
- python 3.10
- bash
<hr>

## Install
(Works on bash)<br>
go to install directory example
```
cd /home/$USER/.apps/
```
clone repository
```
git clone https://github.com/michalecznik123/ani-cli.git
```
go to cloned repository
```
cd ani-cli
```
create venv
```
python3.10 -m venv venv
```
activate venv 
```
source venv/bin/activate
```
Install dependencies
```
pip install -r requirements.txt
```
Deactivate venv
```
deactivate
```
add alias for easy run application
```
echo 'alias ani-cli="source /home/$USER/.apps/ani-cli/venv/bin/activate && python /home/$USER/.apps/ani-cli/main.py && deactivate"' >> ~/.bashrc
```
Done!
<hr>

## How to use
run app with command `ani-cli`
Find anime with you would like to watch using commands explained below.
### Commands
- :help <br>
Get list of commands in application
- :next <br>
Go to the next page in search results
- :prev <br>
Go to the previous page in search results
- ?search <br>
Search 'search' anime 
- :number <br>
Open position with 'number' (first column in table)
- :q or :quit <br>
Exit search or close the program :)


