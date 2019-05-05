import subprocess

# Encoding used for Unicode data
UNICODE_ENCODING = "utf8"

# Marker for program piped input
STDIN_PIPE_DASH = '-'

# Approximate chunk length (in bytes) used by BigArray objects (only last chunk and cached one are held in memory)
BIGARRAY_CHUNK_SIZE = 1024 * 1024

# Compress level used for storing BigArray chunks to disk (0-9)
BIGARRAY_COMPRESS_LEVEL = 9