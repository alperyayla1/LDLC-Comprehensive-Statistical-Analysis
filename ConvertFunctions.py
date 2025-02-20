def convert_to_int(value):
    try:
        return int(value)
    except ValueError:
        return value
def convert_to_float(value):
    try:
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

#end

