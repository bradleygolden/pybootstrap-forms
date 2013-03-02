import re

ATTRIBUTE_SANATIZE = re.compile(r'[^A-Za-z0-9\-_\[\]]')


def _attribute_sanatize(val):
    return ATTRIBUTE_SANATIZE.sub('', val)


def _value_to_id(name, val):
    return name + "_" + _attribute_sanatize(val)


class Field(object):

    def __init__(self, name, label=None, help=None, current=None, attrs=None):
        self.name = name
        self.field_type = "text"
        self.label = label
        self.attrs = attrs
        self.help = help
        self.current = current

    def attrs_string(self):
        if self.attrs is None:
            return ""
        else:
            return " ".join(("%s='%s'" % (k, v) for k, v in self.attrs.items()))

    def render_label(self):
        return '<label for="%s">%s</label>' % (self.name, self.label) if self.label else ""

    def render_field(self):
        return '<input type="%s" id="%s" name="%s" %s>' % (
            self.field_type, self.name, self.name, self.attr_string())

    def render_description(self):
        if self.help:
            return '<span class="help-block">%s</span>' % (self.help,)
        else:
            return ""

    def render_group(self):
        params = (self.render_label(), self.render_field(),
                  self.render_description())
        return """
            <div class="control-group">
                %s
                %s
                %s
            </div>""" % params


class Checkbox(Field):

    def __init__(self, name, value, **kwargs):
        self.value = value
        super(Checkbox, self).__init__(name, **kwargs)
        self.label = None

    def render_field(self):
        template = """
            <label class="checkbox">
                <input type="checkbox" name="%s" id="%s" value="%s" %s %s>
                %s
            </label>"""
        return template % (self.name, self.name, self.value, "checked='checked'" if self.current == self.value else "", self.attr_string(), self.label)


class TextArea(Field):

    def __init__(self, name, rows=3, current="", **kwargs):
        self.rows = rows
        super(TextArea, self).__init__(name, current=current, **kwargs)

    def render_field(self):
        return '<textarea id="%s" name="%s" rows="%d" %s>%s</textarea>' % (
            self.name, self.name, self.rows, self.attr_string(), self.current)


class Multiple(Field):

    def __init__(self, name, values, **kwargs):
        self.values = values
        super(Multiple, self).__init__(name, **kwargs)


class Dropdown(Multiple):

    def render_field(self):
        options = ("<option value='%s' %s>%s</option>" % (val, "selected='selected'" if val == self.current else "", label) for val, label in self.values)
        return """
            <select name="%s" id="%s" %s>
                %s
            </select>
        """ % (self.name, self.name, self.attr_string(), "\t\n".join(options))


class Radios(Multiple):

    def render_field(self):
        template = """
            <label class="radio">
                <input type="radio" name="%s" id="%s" value="%s" %s>
                %s
            </label>
        """
        radios = (template % (self.name, _value_to_id(self.name, val), val, "checked='checked'" if val == self.current else "", label) for (val, label) in self.values)
        return "\n".join(radios)
