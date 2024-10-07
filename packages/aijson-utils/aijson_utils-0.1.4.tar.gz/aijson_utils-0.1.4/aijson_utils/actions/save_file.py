import os

from aijson import register_action


@register_action(
    cache=False,
)
def save_file(contents: str, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    print(path)
    print(contents)
    with open(path, "w") as f:
        f.write(contents)
        print('done')
