from django.contrib.auth.models import User

#
# 内置的User模型拥有以下的字段：
#
# username： 用户名。150个字符以内。可以包含数字和英文字符，以及_、@、+、.和-字符。不能为空，且必须唯一！
# first_name：歪果仁的first_name，在30个字符以内。可以为空。
# last_name：歪果仁的last_name，在150个字符以内。可以为空。
# email：邮箱。可以为空。
# password：密码。经过哈希过后的密码。
# groups：分组。一个用户可以属于多个分组，一个分组可以拥有多个用户。groups这个字段是跟Group的一个多对多的关系。
# user_permissions：权限。一个用户可以拥有多个权限，一个权限可以被多个用户所有用。和Permission属于一种多对多的关系。
# is_staff：是否可以进入到admin的站点。代表是否是员工。
# is_active：是否是可用的。对于一些想要删除账号的数据，我们设置这个值为0就可以了，而不是真正的从数据库中删除。
# is_superuser：是否是超级管理员。如果是超级管理员，那么拥有整个网站的所有权限。
# last_login：上次登录的时间。
# date_joined：账号创建的时间。
