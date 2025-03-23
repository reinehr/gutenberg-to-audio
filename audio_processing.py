import os
import glob
from pydub import AudioSegment
from pydub.silence import detect_silence
import concurrent.futures
from functools import partial

def process_single_mp3(mp3_file, book_id, silence_threshold, min_silence_duration,
                       expected_seconds_per_1000_chars, length_tolerance):
    """Process a single MP3 file to detect silence and length issues."""
    txt_dir = f"books/{book_id}/txt"

    # Extract chapter and section IDs from filename
    filename = os.path.basename(mp3_file)
    parts = filename.split('_')
    if len(parts) < 4:
        print(f"Couldn't parse chapter and section IDs from filename: {filename}")
        return None

    chapter_id = parts[2]
    section_id = parts[3].split('.')[0]

    # Find corresponding text file
    txt_file = f"{txt_dir}/clean_text_{chapter_id}_{section_id}.txt"

    try:
        # Load audio file
        audio = AudioSegment.from_mp3(mp3_file)
        audio_duration_sec = len(audio) / 1000  # Total duration in seconds

        # Check if audio is not empty
        if len(audio) == 0:
            print(f"Warning: {mp3_file} appears to be empty (0 length)")
            return {
                'filename': filename,
                'chapter_id': chapter_id,
                'section_id': section_id,
                'silent_segments': [],
                'duration': 0,
                'has_silence_issue': False,
                'has_length_issue': True,
                'text_length': 0 if not os.path.exists(txt_file) else len(open(txt_file, 'r').read()),
                'expected_duration': 0,
                'duration_diff_percent': 100
            }

        # Detect silent segments
        silent_segments = detect_silence(
            audio,
            min_silence_len=min_silence_duration,
            silence_thresh=silence_threshold
        )

        # Convert milliseconds to seconds for display
        silent_segments_sec = [(start/1000, end/1000, (end-start)/1000)
                              for start, end in silent_segments]

        # Check text length if text file exists
        length_issue = False
        text_length = 0
        expected_duration = 0
        duration_diff_percent = 0

        if os.path.exists(txt_file):
            with open(txt_file, 'r') as f:
                text = f.read()
                text_length = len(text)
                expected_duration = (text_length / 1000) * expected_seconds_per_1000_chars

                # Calculate difference percentage
                duration_diff = abs(audio_duration_sec - expected_duration)
                duration_diff_percent = (duration_diff / expected_duration) * 100

                # Check if difference exceeds tolerance
                if duration_diff / expected_duration > length_tolerance:
                    length_issue = True

        # If silent segments found or length issue detected, return info
        if silent_segments or length_issue:
            issue_info = {
                'filename': filename,
                'chapter_id': chapter_id,
                'section_id': section_id,
                'silent_segments': silent_segments_sec,
                'duration': audio_duration_sec,
                'has_silence_issue': len(silent_segments) > 0
            }

            # Add length information if available
            if os.path.exists(txt_file):
                issue_info.update({
                    'text_length': text_length,
                    'expected_duration': expected_duration,
                    'duration_diff_percent': duration_diff_percent,
                    'has_length_issue': length_issue
                })

            return issue_info

        return None  # No issues found

    except Exception as e:
        print(f"Error processing {mp3_file}: {e}")
        return None

def detect_silence_in_mp3_parallel(book_id, silence_threshold=-50, min_silence_duration=3000, silence_results=None,
                          expected_seconds_per_1000_chars=5.0, length_tolerance=0.2, max_workers=None):
    """
    Analyze MP3 files in parallel to detect sections with silence and length issues.
    """
    # Path to audio files
    audio_dir = f"books/{book_id}/audio"

    # Find MP3 files to analyze
    if silence_results:
        # Only check files that were previously identified with silence issues
        mp3_files = [f"{audio_dir}/gutenberg_{book_id}_{file_info['chapter_id']}_{file_info['section_id']}.mp3"
                     for file_info in silence_results]
        print(f"Rechecking {len(mp3_files)} previously identified files with silence issues")
    else:
        # Find all MP3 files
        mp3_files = glob.glob(f"{audio_dir}/*.mp3")
        # Sort files by chapter and section
        mp3_files.sort()
        print(f"Found {len(mp3_files)} MP3 files to analyze")

    # Create a partial function with fixed parameters
    process_file = partial(
        process_single_mp3,
        book_id=book_id,
        silence_threshold=silence_threshold,
        min_silence_duration=min_silence_duration,
        expected_seconds_per_1000_chars=expected_seconds_per_1000_chars,
        length_tolerance=length_tolerance
    )

    # Process files in parallel
    files_with_issues = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_file, mp3_files))

        # Filter out None results and add to issues list
        for result in results:
            if result:
                files_with_issues.append(result)

                # Print information about the issue
                chapter_id = result['chapter_id']
                section_id = result['section_id']

                if result.get('has_silence_issue', False):
                    silent_segments = result['silent_segments']
                    print(f"Chapter {chapter_id}, Section {section_id} contains {len(silent_segments)} silent segments:")
                    for start, end, duration in silent_segments:
                        print(f"  Silent from {start:.2f}s to {end:.2f}s (duration: {duration:.2f}s)")

                if result.get('has_length_issue', False):
                    print(f"Chapter {chapter_id}, Section {section_id} has length mismatch:")
                    print(f"  Text length: {result.get('text_length', 'N/A')} chars, expected duration: {result.get('expected_duration', 'N/A'):.2f}s")
                    print(f"  Actual duration: {result['duration']:.2f}s, difference: {result.get('duration_diff_percent', 'N/A'):.2f}%")

    return files_with_issues
