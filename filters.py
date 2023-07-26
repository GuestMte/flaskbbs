import hashlib

def email_hash(email):
  return hashlib.md5(email.lower().encode("utf-8")).hexdigest()#将用户的电子邮件地址转换为一个固定长度的哈希值，这个哈希值可以用于生成用户头像的 Gravatar URL