import os


def get_number_of_levels():
    files = os.listdir(os.path.join('data', 'levels'))
    count = 0
    for file in files:
        if file.startswith('map') and file.endswith('.txt'):
            count += 1
    return count
