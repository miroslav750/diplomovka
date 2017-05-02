import unicodedata

# own basic SELECT function
# use: select(cursor, columns_to_select, table_name (can add WHERE condition too))
def select(cur, columns, tables):
    cur.execute("""
        SELECT {0}
        FROM {1}
        """.format(columns, tables))
    rows = cur.fetchall()
    return rows


# own UPDATE function
# use: update(cursor, table_name, update_parameter, update_value, where_condition_param, where_condition_value)
def update(cur, table, set_param, set_val, where_param, where_val):
    cur.execute("""
    UPDATE {0}
    SET {1} = {2}
    WHERE {3} = {4}
    """.format(table, set_param, set_val, where_param, where_val))


def delete_apostrophe(string):
    if "'" in str(string):
        return string.replace("'", "")
    else:
        return string


def diacritics(text):
    text = str(text)
    vstup = unicode(text, 'utf-8')
    vstup = unicodedata.normalize('NFKD', vstup)
    output = ''
    for c in vstup:
        if not unicodedata.combining(c):
            output += c
    return output


def loading(full, actual):
    if int(round(full * 0.01)) == actual:
        print 'vlozenych 1 %'
    if int(round(full * 0.02)) == actual:
        print 'vlozenych 2 %'
    if int(round(full * 0.03)) == actual:
        print 'vlozenych 3 %'
    elif int(round(full * 0.1)) == actual:
        print 'vlozenych 10 %'
    elif int(round(full * 0.2)) == actual:
        print 'vlozenych 20 %'
    elif int(round(full * 0.3)) == actual:
        print 'vlozenych 30 %'
    elif int(round(full * 0.4)) == actual:
        print 'vlozenych 40 %'
    elif int(round(full * 0.5)) == actual:
        print 'vlozenych 50 %'
    elif int(round(full * 0.6)) == actual:
        print 'vlozenych 60 %'
    elif int(round(full * 0.7)) == actual:
        print 'vlozenych 70 %'
    elif int(round(full * 0.8)) == actual:
        print 'vlozenych 80 %'
    elif int(round(full * 0.9)) == actual:
        print 'vlozenych 90 %'
    elif int(round(full * 0.99)) == actual:
        print 'vlozenych 100 % ---> {0} zaznamov'.format(full)
