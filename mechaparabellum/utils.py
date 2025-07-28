def get_newest(log_files):
    newest = max(filter(lambda p: p.lstat().st_size > 100_000, log_files), key=lambda p: p.lstat().st_mtime)
    return newest
