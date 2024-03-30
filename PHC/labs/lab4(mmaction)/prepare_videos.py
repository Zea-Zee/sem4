import os


def rename_videos(path: str, prefix: str, exclude='') -> None:
    # print(os.getcwd())
    files = os.listdir(path)
    index = 1
    for file in files:
        if exclude and exclude in file:
            continue
        if '.mp4' == file[-4:]:
            old_path = os.path.join(path, file)
            new_path = os.path.join(path, f"{prefix}_{index}.mp4")
            os.rename(old_path, new_path)
            index += 1


# def train_test_split(path: str, partition: float):

# def make_labels


# rename_videos('./media/train', 'karate_fighting')
rename_videos('./media/train', 'teaching', 'karate_fighting')
