# CodeTemplate
本项目实现了一个类似Django的模板引擎，语法类似。用于生成代码。实现了变量，For，IF这三个功能。

### 变量

```
{{%VarName%}}
```

用{{%%}}括起来的代表变量,模板引擎会根据传进来的数据来替换这个变量

### 循环

```
{% for it in xlist %}
{{%it%}}
{% endfor %}
```

循环我只实现了for,不过我觉的应该足够了。需要{%for python语句%}{% endfor %}括起来。模板引擎会将循环输出括起来的内容。for循环里面可以嵌套for循环。

### 条件

```
{% if 条件 %}
内容
{% endif %}
```

模板引擎会根据条件是否满足来决定是否显示里面的内容。



## 例子

```python
from CodeTemplate import Template
code = '''
struct {{%Name%}}
{
{% for it in Rules %}
    {{%it['Type']%}} {{%it['Name']%}};
{% endfor %}
    vector<string> Other;

    static ARGS FromStringList(int argc, char *argv[])
    {
        ARGS ret ;
        {% for it in Rules %}
        {% if it['IsPrefix']==0 and it['Type'] == 'bool' %}
        ret.{{%it['Name']%}} = false;
        {% endif %}
        {% endfor %}

        int i=0;
        while(++i<argc)
        {
            string current = argv[i];
            {% for it in Rules %}
            {% if it['IsPrefix']==1 and it['Type'] == 'string' %}
            if(current.compare("{{%it['ArgName']%}}") == 0){
                if(++i>=argc) throw exception("After {{%it['ArgName']%}} Is Nothing");
                ret.{{%it['Name']%}} = argv[i];
                continue;
            }
            {% endif %}
            {% endfor %}

            {% for it in Rules %}
            {% if it['IsPrefix']==0 and it['Type'] == 'bool' %}
            if(current.compare("{{%it['ArgName']%}}") == 0 ){
                ret.{{%it['Name']%}} = true;
                continue;
            }
            {% endif %}
            {% endfor %}

            {% for it in Rules %}
            {% if it['ArgName']=="" %}
            if(ret.{{%it['Name']%}}.empty())
            {
                ret.{{%it['Name']%}} = current;
                continue;
            }
            {% endif %}
            {% endfor %}
            ret.Other.push_back(current);
        }
        return ret;
    }

};
'''
#<RULE IsPrefix="0" ArgName="" Name="FileName" Type="string"/>
codecontext = {
    'Name':'ARGS',
    'Rules':[
        {'IsPrefix':0,'ArgName':'','Name':"FileName",'Type':'string'},
        {'IsPrefix':1,'ArgName':'-x','Name':"XMLFileName",'Type':'string'},
        {'IsPrefix':1,'ArgName':'-cs','Name':"CSFileName",'Type':'string'},
        {'IsPrefix':0,'ArgName':'-c','Name':"CFlag",'Type':'bool'},
        {'IsPrefix':0,'ArgName':'-b','Name':"BFlag",'Type':'bool'},
    ]
}
print(Template(code)(codecontext))
```

运行该程序将会生成一下C++代码

```c++
struct ARGS
{
    string FileName;
    string XMLFileName;
    string CSFileName;
    bool CFlag;
    bool BFlag;
    vector<string> Other;
    static ARGS FromStringList(int argc, char *argv[])
    {
        ARGS ret ;
        ret.CFlag = false;
        ret.BFlag = false;
        int i=0;
        while(++i<argc)
        {
            string current = argv[i];
            if(current.compare("-x") == 0){
                if(++i>=argc) throw exception("After -x Is Nothing");
                ret.XMLFileName = argv[i];
                continue;
            }
            if(current.compare("-cs") == 0){
                if(++i>=argc) throw exception("After -cs Is Nothing");
                ret.CSFileName = argv[i];
                continue;
            }
            if(current.compare("-c") == 0 ){
                ret.CFlag = true;
                continue;
            }
            if(current.compare("-b") == 0 ){
                ret.BFlag = true;
                continue;
            }
            if(ret.FileName.empty())
            {
                ret.FileName = current;
                continue;
            }
            ret.Other.push_back(current);
        }
        return ret;
    }
};
```

本例是为了测试变量，for循环以及if语句。其实如果使用python的高阶函数可以去掉本例的所有if块。如下:

```python
from CodeTemplate import Template
code = '''
struct {{%Name%}}
{
    {% for it in Rules %}
    {{%it['Type']%}} {{%it['Name']%}};
    {% endfor %}
    vector<string> Other;

    static ARGS FromStringList(int argc, char *argv[])
    {
        ARGS ret ;
        {% for it in filter(lambda it:it['IsPrefix']==0 and it['Type'] == 'bool',Rules) %}
        ret.{{%it['Name']%}} = false;
        {% endfor %}

        int i=0;
        while(++i<argc)
        {
            string current = argv[i];
            {% for it in filter(lambda it:it['IsPrefix']==1 and it['Type'] == 'string',Rules) %}
            if(current.compare("{{%it['ArgName']%}}") == 0){
                if(++i>=argc) throw exception("After {{%it['ArgName']%}} Is Nothing");
                ret.{{%it['Name']%}} = argv[i];
                continue;
            }
            {% endfor %}

            {% for it in filter(lambda it: it['IsPrefix']==0 and it['Type'] == 'bool',Rules) %}
            if(current.compare("{{%it['ArgName']%}}") == 0 ){
                ret.{{%it['Name']%}} = true;
                continue;
            }
            {% endfor %}

            {% for it in filter(lambda it:it['ArgName']=="",Rules) %}
            if(ret.{{%it['Name']%}}.empty())
            {
                ret.{{%it['Name']%}} = current;
                continue;
            }
            {% endfor %}
            ret.Other.push_back(current);
        }
        return ret;
    }
};
'''
#<RULE IsPrefix="0" ArgName="" Name="FileName" Type="string"/>
codecontext = {
    'Name':'ARGS',
    'Rules':[
        {'IsPrefix':0,'ArgName':'','Name':"FileName",'Type':'string'},
        {'IsPrefix':1,'ArgName':'-x','Name':"XMLFileName",'Type':'string'},
        {'IsPrefix':1,'ArgName':'-cs','Name':"CSFileName",'Type':'string'},
        {'IsPrefix':0,'ArgName':'-c','Name':"CFlag",'Type':'bool'},
        {'IsPrefix':0,'ArgName':'-b','Name':"BFlag",'Type':'bool'},
    ]
}
print(Template(code)(codecontext))

```

改成这样的话会简洁很多。当然输出的内容是不变的。

