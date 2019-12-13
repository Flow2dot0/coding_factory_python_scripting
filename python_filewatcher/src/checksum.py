import hashlib


def checksum_file(filename):
    """Create checksum of a file
    :return: sha256 string
    """
    sha256 = hashlib.sha256()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)
    return sha256.hexdigest()
