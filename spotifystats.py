import csv

class Song:
    def __init__(self, name, artistCount, artists, listens, album, plays, length):
        self.name = name
        self.artistCount = artistCount
        self.artists = artists
        self.listens = listens
        self.album = album
        self.plays = plays
        self.length = length
    def display(self):
        mins = int(self.length) // 60
        secs = int(self.length) % 60
        print(f'\n{self.name} ({mins}:{secs})')
        i = 0
        while(i < int(self.artistCount)):
            if(i == int(self.artistCount) - 1):
                print(f'{self.artists[i]}', end='')
            else:
                print(f'{self.artists[i]}, ', end='')
            i += 1
        print(f'\n{self.album}\nGlobal Listens: {self.listens}\nTimes Played: {self.plays}')   

def open_playlist(name):
    playlist = []
    try:
        open(f'spotify-shuffle/{name}.txt', 'r', encoding='utf-8')
    except:
        print(f'Playlist not found, creating new playlist file.')
        open(f'spotify-shuffle/{name}.txt', 'x', encoding='utf-8')
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
    return playlist

def add_song(oldPlaylist):
    newPlaylist = oldPlaylist
    loop = True
    while(loop):
        print(f'Enter the song name:')
        tempName = input('NAME> ')
        check = search_for_song(oldPlaylist, tempName)
        if(len(check) > 0):
            print(f'The song {tempName} was found in the playlist already. Continue anyway? (Y/N)')
            yesno = input('Y/N> ')
            if(not yesno.lower() == 'y'):
                return newPlaylist
        print(f'Enter the number of artists:')
        artCount = int(input('ARTIST COUNT> '))
        tempArtists = []
        i = 0
        while(i < artCount):
            print(f'Enter artist {i + 1}:')
            tempArtName = input(f'ARTIST {i + 1}> ')
            tempArtists.append(tempArtName)
            i += 1
        print(f'Enter the minutes and seconds of the song:')
        mins = int(input('MINUTES> '))
        secs = int(input('SECONDS> '))
        print(f'Enter the album the song is on:')
        tempAlbum = input('ALBUM> ')
        print(f'Enter the number of global listens:')
        tempListens = input('LISTENS> ')
        tempLength = (mins * 60) + secs
        song = Song(tempName, artCount, tempArtists, tempListens, tempAlbum, 1, tempLength)
        print(f'\nDoes this look right? (Y/N)')
        song.display()
        choice = input('Y/N> ')
        if(choice == 'Y' or choice == 'y'):
            loop = False
    print(f'Song added.')
    newPlaylist.append(song)
    return newPlaylist

def increment_song(oldPlaylist, song):
    newPlaylist = oldPlaylist
    for tune in newPlaylist:
        if(tune == song):
            value = int(tune.plays)
            value += 1
            tune.plays = value
    return newPlaylist

def display_songs(playlist):
    print(f'\nSonglist:')
    for song in playlist:
        song.display()

def search_for_song(playlist, songToFind):
    matching = []
    for song in playlist:
        if(song.name.lower() == songToFind.lower()):
            matching.append(song)
    return matching

def update_file(playlist, name):
    with open(f'spotify-shuffle/{name}.txt', 'w', encoding='utf-8') as file:
        for song in playlist:
            file.write(f'{song.name}|{song.artistCount}|')
            i = 0
            while(i < int(song.artistCount)):
                file.write(f'{song.artists[i]}|')
                i += 1
            file.write(f'{song.listens}|{song.album}|{song.plays}|{song.length}\n')

# end of definitions

print(f'Enter playlist name:')
playlistName = input('NAME> ')
playlist = open_playlist(playlistName)

while(True):
    print(f'~~~~~~~~~~\nCurrent Playlist: {playlistName}\n~~~~~~~~~~\nChoose an option.\nIf you\'re finished, please use the quit option!\n1) Increment Song\n2) Add Song\n3) Change Playlist\n4) List Songs\n5) Quit')
    option = input('CHOICE> ')

    match option:
        case '1':
            print(f'\nEnter song name:')
            songInc = input('SONG> ')
            matching = search_for_song(playlist, songInc)

            if(len(matching) == 0):
                print(f'No song found with name {songInc}. Please use the Add Song option to add it.')
            elif(len(matching) == 1):
                print(f'Found song.')
                matching[0].display()
                print(f'\nIncremented song play count.\nNew count: {int(matching[0].plays) + 1}')
                playlist = increment_song(playlist, matching[0])
            else:
                print(f'Multiple songs found named {songInc}.\nPlease select the song you wish to increment below.')
                i = 0
                while(i < len(matching)):
                    print(f'{i}) ', end='')
                    matching[i].display()
                conflictChoice = input('CHOICE> ')
                print(f'Incremented song play count.\nNew count: {int(matching[int(conflictChoice)].plays) + 1}')
                playlist = increment_song(playlist, matching[int(conflictChoice)])
        case '2':
            playlist = add_song(playlist)
        case '3':
            print(f'\nEnter playlist name:')
            playlistName = input('NAME> ')
            playlist = open_playlist(playlistName)
        case '4':
            display_songs(playlist)
        case '5':
            update_file(playlist, playlistName)
            break
        case _:
            print(f'Invalid choice selected.')

    update_file(playlist, playlistName)
    print(f'\nPress enter to continue.')
    input()