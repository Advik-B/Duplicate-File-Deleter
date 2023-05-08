from utility.classes import QuickHasher

print(QuickHasher.from_file("requirements.txt").file_hash)