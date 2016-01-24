#!/usr/bin/python
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
DOCUMENTATION = '''
---
module: data_pipeline
short_description: Manage AWS Data Pipelines
requirements: [ boto ]
description:
     - Allows creating or removing AWS Data Pipelines. Previously created pipelines can be activated or deactivated.
version_added: "2.0"
options:
  name:
    description:
      - The name for the pipeline is mandatory when pipeline is created. You can use the same name for multiple pipelines associated with your AWS account, because AWS Data Pipeline assigns each pipeline a unique pipeline identifier. When deleting a pipeline either name or pipeline_id can be used but not both.
    required: false
  unique_id:
    description:
      - A unique identifier, only used if state is 'present'. This identifier is not the same as the pipeline_id which is assigned by AWS Data Pipeline. You are responsible for defining the format and ensuring the uniqueness of this identifier. Used to ensure idempotency during repeated calls to the module.
    required: false
  pipeline_id:
    description:
      - A unique identifier which is assigned by AWS when the pipeline is created. In this module it can be used when state is 'absent' or 'active' to specify the pipeline to work with. Either 'unique_id' or 'name' can be used when state is 'absent'
    required: false
  state:
    description:
      - Create, activate, deactivate or delete the pipeline.
    default: 'present'
    required: false
    choices: ['present', 'active', 'inactive', 'absent']
  description:
    description:
      - The description of the new pipeline. Only used with state 'active' when creating a new pipeline.
  parameters:
    description:
      - A hash of all the parameter values used when activating the pipeline. This overrides parameters from the pipeline definition.
    required: false
    default: {}
  tags:
    description:
      - A hash of tags to associate with the pipeline at creation. Tags let you control access to pipelines.
    required: false
    default: {}
extends_documentation_fragment:
    - aws
'''

EXAMPLES = '''
# Create an AWS Data Pipeline with the name of 'my-big-data-pipeline' and unique id 'my-unique-pipeline-name'.
tasks:
- name: Big Fish swims in the Data Lake
  data_pipeline:
    name: my-big-data-pipeline
    unique_id: my-unique-pipeline-name
    state: present

# A reverse action that removes previously created pipelines 'my-big-data-pipeline' and 'my-event-pipeline'
task:
- name: The Fish follows the Flow
  data_pipeline:
    name: "{{ item }}"
    state: absent
  with_items:
  - my-big-data-pipeline
  - my-event-pipeline
'''
try:
    import boto
    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False

try:
    import boto3
    import boto3.datapipeline
    import boto3.datapipeline.layer1
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False

try:
    from awscli.customizations.datapipeline import translator
    HAS_AWS_CLI = True
except ImportError:
    HAS_AWS_CLI = False


def boto_exception(err):
    '''generic error message handler'''
    if hasattr(err, 'error_message'):
        error = err.error_message
    elif hasattr(err, 'message'):
        error = err.message
    else:
        error = '%s: %s' % (Exception, err)

    return error


def delete_pipeline(module, dp, pipeline_id):
    try:
        dp.delete_pipeline(pipelineId=pipeline_id)
    except boto.exception.BotoServerError, err:
        module.fail_json(changed=False, msg=boto_exception(err))
    else:
        return True


def create_pipeline(module, dp, name, unique_id, description=None, tags=None):
    try:
        req = dict(name=name, uniqueId=unique_id,)
        if description is not None:
            req['description'] = description
        if tags is not None:
            req['tags'] = convert_tags(tags)
        res = dp.create_pipeline(**req)
    except boto.exception.BotoServerError, err:
        module.fail_json(changed=False, msg=boto_exception(err))
    else:
        return True, res['pipelineId']


def convert_tags(tags):
    res = []
    for key in tags:
        res.append(dict(key=key, value=tags[key]))
    return res


def activate_pipeline(module, dp, pipeline_id, parameters):
    try:
        req = dict(pipelineId=pipeline_id)
        if parameters is not None:
            req['parameterValues'] = translator.definition_to_parameter_values({'values': parameters})
        dp.activate_pipeline(**req)
    except boto.exception.BotoServerError, err:
        module.fail_json(changed=False, msg=boto_exception(err))
    else:
        return True


