import boto
from fabric.colors import red
from fabric.api import task

import logging
logging.basicConfig()
log = logging.getLogger(__name__)

@task
def setup(shortname=None):
	"""Setup 3 s3 buckets and tag them.  Pass shortname into task"""
	if shortname is None:
		log.error(red('You must provide a shortname'))

	conn = boto.connect_s3()

	buckets = (shortname, shortname + '_staging', shortname + '_dev')
	tagset = boto.s3.tagging.TagSet()
	tagset.add_tag("project",shortname)

	tags = boto.s3.tagging.Tags()
	tags.add_tag_set(tagset)

	for bucket in buckets:
		conn.create_bucket(bucket)
		bucket = conn.get_bucket(bucket)
		bucket.set_tags(tags)