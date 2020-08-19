import django_ixctl.models as models
import django_peeringdb.models.concrete as pdb_models

def test_org_permission_id(db, pdb_data, account_objects):
    org = account_objects.org
    org.remote_id = 123
    assert org.permission_id == 123

def test_org_tag(db, pdb_data, account_objects):
    org = account_objects.org
    org.slug = "new slug"
    assert org.tag == "new slug"

def test_org_display_name(db, pdb_data, account_objects):
    org = account_objects.org
    assert org.display_name == "Personal"
    assert account_objects.orgs[1].display_name == "ORGtest-2"

def test_org_sync_single_change(db, pdb_data, account_objects):
    org = account_objects.org
    data = {
        "id": org.id,
        "name": "changed name", 
        "slug": org.slug, 
        "personal": org.personal
    }
    org = models.Organization.sync_single(data, account_objects.user, None)
    org.refresh_from_db()
    assert org.name == "changed name"
    assert org.slug == "test"

def test_org_sync_single_new(db, pdb_data, account_objects):
    org = account_objects.org
    data = {
        "id": 3,
        "name": "org3-test", 
        "slug": "org3", 
        "personal": False
    }
    new_org = models.Organization.sync_single(data, account_objects.user, None)
    assert new_org.name == "org3-test"
    assert new_org.slug == "org3"
    assert models.OrganizationUser.objects.filter(org=new_org.id, user=account_objects.user.id).exists()

def test_org_sync_multiple(db, pdb_data, account_objects):
    orgs = [{
                "id": 3,
                "name": "org3-test", 
                "slug": "org3", 
                "personal": False
            },
            {
                "id": 4,
                "name": "org4-test", 
                "slug": "org4", 
                "personal": False
            }
        ]
    synced = models.Organization.sync(orgs, account_objects.user, None)
    assert models.Organization.objects.filter(name="org3-test").exists()
    assert models.Organization.objects.filter(name="org4-test").exists()
    # Assert the synced orgs are the only orgs that the user belongs to now
    org_names = set([orguser.org.name for orguser in account_objects.user.org_set.all()])
    assert org_names == set(["org3-test", "org4-test"])

def test_instance(db, pdb_data, account_objects):
    instance = account_objects.ixctl_instance
    assert instance.org == account_objects.org
    assert instance.__str__() == f"{account_objects.org} 1"

def test_instance_create(db, pdb_data, account_objects):
    org = account_objects.orgs[1]
    instance = models.Instance.get_or_create(org)
    assert instance.org == org
    assert instance.org.status == "ok"

def test_orguser(db, pdb_data, account_objects):
    orguser = models.OrganizationUser.objects.filter(org=account_objects.org, user=account_objects.user).first()
    assert orguser.__str__() == "user_test <test@localhost>"

def test_apikey(db, pdb_data, account_objects):
    user = account_objects.user
    models.APIKey.objects.create(key="abcdefgh",user=user)
    user.refresh_from_db()
    assert type(user.key_set.first()) == models.APIKey

def test_ix(db, pdb_data, account_objects):
    ix = models.InternetExchange.create_from_pdb(
        account_objects.ixctl_instance, account_objects.pdb_ixlan
    )

    assert ix.pdb_id == account_objects.pdb_ixlan.id
    assert ix.pdb == account_objects.pdb_ixlan

def test_ixmember(db, pdb_data, account_objects):

    net = account_objects.pdb_net
    netixlan = pdb_models.NetworkIXLan.objects.filter(ixlan_id=239).first()
    # The following line also runs the
    # create_from_pdb method of the InternetExchangeMember
    # corresonding to the IX.
    ix = models.InternetExchange.create_from_pdb(
        account_objects.ixctl_instance, account_objects.pdb_ixlan
    )

    ixmember = ix.member_set.first()
    assert ixmember.pdb_id == netixlan.id
    assert ixmember.pdb == netixlan

    assert ixmember.name == netixlan.net.name
    assert ixmember.display_name == netixlan.net.name

    ixmember.name = "override"
    assert ixmember.display_name == "override"



