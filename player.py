from playsound import playsound 
import os
import argparse
from enum import Enum
import re
from pathlib import Path, PureWindowsPath
import random
def configure():
    with open("player.cfg", "w+") as cfg:
        print("Just setting things up first :)")
        root = input("Enter the root address of all your music. This is where the music will be searched for : ")
        cfg.write(f"root={root}\n")
class Action(Enum):
    Play = 1

def process_str(string):
    return string.replace("\"","").strip().lower() if string != None else None

def str_to_action(string):
    string = process_str(string) 
    if string == "play":
        return Action.Play
    return None
    
def main():
    if not os.path.exists("player.cfg"):
        configure()
    parser = argparse.ArgumentParser(description = "A simple program to play music from the commandline")
    parser.add_argument("command",help = "The action you would like the program to take")
    parser.add_argument("song", help="The song to perform the action")
    parser.add_argument("-s","--shuffle", help="Flag to shuffle music",action="store_true")
    args = parser.parse_args()

    action = str_to_action(args.command)
    song = process_str(args.song)


    config_dict = {}
    with open("player.cfg","r") as config:
        for line in config:
           line  = "".join(line.split())
           ind = line.find("=")
           if ind == -1:
               print("Error in config file")
               print("Only valid statements are 'root = xxx/yyy'")
           config_dict[line[0:ind]] = Path(line[ind+1:])

     
    

    with os.scandir(config_dict["root"]) as songs:
        lsongs = list(songs)
        choices = [s for s in lsongs if re.search(song, " ".join(re.split("[-_ ]+", s.name.lower()))) != None]
        
     
     
        if len(choices) == 0 :
            print("Sorry. Could not find song specified :("
            )
            exit()
        song_to_play = choices[0]
        if len(choices) > 1:
            print("Multiple songs fit that request")
            print("Please pick from the list")
            for i,c in enumerate(choices):
                print(f"{i+1} => {c.name}")
            choice = int(input("Enter the song you would like "))
            song_to_play = choices[choice-1]
        os.system("start")
        while True:
            print(f"Playing : {song_to_play.name}")
            playsound(f'{config_dict["root"] / song_to_play.name}')
            
            while not (song_to_play := random.choice(lsongs)).name.endswith(".mp3"):
               pass
                
    

if __name__ == "__main__":
    main()
