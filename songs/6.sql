SELECT songs.name FROM songs JOIN artists ON songs.artist_id = artists.id WHERE artists.name = 'Post Malone';
ou
SELECT songs.name FROM songs JOIN artists ON artists.id = songs.artist_id WHERE artists.name = 'Post Malone';