def deactivate_pipeline(module, dp, pipeline_id):
    try:
        dp.deactivate_pipeline(pipelineId=pipeline_id)
    except boto.exception.BotoServerError, err:
        module.fail_json(changed=False, msg=boto_exception(err))
    else:
        return True


def get_all_pipelines(dp):
    all_pipelines = []
    some_response = dp.list_pipelines()
    all_pipelines.extend(some_response['pipelineIdList'])
    while some_response['hasMoreResults']:
        some_response = dp.list_pipelines(some_response['marker'])
        all_pipelines.extend(some_response['pipelineIdList'])
    return all_pipelines


def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(
            name=dict(default=None, required=False),
            pipeline_id=dict(default=None, required=False),
            unique_id=dict(default=None, required=False),
            description=dict(default=None, required=False),
            state=dict(default='present', choices=['present', 'active', 'inactive', 'absent']),
            parameters=dict(default=None, required=False),
            tags=dict(default=None, required=False)
    ))

    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[['name', 'pipeline_id'], ['description', 'pipeline_id']],
    )

    if not HAS_BOTO:
        module.fail_json(msg='This module requires Boto, please install it')

    if not HAS_BOTO3:
        module.fail_json(msg='This module requires Boto3, please install it')

    if not HAS_AWS_CLI:
        module.fail_json(msg='This module requires awscli, please install it')

    name = module.params.get('name')
    unique_id = module.params.get('unique_id')
    pipeline_id = module.params.get('pipeline_id')
    state = module.params.get('state').lower()
    activation_parameters = module.params.get('parameters')
    tags = module.params.get('tags')

    changed = False

    if state == 'present':
        if name is None:
            module.fail_json(changed=False, msg="data_pipeline: name must be defined when creating a pipeline")
        elif unique_id is None:
            module.fail_json(changed=False, msg="data_pipeline: unique_id must be defined when creating a pipeline")
    elif state == 'absent':
        if unique_id is not None:
            module.fail_json(changed=False, msg="data_pipeline: when deleting an existing pipeline either name or pipeline_id should be used but not unique_id")
        elif name is None and pipeline_id is None:
            module.fail_json(changed=False, msg="data_pipeline: when deleting an existing pipeline either name or pipeline_id should be used")
    elif state == 'active' or state == 'inactive':
        if pipeline_id is None:
            module.fail_json(changed=False, msg="data_pipeline: unique_id must be defined when activating or deactivating a pipeline")

    region, ec2_url, aws_connect_kwargs = get_aws_connection_info(module, boto3=True)

    try:
        dp = boto3_conn(module, conn_type='client', resource='datapipeline', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    except boto.exception.NoAuthHandlerFound, e:
        module.fail_json(msg=boto_exception(e))
        return

    existing_pipelines = get_all_pipelines(dp)
    existing_pipeline_ids = [p['id'] for p in existing_pipelines]

    if state == 'absent':
        deleted_pipeline_ids = []
        pipeline_ids_to_be_deleted = []
        if pipeline_id is not None and pipeline_id in existing_pipeline_ids:
            pipeline_ids_to_be_deleted = [pipeline_id]
        else:
            for some_pipeline in existing_pipelines:
                if name == some_pipeline['name']:
                    pipeline_ids_to_be_deleted.append(some_pipeline['id'])
        for pid in pipeline_ids_to_be_deleted:
            deleted = delete_pipeline(module, dp, pid)
            changed |= deleted
            if deleted:
                deleted_pipeline_ids.append(pid)
        module.exit_json(changed=changed, deleted_pipeline_ids=deleted_pipeline_ids)
    elif state == 'present':
        description = module.params.get('description')
        changed, pipeline_id = create_pipeline(module, dp, name, unique_id, description, tags)
        changed = changed and pipeline_id not in existing_pipeline_ids
    elif state == 'active' and pipeline_id in existing_pipeline_ids:
        changed = activate_pipeline(module, dp, pipeline_id, activation_parameters)
    elif state == 'inactive' and pipeline_id in existing_pipeline_ids:
        changed = deactivate_pipeline(module, dp, pipeline_id)

    module.exit_json(changed=changed, pipeline_id=pipeline_id)

from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import *

main()
