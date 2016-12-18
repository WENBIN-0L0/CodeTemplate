from CodeTemplate import Template
text = '''
public class {{%ClassName%}}
{
    {% for it in pl%}
    public {{%it['type']%}} {{%it['name']%}} { get; set; }
    {% endfor %}
}
'''

_context = {
    'ClassName': "ClassA",
    'pl':[{'type':'string','name':'A'},{'type':'string','name':'B'},{'type':'string','name':'C'},]
}
print(Template(text)(_context))