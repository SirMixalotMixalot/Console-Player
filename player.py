from playsound import playsound 
import os
import argparse
from enum import Enum
import re
from pathlib import Path, PureWindowsPath
import random
from tinytag import TinyTag

def configure():
    with open("player.cfg", "w+") as cfg:
        print("Just setting things up first :)")
        root = input("Enter the root address of all your music. This is where the music will be searched for : ")
        cfg.write(f"root={root}\n")
class Action(Enum):
    Play = 1,
    List = 2

def process_str(string):
    return string.replace("\"","").strip().lower() if string != None else None

def str_to_action(string):
    string = process_str(string) 
    if string == "play":
        return Action.Play
    if string == "list":
        return Action.List
    return None
    
def main():
    if not os.path.exists("player.cfg"):
        configure()
    ### Setting up argument parser ###
    parser = argparse.ArgumentParser(description = "A simple program to play music from the commandline")
    parser.add_argument("command",help = "The action you would like the program to take")
    parser.add_argument("-s","--song", help="The song to perform the action")
    #parser.add_argument("-s","--shuffle", help="Flag to shuffle music",action="store_true")
    args = parser.parse_args()

    action = str_to_action(args.command)
    

    ### Reading config file ###
    config_dict = {}
    with open("player.cfg","r") as config:
        for line in config:
           line  = "".join(line.split())
           ind = line.find("=")
           if ind == -1:
               print("Error in config file")
               print("Only valid statements are 'root = xxx/yyy'")
           config_dict[line[0:ind]] = Path(line[ind+1:])

     
    
    ### Finding song specified and playing it ###
    with os.scandir(config_dict["root"]) as songs:
        lsongs = list(s for s in songs if s.is_file() and s.name.endswith(".mp3"))
        tags = [TinyTag.get(l.path) for l in lsongs]


        if action == Action.List:
            for (s, t) in zip(lsongs, tags):
                if t.title and t.artist:
                    print(f"Title : {t.title} Artist : {t.artist}")
                print(s.name)
                print()
            exit()
        song = process_str(args.song)
        choices = [s for s in lsongs if re.search(fr"\b{song}\b", " ".join(re.split("[-_ ]+", (TinyTag.get(s.path).title or s.name).lower()  ))) != None]
        
     
        ### dealing with multiple matches ###
        if len(choices) == 0 :
            print("Sorry. Could not find song specified :("
            )
            exit()
        song_to_play = choices[0]
        if len(choices) > 1:
            print("Multiple songs fit that request")
            print("Please pick from the list")
            for i, c in enumerate(choices):
                tag = TinyTag.get(c.path)
                print(f"{i+1} => Title : {tag.title or c.name}. Artist : {tag.artist or 'unkown'}")
            choice = int(input("Enter the song you would like "))
            song_to_play = choices[choice - 1]
            
        ### playsound is blocking so I would like a terminal to play with atleast ###
        #os.system("start") ok it gets annoying


        while True:
            tag = TinyTag.get(f'{config_dict["root"] / song_to_play.name}')
            print(f"Playing : { tag.title or song_to_play.name}")
            if tag.artist != None:
                print(f"Song by {tag.artist}")
            print(f"Duration : {tag.duration}s")
            playsound(f'{config_dict["root"] / song_to_play.name}')
            song_to_play = random.choice(lsongs)
              
                
    

if __name__ == "__main__":
    main()
