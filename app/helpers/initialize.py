from mongoengine import NotUniqueError

from app.data.prepare import get_scraping_meta_data


def initialize():
    print("Initializing database with metadata")

    objects_to_be_saved = []
    objects_to_be_updated = []

    for meta_item in get_scraping_meta_data():

        try:
            # for list_page_meta in meta_item.pages:
            #     if ListPageMeta.objects(link=list_page_meta.link).count() == 1:
            #         objects_to_be_updated.append(list_page_meta)
            #     else:
            #         objects_to_be_saved.append(list_page_meta)
            #
            # if len(objects_to_be_saved) > 0:
            #     ListPageMeta.objects.insert(objects_to_be_saved, load_bulk=False)
            # if len(objects_to_be_updated) > 0:
            #     print(objects_to_be_updated)
            #     ListPageMeta.objects.insert(objects_to_be_updated)

            meta_item.save()

        except NotUniqueError as not_unique_error:
            print(not_unique_error)
            continue
