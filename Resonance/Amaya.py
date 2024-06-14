import os
import tempfile
import logging
import requests
from pydub import AudioSegment
from pydub.playback import play
import pyfiglet
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

# Logging configuration
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Function to convert text to audio using the API
def text_to_audio(text, api_key=None, voice="alloy", output_format="mp3"):
    if api_key is None:
        return {"error": "API Key not provided"}

    url = "https://open-ai-text-to-speech1.p.rapidapi.com/"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "open-ai-text-to-speech1.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    data = {
        "model": "tts-1",
        "input": text,
        "voice": voice,
        "output_format": output_format
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            audio_data = response.content
            return {"audio_data": audio_data, "output_format": output_format}
        else:
            return {"error": f"HTTP status {response.status_code}. {response.text}"}
    except requests.RequestException as e:
        return {"error": f"Error converting text to audio: {e}"}

# Function to play the generated audio
def play_audio(audio_data, output_format):
    try:
        # Create a temporary file to save the audio data
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{output_format}')
        temp_file.write(audio_data)
        temp_file.close()

        # Load the audio from the temporary file using pydub
        audio_segment = AudioSegment.from_file(temp_file.name, format=output_format)

        # Play the audio segment
        play(audio_segment)

    except Exception as e:
        logging.error(f"Error playing audio: {e}")
        print(f"{Fore.RED}Error playing audio: {e}")

    finally:
        # Clean up: delete the temporary file
        if temp_file:
            try:
                os.remove(temp_file.name)
            except Exception as e:
                logging.error(f"Error cleaning up temporary file: {e}")

# Function to display the banner
def display_banner():
    nameOfTheScript = "028-Amaya Resonance"
    banner = pyfiglet.figlet_format(nameOfTheScript, font="slant")
    print(Fore.CYAN + banner)
    print(Fore.YELLOW + f"\tScript by J3ff_28 V.1.0\n")
    print(Fore.YELLOW + f"This script is for educational purpose only. The author will not be responsible for any misuse or damage caused by this script.\n")

# Main function to handle the text-to-audio conversion process
def main():
    api_key = "65a73fd492msh82a25951c975330p1a91b5jsn87fe2844ce0a"  # Replace with your actual API key
    display_banner()
    print(Fore.GREEN + "Welcome to the Text-to-Audio Converter")
    print(Fore.GREEN + "======================================\n")

    while True:
        text = input(Fore.CYAN + "Enter the text to convert to audio (or 'exit' to quit): ")
        if text.lower() == 'exit':
            break

        print(Fore.CYAN + "Available voices: alloy, echo, fable, onyx, nova, shimmer")
        voice = input(Fore.CYAN + "Choose a voice (default 'alloy'): ").lower() or "alloy"

        logging.info("Converting text to audio...")
        audio_results = text_to_audio(text, api_key, voice=voice)
        if "error" in audio_results:
            logging.error(f"Error: {audio_results['error']}")
            print(Fore.RED + f"Error: {audio_results['error']}")
        elif "audio_data" in audio_results:
            audio_data = audio_results["audio_data"]
            output_format = audio_results["output_format"]
            logging.info("Playing audio...")
            print(Fore.GREEN + "Playing audio...")
            play_audio(audio_data, output_format)
        else:
            logging.error("Error: Could not retrieve audio data.")
            print(Fore.RED + "Error: Could not retrieve audio data.")

        input(Fore.CYAN + "Press Enter to continue...")

if __name__ == "__main__":
    main()
