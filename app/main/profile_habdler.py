from .. import db
from ..utils import query_builder as qbuilder

cursor = db.connect().cursor()

"""return list of list of profiles data"""
def profileFiller():
    cursor.execute(
        qbuilder.build_query("select sip_user_id, sip_displayname, outbound_caller_id_name, outbound_caller_id_number, is_default_profile from demo.fs_profiles"))
    return cursor.fetchall()

"""return count of profiles usage for particular user is"""
def getUserProfileCount(user_id):
    cursor.execute(qbuilder.build_query("select count(*) from demo.fs_profiles where user_id = {0}".format(user_id)))
    return cursor.fetchone()[0]


"""
in params:
    user_id
    sip_user_id
    sip_passwd
    sip_displ_name
    vm_passwd
    out_caller_name
    out_caller_number
    is_default_profile
"""
def createFsProfile(**kwargs):
    return cursor.execute(qbuilder.build_query("insert into demo.fs_profiles(user_id, " \
                                        "sip_user_id, " \
                                        "sip_password, " \
                                        "sip_displayname, " \
                                        "vmpasswd, " \
                                        "accountcode, " \
                                        "outbound_caller_id_name, " \
                                        "outbound_caller_id_number, " \
                                        "is_default_profile) "\
                                        "values ('{0}', '{1}', '{2}', '{3}', '{4}', '{0}', '{5}', '{6}', '{7}');" \
                                        "commit".format(kwargs.get('user_id', None),
                                                        kwargs.get('sip_user_id', None),
                                                        kwargs.get('sip_passwd', None),
                                                        kwargs.get('sip_displ_name', None),
                                                        kwargs.get('vm_passwd', None),
                                                        kwargs.get('out_caller_name', None),
                                                        kwargs.get('out_caller_number', None),
                                                        kwargs.get('is_default_profile', None)
                                                        )
                                            )
                        )