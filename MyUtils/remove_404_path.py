from DataControl.Repo import load_all_downloaded_item, session
from Obj.Image import Image
from  os.path import exists

items = load_all_downloaded_item(Image)

for item in items:
    if item.file_path == "404":
        print("ooh!!! " + item.file_path)
        session.delete(item)
session.commit()
