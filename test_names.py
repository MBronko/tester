import os


def get_test_names(path: str) -> list[tuple[str, str]]:
    names = {}

    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            filename, ext = os.path.splitext(file)

            if filename not in names:
                names[filename] = {
                    '.in': '',
                    '.out': '',
                }

            names[filename][ext] = file

    return sorted([(val['.in'], val['.out']) for key, val in names.items() if val['.in']], key=lambda x: x[0])
