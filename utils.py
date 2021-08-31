from argparse import ArgumentParser


def get_video_input(input_value):
    if input_value.isnumeric():
        print("using camera %s as input device..." % input_value)
        return int(input_value)

    print("using video '%s' as input..." % input_value)
    return input_value

