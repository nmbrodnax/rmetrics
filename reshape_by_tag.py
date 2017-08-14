# Reshaping data from the Stack Exchange API

import csv


def main():
    srcfieldnames = ['tags', 'view_count', 'answer_count', 'last_activity_date',
                     'creation_date', 'link', 'title', 'site', 'question_id',
                     'topic', 'search_type']
    with open('by_topic.csv', 'r') as sourcefile:
        reader = csv.DictReader(sourcefile, srcfieldnames)
        next(reader, None)
        questions = []
        for i in reader:
            questions.append(i)
    print(len(questions))
    print(questions[0]['tags'])
    mystr = questions[0]['tags']
    print(type(mystr[2:-2].split("', '")))

    outfieldnames = ['tag', 'question_count', 'view_count', 'answer_count']
    with open('by_tag.csv', 'w') as outfile:
        writer = csv.DictWriter(outfile, outfieldnames)
        writer.writeheader()
        question_ids = []
        tag_names = []
        tags = {}
        for q in questions:
            if q.get('question_id') not in question_ids:
                question_ids.append(q.get('question_id'))
                qtags = q['tags'][2:-2].split("', '")
                for t in qtags:
                    if t not in tag_names:
                        tag_names.append(t)
                        tags[t] = {'tag': t, 'question_count': 1,
                                   'view_count': int(q['view_count']),
                                   'answer_count': int(q['answer_count'])}
                    else:
                        tags[t]['question_count'] += 1
                        tags[t]['view_count'] += int(q['view_count'])
                        tags[t]['answer_count'] += int(q['answer_count'])
        for tag in tags:
            writer.writerow(tags.get(tag))
    print(tag_names)


if __name__ == '__main__':
    main()
