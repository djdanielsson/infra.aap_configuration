# Ansible Role infra.aap_configuration.gateway_role_user_assignments

## Description

An Ansible Role to give a user permission to a resource like an organization.

## Variables

|Variable Name|Default Value|Required|Description|Example|
|:---|:---:|:---:|:---|:---|
|`platform_state`|"present"|no|The state all objects will take unless overridden by object default|'absent'|
|`aap_hostname`|""|yes|URL to the Ansible Automation Platform Server.|127.0.0.1|
|`aap_validate_certs`|`true`|no|Whether or not to validate the Ansible Automation Platform Server's SSL certificate.||
|`aap_username`|""|no|Admin User on the Ansible Automation Platform Server. Either username / password or oauthtoken need to be specified.||
|`aap_password`|""|no|Platform Admin User's password on the Server.  This should be stored in an Ansible Vault at vars/platform-secrets.yml or elsewhere and called from a parent playbook.||
|`aap_token`|""|no|Controller Admin User's token on the Ansible Automation Platform Server. This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook. Either username / password or oauthtoken need to be specified.||
|`aap_request_timeout`|`10`|no|Specify the timeout in seconds Ansible should use in requests to the Ansible Automation Platform host.||
|`aap_configuration_collect_logs`|`false`|no|Specify whether to collect async results and continue for all failed async tasks instead of failing on the first error. Collected results are available in the `aap_configuration_role_errors` variable.||
|`gateway_role_user_assignments`|`see below`|yes|Data structure describing your gateway_role_user_assignment Described below.||

### Secure Logging Variables

The following Variables complement each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add ee_registry task does not include sensitive information.
gateway_role_user_assignments_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`gateway_role_user_assignments_secure_logging`|`false`|no|Whether or not to include the sensitive Registry role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`gateway_role_user_assignments_async_retries`|`aap_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`gateway_role_user_assignments_async_delay`|`aap_configuration_async_delay`|no|This sets the delay between retries for the role.|
|`aap_configuration_loop_delay`|1000|no|This variable sets the loop_delay for the role globally.|
|`gateway_role_user_assignments_loop_delay`|`aap_configuration_loop_delay`|no|This variable sets the loop_delay for the role.|
|`aap_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.|

## Data Structure

### Role User Assignments Arguments

Options for the `gateway_role_user_assignments` variable:

| Variable Name       | Default Value | Required | Type | Description                                                                                           |
|:--------------------|:-------------:|:--------:|:----:|:------------------------------------------------------------------------------------------------------|
| `role_definition`   |      N/A      |   yes    | str  | The name or id of the role definition to assign to the user.                                          |
| `user`              |      N/A      |    no    | str  | The username of the user to assign to the object.                                                     |
| `user_ansible_id`   |      N/A      |    no    | str  | Resource id of the user who will receive permissions from this assignment. Alternative to user field. |
| `object_id`         |      N/A      |    no    | int  | Primary key of the object this assignment applies to.  This option is deprecated and will be removed in a release after 2026-01-31.                                               |
| `object_ids`         |      N/A     |    no    | list | List of object IDs(Primary Key ) or names this assignment applies to.                                                 |
| `object_ansible_id` |      N/A      |    no    | str  | Resource id of the object this role applies to. Alternative to the object_id field.                         |
| `state`             |   `present`   |    no    | str  | Desired state of the resource.                                                                        |

**Unique value:**

- [`user`, `object_id`] (`*_ansible_id` alternatives can be provided)

## Usage

### Json Example

- Assign Organization Member role (object_id is an organization with ID 1)

```json
{
  "gateway_role_user_assignments": [
    {
      "role_definition": "Organization Member",
      "user": "Bob",
      "object_id": "1",
    }
  ]
}
```

Description: An Ansible Role to create RBAC Role User Assignments in Automation Platform gateway.


| Field                | Value           |
|--------------------- |-----------------|
| Readme update        | 26/08/2025 |




<details>
<summary><b>🧩 Argument Specifications in meta/argument_specs</b></summary>

