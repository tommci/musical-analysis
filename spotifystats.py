from tkinter import *
from tkinter import ttk
from pathlib import Path

import csv

tk = Tk(className=" Spotify Shuffle")
tk.geometry("500x500")

Path("spotify-shuffle/data").mkdir(exist_ok=True)

class Song:
    def __init__(self, name, artistCount, artists, listens, album, plays, length, explicit):
        self.name = name
        self.artistCount = artistCount
        self.artists = artists
        self.listens = listens
        self.album = album
        self.plays = plays
        self.length = length
        self.explicit = explicit
    def change_artist(self, index, newName):
        self.artists[index] = newName
    def add_artist(self):
        newCount = int(self.artistCount) + 1
        self.artists.append("New Artist")
        self.artistCount = newCount
    def remove_artist(self):
        if(len(self.artists) < 2):
            return 0
        else:
            newCount = int(self.artistCount) - 1
            self.artists.pop()
            self.artistCount = newCount
            return 1
    def get_length(self):
        mins = int(self.length) // 60
        secs = int(self.length) % 60
        if(secs < 10):
            secs = (f'0{secs}')
        return [mins, secs]
    def get_artist_string(self):
        allArtists = ""
        i = 0
        while(i < (len(self.artists) - 1)):
            allArtists = allArtists + self.artists[i] + ", "
            i += 1
        allArtists = allArtists + self.artists[i]
        return allArtists
    def get_expl_string(self):
        expl = ""
        if(int(self.explicit) == 1):
            expl = " [E]"
        return expl

