from DataControl.Repo import load_all_downloaded_item, session
from Obj.Image import Image
from  os.path import exists

items = load_all_downloaded_item(Image)

for item in items:
    if item.file_path and not exists(item.file_path):
        print("ooh!!! " + item.file_path)
        # item.file_path = None
        # session.commit()
    else:
        # print("yes!")
        pass
