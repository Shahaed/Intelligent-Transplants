import csv


def remove_irrelevant_columns(csv_list):
    out = []
    for line in csv_list:
        # replace hist_hypertens_don (Y/N with 1/0)
        line[4] = replace_binary(line[4])
        line[8] = replace_binary(line[4])
        line[9] = replace_binary(line[9])
        blank = False
        for col in line:
            if col == "N/A" or col == "" or col == "NA":
                blank = True
        if not blank:
            out.append(line)
    return out


def replace_binary(letter):
    if letter == 'N':
        return 0
    elif letter == 'Y':
        return 1
    elif letter == 'P':
        return 1
    else:
        return letter


if __name__ == '__main__':
    temp = []
    with open('organTXP.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        temp.append(list(reader))

    cleaned_data = remove_irrelevant_columns(temp[0][2:])

    with open('cleanData.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for line in cleaned_data:
            writer.writerow(line)



