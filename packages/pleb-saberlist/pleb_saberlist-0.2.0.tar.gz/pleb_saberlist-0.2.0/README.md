# SaberList

SaberList is a tool for generating custom Beat Saber playlists based on a player's performance data from Beat Leader.

## Resources

* Beat Leader [swagger](https://api.beatleader.xyz/swagger/index.html), [GitHub](https://github.com/BeatLeader)
* Score Saber [swagger](https://docs.scoresaber.com/), [Github](https://github.com/ScoreSaber) (backend remains closed-source)
* Beat Saver [swagger](https://api.beatsaver.com/docs/), [GitHub](https://github.com/beatmaps-io/beatsaver-main)

## Features

- Fetches player scores from Beat Leader API
- Generates difficulty-based playlists
- Automatically selects a random cover image for each playlist
- Avoids duplicating songs across multiple playlist generations
- Caches player data for faster subsequent runs

## Playlist generations

The program has the following playlist generation modes:

### Replay songs by age

```sh
saberlist_replay_bl
```

This will generate a playlist of oldest songs that you have previously played, ostensibly because you probably can improve your score. It will add low star songs, mid star songs, and high star songs to the playlist. That way you can warm up on the low star songs, and then move on to the harder songs. Each time you run this command it will generate a completely new playlist.

## Covers

The program will automatically select a random cover image for each playlist. The cover image is selected from the `covers` directory. We suggest using a latent diffusion model to generate random cover images for your playlists.

## Configuration

The program uses a `playlist_history.json` file to keep track of previously used songs and cover images. This ensures that subsequent runs generate fresh playlists without duplicates.

## Output

The program generates:

1. A `.bplist` file containing the playlist data in JSON format
2. Console output listing the songs included in the playlist

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.