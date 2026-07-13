import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "src")
    )
)

from recognition.acoustid import AcoustIDRecognizer


def main():
    recognizer = AcoustIDRecognizer()

    file_path = "recordings/test200.wav"
    matches = recognizer.recognize_file(file_path)

    if not matches:
        print("No matches found")
        return

    print("Matches found:")
    print("-" * 40)

    for match in matches[:5]:
        print(f"Score  : {match['score']}")
        print(f"Artist : {match['artist']}")
        print(f"Title  : {match['title']}")
        print(f"MBID   : {match['recording_id']}")
        print("-" * 40)


if __name__ == "__main__":
    main()