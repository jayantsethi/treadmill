from treadmill.infra.setup import base_provision


class LDAP(base_provision.BaseProvision):
    def __init__(
            self,
            name,
            vpc_id,
            domain,
            region_name
    ):
        super(LDAP, self).__init__(
            name=name,
            vpc_id=vpc_id,
            domain=domain,
            region_name=region_name
        )