import boto
from fabric.colors import red
from fabric.api import task
from time import sleep

import logging
logging.basicConfig()
log = logging.getLogger(__name__)



def create_buckets(shortname):
	
	conn = boto.connect_s3()

	buckets = (shortname, shortname + '-staging', shortname + '-dev')
	tagset = boto.s3.tagging.TagSet()
	tagset.add_tag("project",shortname)

	tags = boto.s3.tagging.Tags()
	tags.add_tag_set(tagset)

	for bucket in buckets:
		conn.create_bucket(bucket)
		bucket = conn.get_bucket(bucket)
		bucket.set_tags(tags)
		bucket.make_public(True)


policy = """{{	
"Statement": [
        {{
            "Effect": "Allow",
            "Action": "s3:ListAllMyBuckets",
            "Resource": "arn:aws:s3:::*"
        }},
        {{
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::{0}-dev",
                "arn:aws:s3:::{0}-dev/*",
                "arn:aws:s3:::{0}-staging",
                "arn:aws:s3:::{0}-staging/*",
                "arn:aws:s3:::{0}-prod",
                "arn:aws:s3:::{0}-prod/*"

            ]:
        }}
    ]
}}"""	

def create_user(shortname=None):

	conn = boto.connect_iam()
	response = conn.create_group(shortname)
	response = conn.put_group_policy(shortname, shortname + 'Policy', policy.format(shortname))
	
	# make the user
	response = conn.create_user(shortname)
	response = conn.add_user_to_group(shortname, shortname)
	response = conn.create_access_key(shortname)

	sleep(5) # give the access key a chance to propogate
	create_buckets(shortname=shortname)

@task
def setup(shortname=None):
	"""Setup 3 s3 buckets and tag them.  Pass shortname into task"""
	if shortname is None:
		log.error(red('You must provide a shortname'))
		return

	create_user(shortname);	

