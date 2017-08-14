# Reshaping data from the Stack Exchange API

import csv


def main():
    fieldnames = ['tags', 'view_count', 'answer_count', 'last_activity_date',
                  'creation_date', 'link', 'title', 'site', 'question_id',
                  'topic', 'search_type']
    with open('by_topic.csv', 'r') as sourcefile:
        reader = csv.DictReader(sourcefile, fieldnames)
        next(reader, None)
        all_tags = []
        all_questions = []
        for i in reader:
            [all_tags.append(t) for t in i.get('tags') if t not in all_tags]
            [all_questions.append(q) for q in [i.get('question_id')] if q not in
             all_questions]

    print('Tags: ' + str(len(all_tags)))
    print('Questions: ' + str(len(all_questions)))


if __name__ == '__main__':
    main()
