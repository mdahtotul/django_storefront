from django.core.exceptions import ValidationError


def validate_file_size(file):
    filesize = file.size
    max_size_kb = 50

    if filesize > max_size_kb * 1024:
        raise ValidationError(f"Maximum file size is {max_size_kb} KB")