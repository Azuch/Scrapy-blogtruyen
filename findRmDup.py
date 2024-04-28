import os
import hashlib
import asyncio

async def find_duplicates(root_dir):
    file_checksums = {}
    duplicates = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            with open(file_path, "rb") as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            if file_hash in file_checksums:
                duplicates.append((file_path, file_checksums[file_hash]))
            else:
                file_checksums[file_hash] = file_path

    return duplicates

async def remove_duplicates(duplicates):
    for duplicate in duplicates:
        file_path, original_path = duplicate
        print(f"File '{file_path}' is a duplicate of '{original_path}'")
    
    confirmation = input("Do you want to delete these files? (yes/no): ").lower()
    if confirmation == "yes":
        for duplicate in duplicates:
            file_path, original_path = duplicate
            try:
                os.remove(file_path)
                print(f"File '{file_path}' removed (duplicate of '{original_path}')")
            except OSError as e:
                print(f"Error: {e.strerror} - {file_path}")
    else:
        print("Deletion cancelled.")

async def main():
    root_directory = input("Enter dir: ")
    duplicates = await find_duplicates(root_directory)
    await remove_duplicates(duplicates)

# Run the script asynchronously
asyncio.run(main())