class Playlist:
    def __init__(self):
        self.playlistEntry = Entry(tk)
        self.playlistPrompt = Label(tk)
        self.confirmButton = Button(tk)
        self.denyButton = Button(tk)
        self.cancelButton = Button(tk)
        self.explicitCheckbox = ttk.Checkbutton(tk)
        self.playlistExists = False
        self.playlistName = ""
        self.list = []
        self.prompt = -1
        self.tempSongName = ""
        self.tempArtistCount = 0
        self.counter = 1
        self.tempArtists = []
        self.tempMinute = 0
        self.tempLength = 0
        self.tempAlbum = ""
        self.tempGlobal = 0
        self.tempExpl = 0
        self.expl = IntVar()
    def destroy_items(self):
        self.playlistEntry.destroy()
        self.playlistPrompt.destroy()
        self.confirmButton.destroy()
        self.denyButton.destroy()
        self.cancelButton.destroy()
        self.explicitCheckbox.destroy()
    def try_playlist(self):
        self.playlistName = self.playlistEntry.get()
        self.destroy_items()
        try:
            open(f'spotify-shuffle/data/{playlist.playlistName}.dat', 'r', encoding='utf-8')
        except:
            self.playlistExists = False

            self.playlistPrompt = ttk.Label(tk, text=f"Playlist \"{self.playlistName}\" not found. Create new file?")
            self.playlistPrompt.place(relx=0.5, rely=0.4, anchor="center")

            self.confirmButton = ttk.Button(tk, text="YES", command=self.open_playlist)
            self.confirmButton.place(relx=0.4, rely=0.6, anchor="center")

            self.denyButton = ttk.Button(tk, text="NO", command=self.select_playlist)
            self.denyButton.place(relx=0.6, rely=0.6, anchor="center")
        else:
            self.playlistExists = True
            self.open_playlist()
    def open_playlist(self):
        name = self.playlistName
        if(not self.playlistExists):
            open(f'spotify-shuffle/data/{name}.dat', 'x', encoding='utf-8')
        playlist = []
        with open(f'spotify-shuffle/data/{name}.dat', 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter='|')
            for line in reader:
                tempName = line[0]
                artCount = line[1]
                tempArtists = []
                j = 2
                while(j < int(artCount) + 2):
                    tempArtists.append(line[j])
                    j += 1
                tempListens = line[j]
                tempAlbum = line[j + 1]
                tempPlays = line[j + 2]
                tempLength = line[j + 3]
                tempExpl = line[j + 4]
                song = Song(tempName, artCount, tempArtists, tempListens, tempAlbum, tempPlays, tempLength, tempExpl)
                playlist.append(song)
        self.list = playlist
        menu.main()
    def select_playlist(self):
        self.destroy_items()
        menu.destroy_items()

        self.playlistPrompt = ttk.Label(tk, text="Enter playlist name.")
        self.playlistPrompt.place(relx=0.5, rely=0.3, anchor="center")

        self.playlistEntry = ttk.Entry(tk, width=20)
        self.playlistEntry.place(relx=0.5, rely=0.45, anchor="center")

        self.confirmButton = ttk.Button(tk, text="OK", command=self.try_playlist)
        self.confirmButton.place(relx=0.5, rely=0.6, anchor="center")
    def add_song(self):
        self.prompt += 1
        if(self.prompt > 1 and self.prompt < 9):
            entryVal = self.playlistEntry.get()
        self.playlistEntry.destroy() # this resets the entry box each menu
        self.playlistEntry = ttk.Entry(tk, width=20)
        self.playlistEntry.place(relx=0.5, rely=0.45, anchor="center")
        match self.prompt:
            case 0:
                menu.destroy_items()
                self.add_song()
            case 1:
                self.playlistPrompt = ttk.Label(tk, text="Enter song name.", justify='center')
                self.playlistPrompt.place(relx=0.5, rely=0.3, anchor="center")

                self.explicitCheckbox = ttk.Checkbutton(tk, variable=self.expl, text="Explicit?")
                self.explicitCheckbox.place(relx=0.7, rely=0.45, anchor="center")
                self.expl.set(0)

                self.confirmButton = ttk.Button(tk, text="OK", command=self.add_song)
                self.confirmButton.place(relx=0.5, rely=0.6, anchor="center")
                
                self.cancelButton = ttk.Button(tk, text="Cancel", command=self.cancel_add_song)
                self.cancelButton.place(relx=0.5, rely=0.7, anchor="center")
            case 2:
                self.tempExpl = self.expl.get()
                self.explicitCheckbox.destroy()
                songExists = False
                for song in self.list:
                    if(entryVal.lower() == song.name.lower()):
                        songExists = True
                self.tempSongName = entryVal
                if(songExists):
                    self.playlistEntry.destroy()
                    self.playlistPrompt.configure(text=f"\n\n\nThe song \"{entryVal}\" already exists on this playlist.\nContinue anyway?")
                    self.prompt = 9
                else:
                    self.playlistPrompt.configure(text="Enter number of artists.")
            case 3:
                if((entryVal.isdigit() == True) and (int(entryVal) > 0)):
                    self.tempArtistCount = int(entryVal)
                    self.playlistPrompt.configure(text=f"Enter artist {self.counter}.")
                else:
                    self.prompt -= 1
                    self.playlistPrompt.configure(text="Invalid value. Enter a number.\nEnter number of artists.")
            case 4:
                self.tempArtists.append(entryVal)
                if(not self.tempArtistCount == self.counter):
                    self.counter += 1
                    self.prompt -= 1
                    self.playlistPrompt.configure(text=f"Enter artist {self.counter}.")
                else:
                    self.counter = 1
                    self.playlistPrompt.configure(text="Enter the minute length of the song.")
            case 5: 
                if((entryVal.isdigit() == True) and (int(entryVal) > -1)):
                    self.tempMinute = entryVal
                    self.playlistPrompt.configure(text="Enter the second length of the song.")
                else:
                    self.prompt -= 1
                    self.playlistPrompt.configure(text="Invalid value. Enter a number.\nEnter the minute length of the song.")
            case 6:
                if((entryVal.isdigit() == True) and (int(entryVal) > -1)):
                    self.tempLength = (int(self.tempMinute) * 60) + int(entryVal)
                    self.playlistPrompt.configure(text="Enter the album/EP/single the song is on.\n(If the song is on multiple, enter whichever version is on your playlist.)")
                else:
                    self.prompt -= 1
                    self.playlistPrompt.configure(text="Invalid value. Enter a number.\nEnter the second length of the song.")
            case 7:
                self.tempAlbum = entryVal
                self.playlistPrompt.configure(text="Enter the number of global listens.\nIf this value is unknown, enter \"?\"")
            case 8:
                if(((entryVal.isdigit() == True) and (int(entryVal) > -1)) or (entryVal == '?')):
                    self.playlistEntry.destroy()
                    self.cancelButton.destroy()
                    if(entryVal == '?'):
                        self.tempGlobal = "Unknown"
                    else:
                        self.tempGlobal = int(entryVal)

                    self.confirmButton.configure(text="YES", command=self.finish_song)
                    self.confirmButton.place(relx=0.4, rely=0.6, anchor="center")

                    self.denyButton = ttk.Button(tk, text="NO", command=self.add_song)
                    self.denyButton.place(relx=0.6, rely=0.6, anchor="center")
                    
                    song = Song(self.tempSongName, self.tempArtistCount, self.tempArtists, self.tempGlobal, self.tempAlbum, 1, self.tempLength, self.tempExpl)
                    self.playlistPrompt.configure(text=f"Is this correct?\n\n\n{song.name}{song.get_expl_string()} ({song.get_length()[0]}:{song.get_length()[1]})\n{song.get_artist_string()}\n{song.album}\nGlobal Listens: {song.listens}\nPlay Count: {song.plays}", justify='left')
                else:
                    self.prompt -= 1
                    self.playlistPrompt.configure(text="Invalid value. Enter a number.\nEnter the number of global listens.")
            case 9: # if the user decides the song info is not correct
                self.destroy_items()
                self.prompt = 0
                self.add_song()
            case 10: # this is for when the song name already exists in the playlist but the user continues anyway
                self.prompt = 2
                self.playlistPrompt.configure(text="Enter number of artists.")
            case _:
                print(f"Something went wrong in class Playlist > add_song\nDefault case checked\nCase value: {self.prompt}")
    def finish_song(self):
        song = Song(self.tempSongName, self.tempArtistCount, self.tempArtists, self.tempGlobal, self.tempAlbum, 1, self.tempLength, self.tempExpl)
        self.list.append(song)
        self.destroy_items()
        self.tempArtists = []
        self.tempArtistCount = 0
        self.tempExpl = 0
        self.prompt = -1
        menu.main()
    def cancel_add_song(self):
        self.destroy_items()
        self.tempSongName = ""
        self.tempArtists = []
        self.tempArtistCount = 0
        self.tempExpl = 0
        self.prompt = -1
        menu.main()

