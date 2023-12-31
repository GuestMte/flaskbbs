from wtforms import Form

class BaseForm(Form):
  @property#装饰器，转化为只读属性
  def messages(self):
    message_list = []
    if self.errors:
      for errors in self.errors.values():
        message_list.extend(errors)
    return message_list