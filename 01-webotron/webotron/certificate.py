# -*- coding: utf-8 -*-

"""Classes for ACM Certificates."""


class CertificateManager:
    """Manage an ACM Certificate."""

    def __init__(self, session):
        """Manage an ACM Certificate."""
        self.session = session
        self.client = self.session.client('acm', region_name='us-east-1')

    def cert_matches(self, cert_arn, domain_name):
        """Check if certificate matches."""
        cert_details = self.client.describe_certificate(
                CertificateArn=cert_arn
        )
        # note - the following statement returns a list of values,
        # (e.g. ['themdbelchers.com', '*.themdbelchers.com'] and later
        # each is referred to as 'name'
        alt_names = cert_details['Certificate']['SubjectAlternativeNames']
        for name in alt_names:
            if name == domain_name:
                # print("path1")
                # print("name = ", name)
                # print("domain_name = ", domain_name)
                return True
            # if name in certificate name list = * & domain_name ends with the
            # same string as the end of name then consider it a wildcard match
            if name[0] == '*' and domain_name.endswith(name[1:]):
                # print("path2")
                # print("name = ", name)
                # print("domain_name = ", domain_name)
                return True
            # print("path3")
            # print("name = ", name)
            # print("domain_name = ", domain_name)
        return False

    def find_matching_cert(self, domain_name):
        """Find matching certificate."""
        paginator = self.client.get_paginator('list_certificates')
# paginate thru only issued certs to find a match against our
# domain_name for bucket - either exact: themdbelchers.com
#   or wildcard: #.themdbelchers.com like kittentest.themdbelchers.com
        for page in paginator.paginate(CertificateStatuses=['ISSUED']):
            for cert in page['CertificateSummaryList']:
                if self.cert_matches(cert['CertificateArn'], domain_name):
                    return cert

        return None
