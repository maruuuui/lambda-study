import base64
import io
import six
import uuid

def decode_base64_file(data, org_name):
    """
    Fuction to convert base 64 to readable IO bytes and auto-generate file name with extension
    :param data: base64 file input
    :param org_name: もともとのファイル名
    :return: tuple containing IO bytes file and filename
    """
    # Check if this is a base64 string
    if isinstance(data, six.string_types):
        # Check if the base64 string is in the "data:" format
        if 'data:' in data and ';base64,' in data:
            # Break out the header from the base64 content
            header, data = data.split(';base64,')

        # Try to decode the file. Return validation error if it fails.
        try:
            decoded_file = base64.b64decode(data)
        except TypeError:
            TypeError('invalid_image')

        # Generate directory name:
        dir_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.

        complete_file_name = "%s/%s" % (dir_name, org_name,)

        return io.BytesIO(decoded_file), complete_file_name
    else:
        print("not base64",data)
