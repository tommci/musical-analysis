I have noticed that the Spotify shuffle algorithm doesn't feel random. Inspired by this, I put together a script in python to track the number of times a song has played in a playlist, as well as some basic info and data about songs from any music application. I intend on adding some analysis features to step towards an answer to my original question: is there any pattern to Spotify's shuffling algorithm?

The project is not directly focused on Spotify. In fact, any music application could be used and analyzed with this code.
As I have evolved in my programming journey I have realized there are better ways to handle a project of this nature, specifically utilizing Spotify's developer API. I currently have a seperate project in the works for that very purpose.
As a result, this project has become more of a general catch-all musical analysis and tracking system.

spotifystats-old only utilizes the csv library, but is no longer maintained or updated by me.
Otherwise, tkinter is needed to utilize the full GUI of the project (within the main musicalstats.py file).

Run the python script from the same directory that any playlist txt files are stored!
