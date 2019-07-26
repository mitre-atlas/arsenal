import json as json_library
import re


def json(parser, blob):
    matched_facts = []
    if blob:
        structured = json_library.loads(blob)
        if isinstance(structured, (list,)):
            for i, entry in enumerate(structured):
                matched_facts.append((dict(fact=parser['property'], value=entry.get(parser['script']), set_id=i)))
        elif isinstance(structured, (dict,)):
            dict_match = parser['script']
            dict_match = dict_match.split(',')
            match = structured
            for d in dict_match:
                match = match[d]
            matched_facts.append((dict(fact=parser['property'], value=match, set_id=0)))
        else:
            matched_facts.append((dict(fact=parser['property'], value=structured[parser['script']], set_id=0)))
    return matched_facts


def regex(parser, blob):
    matched_facts = []
    for i, v in enumerate([m for m in re.findall(parser['script'], blob)]):
        matched_facts.append(dict(fact=parser['property'], value=v, set_id=i))
    return matched_facts


def line(parser, blob):
    return [dict(fact=parser['property'], value=f.strip(), set_id=0) for f in blob.split('\n') if f]

