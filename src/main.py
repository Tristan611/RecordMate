from datetime import datetime

async def main():

    print("🎵 RecordMate gestart")

    print("🎙 Audio opnemen...")

    audio_file = "recordings/sample.wav"

    print("✅ Audio opgenomen.")

    print()

    print("🔍 Nummer herkennen...")

    track = await recognition_manager.recognize(audio_file)

    print(f"✅ {track.artist} - {track.title}")

    print()

    print("🎧 Spotify zoeken...")

    spotify_track = spotify_search.search_track(
        track.artist,
        track.title
    )

    print("✅ Track gevonden.")

    print()

    print("▶ Spotify playback starten...")

    spotify_player.play(spotify_track.uri)

    print("✅ Playback gestart.")

if __name__ == "__main__":
    main()
