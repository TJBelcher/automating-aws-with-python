# -*- coding: utf-8 -*-

"""Classes for Route 53 domains."""

import uuid


class DomainManager:
    """Manage a Route 53 domain."""

    def __init__(self, session):
        """Create DomainManager object."""
        self.session = session
        self.client = self.session.client('route53')

# possible domain values - note subdomain in second case:
#   kittentest.themdbelchers.com
#   subdomain.kittentest.themdbelchers.com
    def find_hosted_zone(self, domain_name):
        """Find Hosted Zone."""
        paginator = self.client.get_paginator('list_hosted_zones')
        for page in paginator.paginate():
            for zone in page['HostedZones']:
                # test if domain name ends with the zone name,
                # except for the final period
                if domain_name.endswith(zone['Name'][:-1]):
                    return zone
        # if no match of the zone and return of Zone doesn't
        # occur above, then return with find_hosted_zone
        return None

# desired values:
#   domain_name = 'subdomain.kittentest.themdbelchers.com
#   zone_name = 'themdbelchers.com.'
    def create_hosted_zone(self, domain_name):
        """Create Hosted Zone when none present."""
        zone_name = '.'.join(domain_name.split('.')[-2:]) + '.'
        return self.client.create_hosted_zone(
            Name=zone_name,
            CallerReference=str(uuid.uuid4())
        )

    def create_s3_domain_record(self, zone, domain_name, endpoint):
        """Create S3 Domain Record when not present."""
        return self.client.change_resource_record_sets(
            HostedZoneId=zone["Id"],
            ChangeBatch={
                'Comment': 'Creatd by webotron',
                'Changes': [{
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': domain_name,
                            'Type': 'A',
                            'AliasTarget': {
                                'HostedZoneId': endpoint.zone,
                                'DNSName': endpoint.host,
                                'EvaluateTargetHealth': False
                            }
                        }
                    }
                ]
            }
        )