class Menu:
    def __init__(self):
        self.menuPrompt = Label(tk)
        self.menuSplash = Label(tk)
        self.addSongBut = Button(tk)
        self.changePlaylistBut = Button(tk)
        self.quitBut = Button(tk)
        self.saveBut = Button(tk)
        self.confirmBut = Button(tk)
        self.denyBut = Button(tk)
        self.songList = Listbox(tk)
        self.scroll = Scrollbar(tk)
        self.incButton = Button(tk)
        self.quitCheck = False
        self.editBut = Button(tk)
        self.menuEntry = Entry(tk)
        self.songUpdated = False
        self.songToEdit = 0  # this value is the INDEX of the song in the playlist
        self.updateSongCheck = 0 # 0 = don't add/remove artist, 1 = add artist, 2 = remove artist, 3 = failed to remove artist, 4 = toggle explicit
        self.addArtistBut = Button(tk)
        self.removeBut = Button(tk)
        self.sortBut = Button(tk)
    def destroy_items(self):
        self.menuPrompt.destroy()
        self.menuSplash.destroy()
        self.addSongBut.destroy()
        self.changePlaylistBut.destroy()
        self.quitBut.destroy()
        self.confirmBut.destroy()
        self.denyBut.destroy()
        self.songList.destroy()
        self.scroll.destroy()
        self.saveBut.destroy()
        self.incButton.destroy()
        self.editBut.destroy()
        self.menuEntry.destroy()
        self.addArtistBut.destroy()
        self.removeBut.destroy()
        self.sortBut.destroy()
    def main(self):
        playlist.destroy_items()
        self.destroy_items()
        self.quitCheck = False
        self.songUpdated = False
        self.updateSongCheck = 0
        if(len(playlist.list) < 1):
            self.menuPrompt = ttk.Label(tk, text=f"Playlist \"{playlist.playlistName}\" is currently empty. Start by adding a song.")
            self.menuPrompt.place(relx=0.5, rely=0.5, anchor="center")

            self.addSongBut = ttk.Button(tk, text="Add Song", command=playlist.add_song)
            self.addSongBut.place(relx=0.3, rely=0.6, anchor="center")

            self.changePlaylistBut = ttk.Button(tk, text="Change Playlist", command=playlist.select_playlist)
            self.changePlaylistBut.place(relx=0.5, rely=0.6, anchor="center")

            self.quitBut = ttk.Button(tk, text="Quit", command=self.quit)
            self.quitBut.place(relx=0.7, rely=0.6, anchor="center")
        else:
            self.menuPrompt = ttk.Label(tk, text=f"Playlist: {playlist.playlistName}")
            self.menuPrompt.place(relx=0.5, rely=0.2, anchor="center")

            self.songlist_update()

            self.addSongBut = ttk.Button(tk, text="Add Song", command=playlist.add_song)
            self.addSongBut.place(relx=0.3, rely=0.7, anchor="center")

            self.incButton = ttk.Button(tk, text="Increment Song", command=self.increment)
            self.incButton.place(relx=0.5, rely=0.7, anchor="center")

            self.changePlaylistBut = ttk.Button(tk, text="New Playlist", command=playlist.select_playlist)
            self.changePlaylistBut.place(relx=0.7, rely=0.7, anchor="center")

            self.quitBut = ttk.Button(tk, text="Quit", command=self.quit)
            self.quitBut.place(relx=0.7, rely=0.76, anchor="center")

            self.saveBut = ttk.Button(tk, text="Save", command=self.save)
            self.saveBut.place(relx=0.3, rely=0.76, anchor="center")

            self.editBut = ttk.Button(tk, text="Edit Song", command=self.edit)
            self.editBut.place(relx=0.5, rely=0.76, anchor="center")
            
            self.sortBut = ttk.Button(tk, text="Sort")
            self.sortBut.place(relx=0.3, rely=0.82, anchor="center")

            self.removeBut = ttk.Button(tk, text="Remove Song", command=self.remove_song)
            self.removeBut.place(relx=0.5, rely=0.82, anchor="center")
    def quit(self):
        self.quitCheck = True
        if(len(playlist.list) > 0):
            self.destroy_items()

            self.menuPrompt = ttk.Label(tk, text="Would you like to save your playlist data?")
            self.menuPrompt.place(relx=0.5, rely=0.4, anchor="center")

            self.confirmBut = ttk.Button(tk, text="YES", command=self.save)
            self.confirmBut.place(relx=0.4, rely=0.6, anchor="center")

            self.denyBut = ttk.Button(tk, text="NO", command=tk.destroy)
            self.denyBut.place(relx=0.6, rely=0.6, anchor="center")

            self.quitBut = ttk.Button(tk, text="Cancel", command=self.main)
            self.quitBut.place(relx=0.5, rely=0.7, anchor="center")
        else:
            tk.destroy()
    def save(self):
        self.destroy_items()
        with open(f'spotify-shuffle/data/{playlist.playlistName}.dat', 'w', encoding='utf-8') as file:
            for song in playlist.list:
                file.write(f'{song.name}|{song.artistCount}|')
                i = 0
                while(i < int(song.artistCount)):
                    file.write(f'{song.artists[i]}|')
                    i += 1
                file.write(f'{song.listens}|{song.album}|{song.plays}|{song.length}|{song.explicit}\n')
        if(self.quitCheck):
            tk.destroy() # closes window, ends program
        else:
            self.menuSplash = ttk.Label(tk, text="Data saved.")
            self.menuSplash.place(relx=0.5, rely=0.4, anchor="center")

            self.confirmBut = ttk.Button(tk, text="OK", command=self.main)
            self.confirmBut.place(relx=0.5, rely=0.6, anchor="center")
    def increment(self):
        self.menuSplash.destroy()
        if(len(self.songList.curselection()) > 0):
            value = int(playlist.list[self.songList.curselection()[0]].plays)
            value += 1
            playlist.list[self.songList.curselection()[0]].plays = value
            self.songlist_update()
            self.menuSplash = ttk.Label(tk, text=f"Song updated. New play count: {value}")
            self.menuSplash.place(relx=0.5, rely=0.9, anchor="center")
        else:
            self.menuSplash = ttk.Label(tk, text="No song selected. Select a song from the list above.")
            self.menuSplash.place(relx=0.5, rely=0.9, anchor="center")
    def edit(self):
        self.menuSplash.destroy()
        match self.updateSongCheck:
            case 0:
                if(len(self.songList.curselection()) > 0):
                    self.edit_menu()
                else:
                    self.menuSplash = ttk.Label(tk, text="No song selected. Select a song from the list above.")
                    self.menuSplash.place(relx=0.5, rely=0.9, anchor="center")
            case _:
                self.edit_menu()
    def edit_menu(self):
        if(not self.songUpdated):
            self.songToEdit = self.songList.curselection()[0]
            self.updateSongCheck = 0
        song = playlist.list[self.songToEdit]

        self.destroy_items()

        match self.updateSongCheck:
            case 1:
                self.menuSplash = ttk.Label(tk, text="Artist added.")
            case 2:
                self.menuSplash = ttk.Label(tk, text="Artist removed.")
            case 3:
                self.menuSplash = ttk.Label(tk, text="Cannot remove any more artists!")
            case 4:
                self.menuSplash = ttk.Label(tk)
                match song.explicit:
                    case 0:
                        song.explicit = 1
                    case '0':
                        song.explicit = 1
                    case _:
                        song.explicit = 0
            case _:
                self.menuSplash = ttk.Label(tk)
        self.updateSongCheck = 0
        self.menuSplash.place(relx=0.5, rely=0.9, anchor="center")

        prompt = "Select an entry from below, enter its new value, then press Update Info."
        if(self.songUpdated):
            prompt = "Song info updated."

        self.menuPrompt = ttk.Label(tk, text=prompt)
        self.menuPrompt.place(relx=0.5, rely=0.25, anchor="center")

        secs = int(song.length) % 60
        if(secs < 10):
            secs = (f"0{secs}")

        explDisplay = ""
        if(int(song.explicit)):
            explDisplay = " [E]"

        songDataList = []
        songDataList.append(f"                  Title)    {song.name}{explDisplay}")
        i = 0
        while(i < int(song.artistCount)):
            songDataList.append(f"             Artist {i + 1})    {song.artists[i]}")
            i += 1
        songDataList.append(f"             Length)    {int(song.length) // 60}:{secs}")
        songDataList.append(f"             Album)    {song.album}")
        songDataList.append(f" Global Listens)    {song.listens}")
        songDataList.append(f"      Play Count)    {song.plays}")

        self.songList = Listbox(tk, activestyle=DOTBOX, height=8, width=60, selectmode=SINGLE)
        self.songList.place(relx=0.5, rely=0.45, anchor="center")

        for stat in songDataList:
            self.songList.insert(END, stat)

        self.quitBut = ttk.Button(tk, text="Save Changes", command=self.main)
        self.quitBut.place(relx=0.4, rely=0.76, anchor="center")

        self.confirmBut = ttk.Button(tk, text="  Update Info  ", command=self.update_song)
        self.confirmBut.place(relx=0.6, rely=0.76, anchor="center")

        self.menuEntry = ttk.Entry(tk, width=20)
        self.menuEntry.place(relx=0.5, rely=0.63, anchor="center")

        self.addArtistBut = ttk.Button(tk, text="   Add Artist   ", command=self.add_artist)
        self.addArtistBut.place(relx=0.4, rely=0.82, anchor="center")

        self.removeBut = ttk.Button(tk, text="Remove Artist", command=self.remove_artist)
        self.removeBut.place(relx=0.6, rely=0.82, anchor="center")

        self.editBut = ttk.Button(tk, command=self.explicit_toggle, text="Toggle Explicit")
        self.editBut.place(relx=0.5, rely=0.69, anchor="center")
    def update_song(self):
        self.menuSplash.destroy()
        match self.updateSongCheck:
            case 0:
                if(len(self.songList.curselection()) > 0):
                    newVal = self.menuEntry.get()
                    artistCount = int(playlist.list[self.songToEdit].artistCount)
                    if(self.songList.curselection()[0] == 0): # update name
                        playlist.list[self.songToEdit].name = newVal
                    elif(self.songList.curselection()[0] <= artistCount): # update artist name
                        playlist.list[self.songToEdit].change_artist((self.songList.curselection()[0] - 1), newVal)
                    elif(self.songList.curselection()[0] == artistCount + 1): # update song length
                        if(newVal.isdigit() and (int(newVal) > 0)):
                            playlist.list[self.songToEdit].length = newVal
                        else:
                            print("Invalid value entered")
                    elif(self.songList.curselection()[0] == artistCount + 2): # update album
                        playlist.list[self.songToEdit].album = newVal
                    elif(self.songList.curselection()[0] == artistCount + 3): # update global listens
                        if(newVal.isdigit() and (int(newVal) > 0)):
                            playlist.list[self.songToEdit].listens = newVal
                        else:
                            print("Invalid value entered")
                    elif(self.songList.curselection()[0] == artistCount + 4): # update play count
                        if(newVal.isdigit() and (int(newVal) > 0)):
                            playlist.list[self.songToEdit].plays = newVal
                        else:
                            print("Invalid value entered")
                    self.songUpdated = True
                    self.edit()
                else:
                    self.menuSplash = ttk.Label(tk, text="Nothing selected. Select an item from the list above.")
                    self.menuSplash.place(relx=0.5, rely=0.9, anchor="center")
            case 1:
                playlist.list[self.songToEdit].add_artist()
                self.menuSplash = ttk.Label(tk, text="Artist added.")
                self.menuSplash.place(relx=0.5, rely=0.9, anchor="center")
                self.songUpdated = True
                self.edit()
            case 2:
                if(playlist.list[self.songToEdit].remove_artist() == 0):
                    self.updateSongCheck = 3
                self.songUpdated = True
                self.edit()
            case _:
                print(f"Something went wrong in class Menu > update_song\nDefault case checked\nCase value: {self.updateSongCheck}")
                self.songUpdated = True
                self.edit()
    def explicit_toggle(self):
        self.updateSongCheck = 4
        self.songUpdated = True
        self.edit()
    def add_artist(self):
        self.updateSongCheck = 1
        self.update_song()
    def remove_artist(self):
        self.updateSongCheck = 2
        self.update_song()
    def songlist_update(self):
        self.songList.destroy()
        self.scroll.destroy()

        self.songList = Listbox(tk, activestyle=DOTBOX, height=12, width=65, selectmode=SINGLE)
        self.songList.place(relx=0.5, rely=0.45, anchor="center")

        self.scroll = ttk.Scrollbar(tk, orient="vertical")
        self.scroll.config(command=self.songList.yview)
        self.scroll.pack(side="right", fill="both")

        self.songList.config(yscrollcommand=self.scroll.set)

        for song in playlist.list:
            songString = (f"{song.name}{song.get_expl_string()} || {song.get_artist_string()} || {song.album} || Total Plays: {str(song.plays)}")
            self.songList.insert(END, songString)
    def remove_song(self):
        self.menuSplash.destroy()
        self.updateSongCheck += 1
        match self.updateSongCheck:
            case 1:
                if(len(self.songList.curselection()) > 0):
                    self.songToEdit = self.songList.curselection()[0]
                    song = playlist.list[self.songToEdit]
                    self.destroy_items()

                    self.menuPrompt = ttk.Label(tk, text="Are you sure you want to remove this song?")
                    self.menuPrompt.place(relx=0.5, rely=0.25, anchor="center")

                    self.menuSplash = ttk.Label(tk, text=f"{song.name}{song.get_expl_string()} ({song.get_length()[0]}:{song.get_length()[1]})\n{song.get_artist_string()}\n{song.album}\nGlobal Listens: {song.listens}\nPlay Count: {song.plays}", justify='left')
                    self.menuSplash.place(relx=0.5, rely=0.4, anchor="center")

                    self.confirmBut = ttk.Button(tk, text="YES", command=self.remove_song)
                    self.confirmBut.place(relx=0.4, rely=0.6, anchor="center")

                    self.denyBut = ttk.Button(tk, text="NO", command=self.main)
                    self.denyBut.place(relx=0.6, rely=0.6, anchor="center")
                else:
                    self.updateSongCheck = 0
                    self.menuSplash = ttk.Label(tk, text="No song selected. Select a song from the list above.")
                    self.menuSplash.place(relx=0.5, rely=0.9, anchor="center")
            case 2:
                playlist.list.pop(self.songToEdit)
                self.main()
            case _:
                print(f"Something went wrong in class Menu > remove_song\nDefault case checked\nCase value: {self.updateSongCheck}")

# end of definitions
# instantiations:

playlist = Playlist()
menu = Menu()

# begin tk loop

playlist.select_playlist()
tk.mainloop()