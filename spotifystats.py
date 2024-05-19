from tkinter import *
from tkinter import ttk
import csv

tk = Tk(className=" Spotify Shuffle")
tk.geometry("500x500")

class Song:
    def __init__(self, name, artistCount, artists, listens, album, plays, length):
        self.name = name
        self.artistCount = artistCount
        self.artists = artists
        self.listens = listens
        self.album = album
        self.plays = plays
        self.length = length

class Playlist:
    def __init__(self):
        self.playlistEntry = Entry(tk)
        self.playlistPrompt = Label(tk)
        self.confirmButton = Button(tk)
        self.denyButton = Button(tk)
        self.cancelButton = Button(tk)
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
    def destroy_items(self):
        self.playlistEntry.destroy()
        self.playlistPrompt.destroy()
        self.confirmButton.destroy()
        self.denyButton.destroy()
        self.cancelButton.destroy()
    def try_playlist(self):
        self.playlistName = self.playlistEntry.get()
        self.destroy_items()
        try:
            open(f'spotify-shuffle/{self.playlistName}.txt', 'r', encoding='utf-8')
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
            open(f'spotify-shuffle/{name}.txt', 'x', encoding='utf-8')
        playlist = []
        with open(f'spotify-shuffle/{name}.txt', 'r', encoding='utf-8') as file:
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
                song = Song(tempName, artCount, tempArtists, tempListens, tempAlbum, tempPlays, tempLength)
                playlist.append(song)
        self.list = playlist
        menu.main()
    def select_playlist(self):
        self.destroy_items()
        menu.destroy_items()

        self.playlistPrompt = ttk.Label(tk, text="Enter playlist name:")
        self.playlistPrompt.place(relx=0.5, rely=0.3, anchor="center")

        self.playlistEntry = ttk.Entry(tk, width=20)
        self.playlistEntry.place(relx=0.5, rely=0.45, anchor="center")

        self.confirmButton = ttk.Button(tk, text="OK", command=self.try_playlist)
        self.confirmButton.place(relx=0.5, rely=0.6, anchor="center")
    def add_song(self):
        self.prompt += 1
        match self.prompt:
            case 0:
                menu.destroy_items()
                self.add_song()
            case 1:
                self.playlistPrompt = ttk.Label(tk, text="Enter song name:")
                self.playlistPrompt.place(relx=0.5, rely=0.3, anchor="center")
            
                self.playlistEntry = ttk.Entry(tk, width=20)
                self.playlistEntry.place(relx=0.5, rely=0.45, anchor="center")

                self.confirmButton = ttk.Button(tk, text="OK", command=self.add_song)
                self.confirmButton.place(relx=0.5, rely=0.6, anchor="center")
                
                self.cancelButton = ttk.Button(tk, text="Cancel", command=self.cancel_add_song)
                self.cancelButton.place(relx=0.5, rely=0.7, anchor="center")
            case 2:
                self.tempSongName = self.playlistEntry.get()
                self.playlistPrompt.configure(text="Enter number of artists:")
            case 3:
                if((self.playlistEntry.get().isdigit() == True) and (int(self.playlistEntry.get()) > 0)):
                    self.tempArtistCount = int(self.playlistEntry.get())
                    self.playlistPrompt.configure(text=f"Enter artist {self.counter}:")
                else:
                    self.prompt -= 1
                    self.playlistPrompt.configure(text="Invalid value. Enter a number.\nEnter number of artists:")
            case 4:
                self.tempArtists.append(self.playlistEntry.get())
                if(not self.tempArtistCount == self.counter):
                    self.counter += 1
                    self.prompt -= 1
                    self.playlistPrompt.configure(text=f"Enter artist {self.counter}:")
                else:
                    self.counter = 1
                    self.playlistPrompt.configure(text="Enter the minute length of the song:")
            case 5: 
                if((self.playlistEntry.get().isdigit() == True) and (int(self.playlistEntry.get()) > -1)):
                    self.tempMinute = self.playlistEntry.get()
                    self.playlistPrompt.configure(text="Enter the second length of the song:")
                else:
                    self.prompt -= 1
                    self.playlistPrompt.configure(text="Invalid value. Enter a number.\nEnter the minute length of the song:")
            case 6:
                if((self.playlistEntry.get().isdigit() == True) and (int(self.playlistEntry.get()) > -1)):
                    self.tempLength = (int(self.tempMinute) * 60) + int(self.playlistEntry.get())
                    self.playlistPrompt.configure(text="Enter the album the song is on:")
                else:
                    self.prompt -= 1
                    self.playlistPrompt.configure(text="Invalid value. Enter a number.\nEnter the second length of the song:")
            case 7:
                self.tempAlbum = self.playlistEntry.get()
                self.playlistPrompt.configure(text="Enter the number of global listens:")
            case 8:
                if((self.playlistEntry.get().isdigit() == True) and (int(self.playlistEntry.get()) > -1)):
                    self.tempGlobal = int(self.playlistEntry.get())

                    mins = int(self.tempLength) // 60
                    secs = int(self.tempLength) % 60
                    allArtists = ""
                    i = 0
                    while(i < len(self.tempArtists) - 1):
                        allArtists = allArtists + self.tempArtists[i] + ", "
                        i += 1
                    allArtists = allArtists + self.tempArtists[i]
                    if(secs < 10):
                        secs = (f'0{secs}')

                    self.confirmButton.configure(text="YES", command=self.finish_song)
                    self.confirmButton.place(relx=0.4, rely=0.6, anchor="center")

                    self.denyButton = ttk.Button(tk, text="NO", command=self.add_song)
                    self.denyButton.place(relx=0.6, rely=0.6, anchor="center")

                    self.playlistEntry.destroy()
                    self.cancelButton.destroy()

                    self.playlistPrompt.configure(text=f"Does this look correct?\n\n{self.tempSongName} ({mins}:{secs})\n{allArtists}\n{self.tempAlbum}\nGlobal Listens: {self.tempGlobal}")
                else:
                    self.prompt -= 1
                    self.playlistPrompt.configure(text="Invalid value. Enter a number.\nEnter the number of global listens:")
            case 9:
                self.destroy_items()
                self.prompt = 0
                self.add_song()
            case _:
                print(f"Something went wrong in class Playlist > add_song\nDefault case checked\nCase value: {self.prompt}")
    def finish_song(self):
        song = Song(self.tempSongName, self.tempArtistCount, self.tempArtists, self.tempGlobal, self.tempAlbum, 1, self.tempLength)
        self.list.append(song)
        self.destroy_items()
        self.tempArtists = []
        self.tempArtistCount = 0
        self.prompt = -1
        menu.main()
    def cancel_add_song(self):
        self.destroy_items()
        self.tempArtists = []
        self.tempArtistCount = 0
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
    def main(self):
        playlist.destroy_items()
        self.destroy_items()
        self.quitCheck = False
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
        with open(f'spotify-shuffle/{playlist.playlistName}.txt', 'w', encoding='utf-8') as file:
            for song in playlist.list:
                file.write(f'{song.name}|{song.artistCount}|')
                i = 0
                while(i < int(song.artistCount)):
                    file.write(f'{song.artists[i]}|')
                    i += 1
                file.write(f'{song.listens}|{song.album}|{song.plays}|{song.length}\n')
        if(self.quitCheck):
            tk.destroy()
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
        else:
            self.menuSplash = ttk.Label(tk, text="No song selected. Select a song from the list below.")
            self.menuSplash.place(relx=0.5, rely=0.85, anchor="center")
    def songlist_update(self):
        self.songList.destroy()
        self.scroll.destroy()

        self.songList = Listbox(tk, activestyle=DOTBOX, height=12, width=60, selectmode=SINGLE)
        self.songList.place(relx=0.5, rely=0.45, anchor="center")

        self.scroll = ttk.Scrollbar(tk, orient="vertical")
        self.scroll.config(command=self.songList.yview)
        self.scroll.pack(side="right", fill="both")

        self.songList.config(yscrollcommand=self.scroll.set)

        for song in playlist.list:
            songString = song.name + " | "
            i = 0
            while(i < len(song.artists) - 1):
                songString = songString + song.artists[i] + ", "
                i += 1
            songString = songString + song.artists[i] + " | "
            songString = songString + song.album + " | Total Plays: " + str(song.plays)
            self.songList.insert(END, songString)

# end of definitions
# instantiations:

playlist = Playlist()
menu = Menu()

# begin tk loop

playlist.select_playlist()
tk.mainloop()