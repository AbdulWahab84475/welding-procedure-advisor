import json


def load_welding_database():

    file_path = "data/welding_knowledge.json"

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def get_material(material):

    database = load_welding_database()

    return database["materials"].get(
        material,
        {}
    )


def get_process(process):

    database = load_welding_database()

    return database["processes"].get(
        process,
        {}
    )


def get_consumable(consumable):

    database = load_welding_database()

    return database["consumables"].get(
        consumable,
        {}
    )


def get_inspection(method):

    database = load_welding_database()

    return database["inspection"].get(
        method,
        {}
    )


def get_rules(category):

    database = load_welding_database()

    return database["rules"].get(
        category,
        []
    )


def get_standards():

    database = load_welding_database()

    return database["standards"]
