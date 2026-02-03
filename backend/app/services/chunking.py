def chunk_segments(segments, max_words=500):
    """
    Groups small Whisper segments into larger semantic chunks 
    based on word count (~500 words) while respecting segment boundaries.
    """
    chunks = []
    current_chunk = {
        "text": "",
        "start": 0.0,
        "end": 0.0,
        "segments": []
    }
    word_count = 0

    for i, seg in enumerate(segments):
        # Initialize start time for new chunk
        if not current_chunk["segments"]:
            current_chunk["start"] = seg["start"]

        seg_text = seg["text"].strip()
        words = seg_text.split()
        seg_word_count = len(words)

        # Check if adding this segment exceeds max_words
        # (But always add at least one segment to avoid empty chunks)
        if word_count + seg_word_count > max_words and current_chunk["segments"]:
            # Finalize current chunk
            current_chunk["end"] = segments[i-1]["end"]
            current_chunk["text"] = current_chunk["text"].strip()
            chunks.append(current_chunk)

            # Start new chunk
            current_chunk = {
                "text": "",
                "start": seg["start"],
                "end": 0.0,
                "segments": []
            }
            word_count = 0

        # Add segment to current chunk
        current_chunk["text"] += " " + seg_text
        current_chunk["segments"].append(seg)
        word_count += seg_word_count

    # Append the last chunk if it exists
    if current_chunk["segments"]:
        current_chunk["end"] = segments[-1]["end"]
        current_chunk["text"] = current_chunk["text"].strip()
        chunks.append(current_chunk)

    return chunks
