import argparse
import datetime
import os

from breakdown import get_breakdown
from receipt import generate_image


TARGET_DIRNAME = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
os.makedirs(TARGET_DIRNAME, exist_ok=True)


def add_to_target(entity, image):
    used_datetime = datetime.datetime.strptime(
        f'{entity["이용일"]} {entity["이용시간"]}',
        '%Y-%m-%d %H:%M',
    )
    dinner_criteria = 16 * 60 + 30
    minute_of_the_day = used_datetime.hour * 60 + used_datetime.minute
    is_dinner = 'L' if minute_of_the_day < dinner_criteria else 'D'
    filename = f'{used_datetime.strftime("%Y%m%dT%H%M%S")}_{is_dinner}.png'
    image.save(f'{TARGET_DIRNAME}/{filename}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('breakdown')
    args = parser.parse_args()

    for entity in get_breakdown(args.breakdown):
        print(entity)

        if datetime.date.fromisoformat(entity['이용일']).weekday() in [5, 6]:
            # skip weekend
            continue

        image = generate_image(entity)
        add_to_target(entity, image)


if __name__ == '__main__':
    main()
