# infra.aap_configuration.collect_async_status

## Description

Ansible role that checks the status of asynchronous tasks and optionally collects errors.

This is an internal role that is not meant to be called directly by users of this collection.

## Task Files

The role provides composable task files. `main.yml` loops over a configurable list of task files to include, so callers can control exactly which steps run and avoid unnecessary output.

### Available task files

|Task File|Description|Self-guarded|
|:---|:---|:---:|
|`collect_async_status.yml`|Polls `async_status` until the async job completes. Registers the result in `__cas_job_async_result`. Uses `failed_when: false` so subsequent task files can inspect the result.|no|
|`register_value.yml`|Registers the async result into a caller-specified variable. Only runs when `aap_configuration_register` or the item's `register` field is defined.|yes|
|`handle_error.yml`|Handles failed async results. Only runs when `__cas_job_async_result` is failed. In fail-fast mode (default), fails immediately with the error message and API response detail. In log-collection mode (`aap_configuration_collect_logs: true`), collects errors into `aap_configuration_role_errors` and continues.|yes|

### Controlling which task files run

`main.yml` iterates over the `cas_task_files` list variable. The default is:

```yaml
cas_task_files:
  - collect_async_status.yml
  - handle_error.yml
```

Files are included in list order. Each file is self-guarded (has its own `when` conditions), so it is safe to include files that may not apply — they will skip cleanly.

To customize, pass `cas_task_files` in the caller's `vars`:

```yaml
# Only poll, no error handling (caller handles errors itself)
- ansible.builtin.include_role:
    name: infra.aap_configuration.collect_async_status
  vars:
    cas_task_files:
      - collect_async_status.yml

# Poll + register + error handling
- ansible.builtin.include_role:
    name: infra.aap_configuration.collect_async_status
  vars:
    cas_task_files:
      - collect_async_status.yml
      - register_value.yml
      - handle_error.yml
```

Individual files can also be included directly using `tasks_from`:

```yaml
- ansible.builtin.include_role:
    name: infra.aap_configuration.collect_async_status
    tasks_from: collect_async_status.yml
```

## Variables

|Variable Name|Default Value|Required|Description|
|:---|:---:|:---:|:---|
|`cas_job_async_results_item`||yes|The asynchronous item to check the status of. This must be from the registered `async` task|
|`cas_task_files`|`[collect_async_status.yml, handle_error.yml]`|no|Ordered list of task files to include. Controls which steps run and their order.|
|`cas_error_list_var_name`||yes|The name of the dictionary key to use when collecting errors|
|`cas_register_subvar`||yes|The name of the dictionary key to use when registering values|
|`cas_object_label`||no|Custom task label for the async_status polling task. When provided, replaces the default task name for better output readability.|
|`cas_collect_logs`|`{{ aap_configuration_collect_logs \| default(false) }}`|no|When `true`, async task failures are suppressed (`failed_when: false`) so that `handle_error.yml` can collect error details and continue execution. Errors are collected in `aap_configuration_role_errors`. When `false` (default), the async task fails immediately on error.|

### Error Output

When a task fails, the error output includes:

|Field|Description|
|:---|:---|
|`ERROR_MESSAGE`|The module error message (e.g. "Unable to update schedule server_report, see response")|
|`ERROR_STATUS_CODE`|The HTTP status code from the API response (e.g. 400, 403, 404), if available|
|`ERROR_RESPONSE`|The full JSON body from the API response (e.g. `{"detail": "Bad data found in related field execution_environment."}`), if available|

When `aap_configuration_collect_logs` is `false` (default), the role fails immediately and displays the error message along with the API response detail. When `aap_configuration_collect_logs` is `true`, errors are collected into `aap_configuration_role_errors` with the above fields plus any identifying fields from the failed item (such as `name`, `organization`, etc.).

### Secure Logging Variables

The following Variables complement each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add host task does not include sensitive information.
`controller_configuration_host_secure_logging` defaults to the value of `aap_configuration_secure_logging` if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|
|`cas_secure_logging`|`false`|no|Whether or not to include the sensitive host role tasks in the log. Set this value to `true` if you will be providing your sensitive values from elsewhere.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`cas_async_retries`|`{{ aap_configuration_async_retries }}`|no|This variable sets the number of retries to attempt for the role.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`cas_async_delay`|`aap_configuration_async_delay`|no|This sets the delay between retries for the role.|

## License

[GPLv3+](https://github.com/redhat-cop/infra.aap_configuration/blob/devel/LICENSE)

## Author

[Brant Evans](https://github.com/branic/)
