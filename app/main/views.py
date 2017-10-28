from flask import render_template, session, redirect, url_for
from ..models import User
from . import main
from . forms import FsProfileForm
from lxml.builder import E
from lxml import etree
import hashlib
from . profile_habdler import *
from flask import current_app

@main.route('/', methods=['GET', 'POST'])
def index():
    profiles = profileFiller()
    return render_template('profiles.html', profiles=profiles)


@main.route('/new_profile', methods=['GET', 'POST'])
def new_profile():
    form = FsProfileForm()
    if form.validate_on_submit():
        sip_user_id = form.sip_user_id.data
        sip_password = form.sip_password.data
        sip_display_name = form.sip_display_name.data
        voice_main_passwd = form.vm_password.data
        outbound_caller_name = form.outbound_caller_name.data
        outbound_caller_number = form.outbound_caller_number.data
        is_default_profile = int(form.is_default_profile.data)
        createFsProfile(user_id=session['user_id'],
                        sip_user_id=sip_user_id,
                        sip_passwd=sip_password,
                        sip_displ_name=sip_display_name,
                        vm_passwd=voice_main_passwd,
                        out_caller_name=outbound_caller_name,
                        out_caller_number=outbound_caller_number,
                        is_default_profile=is_default_profile)
        return redirect(url_for('main.index'))
    if getUserProfileCount(session['user_id']) > current_app.config['MAX_PROFILE_ALLOWED']:
        return render_template('max_allowed_reached.html', limit_for="profiles")
    return render_template('new_profile.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))


def create_base_directory_xml_doc():
    doc = (
        E.document(
            E.section(name="directory")
        ,type="freeswitch/xml")
    )
    return doc


def hash_password(domain, username, password):
     hash = hashlib.md5()
     hash.update(username + ":" + domain + ":" + password)
     password_hash = hash.hexdigest()
     password_param = "a1-hash"
     return password_param, password_hash


def add_directory_domain_user(doc, domain, username, password):
    password_param = "password"
    # comment out the line below to test with plain text passwords
    #password_param, password = hash_password(domain, username, password)

    section = doc.find("section")

    # search for a domain tag for the indicated domain
    # if the domain is not found, add it
    searchStr = 'domain[@name="{}"]'.format(domain)
    results = section.xpath(searchStr)
    if len(results) > 0:
        dom = results[0]
    else:
        dom = (
            E.domain(
                E.params(
                    E.param(
                        name="dial-string",
                        value='{presence_id=${dialed_user}@${dialed_domain}}${sofia_contact(${dialed_user}@${dialed_domain})}'
                    )
                ),
                E.groups(
                )
            ,name=domain)
        )
        section.append(dom)

    # search for a group tag (for the "default" context)
    # if the group is not found, add it
    groups = dom.find("groups")
    searchStr = 'group[@name="{}"]'.format("default")
    results = groups.xpath(searchStr)
    if len(results) > 0:
       grp = results[0]
    else:
       grp = E.group(
           E.users()
       ,name="default")
       groups.append(grp)

    # add the new user
    grp.find("users").append(
       E.user(
           E.params(
               E.param(name=password_param, value=password)
           )
       ,id=username)
    )

@main.route('/fs_api_directory', methods=['GET', 'POST'])
def fs_directory():
    document = create_base_directory_xml_doc()
    add_directory_domain_user(document, "54.93.196.83", "1011", "pass")

    return etree.tostring(document)



"""    query = "SELECT fs_user_id, password, displayname, vmpasswd, accountcode, outbound_caller_id_name, " \
            "outbound_caller_id_number from extensions where fs_user_id = '" + POST['user'] + "'"
    cursor = db.connect().cursor()
    cursor.execute(query)
    data = cursor.fetchone()
    if data is None:
        xml = 'foo'
        return Response(xml, mimetype='text/xml')"""

"""return User(user_id=data[0],
                username=data[1],
                email=data[2],
                password_hash=data[3],
                role=Role(role_id=data[4], name=data[6], permission=data[7]),
                confirmed=data[5],
                location=data[8],
                about=data[9],
                member_since=data[10],
                last_seen=data[11] )"""