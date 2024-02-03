import yt_dlp
import subprocess

def download_and_play_audio(search_query, output_directory='songs', output_file=''):
    
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [
            # {
            #     'key': 'FFmpegVideoConvertor',  # Fix the typo here
            #     'preferedformat': 'mp3',
            # }
            ],
            'outtmpl': f'{output_directory}/%(id)s.mp3',
            'default_search': 'ytsearch',
        }

        # Create a YouTube downloader object
        outtmpl_value = ydl_opts.get('outtmpl', '')
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f'{search_query}', download=True)
            

        if 'entries' in result:
                # If it's a playlist, take the first video's ID
            video_id = result['entries'][0]['id']
        else:
            # If it's a single video, take its ID
            video_id = result['id']
        downloaded_filename = f'{output_directory}/{video_id}.mp3'
        output_file = downloaded_filename
        print(f"Video ID for '{search_query}': {video_id}")
        print(f"Audio for '{search_query}' downloaded successfully as '{downloaded_filename}'.")

        subprocess.run(["start", "", downloaded_filename], shell=True)
        # Open the file with the default system player
    # return downloaded_filename

    except Exception as e:
        print(f"Error: {e}")

# Example usage

# Example usage
def play(query):

    download_and_play_audio(query, output_file="")
    # subprocess.run(["start", "", musicLOC], shell=True)


