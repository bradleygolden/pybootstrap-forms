class Form(object):

    def __init__(self, name=None, *args):
        self.name = name
        self.fields = args

    def render(self):
        groups = (field.render_group() for field in self.fields)
        legend = "<legend>" + self.name + "</legend>" if self.name else ""
        return """
            <fieldset>
                %s
                %s
            </fieldset>
        """ % (legend, "\t\n".join(groups))

