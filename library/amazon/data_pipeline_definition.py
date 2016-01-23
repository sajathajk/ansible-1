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
module: data_pipeline_definition
short_description: Manage AWS Data Pipeline Definition
requirements: [ boto3, awscli ]
description:
     - Allows working with AWS Data Pipelines Definition: creating definitions from JSON templates and using parameters.
version_added: "2.0"
options:
  pipeline_id:
    description:
      - A unique identifier which is assigned by AWS when the pipeline is created.
    required: true
  definition:
    description:
      -  The local path of the data pipeline definition JSON file. Must give full path to the file, relative to the working directory. If using roles this may look like "roles/cloudformation/files/cloudformation-example.json"
    required: true
  parameters:
    description:
      - A hash of all the parameter values used with the pipeline. This overrides parameter values from the JSON file. Note that you can also specify the values when activating the pipeline.
    required: false
    default: {}
extends_documentation_fragment:
    - aws
'''

EXAMPLES = '''
# Create a new AWS Data Pipeline with definition including parameters and their values
- name: Big Fish swims in the Data Lake
  data_pipeline:
    name: my-big-data-pipeline
    unique_id: my-unique-pipeline-name
  register: new_pipeline

- name: It has a funny shape
  data_pipeline_definition:
    pipeline_id: "{{ new_pipeline.pipeline_id }}"
    objects:

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


def define_pipeline(module, dp, pipeline_id, new_definition, parameters):
    changed = False
    try:
        old_definition_objects = dp.get_pipeline_definition(pipelineId=pipeline_id)
        new_definition_objects = to_new_definition_objects(new_definition, parameters)
        dp.put_pipeline_definition(
            pipelineId=pipeline_id,
            pipelineObjects=new_definition_objects['pipelineObjects'],
            parameterObjects=new_definition_objects['parameterObjects'],
            parameterValues=new_definition_objects['parameterValues']
        )
        changed = not is_definition_same(old_definition_objects, dp.get_pipeline_definition(pipelineId=pipeline_id))
    except boto.exception.BotoServerError, err:
        module.fail_json(changed=changed, msg=boto_exception(err))
    else:
        return changed


def is_definition_same(old_def, new_def):
    del old_def['ResponseMetadata']
    del new_def['ResponseMetadata']
    return old_def == new_def


def to_new_definition_objects(new_definition, new_parameter_values):
    if new_parameter_values is not None:
        new_definition['values'] = new_parameter_values
    return dict(
        pipelineObjects=translator.definition_to_api_objects(new_definition),
        parameterObjects=translator.definition_to_api_parameters(new_definition),
        parameterValues=translator.definition_to_parameter_values(new_definition)
    )


def get_all_pipelines(dp):
    all_pipelines = []
    some_response = dp.list_pipelines()
    all_pipelines.extend(some_response['pipelineIdList'])
    while some_response['hasMoreResults']:
        some_response = dp.list_pipelines(some_response['marker'])
        all_pipelines.extend(some_response['pipelineIdList'])
    return all_pipelines


def read_pipeline_definition(filename):
    return json.load(open(filename, 'r'))


def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(
            pipeline_id=dict(default=None, required=True),
            definition=dict(default=None, required=True),
            parameters=dict(default=None, required=False)
    ))

    module = AnsibleModule(
            argument_spec=argument_spec,
    )

    if not HAS_BOTO:
        module.fail_json(msg='This module requires Boto, please install it')

    if not HAS_BOTO3:
        module.fail_json(msg='This module requires Boto3, please install it')

    if not HAS_AWS_CLI:
        module.fail_json(msg='This module requires awscli, please install it')

    pipeline_id = module.params.get('pipeline_id')
    parameters = module.params.get('parameters')
    definition = read_pipeline_definition(module.params.get('definition'))

    region, ec2_url, aws_connect_kwargs = get_aws_connection_info(module, boto3=True)

    try:
        dp = boto3_conn(module, conn_type='client', resource='datapipeline', region=region, endpoint=ec2_url, **aws_connect_kwargs)
    except boto.exception.NoAuthHandlerFound, e:
        module.fail_json(msg=boto_exception(e))
        return

    existing_pipelines = get_all_pipelines(dp)
    existing_pipeline_ids = [p['id'] for p in existing_pipelines]

    if pipeline_id not in existing_pipeline_ids:
        module.fail_json(msg=("pipeline_id %s doesn't exist in region %s" % pipeline_id, region))

    changed = define_pipeline(module, dp, pipeline_id, definition, parameters)

    module.exit_json(changed=changed, pipeline_id=pipeline_id)


from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import *

main()