#### Key: main
**Description**: An Ansible Role to create role_user_assignments on Ansible gateway.


  - **aap_role_user_assignments**
    - **Required**: True
    - **Type**: list
    - **Default**: none
    - **Description**: Data structure describing your role_user_assignments
  
  
  
    
  

  - **role_user_assignments_async_retries**
    - **Required**: False
    - **Type**: 
    - **Default**: {{ aap_configuration_async_retries | default(30) }}
    - **Description**: This variable sets the number of retries to attempt for the role.
  
  
  

  - **aap_configuration_async_retries**
    - **Required**: False
    - **Type**: 
    - **Default**: 30
    - **Description**: This variable sets number of retries across all roles as a default.
  
  
  

  - **role_user_assignments_async_delay**
    - **Required**: False
    - **Type**: 
    - **Default**: {{ aap_configuration_async_delay | default(1) }}
    - **Description**: This variable sets delay between retries for the role.
  
  
  

  - **aap_configuration_async_delay**
    - **Required**: False
    - **Type**: 
    - **Default**: 1
    - **Description**: This variable sets delay between retries across all roles as a default.
  
  
  

  - **aap_configuration_async_dir**
    - **Required**: False
    - **Type**: 
    - **Default**: None
    - **Description**: Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.
  
  
  

  - **gateway_role_user_assignments_secure_logging**
    - **Required**: False
    - **Type**: bool
    - **Default**: {{ aap_configuration_secure_logging | default(false) }}
    - **Description**: Whether or not to include the sensitive tasks from this role in the log. Set this value to `true` if you will be providing your sensitive values from elsewhere.
  
  
  

  - **aap_configuration_secure_logging**
    - **Required**: False
    - **Type**: bool
    - **Default**: False
    - **Description**: This variable enables secure logging across all roles as a default.
  
  
  

  - **platform_state**
    - **Required**: False
    - **Type**: str
    - **Default**: present
    - **Description**: The state all objects will take unless overridden by object default
  
  
  

  - **aap_hostname**
    - **Required**: False
    - **Type**: str
    - **Default**: None
    - **Description**: URL to the Ansible gateway Server.
  
  
  

  - **aap_validate_certs**
    - **Required**: False
    - **Type**: str
    - **Default**: True
    - **Description**: Whether or not to validate the Ansible gateway Server's SSL certificate.
  
  
  

  - **aap_username**
    - **Required**: False
    - **Type**: str
    - **Default**: None
    - **Description**: Admin User on the Ansible gateway Server. Either username / password or oauthtoken need to be specified.
  
  
  

  - **aap_password**
    - **Required**: False
    - **Type**: str
    - **Default**: None
    - **Description**: Gateway Admin User's password on the Ansible gateway Server. This should be stored in an Ansible Vault at vars/gateway-secrets.yml or elsewhere and called from a parent playbook. Either username / password or oauthtoken need to be specified.
  
  
  

  - **aap_token**
    - **Required**: False
    - **Type**: str
    - **Default**: None
    - **Description**: Gateway Admin User's token on the Ansible gateway Server. This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook. Either username / password or oauthtoken need to be specified.
  
  
  



</details>


### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |Required    | Title       |
|--------------|--------------|-------------|-------------|-------------|
| [gateway_role_user_assignments](defaults/main.yml#L11)   | list   | `[]` |    n/a  |  n/a |
| [gateway_role_user_assignments_secure_logging](defaults/main.yml#L12)   | str   | `{{ aap_configuration_secure_logging ¦ default('false') }}` |    n/a  |  n/a |
| [gateway_role_user_assignments_async_retries](defaults/main.yml#L13)   | str   | `{{ aap_configuration_async_retries ¦ default(30) }}` |    n/a  |  n/a |
| [gateway_role_user_assignments_async_delay](defaults/main.yml#L14)   | str   | `{{ aap_configuration_async_delay ¦ default(1) }}` |    n/a  |  n/a |
| [gateway_role_user_assignments_enforce_defaults](defaults/main.yml#L15)   | str   | `{{ aap_configuration_enforce_defaults ¦ default(false) }}` |    n/a  |  n/a |
| [gateway_role_user_assignments_loop_delay](defaults/main.yml#L16)   | str   | `{{ aap_configuration_loop_delay ¦ default(0) }}` |    n/a  |  n/a |
| [aap_configuration_async_dir](defaults/main.yml#L17)   | NoneType   | `None` |    n/a  |  n/a |





### Tasks


#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Manage Gateway Role User Assignments Block | block | False |
| Role User Assignments ¦ Configuration | ansible.platform.role_user_assignment | False |
| Role User Assignments ¦ Wait for finish the configuration | ansible.builtin.include_role | True |







## Author Information
Martin Slemr

#### License

GPLv3

#### Minimum Ansible Version

2.16.0

#### Platforms

- **EL**: ['all']

<!-- DOCSIBLE END -->