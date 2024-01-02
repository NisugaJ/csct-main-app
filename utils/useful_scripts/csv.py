import random
from pprint import pprint


def get_item_name_and_type():
    import csv
    from itertools import groupby

    base_dir = "data/external-datasets"
    items = {}

    with open(f'{base_dir}/20210310Nutrientdatabase-utf-8.csv', encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # Group rows by data type of 'age' column
        grouped = groupby(
            reader,
            key=lambda x: type(
                x['Item No.']
            ).__name__
        )

        for dtype, group in grouped:
            print(
                f"Data Type: {dtype}"
                )

            for row in group:
                # print(f"{row['Item name']}; {row['Type of protein']}")

                raw_type = "".join(
                    row['Type of protein']
                    ).lower()

                if raw_type.find("animal") != -1:
                    item_type = 0  # "ANIMAL_BASED"
                elif raw_type.find("plant") != -1:
                    item_type = 1  # "PLANT_BASED"
                else:
                    item_type = -1  # "NOT_FOUND"
                    continue

                if item_type != -1:
                    items[row['Item No.']] = {"id": row["Item No."], "name": row['Item name'], "label": item_type}

    with open(f'{base_dir}/plant-based-food-items.csv', encoding="utf-8") as f:
        reader = csv.DictReader(f)

        i = 0
        for row in reader:
            print(f"name:{row['name']}, label:{row['label']}")
            items[f"plant-based-{i}"] = {"id": f"plant-based-{i}", "name": row['name'], "label": row['label']}
            i += 1


    keys = list(items.keys())
    random.shuffle(keys)

    train_data_keys = keys[:int(len(keys)*0.8)]
    test_data_keys = keys[int(len(keys)*0.8):]

    with open(f'{base_dir}/train.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write header row
        writer.writerow(['id', 'name', 'label'])

        for key in train_data_keys:
            # Write data row
            writer.writerow([items[key]["id"], items[key]["name"], items[key]["label"]])

        csvfile.close()

    with open(f'{base_dir}/test.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write header row
        writer.writerow(['id', 'name', 'label'])

        for key in test_data_keys:
            # Write data row
            writer.writerow([items[key]["id"], items[key]["name"], items[key]["label"]])


