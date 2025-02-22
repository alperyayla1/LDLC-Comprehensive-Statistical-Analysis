def convert_to_int(value):
    try:
        # First try to convert to float (handling commas)
        float_val = convert_to_float(value)
        # Then if successful, convert to int
        if isinstance(float_val, float):
            return int(float_val)
        return value
    except ValueError:
        return value
def convert_to_float(value):
    try:
        # First, handle string values with commas
        if isinstance(value, str):
            value = value.replace(',', '.')
        return float(value)
    except ValueError:
        return value

def clear_db(db):
    DeletingRows = []

    i = 0
    while i < (len(db['test'])):
        checker = 0
        for j in range(4):
            try:
                if isinstance(db['result'].iloc[i + j], int):
                    checker += 1

            except:
                break

        if checker == 4:
            i += 4

        else:
            DeletingRows.append(i)
            i += 1

    db.drop(DeletingRows, inplace=True)
    db.dropna()



