import csv
import re
from io import StringIO

def timeformat_srt(time):
    hours = time // 3600
    minutes = (time - hours * 3600) // 60
    seconds = time - hours * 3600 - minutes * 60
    milliseconds = (time - int(time)) * 1000
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{int(milliseconds):03d}"


def timeformat_vtt(time):
    hours = time // 3600
    minutes = (time - hours * 3600) // 60
    seconds = time - hours * 3600 - minutes * 60
    milliseconds = (time - int(time)) * 1000
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.{int(milliseconds):03d}"


def write_file(subtitle, output_file, encoding='utf-8'):
    with open(output_file, 'w', encoding=encoding) as f:
        f.write(subtitle)


def get_srt(segments):
    output = ""
    for i, segment in enumerate(segments):
        output += f"{i + 1}\n"
        output += f"{timeformat_srt(segment['start'])} --> {timeformat_srt(segment['end'])}\n"
        if segment['text'].startswith(' '):
            segment['text'] = segment['text'][1:]
        output += f"{segment['text']}\n\n"
    return output


def get_vtt(segments):
    output = "WebVTT\n\n"
    for i, segment in enumerate(segments):
        output += f"{i + 1}\n"
        output += f"{timeformat_vtt(segment['start'])} --> {timeformat_vtt(segment['end'])}\n"
        if segment['text'].startswith(' '):
            segment['text'] = segment['text'][1:]
        output += f"{segment['text']}\n\n"
    return output


def get_txt(segments):
    output = ""
    for i, segment in enumerate(segments):
        if segment['text'].startswith(' '):
            segment['text'] = segment['text'][1:]
        output += f"{segment['text']}\n"
    return output


def parse_srt(file_path):
    """Reads SRT file and returns as dict"""
    with open(file_path, 'r', encoding='utf-8') as file:
        srt_data = file.read()

    data = []
    blocks = srt_data.split('\n\n')

    for block in blocks:
        if block.strip() != '':
            lines = block.strip().split('\n')
            index = lines[0]
            timestamp = lines[1]
            sentence = ' '.join(lines[2:])

            data.append({
                "index": index,
                "timestamp": timestamp,
                "sentence": sentence
            })
    return data


def parse_vtt(file_path):
    """Reads WebVTT file and returns as dict"""
    with open(file_path, 'r', encoding='utf-8') as file:
        webvtt_data = file.read()

    data = []
    blocks = webvtt_data.split('\n\n')

    for block in blocks:
        if block.strip() != '' and not block.strip().startswith("WebVTT"):
            lines = block.strip().split('\n')
            index = lines[0]
            timestamp = lines[1]
            sentence = ' '.join(lines[2:])

            data.append({
                "index": index,
                "timestamp": timestamp,
                "sentence": sentence
            })

    return data


def get_serialized_srt(dicts):
    output = ""
    for dic in dicts:
        output += f'{dic["index"]}\n'
        output += f'{dic["timestamp"]}\n'
        output += f'{dic["sentence"]}\n\n'
    return output


def get_serialized_vtt(dicts):
    output = "WebVTT\n\n"
    for dic in dicts:
        output += f'{dic["index"]}\n'
        output += f'{dic["timestamp"]}\n'
        output += f'{dic["sentence"]}\n\n'
    return output


def safe_filename(name):
    from app import _args
    INVALID_FILENAME_CHARS = r'[<>:"/\\|?*\x00-\x1f]'
    safe_name = re.sub(INVALID_FILENAME_CHARS, '_', name)
    if not _args.colab:
        return safe_name
    # Truncate the filename if it exceeds the max_length (20)
    if len(safe_name) > 20:
        file_extension = safe_name.split('.')[-1]
        if len(file_extension) + 1 < 20:
            truncated_name = safe_name[:20 - len(file_extension) - 1]
            safe_name = truncated_name + '.' + file_extension
        else:
            safe_name = safe_name[:20]
    return safe_name


def srt_string_to_csv(srt_data, title_name):
    # Regex to match SRT file patterns
    srt_pattern = re.compile(r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?=\n\d+\n|\Z)", re.S)

    # Use StringIO to read the string as a file
    srt_file = StringIO(srt_data)

    srt_content = srt_file.read()
    subtitles = srt_pattern.findall(srt_content)

    # Create CSV data as string
    csv_data = StringIO()
    csv_writer = csv.writer(csv_data)
        # Write the required headers

    
    # for subtitle in subtitles:
    #     index, start_time, end_time, text = subtitle
    #     text = text.replace('\n', ' ')  # Replace newlines in the subtitle text with a space
    #     csv_writer.writerow([index, start_time, end_time, text])
    
    # csv_content = csv_data.getvalue()
    for subtitle in subtitles:
        index, start_time, end_time, text = subtitle
        text = text.replace('\n', ' ')  # Replace newlines in the subtitle text with a space
        
        # Write the subtitle data
        csv_writer.writerow(['', index, '', ''])
        csv_writer.writerow(['', f"{start_time} -->{end_time}", '', ''])
        csv_writer.writerow(['', text, '', ''])
        csv_writer.writerow(['', '', '', ''])  # Add an empty row for spacing
        
    csv_content = csv_data.getvalue()

    return csv_content