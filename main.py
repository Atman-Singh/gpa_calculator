import PyPDF2


def main():
    grades, weightages = extract_data('transcript.pdf')
    # del grades[42:48]
    # del weightages[42:48]
    # grades = grades[6:]
    # weightages = weightages[6:]
    print(grades)
    print(weightages)
    print('GPA:', average(grades, weightages))


def extract_data(pdf):
    grades = []
    weightages = []
    for idx, word in enumerate(format_pdf(pdf)):
        if check_if_slash(word):
            if check_if_grade(word):
                grades.append(convert_to_four_point(format_grade(word)))
        if check_if_weightage(word):
            weightages.append(float(word)*2)
    return grades, weightages


def check_if_slash(word):
    return word.__contains__('/') and not word.lower().__contains__('cr')


def check_if_grade(word):
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for number in numbers:
        if word.__contains__(str(number)):
            return True
    return False


def check_if_weightage(word):
    return word == '0.5000' or word == '1.0000'


def format_pdf(pdf):
    reader = PyPDF2.PdfReader(pdf)
    text = reader.pages[0].extract_text().split()

    for idx, word in enumerate(text):
        if word.lower() == 'term':
            text = text[idx:]
            break
    return text


def format_grade(grade):
    for idy, char in enumerate(grade):
        if char == '/':
            grade = grade[idy + 1:]
    return int(grade)


def convert_to_four_point(grade):
    x_to_id = {}
    y = [1.0, 1.0, 1.3, 1.3, 1.3, 1.7, 1.7, 1.7, 2.0, 2.0, 2.0, 2.0, 2.3, 2.3, 2.3, 2.7, 2.7, 2.7, 3.0, 3.0, 3.0, 3.0,
         3.3, 3.3, 3.3, 3.7, 3.7, 3.7, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0]
    for count, idx in enumerate(range(65, 101)):
        x_to_id.update({idx: y[count]})
    if grade in x_to_id:
        return x_to_id[grade]
    else:
        return 0


def average(grades, weightages):
    total_points = 0
    total_credits = 0
    for idx, grade in enumerate(grades):
        total_points += grade * weightages[idx]
        total_credits += weightages[idx]
    return round(total_points / total_credits, 2)


if __name__ == '__main__':
    main()
