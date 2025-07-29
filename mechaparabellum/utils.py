def modification_time(path):
    return path.lstat().st_mtime

def get_newest(log_files):
    newest = max(filter(lambda p: p.lstat().st_size > 100_000, log_files), key=modification_time)
    return newest
