r'''
# `data_databricks_cluster_pluginframework`

Refer to the Terraform Registry for docs: [`data_databricks_cluster_pluginframework`](https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class DataDatabricksClusterPluginframework(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframework",
):
    '''Represents a {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework databricks_cluster_pluginframework}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cluster_id: typing.Optional[builtins.str] = None,
        cluster_info: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework databricks_cluster_pluginframework} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_id DataDatabricksClusterPluginframework#cluster_id}.
        :param cluster_info: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_info DataDatabricksClusterPluginframework#cluster_info}.
        :param cluster_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_name DataDatabricksClusterPluginframework#cluster_name}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e366a91d00295d072b70f1a4e627cc9579b8fe5cafd12a160382a2fdb2e5d65c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataDatabricksClusterPluginframeworkConfig(
            cluster_id=cluster_id,
            cluster_info=cluster_info,
            cluster_name=cluster_name,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a DataDatabricksClusterPluginframework resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataDatabricksClusterPluginframework to import.
        :param import_from_id: The id of the existing DataDatabricksClusterPluginframework that should be imported. Refer to the {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataDatabricksClusterPluginframework to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02b3fe730f0239a2886dd2b2b7a984548fb31f98aaafab93756102ed31ab2240)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putClusterInfo")
    def put_cluster_info(
        self,
        *,
        autoscale: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoAutoscale", typing.Dict[builtins.str, typing.Any]]] = None,
        autotermination_minutes: typing.Optional[jsii.Number] = None,
        aws_attributes: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoAwsAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
        azure_attributes: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoAzureAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_cores: typing.Optional[jsii.Number] = None,
        cluster_id: typing.Optional[builtins.str] = None,
        cluster_log_conf: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoClusterLogConf", typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_log_status: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoClusterLogStatus", typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_memory_mb: typing.Optional[jsii.Number] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        cluster_source: typing.Optional[builtins.str] = None,
        creator_user_name: typing.Optional[builtins.str] = None,
        custom_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        data_security_mode: typing.Optional[builtins.str] = None,
        default_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        docker_image: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoDockerImage", typing.Dict[builtins.str, typing.Any]]] = None,
        driver: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoDriver", typing.Dict[builtins.str, typing.Any]]] = None,
        driver_instance_pool_id: typing.Optional[builtins.str] = None,
        driver_node_type_id: typing.Optional[builtins.str] = None,
        enable_elastic_disk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_local_disk_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        executors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoExecutors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        gcp_attributes: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoGcpAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
        init_scripts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoInitScripts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        instance_pool_id: typing.Optional[builtins.str] = None,
        jdbc_port: typing.Optional[jsii.Number] = None,
        last_restarted_time: typing.Optional[jsii.Number] = None,
        last_state_loss_time: typing.Optional[jsii.Number] = None,
        node_type_id: typing.Optional[builtins.str] = None,
        num_workers: typing.Optional[jsii.Number] = None,
        policy_id: typing.Optional[builtins.str] = None,
        runtime_engine: typing.Optional[builtins.str] = None,
        single_user_name: typing.Optional[builtins.str] = None,
        spark_conf: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        spark_context_id: typing.Optional[jsii.Number] = None,
        spark_env_vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        spark_version: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        ssh_public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        start_time: typing.Optional[jsii.Number] = None,
        state: typing.Optional[builtins.str] = None,
        state_message: typing.Optional[builtins.str] = None,
        terminated_time: typing.Optional[jsii.Number] = None,
        termination_reason: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoTerminationReason", typing.Dict[builtins.str, typing.Any]]] = None,
        workload_type: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoWorkloadType", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param autoscale: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#autoscale DataDatabricksClusterPluginframework#autoscale}.
        :param autotermination_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#autotermination_minutes DataDatabricksClusterPluginframework#autotermination_minutes}.
        :param aws_attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#aws_attributes DataDatabricksClusterPluginframework#aws_attributes}.
        :param azure_attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#azure_attributes DataDatabricksClusterPluginframework#azure_attributes}.
        :param cluster_cores: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_cores DataDatabricksClusterPluginframework#cluster_cores}.
        :param cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_id DataDatabricksClusterPluginframework#cluster_id}.
        :param cluster_log_conf: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_log_conf DataDatabricksClusterPluginframework#cluster_log_conf}.
        :param cluster_log_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_log_status DataDatabricksClusterPluginframework#cluster_log_status}.
        :param cluster_memory_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_memory_mb DataDatabricksClusterPluginframework#cluster_memory_mb}.
        :param cluster_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_name DataDatabricksClusterPluginframework#cluster_name}.
        :param cluster_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_source DataDatabricksClusterPluginframework#cluster_source}.
        :param creator_user_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#creator_user_name DataDatabricksClusterPluginframework#creator_user_name}.
        :param custom_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#custom_tags DataDatabricksClusterPluginframework#custom_tags}.
        :param data_security_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#data_security_mode DataDatabricksClusterPluginframework#data_security_mode}.
        :param default_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#default_tags DataDatabricksClusterPluginframework#default_tags}.
        :param docker_image: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#docker_image DataDatabricksClusterPluginframework#docker_image}.
        :param driver: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#driver DataDatabricksClusterPluginframework#driver}.
        :param driver_instance_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#driver_instance_pool_id DataDatabricksClusterPluginframework#driver_instance_pool_id}.
        :param driver_node_type_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#driver_node_type_id DataDatabricksClusterPluginframework#driver_node_type_id}.
        :param enable_elastic_disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#enable_elastic_disk DataDatabricksClusterPluginframework#enable_elastic_disk}.
        :param enable_local_disk_encryption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#enable_local_disk_encryption DataDatabricksClusterPluginframework#enable_local_disk_encryption}.
        :param executors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#executors DataDatabricksClusterPluginframework#executors}.
        :param gcp_attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#gcp_attributes DataDatabricksClusterPluginframework#gcp_attributes}.
        :param init_scripts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#init_scripts DataDatabricksClusterPluginframework#init_scripts}.
        :param instance_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#instance_pool_id DataDatabricksClusterPluginframework#instance_pool_id}.
        :param jdbc_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#jdbc_port DataDatabricksClusterPluginframework#jdbc_port}.
        :param last_restarted_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#last_restarted_time DataDatabricksClusterPluginframework#last_restarted_time}.
        :param last_state_loss_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#last_state_loss_time DataDatabricksClusterPluginframework#last_state_loss_time}.
        :param node_type_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#node_type_id DataDatabricksClusterPluginframework#node_type_id}.
        :param num_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#num_workers DataDatabricksClusterPluginframework#num_workers}.
        :param policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#policy_id DataDatabricksClusterPluginframework#policy_id}.
        :param runtime_engine: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#runtime_engine DataDatabricksClusterPluginframework#runtime_engine}.
        :param single_user_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#single_user_name DataDatabricksClusterPluginframework#single_user_name}.
        :param spark_conf: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spark_conf DataDatabricksClusterPluginframework#spark_conf}.
        :param spark_context_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spark_context_id DataDatabricksClusterPluginframework#spark_context_id}.
        :param spark_env_vars: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spark_env_vars DataDatabricksClusterPluginframework#spark_env_vars}.
        :param spark_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spark_version DataDatabricksClusterPluginframework#spark_version}.
        :param spec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spec DataDatabricksClusterPluginframework#spec}.
        :param ssh_public_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ssh_public_keys DataDatabricksClusterPluginframework#ssh_public_keys}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#start_time DataDatabricksClusterPluginframework#start_time}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#state DataDatabricksClusterPluginframework#state}.
        :param state_message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#state_message DataDatabricksClusterPluginframework#state_message}.
        :param terminated_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#terminated_time DataDatabricksClusterPluginframework#terminated_time}.
        :param termination_reason: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#termination_reason DataDatabricksClusterPluginframework#termination_reason}.
        :param workload_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#workload_type DataDatabricksClusterPluginframework#workload_type}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfo(
            autoscale=autoscale,
            autotermination_minutes=autotermination_minutes,
            aws_attributes=aws_attributes,
            azure_attributes=azure_attributes,
            cluster_cores=cluster_cores,
            cluster_id=cluster_id,
            cluster_log_conf=cluster_log_conf,
            cluster_log_status=cluster_log_status,
            cluster_memory_mb=cluster_memory_mb,
            cluster_name=cluster_name,
            cluster_source=cluster_source,
            creator_user_name=creator_user_name,
            custom_tags=custom_tags,
            data_security_mode=data_security_mode,
            default_tags=default_tags,
            docker_image=docker_image,
            driver=driver,
            driver_instance_pool_id=driver_instance_pool_id,
            driver_node_type_id=driver_node_type_id,
            enable_elastic_disk=enable_elastic_disk,
            enable_local_disk_encryption=enable_local_disk_encryption,
            executors=executors,
            gcp_attributes=gcp_attributes,
            init_scripts=init_scripts,
            instance_pool_id=instance_pool_id,
            jdbc_port=jdbc_port,
            last_restarted_time=last_restarted_time,
            last_state_loss_time=last_state_loss_time,
            node_type_id=node_type_id,
            num_workers=num_workers,
            policy_id=policy_id,
            runtime_engine=runtime_engine,
            single_user_name=single_user_name,
            spark_conf=spark_conf,
            spark_context_id=spark_context_id,
            spark_env_vars=spark_env_vars,
            spark_version=spark_version,
            spec=spec,
            ssh_public_keys=ssh_public_keys,
            start_time=start_time,
            state=state,
            state_message=state_message,
            terminated_time=terminated_time,
            termination_reason=termination_reason,
            workload_type=workload_type,
        )

        return typing.cast(None, jsii.invoke(self, "putClusterInfo", [value]))

    @jsii.member(jsii_name="resetClusterId")
    def reset_cluster_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterId", []))

    @jsii.member(jsii_name="resetClusterInfo")
    def reset_cluster_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterInfo", []))

    @jsii.member(jsii_name="resetClusterName")
    def reset_cluster_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterName", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="clusterInfo")
    def cluster_info(
        self,
    ) -> "DataDatabricksClusterPluginframeworkClusterInfoOutputReference":
        return typing.cast("DataDatabricksClusterPluginframeworkClusterInfoOutputReference", jsii.get(self, "clusterInfo"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterInfoInput")
    def cluster_info_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfo"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfo"]], jsii.get(self, "clusterInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterNameInput")
    def cluster_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61117428e448e89f7262a790000b078ad9011cd3953b9bffcb89483abb2ab8f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @cluster_name.setter
    def cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52288c752f765542de324754ed21ed43bffa4f75f8df8101044aeb301d1c828f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfo",
    jsii_struct_bases=[],
    name_mapping={
        "autoscale": "autoscale",
        "autotermination_minutes": "autoterminationMinutes",
        "aws_attributes": "awsAttributes",
        "azure_attributes": "azureAttributes",
        "cluster_cores": "clusterCores",
        "cluster_id": "clusterId",
        "cluster_log_conf": "clusterLogConf",
        "cluster_log_status": "clusterLogStatus",
        "cluster_memory_mb": "clusterMemoryMb",
        "cluster_name": "clusterName",
        "cluster_source": "clusterSource",
        "creator_user_name": "creatorUserName",
        "custom_tags": "customTags",
        "data_security_mode": "dataSecurityMode",
        "default_tags": "defaultTags",
        "docker_image": "dockerImage",
        "driver": "driver",
        "driver_instance_pool_id": "driverInstancePoolId",
        "driver_node_type_id": "driverNodeTypeId",
        "enable_elastic_disk": "enableElasticDisk",
        "enable_local_disk_encryption": "enableLocalDiskEncryption",
        "executors": "executors",
        "gcp_attributes": "gcpAttributes",
        "init_scripts": "initScripts",
        "instance_pool_id": "instancePoolId",
        "jdbc_port": "jdbcPort",
        "last_restarted_time": "lastRestartedTime",
        "last_state_loss_time": "lastStateLossTime",
        "node_type_id": "nodeTypeId",
        "num_workers": "numWorkers",
        "policy_id": "policyId",
        "runtime_engine": "runtimeEngine",
        "single_user_name": "singleUserName",
        "spark_conf": "sparkConf",
        "spark_context_id": "sparkContextId",
        "spark_env_vars": "sparkEnvVars",
        "spark_version": "sparkVersion",
        "spec": "spec",
        "ssh_public_keys": "sshPublicKeys",
        "start_time": "startTime",
        "state": "state",
        "state_message": "stateMessage",
        "terminated_time": "terminatedTime",
        "termination_reason": "terminationReason",
        "workload_type": "workloadType",
    },
)
class DataDatabricksClusterPluginframeworkClusterInfo:
    def __init__(
        self,
        *,
        autoscale: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoAutoscale", typing.Dict[builtins.str, typing.Any]]] = None,
        autotermination_minutes: typing.Optional[jsii.Number] = None,
        aws_attributes: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoAwsAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
        azure_attributes: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoAzureAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_cores: typing.Optional[jsii.Number] = None,
        cluster_id: typing.Optional[builtins.str] = None,
        cluster_log_conf: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoClusterLogConf", typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_log_status: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoClusterLogStatus", typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_memory_mb: typing.Optional[jsii.Number] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        cluster_source: typing.Optional[builtins.str] = None,
        creator_user_name: typing.Optional[builtins.str] = None,
        custom_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        data_security_mode: typing.Optional[builtins.str] = None,
        default_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        docker_image: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoDockerImage", typing.Dict[builtins.str, typing.Any]]] = None,
        driver: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoDriver", typing.Dict[builtins.str, typing.Any]]] = None,
        driver_instance_pool_id: typing.Optional[builtins.str] = None,
        driver_node_type_id: typing.Optional[builtins.str] = None,
        enable_elastic_disk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_local_disk_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        executors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoExecutors", typing.Dict[builtins.str, typing.Any]]]]] = None,
        gcp_attributes: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoGcpAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
        init_scripts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoInitScripts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        instance_pool_id: typing.Optional[builtins.str] = None,
        jdbc_port: typing.Optional[jsii.Number] = None,
        last_restarted_time: typing.Optional[jsii.Number] = None,
        last_state_loss_time: typing.Optional[jsii.Number] = None,
        node_type_id: typing.Optional[builtins.str] = None,
        num_workers: typing.Optional[jsii.Number] = None,
        policy_id: typing.Optional[builtins.str] = None,
        runtime_engine: typing.Optional[builtins.str] = None,
        single_user_name: typing.Optional[builtins.str] = None,
        spark_conf: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        spark_context_id: typing.Optional[jsii.Number] = None,
        spark_env_vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        spark_version: typing.Optional[builtins.str] = None,
        spec: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        ssh_public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        start_time: typing.Optional[jsii.Number] = None,
        state: typing.Optional[builtins.str] = None,
        state_message: typing.Optional[builtins.str] = None,
        terminated_time: typing.Optional[jsii.Number] = None,
        termination_reason: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoTerminationReason", typing.Dict[builtins.str, typing.Any]]] = None,
        workload_type: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoWorkloadType", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param autoscale: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#autoscale DataDatabricksClusterPluginframework#autoscale}.
        :param autotermination_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#autotermination_minutes DataDatabricksClusterPluginframework#autotermination_minutes}.
        :param aws_attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#aws_attributes DataDatabricksClusterPluginframework#aws_attributes}.
        :param azure_attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#azure_attributes DataDatabricksClusterPluginframework#azure_attributes}.
        :param cluster_cores: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_cores DataDatabricksClusterPluginframework#cluster_cores}.
        :param cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_id DataDatabricksClusterPluginframework#cluster_id}.
        :param cluster_log_conf: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_log_conf DataDatabricksClusterPluginframework#cluster_log_conf}.
        :param cluster_log_status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_log_status DataDatabricksClusterPluginframework#cluster_log_status}.
        :param cluster_memory_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_memory_mb DataDatabricksClusterPluginframework#cluster_memory_mb}.
        :param cluster_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_name DataDatabricksClusterPluginframework#cluster_name}.
        :param cluster_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_source DataDatabricksClusterPluginframework#cluster_source}.
        :param creator_user_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#creator_user_name DataDatabricksClusterPluginframework#creator_user_name}.
        :param custom_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#custom_tags DataDatabricksClusterPluginframework#custom_tags}.
        :param data_security_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#data_security_mode DataDatabricksClusterPluginframework#data_security_mode}.
        :param default_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#default_tags DataDatabricksClusterPluginframework#default_tags}.
        :param docker_image: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#docker_image DataDatabricksClusterPluginframework#docker_image}.
        :param driver: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#driver DataDatabricksClusterPluginframework#driver}.
        :param driver_instance_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#driver_instance_pool_id DataDatabricksClusterPluginframework#driver_instance_pool_id}.
        :param driver_node_type_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#driver_node_type_id DataDatabricksClusterPluginframework#driver_node_type_id}.
        :param enable_elastic_disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#enable_elastic_disk DataDatabricksClusterPluginframework#enable_elastic_disk}.
        :param enable_local_disk_encryption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#enable_local_disk_encryption DataDatabricksClusterPluginframework#enable_local_disk_encryption}.
        :param executors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#executors DataDatabricksClusterPluginframework#executors}.
        :param gcp_attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#gcp_attributes DataDatabricksClusterPluginframework#gcp_attributes}.
        :param init_scripts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#init_scripts DataDatabricksClusterPluginframework#init_scripts}.
        :param instance_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#instance_pool_id DataDatabricksClusterPluginframework#instance_pool_id}.
        :param jdbc_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#jdbc_port DataDatabricksClusterPluginframework#jdbc_port}.
        :param last_restarted_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#last_restarted_time DataDatabricksClusterPluginframework#last_restarted_time}.
        :param last_state_loss_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#last_state_loss_time DataDatabricksClusterPluginframework#last_state_loss_time}.
        :param node_type_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#node_type_id DataDatabricksClusterPluginframework#node_type_id}.
        :param num_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#num_workers DataDatabricksClusterPluginframework#num_workers}.
        :param policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#policy_id DataDatabricksClusterPluginframework#policy_id}.
        :param runtime_engine: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#runtime_engine DataDatabricksClusterPluginframework#runtime_engine}.
        :param single_user_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#single_user_name DataDatabricksClusterPluginframework#single_user_name}.
        :param spark_conf: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spark_conf DataDatabricksClusterPluginframework#spark_conf}.
        :param spark_context_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spark_context_id DataDatabricksClusterPluginframework#spark_context_id}.
        :param spark_env_vars: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spark_env_vars DataDatabricksClusterPluginframework#spark_env_vars}.
        :param spark_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spark_version DataDatabricksClusterPluginframework#spark_version}.
        :param spec: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spec DataDatabricksClusterPluginframework#spec}.
        :param ssh_public_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ssh_public_keys DataDatabricksClusterPluginframework#ssh_public_keys}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#start_time DataDatabricksClusterPluginframework#start_time}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#state DataDatabricksClusterPluginframework#state}.
        :param state_message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#state_message DataDatabricksClusterPluginframework#state_message}.
        :param terminated_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#terminated_time DataDatabricksClusterPluginframework#terminated_time}.
        :param termination_reason: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#termination_reason DataDatabricksClusterPluginframework#termination_reason}.
        :param workload_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#workload_type DataDatabricksClusterPluginframework#workload_type}.
        '''
        if isinstance(autoscale, dict):
            autoscale = DataDatabricksClusterPluginframeworkClusterInfoAutoscale(**autoscale)
        if isinstance(aws_attributes, dict):
            aws_attributes = DataDatabricksClusterPluginframeworkClusterInfoAwsAttributes(**aws_attributes)
        if isinstance(azure_attributes, dict):
            azure_attributes = DataDatabricksClusterPluginframeworkClusterInfoAzureAttributes(**azure_attributes)
        if isinstance(cluster_log_conf, dict):
            cluster_log_conf = DataDatabricksClusterPluginframeworkClusterInfoClusterLogConf(**cluster_log_conf)
        if isinstance(cluster_log_status, dict):
            cluster_log_status = DataDatabricksClusterPluginframeworkClusterInfoClusterLogStatus(**cluster_log_status)
        if isinstance(docker_image, dict):
            docker_image = DataDatabricksClusterPluginframeworkClusterInfoDockerImage(**docker_image)
        if isinstance(driver, dict):
            driver = DataDatabricksClusterPluginframeworkClusterInfoDriver(**driver)
        if isinstance(gcp_attributes, dict):
            gcp_attributes = DataDatabricksClusterPluginframeworkClusterInfoGcpAttributes(**gcp_attributes)
        if isinstance(spec, dict):
            spec = DataDatabricksClusterPluginframeworkClusterInfoSpec(**spec)
        if isinstance(termination_reason, dict):
            termination_reason = DataDatabricksClusterPluginframeworkClusterInfoTerminationReason(**termination_reason)
        if isinstance(workload_type, dict):
            workload_type = DataDatabricksClusterPluginframeworkClusterInfoWorkloadType(**workload_type)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__861fb60b7278f74f5f9f4062c027552fb238d79c232e98fa917a2f033314f72d)
            check_type(argname="argument autoscale", value=autoscale, expected_type=type_hints["autoscale"])
            check_type(argname="argument autotermination_minutes", value=autotermination_minutes, expected_type=type_hints["autotermination_minutes"])
            check_type(argname="argument aws_attributes", value=aws_attributes, expected_type=type_hints["aws_attributes"])
            check_type(argname="argument azure_attributes", value=azure_attributes, expected_type=type_hints["azure_attributes"])
            check_type(argname="argument cluster_cores", value=cluster_cores, expected_type=type_hints["cluster_cores"])
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument cluster_log_conf", value=cluster_log_conf, expected_type=type_hints["cluster_log_conf"])
            check_type(argname="argument cluster_log_status", value=cluster_log_status, expected_type=type_hints["cluster_log_status"])
            check_type(argname="argument cluster_memory_mb", value=cluster_memory_mb, expected_type=type_hints["cluster_memory_mb"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument cluster_source", value=cluster_source, expected_type=type_hints["cluster_source"])
            check_type(argname="argument creator_user_name", value=creator_user_name, expected_type=type_hints["creator_user_name"])
            check_type(argname="argument custom_tags", value=custom_tags, expected_type=type_hints["custom_tags"])
            check_type(argname="argument data_security_mode", value=data_security_mode, expected_type=type_hints["data_security_mode"])
            check_type(argname="argument default_tags", value=default_tags, expected_type=type_hints["default_tags"])
            check_type(argname="argument docker_image", value=docker_image, expected_type=type_hints["docker_image"])
            check_type(argname="argument driver", value=driver, expected_type=type_hints["driver"])
            check_type(argname="argument driver_instance_pool_id", value=driver_instance_pool_id, expected_type=type_hints["driver_instance_pool_id"])
            check_type(argname="argument driver_node_type_id", value=driver_node_type_id, expected_type=type_hints["driver_node_type_id"])
            check_type(argname="argument enable_elastic_disk", value=enable_elastic_disk, expected_type=type_hints["enable_elastic_disk"])
            check_type(argname="argument enable_local_disk_encryption", value=enable_local_disk_encryption, expected_type=type_hints["enable_local_disk_encryption"])
            check_type(argname="argument executors", value=executors, expected_type=type_hints["executors"])
            check_type(argname="argument gcp_attributes", value=gcp_attributes, expected_type=type_hints["gcp_attributes"])
            check_type(argname="argument init_scripts", value=init_scripts, expected_type=type_hints["init_scripts"])
            check_type(argname="argument instance_pool_id", value=instance_pool_id, expected_type=type_hints["instance_pool_id"])
            check_type(argname="argument jdbc_port", value=jdbc_port, expected_type=type_hints["jdbc_port"])
            check_type(argname="argument last_restarted_time", value=last_restarted_time, expected_type=type_hints["last_restarted_time"])
            check_type(argname="argument last_state_loss_time", value=last_state_loss_time, expected_type=type_hints["last_state_loss_time"])
            check_type(argname="argument node_type_id", value=node_type_id, expected_type=type_hints["node_type_id"])
            check_type(argname="argument num_workers", value=num_workers, expected_type=type_hints["num_workers"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument runtime_engine", value=runtime_engine, expected_type=type_hints["runtime_engine"])
            check_type(argname="argument single_user_name", value=single_user_name, expected_type=type_hints["single_user_name"])
            check_type(argname="argument spark_conf", value=spark_conf, expected_type=type_hints["spark_conf"])
            check_type(argname="argument spark_context_id", value=spark_context_id, expected_type=type_hints["spark_context_id"])
            check_type(argname="argument spark_env_vars", value=spark_env_vars, expected_type=type_hints["spark_env_vars"])
            check_type(argname="argument spark_version", value=spark_version, expected_type=type_hints["spark_version"])
            check_type(argname="argument spec", value=spec, expected_type=type_hints["spec"])
            check_type(argname="argument ssh_public_keys", value=ssh_public_keys, expected_type=type_hints["ssh_public_keys"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument state_message", value=state_message, expected_type=type_hints["state_message"])
            check_type(argname="argument terminated_time", value=terminated_time, expected_type=type_hints["terminated_time"])
            check_type(argname="argument termination_reason", value=termination_reason, expected_type=type_hints["termination_reason"])
            check_type(argname="argument workload_type", value=workload_type, expected_type=type_hints["workload_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if autoscale is not None:
            self._values["autoscale"] = autoscale
        if autotermination_minutes is not None:
            self._values["autotermination_minutes"] = autotermination_minutes
        if aws_attributes is not None:
            self._values["aws_attributes"] = aws_attributes
        if azure_attributes is not None:
            self._values["azure_attributes"] = azure_attributes
        if cluster_cores is not None:
            self._values["cluster_cores"] = cluster_cores
        if cluster_id is not None:
            self._values["cluster_id"] = cluster_id
        if cluster_log_conf is not None:
            self._values["cluster_log_conf"] = cluster_log_conf
        if cluster_log_status is not None:
            self._values["cluster_log_status"] = cluster_log_status
        if cluster_memory_mb is not None:
            self._values["cluster_memory_mb"] = cluster_memory_mb
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if cluster_source is not None:
            self._values["cluster_source"] = cluster_source
        if creator_user_name is not None:
            self._values["creator_user_name"] = creator_user_name
        if custom_tags is not None:
            self._values["custom_tags"] = custom_tags
        if data_security_mode is not None:
            self._values["data_security_mode"] = data_security_mode
        if default_tags is not None:
            self._values["default_tags"] = default_tags
        if docker_image is not None:
            self._values["docker_image"] = docker_image
        if driver is not None:
            self._values["driver"] = driver
        if driver_instance_pool_id is not None:
            self._values["driver_instance_pool_id"] = driver_instance_pool_id
        if driver_node_type_id is not None:
            self._values["driver_node_type_id"] = driver_node_type_id
        if enable_elastic_disk is not None:
            self._values["enable_elastic_disk"] = enable_elastic_disk
        if enable_local_disk_encryption is not None:
            self._values["enable_local_disk_encryption"] = enable_local_disk_encryption
        if executors is not None:
            self._values["executors"] = executors
        if gcp_attributes is not None:
            self._values["gcp_attributes"] = gcp_attributes
        if init_scripts is not None:
            self._values["init_scripts"] = init_scripts
        if instance_pool_id is not None:
            self._values["instance_pool_id"] = instance_pool_id
        if jdbc_port is not None:
            self._values["jdbc_port"] = jdbc_port
        if last_restarted_time is not None:
            self._values["last_restarted_time"] = last_restarted_time
        if last_state_loss_time is not None:
            self._values["last_state_loss_time"] = last_state_loss_time
        if node_type_id is not None:
            self._values["node_type_id"] = node_type_id
        if num_workers is not None:
            self._values["num_workers"] = num_workers
        if policy_id is not None:
            self._values["policy_id"] = policy_id
        if runtime_engine is not None:
            self._values["runtime_engine"] = runtime_engine
        if single_user_name is not None:
            self._values["single_user_name"] = single_user_name
        if spark_conf is not None:
            self._values["spark_conf"] = spark_conf
        if spark_context_id is not None:
            self._values["spark_context_id"] = spark_context_id
        if spark_env_vars is not None:
            self._values["spark_env_vars"] = spark_env_vars
        if spark_version is not None:
            self._values["spark_version"] = spark_version
        if spec is not None:
            self._values["spec"] = spec
        if ssh_public_keys is not None:
            self._values["ssh_public_keys"] = ssh_public_keys
        if start_time is not None:
            self._values["start_time"] = start_time
        if state is not None:
            self._values["state"] = state
        if state_message is not None:
            self._values["state_message"] = state_message
        if terminated_time is not None:
            self._values["terminated_time"] = terminated_time
        if termination_reason is not None:
            self._values["termination_reason"] = termination_reason
        if workload_type is not None:
            self._values["workload_type"] = workload_type

    @builtins.property
    def autoscale(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoAutoscale"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#autoscale DataDatabricksClusterPluginframework#autoscale}.'''
        result = self._values.get("autoscale")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoAutoscale"], result)

    @builtins.property
    def autotermination_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#autotermination_minutes DataDatabricksClusterPluginframework#autotermination_minutes}.'''
        result = self._values.get("autotermination_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def aws_attributes(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoAwsAttributes"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#aws_attributes DataDatabricksClusterPluginframework#aws_attributes}.'''
        result = self._values.get("aws_attributes")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoAwsAttributes"], result)

    @builtins.property
    def azure_attributes(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoAzureAttributes"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#azure_attributes DataDatabricksClusterPluginframework#azure_attributes}.'''
        result = self._values.get("azure_attributes")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoAzureAttributes"], result)

    @builtins.property
    def cluster_cores(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_cores DataDatabricksClusterPluginframework#cluster_cores}.'''
        result = self._values.get("cluster_cores")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cluster_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_id DataDatabricksClusterPluginframework#cluster_id}.'''
        result = self._values.get("cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_log_conf(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoClusterLogConf"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_log_conf DataDatabricksClusterPluginframework#cluster_log_conf}.'''
        result = self._values.get("cluster_log_conf")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoClusterLogConf"], result)

    @builtins.property
    def cluster_log_status(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoClusterLogStatus"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_log_status DataDatabricksClusterPluginframework#cluster_log_status}.'''
        result = self._values.get("cluster_log_status")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoClusterLogStatus"], result)

    @builtins.property
    def cluster_memory_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_memory_mb DataDatabricksClusterPluginframework#cluster_memory_mb}.'''
        result = self._values.get("cluster_memory_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_name DataDatabricksClusterPluginframework#cluster_name}.'''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_source DataDatabricksClusterPluginframework#cluster_source}.'''
        result = self._values.get("cluster_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def creator_user_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#creator_user_name DataDatabricksClusterPluginframework#creator_user_name}.'''
        result = self._values.get("creator_user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#custom_tags DataDatabricksClusterPluginframework#custom_tags}.'''
        result = self._values.get("custom_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def data_security_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#data_security_mode DataDatabricksClusterPluginframework#data_security_mode}.'''
        result = self._values.get("data_security_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#default_tags DataDatabricksClusterPluginframework#default_tags}.'''
        result = self._values.get("default_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def docker_image(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoDockerImage"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#docker_image DataDatabricksClusterPluginframework#docker_image}.'''
        result = self._values.get("docker_image")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoDockerImage"], result)

    @builtins.property
    def driver(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoDriver"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#driver DataDatabricksClusterPluginframework#driver}.'''
        result = self._values.get("driver")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoDriver"], result)

    @builtins.property
    def driver_instance_pool_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#driver_instance_pool_id DataDatabricksClusterPluginframework#driver_instance_pool_id}.'''
        result = self._values.get("driver_instance_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def driver_node_type_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#driver_node_type_id DataDatabricksClusterPluginframework#driver_node_type_id}.'''
        result = self._values.get("driver_node_type_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_elastic_disk(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#enable_elastic_disk DataDatabricksClusterPluginframework#enable_elastic_disk}.'''
        result = self._values.get("enable_elastic_disk")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_local_disk_encryption(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#enable_local_disk_encryption DataDatabricksClusterPluginframework#enable_local_disk_encryption}.'''
        result = self._values.get("enable_local_disk_encryption")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def executors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatabricksClusterPluginframeworkClusterInfoExecutors"]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#executors DataDatabricksClusterPluginframework#executors}.'''
        result = self._values.get("executors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatabricksClusterPluginframeworkClusterInfoExecutors"]]], result)

    @builtins.property
    def gcp_attributes(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoGcpAttributes"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#gcp_attributes DataDatabricksClusterPluginframework#gcp_attributes}.'''
        result = self._values.get("gcp_attributes")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoGcpAttributes"], result)

    @builtins.property
    def init_scripts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatabricksClusterPluginframeworkClusterInfoInitScripts"]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#init_scripts DataDatabricksClusterPluginframework#init_scripts}.'''
        result = self._values.get("init_scripts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatabricksClusterPluginframeworkClusterInfoInitScripts"]]], result)

    @builtins.property
    def instance_pool_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#instance_pool_id DataDatabricksClusterPluginframework#instance_pool_id}.'''
        result = self._values.get("instance_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jdbc_port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#jdbc_port DataDatabricksClusterPluginframework#jdbc_port}.'''
        result = self._values.get("jdbc_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def last_restarted_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#last_restarted_time DataDatabricksClusterPluginframework#last_restarted_time}.'''
        result = self._values.get("last_restarted_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def last_state_loss_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#last_state_loss_time DataDatabricksClusterPluginframework#last_state_loss_time}.'''
        result = self._values.get("last_state_loss_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def node_type_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#node_type_id DataDatabricksClusterPluginframework#node_type_id}.'''
        result = self._values.get("node_type_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_workers(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#num_workers DataDatabricksClusterPluginframework#num_workers}.'''
        result = self._values.get("num_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#policy_id DataDatabricksClusterPluginframework#policy_id}.'''
        result = self._values.get("policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_engine(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#runtime_engine DataDatabricksClusterPluginframework#runtime_engine}.'''
        result = self._values.get("runtime_engine")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def single_user_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#single_user_name DataDatabricksClusterPluginframework#single_user_name}.'''
        result = self._values.get("single_user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spark_conf(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spark_conf DataDatabricksClusterPluginframework#spark_conf}.'''
        result = self._values.get("spark_conf")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def spark_context_id(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spark_context_id DataDatabricksClusterPluginframework#spark_context_id}.'''
        result = self._values.get("spark_context_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def spark_env_vars(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spark_env_vars DataDatabricksClusterPluginframework#spark_env_vars}.'''
        result = self._values.get("spark_env_vars")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def spark_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spark_version DataDatabricksClusterPluginframework#spark_version}.'''
        result = self._values.get("spark_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spec(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpec"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spec DataDatabricksClusterPluginframework#spec}.'''
        result = self._values.get("spec")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpec"], result)

    @builtins.property
    def ssh_public_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ssh_public_keys DataDatabricksClusterPluginframework#ssh_public_keys}.'''
        result = self._values.get("ssh_public_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def start_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#start_time DataDatabricksClusterPluginframework#start_time}.'''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#state DataDatabricksClusterPluginframework#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state_message(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#state_message DataDatabricksClusterPluginframework#state_message}.'''
        result = self._values.get("state_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def terminated_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#terminated_time DataDatabricksClusterPluginframework#terminated_time}.'''
        result = self._values.get("terminated_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def termination_reason(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoTerminationReason"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#termination_reason DataDatabricksClusterPluginframework#termination_reason}.'''
        result = self._values.get("termination_reason")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoTerminationReason"], result)

    @builtins.property
    def workload_type(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoWorkloadType"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#workload_type DataDatabricksClusterPluginframework#workload_type}.'''
        result = self._values.get("workload_type")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoWorkloadType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoAutoscale",
    jsii_struct_bases=[],
    name_mapping={"max_workers": "maxWorkers", "min_workers": "minWorkers"},
)
class DataDatabricksClusterPluginframeworkClusterInfoAutoscale:
    def __init__(
        self,
        *,
        max_workers: typing.Optional[jsii.Number] = None,
        min_workers: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#max_workers DataDatabricksClusterPluginframework#max_workers}.
        :param min_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#min_workers DataDatabricksClusterPluginframework#min_workers}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a491b50ffd2d0df548ca1223d74097008523070bca7e61f2e5f1da760d7a3147)
            check_type(argname="argument max_workers", value=max_workers, expected_type=type_hints["max_workers"])
            check_type(argname="argument min_workers", value=min_workers, expected_type=type_hints["min_workers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_workers is not None:
            self._values["max_workers"] = max_workers
        if min_workers is not None:
            self._values["min_workers"] = min_workers

    @builtins.property
    def max_workers(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#max_workers DataDatabricksClusterPluginframework#max_workers}.'''
        result = self._values.get("max_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_workers(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#min_workers DataDatabricksClusterPluginframework#min_workers}.'''
        result = self._values.get("min_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoAutoscale(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoAutoscaleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoAutoscaleOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4904f1c6baabcf0658ccb5df187cdfedb6169cb7437bba2961aaa95f040d89dc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxWorkers")
    def reset_max_workers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxWorkers", []))

    @jsii.member(jsii_name="resetMinWorkers")
    def reset_min_workers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinWorkers", []))

    @builtins.property
    @jsii.member(jsii_name="maxWorkersInput")
    def max_workers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxWorkersInput"))

    @builtins.property
    @jsii.member(jsii_name="minWorkersInput")
    def min_workers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minWorkersInput"))

    @builtins.property
    @jsii.member(jsii_name="maxWorkers")
    def max_workers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxWorkers"))

    @max_workers.setter
    def max_workers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__698fef5441edbb1daa034e43e877a7cc57217ed46a88e950e46db7e4650cbb06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxWorkers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minWorkers")
    def min_workers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minWorkers"))

    @min_workers.setter
    def min_workers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94a0b80199c9b0ae6e3b956f6c7ab6bdcb5489b8a5035275127838aa8724c36f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minWorkers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoAutoscale]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoAutoscale]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoAutoscale]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a7b63e7ea72a41861d5a7bf6014139dffd087ddd7f574daff618deb0efa1cb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoAwsAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "availability": "availability",
        "ebs_volume_count": "ebsVolumeCount",
        "ebs_volume_iops": "ebsVolumeIops",
        "ebs_volume_size": "ebsVolumeSize",
        "ebs_volume_throughput": "ebsVolumeThroughput",
        "ebs_volume_type": "ebsVolumeType",
        "first_on_demand": "firstOnDemand",
        "instance_profile_arn": "instanceProfileArn",
        "spot_bid_price_percent": "spotBidPricePercent",
        "zone_id": "zoneId",
    },
)
class DataDatabricksClusterPluginframeworkClusterInfoAwsAttributes:
    def __init__(
        self,
        *,
        availability: typing.Optional[builtins.str] = None,
        ebs_volume_count: typing.Optional[jsii.Number] = None,
        ebs_volume_iops: typing.Optional[jsii.Number] = None,
        ebs_volume_size: typing.Optional[jsii.Number] = None,
        ebs_volume_throughput: typing.Optional[jsii.Number] = None,
        ebs_volume_type: typing.Optional[builtins.str] = None,
        first_on_demand: typing.Optional[jsii.Number] = None,
        instance_profile_arn: typing.Optional[builtins.str] = None,
        spot_bid_price_percent: typing.Optional[jsii.Number] = None,
        zone_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#availability DataDatabricksClusterPluginframework#availability}.
        :param ebs_volume_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_count DataDatabricksClusterPluginframework#ebs_volume_count}.
        :param ebs_volume_iops: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_iops DataDatabricksClusterPluginframework#ebs_volume_iops}.
        :param ebs_volume_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_size DataDatabricksClusterPluginframework#ebs_volume_size}.
        :param ebs_volume_throughput: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_throughput DataDatabricksClusterPluginframework#ebs_volume_throughput}.
        :param ebs_volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_type DataDatabricksClusterPluginframework#ebs_volume_type}.
        :param first_on_demand: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#first_on_demand DataDatabricksClusterPluginframework#first_on_demand}.
        :param instance_profile_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#instance_profile_arn DataDatabricksClusterPluginframework#instance_profile_arn}.
        :param spot_bid_price_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spot_bid_price_percent DataDatabricksClusterPluginframework#spot_bid_price_percent}.
        :param zone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#zone_id DataDatabricksClusterPluginframework#zone_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__142a1d57ec24d0655a019d4b468ec67298c2703f1a99e6e94b46bdd27a719d64)
            check_type(argname="argument availability", value=availability, expected_type=type_hints["availability"])
            check_type(argname="argument ebs_volume_count", value=ebs_volume_count, expected_type=type_hints["ebs_volume_count"])
            check_type(argname="argument ebs_volume_iops", value=ebs_volume_iops, expected_type=type_hints["ebs_volume_iops"])
            check_type(argname="argument ebs_volume_size", value=ebs_volume_size, expected_type=type_hints["ebs_volume_size"])
            check_type(argname="argument ebs_volume_throughput", value=ebs_volume_throughput, expected_type=type_hints["ebs_volume_throughput"])
            check_type(argname="argument ebs_volume_type", value=ebs_volume_type, expected_type=type_hints["ebs_volume_type"])
            check_type(argname="argument first_on_demand", value=first_on_demand, expected_type=type_hints["first_on_demand"])
            check_type(argname="argument instance_profile_arn", value=instance_profile_arn, expected_type=type_hints["instance_profile_arn"])
            check_type(argname="argument spot_bid_price_percent", value=spot_bid_price_percent, expected_type=type_hints["spot_bid_price_percent"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability is not None:
            self._values["availability"] = availability
        if ebs_volume_count is not None:
            self._values["ebs_volume_count"] = ebs_volume_count
        if ebs_volume_iops is not None:
            self._values["ebs_volume_iops"] = ebs_volume_iops
        if ebs_volume_size is not None:
            self._values["ebs_volume_size"] = ebs_volume_size
        if ebs_volume_throughput is not None:
            self._values["ebs_volume_throughput"] = ebs_volume_throughput
        if ebs_volume_type is not None:
            self._values["ebs_volume_type"] = ebs_volume_type
        if first_on_demand is not None:
            self._values["first_on_demand"] = first_on_demand
        if instance_profile_arn is not None:
            self._values["instance_profile_arn"] = instance_profile_arn
        if spot_bid_price_percent is not None:
            self._values["spot_bid_price_percent"] = spot_bid_price_percent
        if zone_id is not None:
            self._values["zone_id"] = zone_id

    @builtins.property
    def availability(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#availability DataDatabricksClusterPluginframework#availability}.'''
        result = self._values.get("availability")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ebs_volume_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_count DataDatabricksClusterPluginframework#ebs_volume_count}.'''
        result = self._values.get("ebs_volume_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ebs_volume_iops(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_iops DataDatabricksClusterPluginframework#ebs_volume_iops}.'''
        result = self._values.get("ebs_volume_iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ebs_volume_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_size DataDatabricksClusterPluginframework#ebs_volume_size}.'''
        result = self._values.get("ebs_volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ebs_volume_throughput(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_throughput DataDatabricksClusterPluginframework#ebs_volume_throughput}.'''
        result = self._values.get("ebs_volume_throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ebs_volume_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_type DataDatabricksClusterPluginframework#ebs_volume_type}.'''
        result = self._values.get("ebs_volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def first_on_demand(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#first_on_demand DataDatabricksClusterPluginframework#first_on_demand}.'''
        result = self._values.get("first_on_demand")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def instance_profile_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#instance_profile_arn DataDatabricksClusterPluginframework#instance_profile_arn}.'''
        result = self._values.get("instance_profile_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spot_bid_price_percent(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spot_bid_price_percent DataDatabricksClusterPluginframework#spot_bid_price_percent}.'''
        result = self._values.get("spot_bid_price_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def zone_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#zone_id DataDatabricksClusterPluginframework#zone_id}.'''
        result = self._values.get("zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoAwsAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoAwsAttributesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoAwsAttributesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e62c8bbe0639e01091d2bc211f2d291012684b198071a0713dc3a254e3eedd63)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAvailability")
    def reset_availability(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailability", []))

    @jsii.member(jsii_name="resetEbsVolumeCount")
    def reset_ebs_volume_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEbsVolumeCount", []))

    @jsii.member(jsii_name="resetEbsVolumeIops")
    def reset_ebs_volume_iops(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEbsVolumeIops", []))

    @jsii.member(jsii_name="resetEbsVolumeSize")
    def reset_ebs_volume_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEbsVolumeSize", []))

    @jsii.member(jsii_name="resetEbsVolumeThroughput")
    def reset_ebs_volume_throughput(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEbsVolumeThroughput", []))

    @jsii.member(jsii_name="resetEbsVolumeType")
    def reset_ebs_volume_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEbsVolumeType", []))

    @jsii.member(jsii_name="resetFirstOnDemand")
    def reset_first_on_demand(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirstOnDemand", []))

    @jsii.member(jsii_name="resetInstanceProfileArn")
    def reset_instance_profile_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceProfileArn", []))

    @jsii.member(jsii_name="resetSpotBidPricePercent")
    def reset_spot_bid_price_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpotBidPricePercent", []))

    @jsii.member(jsii_name="resetZoneId")
    def reset_zone_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZoneId", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityInput")
    def availability_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeCountInput")
    def ebs_volume_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ebsVolumeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeIopsInput")
    def ebs_volume_iops_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ebsVolumeIopsInput"))

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeSizeInput")
    def ebs_volume_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ebsVolumeSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeThroughputInput")
    def ebs_volume_throughput_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ebsVolumeThroughputInput"))

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeTypeInput")
    def ebs_volume_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ebsVolumeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="firstOnDemandInput")
    def first_on_demand_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "firstOnDemandInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceProfileArnInput")
    def instance_profile_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceProfileArnInput"))

    @builtins.property
    @jsii.member(jsii_name="spotBidPricePercentInput")
    def spot_bid_price_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "spotBidPricePercentInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneIdInput")
    def zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="availability")
    def availability(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availability"))

    @availability.setter
    def availability(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__904e31f6e42c22cd19debbf895213aa321fc9103a539ae6324024bde1107d51b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availability", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeCount")
    def ebs_volume_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ebsVolumeCount"))

    @ebs_volume_count.setter
    def ebs_volume_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0c352d5197c4f3ba78d2c2374be9a15c0c0aef00d6ddc6e153c230a9dfe92fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ebsVolumeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeIops")
    def ebs_volume_iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ebsVolumeIops"))

    @ebs_volume_iops.setter
    def ebs_volume_iops(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__275f0b10442867b91c0ad06d8fc05383f9ea2fb7eb5f6dfadfe4962274c56406)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ebsVolumeIops", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeSize")
    def ebs_volume_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ebsVolumeSize"))

    @ebs_volume_size.setter
    def ebs_volume_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a6ed9e1d7216b331270b577ac951111df47814d211a960cfbdb96611b8aca44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ebsVolumeSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeThroughput")
    def ebs_volume_throughput(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ebsVolumeThroughput"))

    @ebs_volume_throughput.setter
    def ebs_volume_throughput(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f29e53e21a527c4c8cf5c00ca3dc12211f9b16a0d39f973ff6945532812796f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ebsVolumeThroughput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeType")
    def ebs_volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ebsVolumeType"))

    @ebs_volume_type.setter
    def ebs_volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ccb26e151487a86d2747fe756daebd4b3e04841a8f7dfb18283cc0b2d94a02d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ebsVolumeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firstOnDemand")
    def first_on_demand(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "firstOnDemand"))

    @first_on_demand.setter
    def first_on_demand(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0698a8228e86d65933796913d83382a52c64526737d1f5d8ef2deb7fe7a5edb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstOnDemand", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceProfileArn")
    def instance_profile_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceProfileArn"))

    @instance_profile_arn.setter
    def instance_profile_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f087f005c035cb88bda9a0af8d925b4f411a6a3aed8a16d509fbc0604db80fde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceProfileArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="spotBidPricePercent")
    def spot_bid_price_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "spotBidPricePercent"))

    @spot_bid_price_percent.setter
    def spot_bid_price_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9950ef57c2924fb82aeed6ee9475c9af8d6d4af6bca5400408edcf2b21f8bd45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spotBidPricePercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__720ce8cc362784d56407b7c1575bc3303dfe3dd8a5a296911412314190882324)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoAwsAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoAwsAttributes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoAwsAttributes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a65d5eb6afd08bf75467f438521c07659a3d9fabd8c23d57f42f66b88f6fb8ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoAzureAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "availability": "availability",
        "first_on_demand": "firstOnDemand",
        "log_analytics_info": "logAnalyticsInfo",
        "spot_bid_max_price": "spotBidMaxPrice",
    },
)
class DataDatabricksClusterPluginframeworkClusterInfoAzureAttributes:
    def __init__(
        self,
        *,
        availability: typing.Optional[builtins.str] = None,
        first_on_demand: typing.Optional[jsii.Number] = None,
        log_analytics_info: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesLogAnalyticsInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        spot_bid_max_price: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param availability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#availability DataDatabricksClusterPluginframework#availability}.
        :param first_on_demand: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#first_on_demand DataDatabricksClusterPluginframework#first_on_demand}.
        :param log_analytics_info: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#log_analytics_info DataDatabricksClusterPluginframework#log_analytics_info}.
        :param spot_bid_max_price: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spot_bid_max_price DataDatabricksClusterPluginframework#spot_bid_max_price}.
        '''
        if isinstance(log_analytics_info, dict):
            log_analytics_info = DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesLogAnalyticsInfo(**log_analytics_info)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c61c05d47a38992ce40e850f42c3a434cf5738de3592f9c72427efe14ac1c06)
            check_type(argname="argument availability", value=availability, expected_type=type_hints["availability"])
            check_type(argname="argument first_on_demand", value=first_on_demand, expected_type=type_hints["first_on_demand"])
            check_type(argname="argument log_analytics_info", value=log_analytics_info, expected_type=type_hints["log_analytics_info"])
            check_type(argname="argument spot_bid_max_price", value=spot_bid_max_price, expected_type=type_hints["spot_bid_max_price"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability is not None:
            self._values["availability"] = availability
        if first_on_demand is not None:
            self._values["first_on_demand"] = first_on_demand
        if log_analytics_info is not None:
            self._values["log_analytics_info"] = log_analytics_info
        if spot_bid_max_price is not None:
            self._values["spot_bid_max_price"] = spot_bid_max_price

    @builtins.property
    def availability(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#availability DataDatabricksClusterPluginframework#availability}.'''
        result = self._values.get("availability")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def first_on_demand(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#first_on_demand DataDatabricksClusterPluginframework#first_on_demand}.'''
        result = self._values.get("first_on_demand")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def log_analytics_info(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesLogAnalyticsInfo"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#log_analytics_info DataDatabricksClusterPluginframework#log_analytics_info}.'''
        result = self._values.get("log_analytics_info")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesLogAnalyticsInfo"], result)

    @builtins.property
    def spot_bid_max_price(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spot_bid_max_price DataDatabricksClusterPluginframework#spot_bid_max_price}.'''
        result = self._values.get("spot_bid_max_price")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoAzureAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesLogAnalyticsInfo",
    jsii_struct_bases=[],
    name_mapping={
        "log_analytics_primary_key": "logAnalyticsPrimaryKey",
        "log_analytics_workspace_id": "logAnalyticsWorkspaceId",
    },
)
class DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesLogAnalyticsInfo:
    def __init__(
        self,
        *,
        log_analytics_primary_key: typing.Optional[builtins.str] = None,
        log_analytics_workspace_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param log_analytics_primary_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#log_analytics_primary_key DataDatabricksClusterPluginframework#log_analytics_primary_key}.
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#log_analytics_workspace_id DataDatabricksClusterPluginframework#log_analytics_workspace_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d1311071d7443791899381b56ddcd2a9b3069ad7a310808fd13999544a9c25e)
            check_type(argname="argument log_analytics_primary_key", value=log_analytics_primary_key, expected_type=type_hints["log_analytics_primary_key"])
            check_type(argname="argument log_analytics_workspace_id", value=log_analytics_workspace_id, expected_type=type_hints["log_analytics_workspace_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_analytics_primary_key is not None:
            self._values["log_analytics_primary_key"] = log_analytics_primary_key
        if log_analytics_workspace_id is not None:
            self._values["log_analytics_workspace_id"] = log_analytics_workspace_id

    @builtins.property
    def log_analytics_primary_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#log_analytics_primary_key DataDatabricksClusterPluginframework#log_analytics_primary_key}.'''
        result = self._values.get("log_analytics_primary_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_analytics_workspace_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#log_analytics_workspace_id DataDatabricksClusterPluginframework#log_analytics_workspace_id}.'''
        result = self._values.get("log_analytics_workspace_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesLogAnalyticsInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesLogAnalyticsInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesLogAnalyticsInfoOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b283e45fbdfc87a748b46573663aa317e9036b00e97eebc85f450a2d315c1a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLogAnalyticsPrimaryKey")
    def reset_log_analytics_primary_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogAnalyticsPrimaryKey", []))

    @jsii.member(jsii_name="resetLogAnalyticsWorkspaceId")
    def reset_log_analytics_workspace_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogAnalyticsWorkspaceId", []))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsPrimaryKeyInput")
    def log_analytics_primary_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logAnalyticsPrimaryKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsWorkspaceIdInput")
    def log_analytics_workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logAnalyticsWorkspaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsPrimaryKey")
    def log_analytics_primary_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logAnalyticsPrimaryKey"))

    @log_analytics_primary_key.setter
    def log_analytics_primary_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf3eafc6f7bf090d0434c663c16cc3c8800f2fd4c568c5cde0e2d44e3d733503)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAnalyticsPrimaryKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsWorkspaceId")
    def log_analytics_workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logAnalyticsWorkspaceId"))

    @log_analytics_workspace_id.setter
    def log_analytics_workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__857c25e4590e5b05ab53b20a8ae6ef252e1d38e128405e448985784b8ca141b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAnalyticsWorkspaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesLogAnalyticsInfo]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesLogAnalyticsInfo]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesLogAnalyticsInfo]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fe46080c75b16c4e6380646f1ee6277bd6315a2688d0b5f9abc0a86be8f38ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__195c567bbe2f4f15052c871cd81cda0ae5d6ee7dd8e27d211942088dec87c439)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLogAnalyticsInfo")
    def put_log_analytics_info(
        self,
        *,
        log_analytics_primary_key: typing.Optional[builtins.str] = None,
        log_analytics_workspace_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param log_analytics_primary_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#log_analytics_primary_key DataDatabricksClusterPluginframework#log_analytics_primary_key}.
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#log_analytics_workspace_id DataDatabricksClusterPluginframework#log_analytics_workspace_id}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesLogAnalyticsInfo(
            log_analytics_primary_key=log_analytics_primary_key,
            log_analytics_workspace_id=log_analytics_workspace_id,
        )

        return typing.cast(None, jsii.invoke(self, "putLogAnalyticsInfo", [value]))

    @jsii.member(jsii_name="resetAvailability")
    def reset_availability(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailability", []))

    @jsii.member(jsii_name="resetFirstOnDemand")
    def reset_first_on_demand(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirstOnDemand", []))

    @jsii.member(jsii_name="resetLogAnalyticsInfo")
    def reset_log_analytics_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogAnalyticsInfo", []))

    @jsii.member(jsii_name="resetSpotBidMaxPrice")
    def reset_spot_bid_max_price(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpotBidMaxPrice", []))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsInfo")
    def log_analytics_info(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesLogAnalyticsInfoOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesLogAnalyticsInfoOutputReference, jsii.get(self, "logAnalyticsInfo"))

    @builtins.property
    @jsii.member(jsii_name="availabilityInput")
    def availability_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="firstOnDemandInput")
    def first_on_demand_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "firstOnDemandInput"))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsInfoInput")
    def log_analytics_info_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesLogAnalyticsInfo]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesLogAnalyticsInfo]], jsii.get(self, "logAnalyticsInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="spotBidMaxPriceInput")
    def spot_bid_max_price_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "spotBidMaxPriceInput"))

    @builtins.property
    @jsii.member(jsii_name="availability")
    def availability(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availability"))

    @availability.setter
    def availability(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__793c0d8feafc6317e8b50bbdfed29f9c383be8e49c1d16cdc11412b3b0266dea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availability", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firstOnDemand")
    def first_on_demand(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "firstOnDemand"))

    @first_on_demand.setter
    def first_on_demand(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c6c35766ca77c3b1f6d39b7ac874f087b59dbcb49565de189e6aba968248245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstOnDemand", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="spotBidMaxPrice")
    def spot_bid_max_price(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "spotBidMaxPrice"))

    @spot_bid_max_price.setter
    def spot_bid_max_price(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f47b453c963543e03cc475bd9e42ca0a0266bfd5d79d9f18260fe691b7075b71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spotBidMaxPrice", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoAzureAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoAzureAttributes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoAzureAttributes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3339022c88de46316fdcc079352dcec63e7ee29a0bd5210e79b8da44c8048074)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoClusterLogConf",
    jsii_struct_bases=[],
    name_mapping={"dbfs": "dbfs", "s3": "s3"},
)
class DataDatabricksClusterPluginframeworkClusterInfoClusterLogConf:
    def __init__(
        self,
        *,
        dbfs: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfDbfs", typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfS3", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dbfs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#dbfs DataDatabricksClusterPluginframework#dbfs}.
        :param s3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#s3 DataDatabricksClusterPluginframework#s3}.
        '''
        if isinstance(dbfs, dict):
            dbfs = DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfDbfs(**dbfs)
        if isinstance(s3, dict):
            s3 = DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfS3(**s3)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95302eabb56e430f0bf11cc230528c1cfb77d2e95370bbefedf10acded5c032c)
            check_type(argname="argument dbfs", value=dbfs, expected_type=type_hints["dbfs"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dbfs is not None:
            self._values["dbfs"] = dbfs
        if s3 is not None:
            self._values["s3"] = s3

    @builtins.property
    def dbfs(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfDbfs"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#dbfs DataDatabricksClusterPluginframework#dbfs}.'''
        result = self._values.get("dbfs")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfDbfs"], result)

    @builtins.property
    def s3(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfS3"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#s3 DataDatabricksClusterPluginframework#s3}.'''
        result = self._values.get("s3")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfS3"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoClusterLogConf(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfDbfs",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination"},
)
class DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfDbfs:
    def __init__(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d5183648012b17b641618704764a775971084023ff2e2f60068931610606a91)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
        }

    @builtins.property
    def destination(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfDbfs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfDbfsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfDbfsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f0850c0d411624f7c6e9e0198d082bf2d71a71b6cfd4297980f41e92492696)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f93007cafddd4b565fb8a01fef8c3af31433dce3aa0f543b02c252d476dba353)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfDbfs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfDbfs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfDbfs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c572f2de82973a2681abe43a44c2495ac11eaedb847e626c991179bf2314bfb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cede6b0bb78cb04c20315c1a9ff59e1a05a47ddae8298b7e7f7c7c22a3cbaec0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDbfs")
    def put_dbfs(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfDbfs(
            destination=destination
        )

        return typing.cast(None, jsii.invoke(self, "putDbfs", [value]))

    @jsii.member(jsii_name="putS3")
    def put_s3(
        self,
        *,
        destination: builtins.str,
        canned_acl: typing.Optional[builtins.str] = None,
        enable_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_type: typing.Optional[builtins.str] = None,
        endpoint: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        :param canned_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#canned_acl DataDatabricksClusterPluginframework#canned_acl}.
        :param enable_encryption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#enable_encryption DataDatabricksClusterPluginframework#enable_encryption}.
        :param encryption_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#encryption_type DataDatabricksClusterPluginframework#encryption_type}.
        :param endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#endpoint DataDatabricksClusterPluginframework#endpoint}.
        :param kms_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#kms_key DataDatabricksClusterPluginframework#kms_key}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#region DataDatabricksClusterPluginframework#region}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfS3(
            destination=destination,
            canned_acl=canned_acl,
            enable_encryption=enable_encryption,
            encryption_type=encryption_type,
            endpoint=endpoint,
            kms_key=kms_key,
            region=region,
        )

        return typing.cast(None, jsii.invoke(self, "putS3", [value]))

    @jsii.member(jsii_name="resetDbfs")
    def reset_dbfs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDbfs", []))

    @jsii.member(jsii_name="resetS3")
    def reset_s3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3", []))

    @builtins.property
    @jsii.member(jsii_name="dbfs")
    def dbfs(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfDbfsOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfDbfsOutputReference, jsii.get(self, "dbfs"))

    @builtins.property
    @jsii.member(jsii_name="s3")
    def s3(
        self,
    ) -> "DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfS3OutputReference":
        return typing.cast("DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfS3OutputReference", jsii.get(self, "s3"))

    @builtins.property
    @jsii.member(jsii_name="dbfsInput")
    def dbfs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfDbfs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfDbfs]], jsii.get(self, "dbfsInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Input")
    def s3_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfS3"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfS3"]], jsii.get(self, "s3Input"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoClusterLogConf]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoClusterLogConf]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoClusterLogConf]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ffee980eddf2c3afa00bf8f51affbe4a315f9b95c02abd1926a9e6153fb421)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfS3",
    jsii_struct_bases=[],
    name_mapping={
        "destination": "destination",
        "canned_acl": "cannedAcl",
        "enable_encryption": "enableEncryption",
        "encryption_type": "encryptionType",
        "endpoint": "endpoint",
        "kms_key": "kmsKey",
        "region": "region",
    },
)
class DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfS3:
    def __init__(
        self,
        *,
        destination: builtins.str,
        canned_acl: typing.Optional[builtins.str] = None,
        enable_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_type: typing.Optional[builtins.str] = None,
        endpoint: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        :param canned_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#canned_acl DataDatabricksClusterPluginframework#canned_acl}.
        :param enable_encryption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#enable_encryption DataDatabricksClusterPluginframework#enable_encryption}.
        :param encryption_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#encryption_type DataDatabricksClusterPluginframework#encryption_type}.
        :param endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#endpoint DataDatabricksClusterPluginframework#endpoint}.
        :param kms_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#kms_key DataDatabricksClusterPluginframework#kms_key}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#region DataDatabricksClusterPluginframework#region}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c98e750f3ea6c7db093fc50b5b184f8d691236b029681782c353f0c94bd6bf63)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument canned_acl", value=canned_acl, expected_type=type_hints["canned_acl"])
            check_type(argname="argument enable_encryption", value=enable_encryption, expected_type=type_hints["enable_encryption"])
            check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
        }
        if canned_acl is not None:
            self._values["canned_acl"] = canned_acl
        if enable_encryption is not None:
            self._values["enable_encryption"] = enable_encryption
        if encryption_type is not None:
            self._values["encryption_type"] = encryption_type
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def destination(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def canned_acl(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#canned_acl DataDatabricksClusterPluginframework#canned_acl}.'''
        result = self._values.get("canned_acl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_encryption(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#enable_encryption DataDatabricksClusterPluginframework#enable_encryption}.'''
        result = self._values.get("enable_encryption")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#encryption_type DataDatabricksClusterPluginframework#encryption_type}.'''
        result = self._values.get("encryption_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#endpoint DataDatabricksClusterPluginframework#endpoint}.'''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#kms_key DataDatabricksClusterPluginframework#kms_key}.'''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#region DataDatabricksClusterPluginframework#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfS3(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfS3OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfS3OutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf7cf385061a94ce6b175b9d54c96a3d78b9a78635b83847e19967be564b626e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCannedAcl")
    def reset_canned_acl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCannedAcl", []))

    @jsii.member(jsii_name="resetEnableEncryption")
    def reset_enable_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableEncryption", []))

    @jsii.member(jsii_name="resetEncryptionType")
    def reset_encryption_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionType", []))

    @jsii.member(jsii_name="resetEndpoint")
    def reset_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpoint", []))

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @builtins.property
    @jsii.member(jsii_name="cannedAclInput")
    def canned_acl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cannedAclInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="enableEncryptionInput")
    def enable_encryption_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionTypeInput")
    def encryption_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointInput")
    def endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="cannedAcl")
    def canned_acl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cannedAcl"))

    @canned_acl.setter
    def canned_acl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__975ca4c0ba52e9415f2c50e90f2ceb956c430634e0c55ba0fb8f4a184ab8f0b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cannedAcl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ad34fa87b4b77d11ed4df63fb8fbde5d9d0ec619edd24df6374df2c5dfa50f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableEncryption")
    def enable_encryption(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableEncryption"))

    @enable_encryption.setter
    def enable_encryption(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a925b7763e61f59762e328046864ab4f84e4594a5382e69bfabd9eebc434d7f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableEncryption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionType")
    def encryption_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionType"))

    @encryption_type.setter
    def encryption_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e4cb417d29e2b0ad71a2768a6b5d259f815b0b6511fc84dff2ff8136978e54a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @endpoint.setter
    def endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__370d3d8c80313b4583ec17e8d6213a9b4d0ea92b64b6a026c28ccba2a94d764e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99577b4567caa6106c489cf26e9efee1b0ec0bb1eb2e31f16eba943ec4cafc8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__951d1731f36f0e1090f807ac5955e36582e17705cbd37807556ee5178cb8900d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfS3]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfS3]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfS3]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f697b98e3928d89e790f67e79925331a10b2b83ed2d7afff2444f56e252db75e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoClusterLogStatus",
    jsii_struct_bases=[],
    name_mapping={
        "last_attempted": "lastAttempted",
        "last_exception": "lastException",
    },
)
class DataDatabricksClusterPluginframeworkClusterInfoClusterLogStatus:
    def __init__(
        self,
        *,
        last_attempted: typing.Optional[jsii.Number] = None,
        last_exception: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param last_attempted: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#last_attempted DataDatabricksClusterPluginframework#last_attempted}.
        :param last_exception: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#last_exception DataDatabricksClusterPluginframework#last_exception}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__144ff888cfde69b59c8d604dc20588fea18685c93aa5241e44e12024973ce3c4)
            check_type(argname="argument last_attempted", value=last_attempted, expected_type=type_hints["last_attempted"])
            check_type(argname="argument last_exception", value=last_exception, expected_type=type_hints["last_exception"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if last_attempted is not None:
            self._values["last_attempted"] = last_attempted
        if last_exception is not None:
            self._values["last_exception"] = last_exception

    @builtins.property
    def last_attempted(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#last_attempted DataDatabricksClusterPluginframework#last_attempted}.'''
        result = self._values.get("last_attempted")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def last_exception(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#last_exception DataDatabricksClusterPluginframework#last_exception}.'''
        result = self._values.get("last_exception")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoClusterLogStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoClusterLogStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoClusterLogStatusOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa0f79b2abaa42e43734c8d32d1029b225f0f2456669c010dcc1f8a552d1f786)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLastAttempted")
    def reset_last_attempted(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastAttempted", []))

    @jsii.member(jsii_name="resetLastException")
    def reset_last_exception(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastException", []))

    @builtins.property
    @jsii.member(jsii_name="lastAttemptedInput")
    def last_attempted_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lastAttemptedInput"))

    @builtins.property
    @jsii.member(jsii_name="lastExceptionInput")
    def last_exception_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastExceptionInput"))

    @builtins.property
    @jsii.member(jsii_name="lastAttempted")
    def last_attempted(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lastAttempted"))

    @last_attempted.setter
    def last_attempted(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8bf40e64683ad0905d9ca42023c302661389a39afb755e521e4b453a07ef9e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastAttempted", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lastException")
    def last_exception(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastException"))

    @last_exception.setter
    def last_exception(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dbc676216696d2dc7b36d8817c9d865a8e8aa657893bdc97b37b62f97530d29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastException", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoClusterLogStatus]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoClusterLogStatus]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoClusterLogStatus]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d270a2fb60128fa29e9d9653fb4ef00f5252efe4b761af762cdfe1bc021ca4be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoDockerImage",
    jsii_struct_bases=[],
    name_mapping={"basic_auth": "basicAuth", "url": "url"},
)
class DataDatabricksClusterPluginframeworkClusterInfoDockerImage:
    def __init__(
        self,
        *,
        basic_auth: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoDockerImageBasicAuth", typing.Dict[builtins.str, typing.Any]]] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param basic_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#basic_auth DataDatabricksClusterPluginframework#basic_auth}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#url DataDatabricksClusterPluginframework#url}.
        '''
        if isinstance(basic_auth, dict):
            basic_auth = DataDatabricksClusterPluginframeworkClusterInfoDockerImageBasicAuth(**basic_auth)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07c456f251d379d56612b7038692260e5ac27b29a34ff0fe6b3c6825f3c4466c)
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if basic_auth is not None:
            self._values["basic_auth"] = basic_auth
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def basic_auth(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoDockerImageBasicAuth"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#basic_auth DataDatabricksClusterPluginframework#basic_auth}.'''
        result = self._values.get("basic_auth")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoDockerImageBasicAuth"], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#url DataDatabricksClusterPluginframework#url}.'''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoDockerImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoDockerImageBasicAuth",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class DataDatabricksClusterPluginframeworkClusterInfoDockerImageBasicAuth:
    def __init__(
        self,
        *,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#password DataDatabricksClusterPluginframework#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#username DataDatabricksClusterPluginframework#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef22e7d121df0b664ce9a72f8022ccf0cb5087301aff9cb0ab689abba37a7c69)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if password is not None:
            self._values["password"] = password
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#password DataDatabricksClusterPluginframework#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#username DataDatabricksClusterPluginframework#username}.'''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoDockerImageBasicAuth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoDockerImageBasicAuthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoDockerImageBasicAuthOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b255db7c5e0ec9495a169e0bda6a701ba707183bc24e3b6f7de929d2b4619ffe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25492122a1c428af1290c8a2b7b5cc683da028513abe10e41bb4caebd426be1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67eee541ad5cc79b66d632ba12ad32d1696415284768f18738f79fbcb2073538)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoDockerImageBasicAuth]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoDockerImageBasicAuth]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoDockerImageBasicAuth]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77c089fd9c55b2744e67f2002099e877b779f7935dbe31fa4b8aa2b9567b4347)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksClusterPluginframeworkClusterInfoDockerImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoDockerImageOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3d04ed0d16050f818adb5ebf739f656524cff2952c064517257145e916b8c7d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBasicAuth")
    def put_basic_auth(
        self,
        *,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#password DataDatabricksClusterPluginframework#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#username DataDatabricksClusterPluginframework#username}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoDockerImageBasicAuth(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putBasicAuth", [value]))

    @jsii.member(jsii_name="resetBasicAuth")
    def reset_basic_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasicAuth", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @builtins.property
    @jsii.member(jsii_name="basicAuth")
    def basic_auth(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoDockerImageBasicAuthOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoDockerImageBasicAuthOutputReference, jsii.get(self, "basicAuth"))

    @builtins.property
    @jsii.member(jsii_name="basicAuthInput")
    def basic_auth_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoDockerImageBasicAuth]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoDockerImageBasicAuth]], jsii.get(self, "basicAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91a866d2e2d518cc072bc2b58df06ab0de1c4e6f4ef887095a71d6b5f461d403)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoDockerImage]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoDockerImage]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoDockerImage]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79b8c4fd40b12ec57488eb9f8b598ca03f32c6d72288d4f03affb7db614ab98e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoDriver",
    jsii_struct_bases=[],
    name_mapping={
        "host_private_ip": "hostPrivateIp",
        "instance_id": "instanceId",
        "node_aws_attributes": "nodeAwsAttributes",
        "node_id": "nodeId",
        "private_ip": "privateIp",
        "public_dns": "publicDns",
        "start_timestamp": "startTimestamp",
    },
)
class DataDatabricksClusterPluginframeworkClusterInfoDriver:
    def __init__(
        self,
        *,
        host_private_ip: typing.Optional[builtins.str] = None,
        instance_id: typing.Optional[builtins.str] = None,
        node_aws_attributes: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoDriverNodeAwsAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
        node_id: typing.Optional[builtins.str] = None,
        private_ip: typing.Optional[builtins.str] = None,
        public_dns: typing.Optional[builtins.str] = None,
        start_timestamp: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param host_private_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#host_private_ip DataDatabricksClusterPluginframework#host_private_ip}.
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#instance_id DataDatabricksClusterPluginframework#instance_id}.
        :param node_aws_attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#node_aws_attributes DataDatabricksClusterPluginframework#node_aws_attributes}.
        :param node_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#node_id DataDatabricksClusterPluginframework#node_id}.
        :param private_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#private_ip DataDatabricksClusterPluginframework#private_ip}.
        :param public_dns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#public_dns DataDatabricksClusterPluginframework#public_dns}.
        :param start_timestamp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#start_timestamp DataDatabricksClusterPluginframework#start_timestamp}.
        '''
        if isinstance(node_aws_attributes, dict):
            node_aws_attributes = DataDatabricksClusterPluginframeworkClusterInfoDriverNodeAwsAttributes(**node_aws_attributes)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f12dfa1954f4075bd8e49fb94e5ad113456f1677ac842a9ecbabe277d9dc1d17)
            check_type(argname="argument host_private_ip", value=host_private_ip, expected_type=type_hints["host_private_ip"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument node_aws_attributes", value=node_aws_attributes, expected_type=type_hints["node_aws_attributes"])
            check_type(argname="argument node_id", value=node_id, expected_type=type_hints["node_id"])
            check_type(argname="argument private_ip", value=private_ip, expected_type=type_hints["private_ip"])
            check_type(argname="argument public_dns", value=public_dns, expected_type=type_hints["public_dns"])
            check_type(argname="argument start_timestamp", value=start_timestamp, expected_type=type_hints["start_timestamp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if host_private_ip is not None:
            self._values["host_private_ip"] = host_private_ip
        if instance_id is not None:
            self._values["instance_id"] = instance_id
        if node_aws_attributes is not None:
            self._values["node_aws_attributes"] = node_aws_attributes
        if node_id is not None:
            self._values["node_id"] = node_id
        if private_ip is not None:
            self._values["private_ip"] = private_ip
        if public_dns is not None:
            self._values["public_dns"] = public_dns
        if start_timestamp is not None:
            self._values["start_timestamp"] = start_timestamp

    @builtins.property
    def host_private_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#host_private_ip DataDatabricksClusterPluginframework#host_private_ip}.'''
        result = self._values.get("host_private_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#instance_id DataDatabricksClusterPluginframework#instance_id}.'''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_aws_attributes(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoDriverNodeAwsAttributes"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#node_aws_attributes DataDatabricksClusterPluginframework#node_aws_attributes}.'''
        result = self._values.get("node_aws_attributes")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoDriverNodeAwsAttributes"], result)

    @builtins.property
    def node_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#node_id DataDatabricksClusterPluginframework#node_id}.'''
        result = self._values.get("node_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#private_ip DataDatabricksClusterPluginframework#private_ip}.'''
        result = self._values.get("private_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_dns(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#public_dns DataDatabricksClusterPluginframework#public_dns}.'''
        result = self._values.get("public_dns")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_timestamp(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#start_timestamp DataDatabricksClusterPluginframework#start_timestamp}.'''
        result = self._values.get("start_timestamp")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoDriver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoDriverNodeAwsAttributes",
    jsii_struct_bases=[],
    name_mapping={"is_spot": "isSpot"},
)
class DataDatabricksClusterPluginframeworkClusterInfoDriverNodeAwsAttributes:
    def __init__(
        self,
        *,
        is_spot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param is_spot: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#is_spot DataDatabricksClusterPluginframework#is_spot}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49d3706d6dd90dcc8863899ab883c718b81d62c5bce028d897b4fbbe319fdde9)
            check_type(argname="argument is_spot", value=is_spot, expected_type=type_hints["is_spot"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if is_spot is not None:
            self._values["is_spot"] = is_spot

    @builtins.property
    def is_spot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#is_spot DataDatabricksClusterPluginframework#is_spot}.'''
        result = self._values.get("is_spot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoDriverNodeAwsAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoDriverNodeAwsAttributesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoDriverNodeAwsAttributesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10b6aa1544838285c98c2d17e7ac7686c85f52c042c231829013c97f8230cb11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsSpot")
    def reset_is_spot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsSpot", []))

    @builtins.property
    @jsii.member(jsii_name="isSpotInput")
    def is_spot_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isSpotInput"))

    @builtins.property
    @jsii.member(jsii_name="isSpot")
    def is_spot(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isSpot"))

    @is_spot.setter
    def is_spot(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__402c40df8534fbd26162e2568120209f1ec61dcf219ca5d65ad7ce290b016fb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSpot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoDriverNodeAwsAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoDriverNodeAwsAttributes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoDriverNodeAwsAttributes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d8a488bd8b841fde7057767c68f1d99353d3a82c28fd668afb9bc45ee9a329b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksClusterPluginframeworkClusterInfoDriverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoDriverOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c16ea6c3c9dcb431d4b459ce055cb786e689c91794f39295e3d5b8b4f14f88ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodeAwsAttributes")
    def put_node_aws_attributes(
        self,
        *,
        is_spot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param is_spot: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#is_spot DataDatabricksClusterPluginframework#is_spot}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoDriverNodeAwsAttributes(
            is_spot=is_spot
        )

        return typing.cast(None, jsii.invoke(self, "putNodeAwsAttributes", [value]))

    @jsii.member(jsii_name="resetHostPrivateIp")
    def reset_host_private_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostPrivateIp", []))

    @jsii.member(jsii_name="resetInstanceId")
    def reset_instance_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceId", []))

    @jsii.member(jsii_name="resetNodeAwsAttributes")
    def reset_node_aws_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeAwsAttributes", []))

    @jsii.member(jsii_name="resetNodeId")
    def reset_node_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeId", []))

    @jsii.member(jsii_name="resetPrivateIp")
    def reset_private_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIp", []))

    @jsii.member(jsii_name="resetPublicDns")
    def reset_public_dns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicDns", []))

    @jsii.member(jsii_name="resetStartTimestamp")
    def reset_start_timestamp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTimestamp", []))

    @builtins.property
    @jsii.member(jsii_name="nodeAwsAttributes")
    def node_aws_attributes(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoDriverNodeAwsAttributesOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoDriverNodeAwsAttributesOutputReference, jsii.get(self, "nodeAwsAttributes"))

    @builtins.property
    @jsii.member(jsii_name="hostPrivateIpInput")
    def host_private_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostPrivateIpInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdInput")
    def instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeAwsAttributesInput")
    def node_aws_attributes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoDriverNodeAwsAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoDriverNodeAwsAttributes]], jsii.get(self, "nodeAwsAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeIdInput")
    def node_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpInput")
    def private_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpInput"))

    @builtins.property
    @jsii.member(jsii_name="publicDnsInput")
    def public_dns_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicDnsInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimestampInput")
    def start_timestamp_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startTimestampInput"))

    @builtins.property
    @jsii.member(jsii_name="hostPrivateIp")
    def host_private_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostPrivateIp"))

    @host_private_ip.setter
    def host_private_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bc9832d7a4fc77fc89b980baff9aae4b433cdc76ed1c092978450d7c4157169)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostPrivateIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba8b315ed569bad79802068ecf82a3a31cfbc8570736e9e4c2391277989c8294)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeId")
    def node_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeId"))

    @node_id.setter
    def node_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f5f70a44436e99478c8f8a0d69ea081aa3d5da0fdcf0c56f875d44788339ccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIp")
    def private_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIp"))

    @private_ip.setter
    def private_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e07a3590d6b33307133e8d4daf582d83b59415eab17ac250a56a8a0878f66f35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicDns")
    def public_dns(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicDns"))

    @public_dns.setter
    def public_dns(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__727a1b84d6a7a0e1759726220cfffbd6512babefe99938f66e9b68adafdbc3c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicDns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTimestamp")
    def start_timestamp(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startTimestamp"))

    @start_timestamp.setter
    def start_timestamp(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3400957b0156361f120e26ed9a28daef28d365639d25aed144e3bf50d828ba72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTimestamp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoDriver]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoDriver]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoDriver]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c2b182ae64f20614470d9d93679b96d1fc60f919b08b2b3bc3c030481fdf058)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoExecutors",
    jsii_struct_bases=[],
    name_mapping={
        "host_private_ip": "hostPrivateIp",
        "instance_id": "instanceId",
        "node_aws_attributes": "nodeAwsAttributes",
        "node_id": "nodeId",
        "private_ip": "privateIp",
        "public_dns": "publicDns",
        "start_timestamp": "startTimestamp",
    },
)
class DataDatabricksClusterPluginframeworkClusterInfoExecutors:
    def __init__(
        self,
        *,
        host_private_ip: typing.Optional[builtins.str] = None,
        instance_id: typing.Optional[builtins.str] = None,
        node_aws_attributes: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoExecutorsNodeAwsAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
        node_id: typing.Optional[builtins.str] = None,
        private_ip: typing.Optional[builtins.str] = None,
        public_dns: typing.Optional[builtins.str] = None,
        start_timestamp: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param host_private_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#host_private_ip DataDatabricksClusterPluginframework#host_private_ip}.
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#instance_id DataDatabricksClusterPluginframework#instance_id}.
        :param node_aws_attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#node_aws_attributes DataDatabricksClusterPluginframework#node_aws_attributes}.
        :param node_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#node_id DataDatabricksClusterPluginframework#node_id}.
        :param private_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#private_ip DataDatabricksClusterPluginframework#private_ip}.
        :param public_dns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#public_dns DataDatabricksClusterPluginframework#public_dns}.
        :param start_timestamp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#start_timestamp DataDatabricksClusterPluginframework#start_timestamp}.
        '''
        if isinstance(node_aws_attributes, dict):
            node_aws_attributes = DataDatabricksClusterPluginframeworkClusterInfoExecutorsNodeAwsAttributes(**node_aws_attributes)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__527830bf026ed34bc1a58b28d476acee9190e64d04fb46e330442043f1f8e18e)
            check_type(argname="argument host_private_ip", value=host_private_ip, expected_type=type_hints["host_private_ip"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument node_aws_attributes", value=node_aws_attributes, expected_type=type_hints["node_aws_attributes"])
            check_type(argname="argument node_id", value=node_id, expected_type=type_hints["node_id"])
            check_type(argname="argument private_ip", value=private_ip, expected_type=type_hints["private_ip"])
            check_type(argname="argument public_dns", value=public_dns, expected_type=type_hints["public_dns"])
            check_type(argname="argument start_timestamp", value=start_timestamp, expected_type=type_hints["start_timestamp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if host_private_ip is not None:
            self._values["host_private_ip"] = host_private_ip
        if instance_id is not None:
            self._values["instance_id"] = instance_id
        if node_aws_attributes is not None:
            self._values["node_aws_attributes"] = node_aws_attributes
        if node_id is not None:
            self._values["node_id"] = node_id
        if private_ip is not None:
            self._values["private_ip"] = private_ip
        if public_dns is not None:
            self._values["public_dns"] = public_dns
        if start_timestamp is not None:
            self._values["start_timestamp"] = start_timestamp

    @builtins.property
    def host_private_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#host_private_ip DataDatabricksClusterPluginframework#host_private_ip}.'''
        result = self._values.get("host_private_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#instance_id DataDatabricksClusterPluginframework#instance_id}.'''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_aws_attributes(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoExecutorsNodeAwsAttributes"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#node_aws_attributes DataDatabricksClusterPluginframework#node_aws_attributes}.'''
        result = self._values.get("node_aws_attributes")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoExecutorsNodeAwsAttributes"], result)

    @builtins.property
    def node_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#node_id DataDatabricksClusterPluginframework#node_id}.'''
        result = self._values.get("node_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#private_ip DataDatabricksClusterPluginframework#private_ip}.'''
        result = self._values.get("private_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_dns(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#public_dns DataDatabricksClusterPluginframework#public_dns}.'''
        result = self._values.get("public_dns")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_timestamp(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#start_timestamp DataDatabricksClusterPluginframework#start_timestamp}.'''
        result = self._values.get("start_timestamp")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoExecutors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoExecutorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoExecutorsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a70242f8a83aaaa9ff98a200bc4f72a63a73601f400d612668a7356cb1e1d257)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataDatabricksClusterPluginframeworkClusterInfoExecutorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9efe5234a0846553ba75fd9ad89ce73ffb15fe7a3179b281c2e13ef4181b7416)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataDatabricksClusterPluginframeworkClusterInfoExecutorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37d6c7d971b4ff09f7a93cde40ec04ab125415a498270c33571f1660adc812b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0b7ebc812a2f3b41330b1b8c2edddb5ef9a2226ef09b961b9ccfee4b6e9b91d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f47a31d54c847e6a5fc30098f133045c7902b3a9c5aee160136064ffb78a161)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksClusterPluginframeworkClusterInfoExecutors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksClusterPluginframeworkClusterInfoExecutors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksClusterPluginframeworkClusterInfoExecutors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a91a2d500dc583e77be07e054482e7dcc01e11c2ca0364f06e7bd9e248b8393)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoExecutorsNodeAwsAttributes",
    jsii_struct_bases=[],
    name_mapping={"is_spot": "isSpot"},
)
class DataDatabricksClusterPluginframeworkClusterInfoExecutorsNodeAwsAttributes:
    def __init__(
        self,
        *,
        is_spot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param is_spot: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#is_spot DataDatabricksClusterPluginframework#is_spot}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6599b2ad6fa5701bcc1d263460d9f484583068dfc7577eca94d2505cb05a963c)
            check_type(argname="argument is_spot", value=is_spot, expected_type=type_hints["is_spot"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if is_spot is not None:
            self._values["is_spot"] = is_spot

    @builtins.property
    def is_spot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#is_spot DataDatabricksClusterPluginframework#is_spot}.'''
        result = self._values.get("is_spot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoExecutorsNodeAwsAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoExecutorsNodeAwsAttributesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoExecutorsNodeAwsAttributesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca078e16956a155c8735d749ded6fab1d1b206142574f870d3e93618810d2a10)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsSpot")
    def reset_is_spot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsSpot", []))

    @builtins.property
    @jsii.member(jsii_name="isSpotInput")
    def is_spot_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isSpotInput"))

    @builtins.property
    @jsii.member(jsii_name="isSpot")
    def is_spot(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isSpot"))

    @is_spot.setter
    def is_spot(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__618585335e6fc3e3397fcb7a7f0cf28213cd3225820d9caa849e2fbb711e622d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSpot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoExecutorsNodeAwsAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoExecutorsNodeAwsAttributes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoExecutorsNodeAwsAttributes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6f4cbb932676d7439d719e62c53ca1ee101002e6962446d6a8cf7d6b1eb5959)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksClusterPluginframeworkClusterInfoExecutorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoExecutorsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be2509eeda1d6f056844116457d4b94d70834d99ffa5854a40c98d185a3d80b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putNodeAwsAttributes")
    def put_node_aws_attributes(
        self,
        *,
        is_spot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param is_spot: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#is_spot DataDatabricksClusterPluginframework#is_spot}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoExecutorsNodeAwsAttributes(
            is_spot=is_spot
        )

        return typing.cast(None, jsii.invoke(self, "putNodeAwsAttributes", [value]))

    @jsii.member(jsii_name="resetHostPrivateIp")
    def reset_host_private_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostPrivateIp", []))

    @jsii.member(jsii_name="resetInstanceId")
    def reset_instance_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceId", []))

    @jsii.member(jsii_name="resetNodeAwsAttributes")
    def reset_node_aws_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeAwsAttributes", []))

    @jsii.member(jsii_name="resetNodeId")
    def reset_node_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeId", []))

    @jsii.member(jsii_name="resetPrivateIp")
    def reset_private_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIp", []))

    @jsii.member(jsii_name="resetPublicDns")
    def reset_public_dns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicDns", []))

    @jsii.member(jsii_name="resetStartTimestamp")
    def reset_start_timestamp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTimestamp", []))

    @builtins.property
    @jsii.member(jsii_name="nodeAwsAttributes")
    def node_aws_attributes(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoExecutorsNodeAwsAttributesOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoExecutorsNodeAwsAttributesOutputReference, jsii.get(self, "nodeAwsAttributes"))

    @builtins.property
    @jsii.member(jsii_name="hostPrivateIpInput")
    def host_private_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostPrivateIpInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdInput")
    def instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeAwsAttributesInput")
    def node_aws_attributes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoExecutorsNodeAwsAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoExecutorsNodeAwsAttributes]], jsii.get(self, "nodeAwsAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeIdInput")
    def node_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpInput")
    def private_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpInput"))

    @builtins.property
    @jsii.member(jsii_name="publicDnsInput")
    def public_dns_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicDnsInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimestampInput")
    def start_timestamp_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startTimestampInput"))

    @builtins.property
    @jsii.member(jsii_name="hostPrivateIp")
    def host_private_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostPrivateIp"))

    @host_private_ip.setter
    def host_private_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d162a495528ee7c2b6dd52b5d6e466c52e856e13ac37ce3281c91c11bc7ea203)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostPrivateIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4f7e015edfd774ffaa788e9463a35645b34f5f29ea9afaeee5dcd94db0b274d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeId")
    def node_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeId"))

    @node_id.setter
    def node_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c91e5ebeeb5a7bdc297ce1c615504409b6eda6b83a7b103df4db42f7c2a1a122)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIp")
    def private_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIp"))

    @private_ip.setter
    def private_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__957b21c3b8245b6c2ffe06ba2f994e742d20f96543634c3a9c1b6084cbbe486f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicDns")
    def public_dns(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicDns"))

    @public_dns.setter
    def public_dns(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff45f15b0fcfa53aadac758eb91ddb25eb5acdddbd96003ad3c8b1cc4f7aaddc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicDns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTimestamp")
    def start_timestamp(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startTimestamp"))

    @start_timestamp.setter
    def start_timestamp(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ea7e0ba22b0ed78efcea6ddfc3d643bef41c502b041e24b66ccd7ea6ad8351f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTimestamp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoExecutors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoExecutors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoExecutors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7994183f60724fdd848b8695bd3c3e5711ee844b428b463daff53799703660db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoGcpAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "availability": "availability",
        "boot_disk_size": "bootDiskSize",
        "google_service_account": "googleServiceAccount",
        "local_ssd_count": "localSsdCount",
        "use_preemptible_executors": "usePreemptibleExecutors",
        "zone_id": "zoneId",
    },
)
class DataDatabricksClusterPluginframeworkClusterInfoGcpAttributes:
    def __init__(
        self,
        *,
        availability: typing.Optional[builtins.str] = None,
        boot_disk_size: typing.Optional[jsii.Number] = None,
        google_service_account: typing.Optional[builtins.str] = None,
        local_ssd_count: typing.Optional[jsii.Number] = None,
        use_preemptible_executors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        zone_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#availability DataDatabricksClusterPluginframework#availability}.
        :param boot_disk_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#boot_disk_size DataDatabricksClusterPluginframework#boot_disk_size}.
        :param google_service_account: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#google_service_account DataDatabricksClusterPluginframework#google_service_account}.
        :param local_ssd_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#local_ssd_count DataDatabricksClusterPluginframework#local_ssd_count}.
        :param use_preemptible_executors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#use_preemptible_executors DataDatabricksClusterPluginframework#use_preemptible_executors}.
        :param zone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#zone_id DataDatabricksClusterPluginframework#zone_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55e234c304877129e2e44796e3f391a8d7e1e166f10819be4bae34253b8134c5)
            check_type(argname="argument availability", value=availability, expected_type=type_hints["availability"])
            check_type(argname="argument boot_disk_size", value=boot_disk_size, expected_type=type_hints["boot_disk_size"])
            check_type(argname="argument google_service_account", value=google_service_account, expected_type=type_hints["google_service_account"])
            check_type(argname="argument local_ssd_count", value=local_ssd_count, expected_type=type_hints["local_ssd_count"])
            check_type(argname="argument use_preemptible_executors", value=use_preemptible_executors, expected_type=type_hints["use_preemptible_executors"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability is not None:
            self._values["availability"] = availability
        if boot_disk_size is not None:
            self._values["boot_disk_size"] = boot_disk_size
        if google_service_account is not None:
            self._values["google_service_account"] = google_service_account
        if local_ssd_count is not None:
            self._values["local_ssd_count"] = local_ssd_count
        if use_preemptible_executors is not None:
            self._values["use_preemptible_executors"] = use_preemptible_executors
        if zone_id is not None:
            self._values["zone_id"] = zone_id

    @builtins.property
    def availability(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#availability DataDatabricksClusterPluginframework#availability}.'''
        result = self._values.get("availability")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def boot_disk_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#boot_disk_size DataDatabricksClusterPluginframework#boot_disk_size}.'''
        result = self._values.get("boot_disk_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def google_service_account(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#google_service_account DataDatabricksClusterPluginframework#google_service_account}.'''
        result = self._values.get("google_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_ssd_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#local_ssd_count DataDatabricksClusterPluginframework#local_ssd_count}.'''
        result = self._values.get("local_ssd_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def use_preemptible_executors(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#use_preemptible_executors DataDatabricksClusterPluginframework#use_preemptible_executors}.'''
        result = self._values.get("use_preemptible_executors")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def zone_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#zone_id DataDatabricksClusterPluginframework#zone_id}.'''
        result = self._values.get("zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoGcpAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoGcpAttributesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoGcpAttributesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e2038a23a7a1b8f208680f8085906a233afb460f684098c8167b62ed7253c06)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAvailability")
    def reset_availability(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailability", []))

    @jsii.member(jsii_name="resetBootDiskSize")
    def reset_boot_disk_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskSize", []))

    @jsii.member(jsii_name="resetGoogleServiceAccount")
    def reset_google_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoogleServiceAccount", []))

    @jsii.member(jsii_name="resetLocalSsdCount")
    def reset_local_ssd_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalSsdCount", []))

    @jsii.member(jsii_name="resetUsePreemptibleExecutors")
    def reset_use_preemptible_executors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsePreemptibleExecutors", []))

    @jsii.member(jsii_name="resetZoneId")
    def reset_zone_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZoneId", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityInput")
    def availability_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeInput")
    def boot_disk_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootDiskSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="googleServiceAccountInput")
    def google_service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "googleServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="localSsdCountInput")
    def local_ssd_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "localSsdCountInput"))

    @builtins.property
    @jsii.member(jsii_name="usePreemptibleExecutorsInput")
    def use_preemptible_executors_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "usePreemptibleExecutorsInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneIdInput")
    def zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="availability")
    def availability(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availability"))

    @availability.setter
    def availability(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68e1631a07717f17c5a8b064f9cf1ba6277cbf74c85bdbb0a0d1c945865f27cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availability", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bootDiskSize")
    def boot_disk_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bootDiskSize"))

    @boot_disk_size.setter
    def boot_disk_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06b4900d5d495c7edc0be74159063b7343d41f30208be44f60fd17c2dd360085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="googleServiceAccount")
    def google_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "googleServiceAccount"))

    @google_service_account.setter
    def google_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c47f502c4d26ccef7f90ea0b7d27fc3cc38be8cc0823fdc5385ef304c0837832)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "googleServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localSsdCount")
    def local_ssd_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "localSsdCount"))

    @local_ssd_count.setter
    def local_ssd_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfa8433e6fef7b00ff052453373acdc77a3d916e44636386fe506b448eb37cd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localSsdCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="usePreemptibleExecutors")
    def use_preemptible_executors(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "usePreemptibleExecutors"))

    @use_preemptible_executors.setter
    def use_preemptible_executors(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34686f25ca3bf072d5640ed2062919a3edf81a636518f4183b8c86917818774d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usePreemptibleExecutors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18352a40af64067c1a17f467af7a6840b128d63e9bae360d26cdea8f8452c114)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoGcpAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoGcpAttributes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoGcpAttributes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a5d1ce6612e303973e56874427a7edccadea09d0b8029330f7854af989af3c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoInitScripts",
    jsii_struct_bases=[],
    name_mapping={
        "abfss": "abfss",
        "dbfs": "dbfs",
        "file": "file",
        "gcs": "gcs",
        "s3": "s3",
        "volumes": "volumes",
        "workspace": "workspace",
    },
)
class DataDatabricksClusterPluginframeworkClusterInfoInitScripts:
    def __init__(
        self,
        *,
        abfss: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoInitScriptsAbfss", typing.Dict[builtins.str, typing.Any]]] = None,
        dbfs: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoInitScriptsDbfs", typing.Dict[builtins.str, typing.Any]]] = None,
        file: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoInitScriptsFile", typing.Dict[builtins.str, typing.Any]]] = None,
        gcs: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoInitScriptsGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoInitScriptsS3", typing.Dict[builtins.str, typing.Any]]] = None,
        volumes: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoInitScriptsVolumes", typing.Dict[builtins.str, typing.Any]]] = None,
        workspace: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoInitScriptsWorkspace", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param abfss: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#abfss DataDatabricksClusterPluginframework#abfss}.
        :param dbfs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#dbfs DataDatabricksClusterPluginframework#dbfs}.
        :param file: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#file DataDatabricksClusterPluginframework#file}.
        :param gcs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#gcs DataDatabricksClusterPluginframework#gcs}.
        :param s3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#s3 DataDatabricksClusterPluginframework#s3}.
        :param volumes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#volumes DataDatabricksClusterPluginframework#volumes}.
        :param workspace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#workspace DataDatabricksClusterPluginframework#workspace}.
        '''
        if isinstance(abfss, dict):
            abfss = DataDatabricksClusterPluginframeworkClusterInfoInitScriptsAbfss(**abfss)
        if isinstance(dbfs, dict):
            dbfs = DataDatabricksClusterPluginframeworkClusterInfoInitScriptsDbfs(**dbfs)
        if isinstance(file, dict):
            file = DataDatabricksClusterPluginframeworkClusterInfoInitScriptsFile(**file)
        if isinstance(gcs, dict):
            gcs = DataDatabricksClusterPluginframeworkClusterInfoInitScriptsGcs(**gcs)
        if isinstance(s3, dict):
            s3 = DataDatabricksClusterPluginframeworkClusterInfoInitScriptsS3(**s3)
        if isinstance(volumes, dict):
            volumes = DataDatabricksClusterPluginframeworkClusterInfoInitScriptsVolumes(**volumes)
        if isinstance(workspace, dict):
            workspace = DataDatabricksClusterPluginframeworkClusterInfoInitScriptsWorkspace(**workspace)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdebcd61f45adbf2793b3fc06eb847644a66b2cc1b4820c03d0b11c99bf6b5a0)
            check_type(argname="argument abfss", value=abfss, expected_type=type_hints["abfss"])
            check_type(argname="argument dbfs", value=dbfs, expected_type=type_hints["dbfs"])
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument gcs", value=gcs, expected_type=type_hints["gcs"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
            check_type(argname="argument workspace", value=workspace, expected_type=type_hints["workspace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if abfss is not None:
            self._values["abfss"] = abfss
        if dbfs is not None:
            self._values["dbfs"] = dbfs
        if file is not None:
            self._values["file"] = file
        if gcs is not None:
            self._values["gcs"] = gcs
        if s3 is not None:
            self._values["s3"] = s3
        if volumes is not None:
            self._values["volumes"] = volumes
        if workspace is not None:
            self._values["workspace"] = workspace

    @builtins.property
    def abfss(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoInitScriptsAbfss"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#abfss DataDatabricksClusterPluginframework#abfss}.'''
        result = self._values.get("abfss")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoInitScriptsAbfss"], result)

    @builtins.property
    def dbfs(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoInitScriptsDbfs"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#dbfs DataDatabricksClusterPluginframework#dbfs}.'''
        result = self._values.get("dbfs")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoInitScriptsDbfs"], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoInitScriptsFile"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#file DataDatabricksClusterPluginframework#file}.'''
        result = self._values.get("file")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoInitScriptsFile"], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoInitScriptsGcs"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#gcs DataDatabricksClusterPluginframework#gcs}.'''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoInitScriptsGcs"], result)

    @builtins.property
    def s3(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoInitScriptsS3"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#s3 DataDatabricksClusterPluginframework#s3}.'''
        result = self._values.get("s3")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoInitScriptsS3"], result)

    @builtins.property
    def volumes(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoInitScriptsVolumes"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#volumes DataDatabricksClusterPluginframework#volumes}.'''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoInitScriptsVolumes"], result)

    @builtins.property
    def workspace(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoInitScriptsWorkspace"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#workspace DataDatabricksClusterPluginframework#workspace}.'''
        result = self._values.get("workspace")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoInitScriptsWorkspace"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoInitScripts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoInitScriptsAbfss",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination"},
)
class DataDatabricksClusterPluginframeworkClusterInfoInitScriptsAbfss:
    def __init__(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd5cf140713279fde4bc68194f26b0ea8de43a9616101eebddf3ccfb4beb55e9)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
        }

    @builtins.property
    def destination(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsAbfss(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoInitScriptsAbfssOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoInitScriptsAbfssOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ce2fb7319f9ef6e9adfe7747de5bc6896b18de02e1089b64dab30ca86272e04)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a62c80d402e379c52b569c478bca3b6b0f7bb38798aaaa2ad514e40bca093c07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsAbfss]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsAbfss]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsAbfss]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4de0b3faa37b872174a7b9a8018957972b1b47f9e8d1b1afaa9d7583987cfba7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoInitScriptsDbfs",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination"},
)
class DataDatabricksClusterPluginframeworkClusterInfoInitScriptsDbfs:
    def __init__(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2df5244fd02fa27eb67a79ec5aaa7a0f36153d1f521d05b268dc0bb57689f61d)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
        }

    @builtins.property
    def destination(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsDbfs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoInitScriptsDbfsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoInitScriptsDbfsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5890865c8d22dd7f9b9b0faf2ccbe4efe6a824fa087797fa981cab0a75d127b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0570727dd09562ccb38ebf652eace60576226dd83f71ce2bc4d2185b0381c02b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsDbfs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsDbfs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsDbfs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1054870082d88e8f93af9819e52918e06bd4f14f9c1e7464e5401b1f0f0d6f4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoInitScriptsFile",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination"},
)
class DataDatabricksClusterPluginframeworkClusterInfoInitScriptsFile:
    def __init__(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab8fdc6bfc9116cd6638882688b3046bf92328073c5b28ee1017d7336c6f27e6)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
        }

    @builtins.property
    def destination(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoInitScriptsFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoInitScriptsFileOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2564ec85c7b18ed5cd098baa60849d81ae0d9ed1243dd532e944717f7c611aaa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__671e21decced6cf92d4fb216e6528eb8e7f42773b92e9d29b807facbc766df1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsFile]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsFile]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsFile]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__796fd6fac516654e3bc7ac86e2be0119684150a68faa45cf8db530c0f9c29be9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoInitScriptsGcs",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination"},
)
class DataDatabricksClusterPluginframeworkClusterInfoInitScriptsGcs:
    def __init__(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__737a0aba020e61008cf1e15fd913b513817b6fe0831a6e118fbfb94b81f7ff2b)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
        }

    @builtins.property
    def destination(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoInitScriptsGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoInitScriptsGcsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cfaf90092a5dd754100a36b010ce85094b9be983bb6fdb5e68751d36df84ee7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b4fc6a4faed5cd84c7ed59ebfb87d93a99a3378be17d869bef1995be75445fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsGcs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsGcs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsGcs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d148b4783f0b6e99357c0ec596c0d89a40054e9a947bbb4f3e89f481b1e1e52a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksClusterPluginframeworkClusterInfoInitScriptsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoInitScriptsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15efa0fbd5e3c101af6003ea70667d1702cc3ddf7d9597cd161849dd588e062f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93af346a236377577fe1ea7b9a8b4d0a47d874e14cfc7ba8cf4e711dab465078)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataDatabricksClusterPluginframeworkClusterInfoInitScriptsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bffc4802a8bc3e070f72ac78a6465c98350ac87835c124dc7bfe79ee8389396b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a08a918accf5cb0f644f8db4d8827e66cd2904b8243d95c8429c3c62be2ea5a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07896b2f6f77d53c7796d813a4c47767135ee42ee510d7e27610a6d709a28f8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksClusterPluginframeworkClusterInfoInitScripts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksClusterPluginframeworkClusterInfoInitScripts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksClusterPluginframeworkClusterInfoInitScripts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54d16d7335750f005a8cd85b44a353f73f6752bf37931b3cfa49a0031f02f924)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksClusterPluginframeworkClusterInfoInitScriptsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoInitScriptsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eee1594b96f24a52d67e8af14a2779e123cb08ff734b137b2b071f4a3f12cbe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAbfss")
    def put_abfss(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoInitScriptsAbfss(
            destination=destination
        )

        return typing.cast(None, jsii.invoke(self, "putAbfss", [value]))

    @jsii.member(jsii_name="putDbfs")
    def put_dbfs(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoInitScriptsDbfs(
            destination=destination
        )

        return typing.cast(None, jsii.invoke(self, "putDbfs", [value]))

    @jsii.member(jsii_name="putFile")
    def put_file(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoInitScriptsFile(
            destination=destination
        )

        return typing.cast(None, jsii.invoke(self, "putFile", [value]))

    @jsii.member(jsii_name="putGcs")
    def put_gcs(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoInitScriptsGcs(
            destination=destination
        )

        return typing.cast(None, jsii.invoke(self, "putGcs", [value]))

    @jsii.member(jsii_name="putS3")
    def put_s3(
        self,
        *,
        destination: builtins.str,
        canned_acl: typing.Optional[builtins.str] = None,
        enable_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_type: typing.Optional[builtins.str] = None,
        endpoint: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        :param canned_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#canned_acl DataDatabricksClusterPluginframework#canned_acl}.
        :param enable_encryption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#enable_encryption DataDatabricksClusterPluginframework#enable_encryption}.
        :param encryption_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#encryption_type DataDatabricksClusterPluginframework#encryption_type}.
        :param endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#endpoint DataDatabricksClusterPluginframework#endpoint}.
        :param kms_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#kms_key DataDatabricksClusterPluginframework#kms_key}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#region DataDatabricksClusterPluginframework#region}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoInitScriptsS3(
            destination=destination,
            canned_acl=canned_acl,
            enable_encryption=enable_encryption,
            encryption_type=encryption_type,
            endpoint=endpoint,
            kms_key=kms_key,
            region=region,
        )

        return typing.cast(None, jsii.invoke(self, "putS3", [value]))

    @jsii.member(jsii_name="putVolumes")
    def put_volumes(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoInitScriptsVolumes(
            destination=destination
        )

        return typing.cast(None, jsii.invoke(self, "putVolumes", [value]))

    @jsii.member(jsii_name="putWorkspace")
    def put_workspace(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoInitScriptsWorkspace(
            destination=destination
        )

        return typing.cast(None, jsii.invoke(self, "putWorkspace", [value]))

    @jsii.member(jsii_name="resetAbfss")
    def reset_abfss(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAbfss", []))

    @jsii.member(jsii_name="resetDbfs")
    def reset_dbfs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDbfs", []))

    @jsii.member(jsii_name="resetFile")
    def reset_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFile", []))

    @jsii.member(jsii_name="resetGcs")
    def reset_gcs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcs", []))

    @jsii.member(jsii_name="resetS3")
    def reset_s3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3", []))

    @jsii.member(jsii_name="resetVolumes")
    def reset_volumes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumes", []))

    @jsii.member(jsii_name="resetWorkspace")
    def reset_workspace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkspace", []))

    @builtins.property
    @jsii.member(jsii_name="abfss")
    def abfss(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoInitScriptsAbfssOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoInitScriptsAbfssOutputReference, jsii.get(self, "abfss"))

    @builtins.property
    @jsii.member(jsii_name="dbfs")
    def dbfs(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoInitScriptsDbfsOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoInitScriptsDbfsOutputReference, jsii.get(self, "dbfs"))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoInitScriptsFileOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoInitScriptsFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="gcs")
    def gcs(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoInitScriptsGcsOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoInitScriptsGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="s3")
    def s3(
        self,
    ) -> "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsS3OutputReference":
        return typing.cast("DataDatabricksClusterPluginframeworkClusterInfoInitScriptsS3OutputReference", jsii.get(self, "s3"))

    @builtins.property
    @jsii.member(jsii_name="volumes")
    def volumes(
        self,
    ) -> "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsVolumesOutputReference":
        return typing.cast("DataDatabricksClusterPluginframeworkClusterInfoInitScriptsVolumesOutputReference", jsii.get(self, "volumes"))

    @builtins.property
    @jsii.member(jsii_name="workspace")
    def workspace(
        self,
    ) -> "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsWorkspaceOutputReference":
        return typing.cast("DataDatabricksClusterPluginframeworkClusterInfoInitScriptsWorkspaceOutputReference", jsii.get(self, "workspace"))

    @builtins.property
    @jsii.member(jsii_name="abfssInput")
    def abfss_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsAbfss]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsAbfss]], jsii.get(self, "abfssInput"))

    @builtins.property
    @jsii.member(jsii_name="dbfsInput")
    def dbfs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsDbfs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsDbfs]], jsii.get(self, "dbfsInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsFile]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsFile]], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsInput")
    def gcs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsGcs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsGcs]], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Input")
    def s3_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsS3"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsS3"]], jsii.get(self, "s3Input"))

    @builtins.property
    @jsii.member(jsii_name="volumesInput")
    def volumes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsVolumes"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsVolumes"]], jsii.get(self, "volumesInput"))

    @builtins.property
    @jsii.member(jsii_name="workspaceInput")
    def workspace_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsWorkspace"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsWorkspace"]], jsii.get(self, "workspaceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScripts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScripts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScripts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6ada2af8560ace81d6e1375f0babbaaadb05e816be21d80623f9f690ab6590f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoInitScriptsS3",
    jsii_struct_bases=[],
    name_mapping={
        "destination": "destination",
        "canned_acl": "cannedAcl",
        "enable_encryption": "enableEncryption",
        "encryption_type": "encryptionType",
        "endpoint": "endpoint",
        "kms_key": "kmsKey",
        "region": "region",
    },
)
class DataDatabricksClusterPluginframeworkClusterInfoInitScriptsS3:
    def __init__(
        self,
        *,
        destination: builtins.str,
        canned_acl: typing.Optional[builtins.str] = None,
        enable_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_type: typing.Optional[builtins.str] = None,
        endpoint: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        :param canned_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#canned_acl DataDatabricksClusterPluginframework#canned_acl}.
        :param enable_encryption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#enable_encryption DataDatabricksClusterPluginframework#enable_encryption}.
        :param encryption_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#encryption_type DataDatabricksClusterPluginframework#encryption_type}.
        :param endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#endpoint DataDatabricksClusterPluginframework#endpoint}.
        :param kms_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#kms_key DataDatabricksClusterPluginframework#kms_key}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#region DataDatabricksClusterPluginframework#region}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f277518e0bc6240e9b14ac1119e0595ee9308cd11be6eb21bd518dbcc081ed6)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument canned_acl", value=canned_acl, expected_type=type_hints["canned_acl"])
            check_type(argname="argument enable_encryption", value=enable_encryption, expected_type=type_hints["enable_encryption"])
            check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
        }
        if canned_acl is not None:
            self._values["canned_acl"] = canned_acl
        if enable_encryption is not None:
            self._values["enable_encryption"] = enable_encryption
        if encryption_type is not None:
            self._values["encryption_type"] = encryption_type
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def destination(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def canned_acl(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#canned_acl DataDatabricksClusterPluginframework#canned_acl}.'''
        result = self._values.get("canned_acl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_encryption(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#enable_encryption DataDatabricksClusterPluginframework#enable_encryption}.'''
        result = self._values.get("enable_encryption")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#encryption_type DataDatabricksClusterPluginframework#encryption_type}.'''
        result = self._values.get("encryption_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#endpoint DataDatabricksClusterPluginframework#endpoint}.'''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#kms_key DataDatabricksClusterPluginframework#kms_key}.'''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#region DataDatabricksClusterPluginframework#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsS3(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoInitScriptsS3OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoInitScriptsS3OutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f301b41e8f5cf3028428113faf05ebe12e85cb38f0cc0d30bdf63f02fbcae69)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCannedAcl")
    def reset_canned_acl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCannedAcl", []))

    @jsii.member(jsii_name="resetEnableEncryption")
    def reset_enable_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableEncryption", []))

    @jsii.member(jsii_name="resetEncryptionType")
    def reset_encryption_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionType", []))

    @jsii.member(jsii_name="resetEndpoint")
    def reset_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpoint", []))

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @builtins.property
    @jsii.member(jsii_name="cannedAclInput")
    def canned_acl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cannedAclInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="enableEncryptionInput")
    def enable_encryption_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionTypeInput")
    def encryption_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointInput")
    def endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="cannedAcl")
    def canned_acl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cannedAcl"))

    @canned_acl.setter
    def canned_acl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__413ad66f45a91c3dffcf3243364bb3ba100d1c670efe06bcf303bc7a3d73beaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cannedAcl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ba7e9d686913cae2d2d7bd0f694d7ffa5c9925628e64753c49a9a772abdbffb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableEncryption")
    def enable_encryption(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableEncryption"))

    @enable_encryption.setter
    def enable_encryption(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a9ae850d8e2d4ecf9f32d60528dda71ddc8949ead99733a2dee477b8c5141b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableEncryption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionType")
    def encryption_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionType"))

    @encryption_type.setter
    def encryption_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0394331140382874e473f275b8445fc47aee275dfa67dad093eda01266bb9ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @endpoint.setter
    def endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58f219c68752d1665c17237b551d14addaa51ab1bb2f638f7f9f793cedc33ab8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5205bb1c6c365b19e57bf28df45ebb1ada8a736c4d88fccf750d0b719e0c0140)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e48ab1f12275ed858ef90bed7aea2c6466b96bfcc52002a977c3039e0cdacce6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsS3]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsS3]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsS3]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68afdea31ca27cc03f0c0f1d4ef971db11bdc580a954b22e251cf86b5caab46e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoInitScriptsVolumes",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination"},
)
class DataDatabricksClusterPluginframeworkClusterInfoInitScriptsVolumes:
    def __init__(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ba1bd655324811f9686b5812f1885ba184ae3f5826076eb21059d01bacf2b1d)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
        }

    @builtins.property
    def destination(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoInitScriptsVolumesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoInitScriptsVolumesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e1fc1ab8829ddfa45d85e6ed5898fd5c2f9ad062f979fd5104af8cf788e98fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82f7dbf039d9805beee10e2f04619773bfcd49f11d8564d6847b7a8643295ade)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsVolumes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsVolumes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsVolumes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f825d95205d5149442f0ac045fce6a99eb593f8b8ad3f07d227b7c790494bf8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoInitScriptsWorkspace",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination"},
)
class DataDatabricksClusterPluginframeworkClusterInfoInitScriptsWorkspace:
    def __init__(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d64af70f1b395584c409d0b282e3589b791d488d6d1ffd77735b2cdddd178b88)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
        }

    @builtins.property
    def destination(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsWorkspace(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoInitScriptsWorkspaceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoInitScriptsWorkspaceOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8a39020c23721d0aac2a1e399507dc10e8a7e9d88fad23f2cc1cfadd8a4c636)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64e2933af3bc8d0d4aaa570eeea248421abed0e983a37bc75e22d3014aa3c6f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsWorkspace]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsWorkspace]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsWorkspace]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c9b60834509e8b28a873dccbe89fce3c9f0cd963cb9d63eccb5d9a656704b2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksClusterPluginframeworkClusterInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c04e1c7ad9ad820d25b577c85ddeb0f1bf52116d206a078d91947f62f1def3c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscale")
    def put_autoscale(
        self,
        *,
        max_workers: typing.Optional[jsii.Number] = None,
        min_workers: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#max_workers DataDatabricksClusterPluginframework#max_workers}.
        :param min_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#min_workers DataDatabricksClusterPluginframework#min_workers}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoAutoscale(
            max_workers=max_workers, min_workers=min_workers
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscale", [value]))

    @jsii.member(jsii_name="putAwsAttributes")
    def put_aws_attributes(
        self,
        *,
        availability: typing.Optional[builtins.str] = None,
        ebs_volume_count: typing.Optional[jsii.Number] = None,
        ebs_volume_iops: typing.Optional[jsii.Number] = None,
        ebs_volume_size: typing.Optional[jsii.Number] = None,
        ebs_volume_throughput: typing.Optional[jsii.Number] = None,
        ebs_volume_type: typing.Optional[builtins.str] = None,
        first_on_demand: typing.Optional[jsii.Number] = None,
        instance_profile_arn: typing.Optional[builtins.str] = None,
        spot_bid_price_percent: typing.Optional[jsii.Number] = None,
        zone_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#availability DataDatabricksClusterPluginframework#availability}.
        :param ebs_volume_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_count DataDatabricksClusterPluginframework#ebs_volume_count}.
        :param ebs_volume_iops: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_iops DataDatabricksClusterPluginframework#ebs_volume_iops}.
        :param ebs_volume_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_size DataDatabricksClusterPluginframework#ebs_volume_size}.
        :param ebs_volume_throughput: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_throughput DataDatabricksClusterPluginframework#ebs_volume_throughput}.
        :param ebs_volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_type DataDatabricksClusterPluginframework#ebs_volume_type}.
        :param first_on_demand: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#first_on_demand DataDatabricksClusterPluginframework#first_on_demand}.
        :param instance_profile_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#instance_profile_arn DataDatabricksClusterPluginframework#instance_profile_arn}.
        :param spot_bid_price_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spot_bid_price_percent DataDatabricksClusterPluginframework#spot_bid_price_percent}.
        :param zone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#zone_id DataDatabricksClusterPluginframework#zone_id}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoAwsAttributes(
            availability=availability,
            ebs_volume_count=ebs_volume_count,
            ebs_volume_iops=ebs_volume_iops,
            ebs_volume_size=ebs_volume_size,
            ebs_volume_throughput=ebs_volume_throughput,
            ebs_volume_type=ebs_volume_type,
            first_on_demand=first_on_demand,
            instance_profile_arn=instance_profile_arn,
            spot_bid_price_percent=spot_bid_price_percent,
            zone_id=zone_id,
        )

        return typing.cast(None, jsii.invoke(self, "putAwsAttributes", [value]))

    @jsii.member(jsii_name="putAzureAttributes")
    def put_azure_attributes(
        self,
        *,
        availability: typing.Optional[builtins.str] = None,
        first_on_demand: typing.Optional[jsii.Number] = None,
        log_analytics_info: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesLogAnalyticsInfo, typing.Dict[builtins.str, typing.Any]]] = None,
        spot_bid_max_price: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param availability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#availability DataDatabricksClusterPluginframework#availability}.
        :param first_on_demand: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#first_on_demand DataDatabricksClusterPluginframework#first_on_demand}.
        :param log_analytics_info: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#log_analytics_info DataDatabricksClusterPluginframework#log_analytics_info}.
        :param spot_bid_max_price: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spot_bid_max_price DataDatabricksClusterPluginframework#spot_bid_max_price}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoAzureAttributes(
            availability=availability,
            first_on_demand=first_on_demand,
            log_analytics_info=log_analytics_info,
            spot_bid_max_price=spot_bid_max_price,
        )

        return typing.cast(None, jsii.invoke(self, "putAzureAttributes", [value]))

    @jsii.member(jsii_name="putClusterLogConf")
    def put_cluster_log_conf(
        self,
        *,
        dbfs: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfDbfs, typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfS3, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dbfs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#dbfs DataDatabricksClusterPluginframework#dbfs}.
        :param s3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#s3 DataDatabricksClusterPluginframework#s3}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoClusterLogConf(
            dbfs=dbfs, s3=s3
        )

        return typing.cast(None, jsii.invoke(self, "putClusterLogConf", [value]))

    @jsii.member(jsii_name="putClusterLogStatus")
    def put_cluster_log_status(
        self,
        *,
        last_attempted: typing.Optional[jsii.Number] = None,
        last_exception: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param last_attempted: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#last_attempted DataDatabricksClusterPluginframework#last_attempted}.
        :param last_exception: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#last_exception DataDatabricksClusterPluginframework#last_exception}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoClusterLogStatus(
            last_attempted=last_attempted, last_exception=last_exception
        )

        return typing.cast(None, jsii.invoke(self, "putClusterLogStatus", [value]))

    @jsii.member(jsii_name="putDockerImage")
    def put_docker_image(
        self,
        *,
        basic_auth: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoDockerImageBasicAuth, typing.Dict[builtins.str, typing.Any]]] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param basic_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#basic_auth DataDatabricksClusterPluginframework#basic_auth}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#url DataDatabricksClusterPluginframework#url}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoDockerImage(
            basic_auth=basic_auth, url=url
        )

        return typing.cast(None, jsii.invoke(self, "putDockerImage", [value]))

    @jsii.member(jsii_name="putDriver")
    def put_driver(
        self,
        *,
        host_private_ip: typing.Optional[builtins.str] = None,
        instance_id: typing.Optional[builtins.str] = None,
        node_aws_attributes: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoDriverNodeAwsAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
        node_id: typing.Optional[builtins.str] = None,
        private_ip: typing.Optional[builtins.str] = None,
        public_dns: typing.Optional[builtins.str] = None,
        start_timestamp: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param host_private_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#host_private_ip DataDatabricksClusterPluginframework#host_private_ip}.
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#instance_id DataDatabricksClusterPluginframework#instance_id}.
        :param node_aws_attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#node_aws_attributes DataDatabricksClusterPluginframework#node_aws_attributes}.
        :param node_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#node_id DataDatabricksClusterPluginframework#node_id}.
        :param private_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#private_ip DataDatabricksClusterPluginframework#private_ip}.
        :param public_dns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#public_dns DataDatabricksClusterPluginframework#public_dns}.
        :param start_timestamp: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#start_timestamp DataDatabricksClusterPluginframework#start_timestamp}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoDriver(
            host_private_ip=host_private_ip,
            instance_id=instance_id,
            node_aws_attributes=node_aws_attributes,
            node_id=node_id,
            private_ip=private_ip,
            public_dns=public_dns,
            start_timestamp=start_timestamp,
        )

        return typing.cast(None, jsii.invoke(self, "putDriver", [value]))

    @jsii.member(jsii_name="putExecutors")
    def put_executors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoExecutors, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ccabe9b9cf5c52869126b2984e8fae528eb60ec8a0782cc92fccf0aa6e5ebf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExecutors", [value]))

    @jsii.member(jsii_name="putGcpAttributes")
    def put_gcp_attributes(
        self,
        *,
        availability: typing.Optional[builtins.str] = None,
        boot_disk_size: typing.Optional[jsii.Number] = None,
        google_service_account: typing.Optional[builtins.str] = None,
        local_ssd_count: typing.Optional[jsii.Number] = None,
        use_preemptible_executors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        zone_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#availability DataDatabricksClusterPluginframework#availability}.
        :param boot_disk_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#boot_disk_size DataDatabricksClusterPluginframework#boot_disk_size}.
        :param google_service_account: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#google_service_account DataDatabricksClusterPluginframework#google_service_account}.
        :param local_ssd_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#local_ssd_count DataDatabricksClusterPluginframework#local_ssd_count}.
        :param use_preemptible_executors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#use_preemptible_executors DataDatabricksClusterPluginframework#use_preemptible_executors}.
        :param zone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#zone_id DataDatabricksClusterPluginframework#zone_id}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoGcpAttributes(
            availability=availability,
            boot_disk_size=boot_disk_size,
            google_service_account=google_service_account,
            local_ssd_count=local_ssd_count,
            use_preemptible_executors=use_preemptible_executors,
            zone_id=zone_id,
        )

        return typing.cast(None, jsii.invoke(self, "putGcpAttributes", [value]))

    @jsii.member(jsii_name="putInitScripts")
    def put_init_scripts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoInitScripts, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05cbc00fead3aab4bc78f0e8cc74469e450ff985c8cadba3db384808fae17781)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInitScripts", [value]))

    @jsii.member(jsii_name="putSpec")
    def put_spec(
        self,
        *,
        apply_policy_default_values: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        autoscale: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecAutoscale", typing.Dict[builtins.str, typing.Any]]] = None,
        autotermination_minutes: typing.Optional[jsii.Number] = None,
        aws_attributes: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecAwsAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
        azure_attributes: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_log_conf: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConf", typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        custom_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        data_security_mode: typing.Optional[builtins.str] = None,
        docker_image: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImage", typing.Dict[builtins.str, typing.Any]]] = None,
        driver_instance_pool_id: typing.Optional[builtins.str] = None,
        driver_node_type_id: typing.Optional[builtins.str] = None,
        enable_elastic_disk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_local_disk_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcp_attributes: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecGcpAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
        init_scripts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScripts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        instance_pool_id: typing.Optional[builtins.str] = None,
        node_type_id: typing.Optional[builtins.str] = None,
        num_workers: typing.Optional[jsii.Number] = None,
        policy_id: typing.Optional[builtins.str] = None,
        runtime_engine: typing.Optional[builtins.str] = None,
        single_user_name: typing.Optional[builtins.str] = None,
        spark_conf: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        spark_env_vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        spark_version: typing.Optional[builtins.str] = None,
        ssh_public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        workload_type: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadType", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param apply_policy_default_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#apply_policy_default_values DataDatabricksClusterPluginframework#apply_policy_default_values}.
        :param autoscale: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#autoscale DataDatabricksClusterPluginframework#autoscale}.
        :param autotermination_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#autotermination_minutes DataDatabricksClusterPluginframework#autotermination_minutes}.
        :param aws_attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#aws_attributes DataDatabricksClusterPluginframework#aws_attributes}.
        :param azure_attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#azure_attributes DataDatabricksClusterPluginframework#azure_attributes}.
        :param cluster_log_conf: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_log_conf DataDatabricksClusterPluginframework#cluster_log_conf}.
        :param cluster_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_name DataDatabricksClusterPluginframework#cluster_name}.
        :param custom_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#custom_tags DataDatabricksClusterPluginframework#custom_tags}.
        :param data_security_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#data_security_mode DataDatabricksClusterPluginframework#data_security_mode}.
        :param docker_image: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#docker_image DataDatabricksClusterPluginframework#docker_image}.
        :param driver_instance_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#driver_instance_pool_id DataDatabricksClusterPluginframework#driver_instance_pool_id}.
        :param driver_node_type_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#driver_node_type_id DataDatabricksClusterPluginframework#driver_node_type_id}.
        :param enable_elastic_disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#enable_elastic_disk DataDatabricksClusterPluginframework#enable_elastic_disk}.
        :param enable_local_disk_encryption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#enable_local_disk_encryption DataDatabricksClusterPluginframework#enable_local_disk_encryption}.
        :param gcp_attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#gcp_attributes DataDatabricksClusterPluginframework#gcp_attributes}.
        :param init_scripts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#init_scripts DataDatabricksClusterPluginframework#init_scripts}.
        :param instance_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#instance_pool_id DataDatabricksClusterPluginframework#instance_pool_id}.
        :param node_type_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#node_type_id DataDatabricksClusterPluginframework#node_type_id}.
        :param num_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#num_workers DataDatabricksClusterPluginframework#num_workers}.
        :param policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#policy_id DataDatabricksClusterPluginframework#policy_id}.
        :param runtime_engine: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#runtime_engine DataDatabricksClusterPluginframework#runtime_engine}.
        :param single_user_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#single_user_name DataDatabricksClusterPluginframework#single_user_name}.
        :param spark_conf: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spark_conf DataDatabricksClusterPluginframework#spark_conf}.
        :param spark_env_vars: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spark_env_vars DataDatabricksClusterPluginframework#spark_env_vars}.
        :param spark_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spark_version DataDatabricksClusterPluginframework#spark_version}.
        :param ssh_public_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ssh_public_keys DataDatabricksClusterPluginframework#ssh_public_keys}.
        :param workload_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#workload_type DataDatabricksClusterPluginframework#workload_type}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoSpec(
            apply_policy_default_values=apply_policy_default_values,
            autoscale=autoscale,
            autotermination_minutes=autotermination_minutes,
            aws_attributes=aws_attributes,
            azure_attributes=azure_attributes,
            cluster_log_conf=cluster_log_conf,
            cluster_name=cluster_name,
            custom_tags=custom_tags,
            data_security_mode=data_security_mode,
            docker_image=docker_image,
            driver_instance_pool_id=driver_instance_pool_id,
            driver_node_type_id=driver_node_type_id,
            enable_elastic_disk=enable_elastic_disk,
            enable_local_disk_encryption=enable_local_disk_encryption,
            gcp_attributes=gcp_attributes,
            init_scripts=init_scripts,
            instance_pool_id=instance_pool_id,
            node_type_id=node_type_id,
            num_workers=num_workers,
            policy_id=policy_id,
            runtime_engine=runtime_engine,
            single_user_name=single_user_name,
            spark_conf=spark_conf,
            spark_env_vars=spark_env_vars,
            spark_version=spark_version,
            ssh_public_keys=ssh_public_keys,
            workload_type=workload_type,
        )

        return typing.cast(None, jsii.invoke(self, "putSpec", [value]))

    @jsii.member(jsii_name="putTerminationReason")
    def put_termination_reason(
        self,
        *,
        code: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#code DataDatabricksClusterPluginframework#code}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#parameters DataDatabricksClusterPluginframework#parameters}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#type DataDatabricksClusterPluginframework#type}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoTerminationReason(
            code=code, parameters=parameters, type=type
        )

        return typing.cast(None, jsii.invoke(self, "putTerminationReason", [value]))

    @jsii.member(jsii_name="putWorkloadType")
    def put_workload_type(
        self,
        *,
        clients: typing.Union["DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeClients", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param clients: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#clients DataDatabricksClusterPluginframework#clients}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoWorkloadType(
            clients=clients
        )

        return typing.cast(None, jsii.invoke(self, "putWorkloadType", [value]))

    @jsii.member(jsii_name="resetAutoscale")
    def reset_autoscale(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscale", []))

    @jsii.member(jsii_name="resetAutoterminationMinutes")
    def reset_autotermination_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoterminationMinutes", []))

    @jsii.member(jsii_name="resetAwsAttributes")
    def reset_aws_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAttributes", []))

    @jsii.member(jsii_name="resetAzureAttributes")
    def reset_azure_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureAttributes", []))

    @jsii.member(jsii_name="resetClusterCores")
    def reset_cluster_cores(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterCores", []))

    @jsii.member(jsii_name="resetClusterId")
    def reset_cluster_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterId", []))

    @jsii.member(jsii_name="resetClusterLogConf")
    def reset_cluster_log_conf(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterLogConf", []))

    @jsii.member(jsii_name="resetClusterLogStatus")
    def reset_cluster_log_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterLogStatus", []))

    @jsii.member(jsii_name="resetClusterMemoryMb")
    def reset_cluster_memory_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterMemoryMb", []))

    @jsii.member(jsii_name="resetClusterName")
    def reset_cluster_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterName", []))

    @jsii.member(jsii_name="resetClusterSource")
    def reset_cluster_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterSource", []))

    @jsii.member(jsii_name="resetCreatorUserName")
    def reset_creator_user_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreatorUserName", []))

    @jsii.member(jsii_name="resetCustomTags")
    def reset_custom_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomTags", []))

    @jsii.member(jsii_name="resetDataSecurityMode")
    def reset_data_security_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataSecurityMode", []))

    @jsii.member(jsii_name="resetDefaultTags")
    def reset_default_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTags", []))

    @jsii.member(jsii_name="resetDockerImage")
    def reset_docker_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerImage", []))

    @jsii.member(jsii_name="resetDriver")
    def reset_driver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDriver", []))

    @jsii.member(jsii_name="resetDriverInstancePoolId")
    def reset_driver_instance_pool_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDriverInstancePoolId", []))

    @jsii.member(jsii_name="resetDriverNodeTypeId")
    def reset_driver_node_type_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDriverNodeTypeId", []))

    @jsii.member(jsii_name="resetEnableElasticDisk")
    def reset_enable_elastic_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableElasticDisk", []))

    @jsii.member(jsii_name="resetEnableLocalDiskEncryption")
    def reset_enable_local_disk_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableLocalDiskEncryption", []))

    @jsii.member(jsii_name="resetExecutors")
    def reset_executors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutors", []))

    @jsii.member(jsii_name="resetGcpAttributes")
    def reset_gcp_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcpAttributes", []))

    @jsii.member(jsii_name="resetInitScripts")
    def reset_init_scripts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitScripts", []))

    @jsii.member(jsii_name="resetInstancePoolId")
    def reset_instance_pool_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstancePoolId", []))

    @jsii.member(jsii_name="resetJdbcPort")
    def reset_jdbc_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJdbcPort", []))

    @jsii.member(jsii_name="resetLastRestartedTime")
    def reset_last_restarted_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastRestartedTime", []))

    @jsii.member(jsii_name="resetLastStateLossTime")
    def reset_last_state_loss_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastStateLossTime", []))

    @jsii.member(jsii_name="resetNodeTypeId")
    def reset_node_type_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeTypeId", []))

    @jsii.member(jsii_name="resetNumWorkers")
    def reset_num_workers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumWorkers", []))

    @jsii.member(jsii_name="resetPolicyId")
    def reset_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyId", []))

    @jsii.member(jsii_name="resetRuntimeEngine")
    def reset_runtime_engine(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeEngine", []))

    @jsii.member(jsii_name="resetSingleUserName")
    def reset_single_user_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSingleUserName", []))

    @jsii.member(jsii_name="resetSparkConf")
    def reset_spark_conf(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkConf", []))

    @jsii.member(jsii_name="resetSparkContextId")
    def reset_spark_context_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkContextId", []))

    @jsii.member(jsii_name="resetSparkEnvVars")
    def reset_spark_env_vars(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkEnvVars", []))

    @jsii.member(jsii_name="resetSparkVersion")
    def reset_spark_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkVersion", []))

    @jsii.member(jsii_name="resetSpec")
    def reset_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpec", []))

    @jsii.member(jsii_name="resetSshPublicKeys")
    def reset_ssh_public_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshPublicKeys", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @jsii.member(jsii_name="resetStateMessage")
    def reset_state_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStateMessage", []))

    @jsii.member(jsii_name="resetTerminatedTime")
    def reset_terminated_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerminatedTime", []))

    @jsii.member(jsii_name="resetTerminationReason")
    def reset_termination_reason(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerminationReason", []))

    @jsii.member(jsii_name="resetWorkloadType")
    def reset_workload_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkloadType", []))

    @builtins.property
    @jsii.member(jsii_name="autoscale")
    def autoscale(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoAutoscaleOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoAutoscaleOutputReference, jsii.get(self, "autoscale"))

    @builtins.property
    @jsii.member(jsii_name="awsAttributes")
    def aws_attributes(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoAwsAttributesOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoAwsAttributesOutputReference, jsii.get(self, "awsAttributes"))

    @builtins.property
    @jsii.member(jsii_name="azureAttributes")
    def azure_attributes(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesOutputReference, jsii.get(self, "azureAttributes"))

    @builtins.property
    @jsii.member(jsii_name="clusterLogConf")
    def cluster_log_conf(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfOutputReference, jsii.get(self, "clusterLogConf"))

    @builtins.property
    @jsii.member(jsii_name="clusterLogStatus")
    def cluster_log_status(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoClusterLogStatusOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoClusterLogStatusOutputReference, jsii.get(self, "clusterLogStatus"))

    @builtins.property
    @jsii.member(jsii_name="dockerImage")
    def docker_image(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoDockerImageOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoDockerImageOutputReference, jsii.get(self, "dockerImage"))

    @builtins.property
    @jsii.member(jsii_name="driver")
    def driver(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoDriverOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoDriverOutputReference, jsii.get(self, "driver"))

    @builtins.property
    @jsii.member(jsii_name="executors")
    def executors(self) -> DataDatabricksClusterPluginframeworkClusterInfoExecutorsList:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoExecutorsList, jsii.get(self, "executors"))

    @builtins.property
    @jsii.member(jsii_name="gcpAttributes")
    def gcp_attributes(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoGcpAttributesOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoGcpAttributesOutputReference, jsii.get(self, "gcpAttributes"))

    @builtins.property
    @jsii.member(jsii_name="initScripts")
    def init_scripts(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoInitScriptsList:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoInitScriptsList, jsii.get(self, "initScripts"))

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(
        self,
    ) -> "DataDatabricksClusterPluginframeworkClusterInfoSpecOutputReference":
        return typing.cast("DataDatabricksClusterPluginframeworkClusterInfoSpecOutputReference", jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="terminationReason")
    def termination_reason(
        self,
    ) -> "DataDatabricksClusterPluginframeworkClusterInfoTerminationReasonOutputReference":
        return typing.cast("DataDatabricksClusterPluginframeworkClusterInfoTerminationReasonOutputReference", jsii.get(self, "terminationReason"))

    @builtins.property
    @jsii.member(jsii_name="workloadType")
    def workload_type(
        self,
    ) -> "DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeOutputReference":
        return typing.cast("DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeOutputReference", jsii.get(self, "workloadType"))

    @builtins.property
    @jsii.member(jsii_name="autoscaleInput")
    def autoscale_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoAutoscale]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoAutoscale]], jsii.get(self, "autoscaleInput"))

    @builtins.property
    @jsii.member(jsii_name="autoterminationMinutesInput")
    def autotermination_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "autoterminationMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="awsAttributesInput")
    def aws_attributes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoAwsAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoAwsAttributes]], jsii.get(self, "awsAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="azureAttributesInput")
    def azure_attributes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoAzureAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoAzureAttributes]], jsii.get(self, "azureAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterCoresInput")
    def cluster_cores_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "clusterCoresInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterLogConfInput")
    def cluster_log_conf_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoClusterLogConf]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoClusterLogConf]], jsii.get(self, "clusterLogConfInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterLogStatusInput")
    def cluster_log_status_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoClusterLogStatus]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoClusterLogStatus]], jsii.get(self, "clusterLogStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterMemoryMbInput")
    def cluster_memory_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "clusterMemoryMbInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterNameInput")
    def cluster_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterSourceInput")
    def cluster_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="creatorUserNameInput")
    def creator_user_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "creatorUserNameInput"))

    @builtins.property
    @jsii.member(jsii_name="customTagsInput")
    def custom_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "customTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSecurityModeInput")
    def data_security_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSecurityModeInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTagsInput")
    def default_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "defaultTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerImageInput")
    def docker_image_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoDockerImage]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoDockerImage]], jsii.get(self, "dockerImageInput"))

    @builtins.property
    @jsii.member(jsii_name="driverInput")
    def driver_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoDriver]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoDriver]], jsii.get(self, "driverInput"))

    @builtins.property
    @jsii.member(jsii_name="driverInstancePoolIdInput")
    def driver_instance_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "driverInstancePoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="driverNodeTypeIdInput")
    def driver_node_type_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "driverNodeTypeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="enableElasticDiskInput")
    def enable_elastic_disk_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableElasticDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="enableLocalDiskEncryptionInput")
    def enable_local_disk_encryption_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableLocalDiskEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="executorsInput")
    def executors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksClusterPluginframeworkClusterInfoExecutors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksClusterPluginframeworkClusterInfoExecutors]]], jsii.get(self, "executorsInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpAttributesInput")
    def gcp_attributes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoGcpAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoGcpAttributes]], jsii.get(self, "gcpAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="initScriptsInput")
    def init_scripts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksClusterPluginframeworkClusterInfoInitScripts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksClusterPluginframeworkClusterInfoInitScripts]]], jsii.get(self, "initScriptsInput"))

    @builtins.property
    @jsii.member(jsii_name="instancePoolIdInput")
    def instance_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instancePoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="jdbcPortInput")
    def jdbc_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "jdbcPortInput"))

    @builtins.property
    @jsii.member(jsii_name="lastRestartedTimeInput")
    def last_restarted_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lastRestartedTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="lastStateLossTimeInput")
    def last_state_loss_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lastStateLossTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeIdInput")
    def node_type_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeTypeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="numWorkersInput")
    def num_workers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numWorkersInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdInput")
    def policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeEngineInput")
    def runtime_engine_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeEngineInput"))

    @builtins.property
    @jsii.member(jsii_name="singleUserNameInput")
    def single_user_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "singleUserNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkConfInput")
    def spark_conf_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "sparkConfInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkContextIdInput")
    def spark_context_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sparkContextIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkEnvVarsInput")
    def spark_env_vars_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "sparkEnvVarsInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkVersionInput")
    def spark_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sparkVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="specInput")
    def spec_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfoSpec"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfoSpec"]], jsii.get(self, "specInput"))

    @builtins.property
    @jsii.member(jsii_name="sshPublicKeysInput")
    def ssh_public_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sshPublicKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="stateMessageInput")
    def state_message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="terminatedTimeInput")
    def terminated_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "terminatedTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="terminationReasonInput")
    def termination_reason_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfoTerminationReason"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfoTerminationReason"]], jsii.get(self, "terminationReasonInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadTypeInput")
    def workload_type_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfoWorkloadType"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfoWorkloadType"]], jsii.get(self, "workloadTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="autoterminationMinutes")
    def autotermination_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autoterminationMinutes"))

    @autotermination_minutes.setter
    def autotermination_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__310f1f473f9753944e6e04c4af062243ae850ef62bac42bf466103215f846362)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoterminationMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterCores")
    def cluster_cores(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clusterCores"))

    @cluster_cores.setter
    def cluster_cores(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbbfe0f01efa30fdaf179559c934858b30b134ac22ee3e231541d6b2a3bdccce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterCores", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59723baccb3d1dfcad18093dbb8d9bd6a0746a22238695c8ba4b3c1efaccc667)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterMemoryMb")
    def cluster_memory_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clusterMemoryMb"))

    @cluster_memory_mb.setter
    def cluster_memory_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4367343ef7436ad3d6ddf1fa2c7754b40eb80e671062995aa565b41a89c5cf07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterMemoryMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @cluster_name.setter
    def cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09483fc6783cbb6e5992dec7011f7e92bb5716c1039900a46e251b40b17eef0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterSource")
    def cluster_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterSource"))

    @cluster_source.setter
    def cluster_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b15fa9ea543b7cd4e309389b88f67c98b87b1d40ea37ae5d8b8282b0358f8a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="creatorUserName")
    def creator_user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creatorUserName"))

    @creator_user_name.setter
    def creator_user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7434234e6f1bda86d8f65ca2ee26d28ebed6e0965517febc7b2940277798a198)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "creatorUserName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customTags")
    def custom_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "customTags"))

    @custom_tags.setter
    def custom_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64272a38b946c47f84fe5313867f58850278ad98f38cb2713c446e594de2ec37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataSecurityMode")
    def data_security_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSecurityMode"))

    @data_security_mode.setter
    def data_security_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__666b0de308e50fffdd84df5a2df90d9c1e68ba45545a5da5492d421c85c122f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSecurityMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTags")
    def default_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "defaultTags"))

    @default_tags.setter
    def default_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53ed07a0699bdc2bd8021149ee36d83f5f32e821c34ae49b96a2454f6d29ea13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="driverInstancePoolId")
    def driver_instance_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "driverInstancePoolId"))

    @driver_instance_pool_id.setter
    def driver_instance_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d5f43f9446948a5f74859746784a142955e4c9f9592eb2d878f6bbea16b2316)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverInstancePoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="driverNodeTypeId")
    def driver_node_type_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "driverNodeTypeId"))

    @driver_node_type_id.setter
    def driver_node_type_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a47a4c171939f992a05afb0e0bb6aa9b77323692e4516b5c5886eb46193826d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverNodeTypeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableElasticDisk")
    def enable_elastic_disk(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableElasticDisk"))

    @enable_elastic_disk.setter
    def enable_elastic_disk(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8626138e188822af894108765c4839364bf84bb40c54a312bf6d7437e601116)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableElasticDisk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableLocalDiskEncryption")
    def enable_local_disk_encryption(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableLocalDiskEncryption"))

    @enable_local_disk_encryption.setter
    def enable_local_disk_encryption(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74e10213ceb110c5210e4196c237c1907d35a0adf4bcbcf6664623dc41db4c97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableLocalDiskEncryption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instancePoolId")
    def instance_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instancePoolId"))

    @instance_pool_id.setter
    def instance_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e82ccb0c92b2ce9002867a657fb39219621fe046d15fe273fadcbac20578b14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instancePoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jdbcPort")
    def jdbc_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "jdbcPort"))

    @jdbc_port.setter
    def jdbc_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c53cb6398b6c33990a96d9e0130c70a2c456773d94989f8a275ad802defec244)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jdbcPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lastRestartedTime")
    def last_restarted_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lastRestartedTime"))

    @last_restarted_time.setter
    def last_restarted_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25467021e336701e11df5a1f0f6709328b0fadf4cb5ca60bbf5015a36d62ea04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastRestartedTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lastStateLossTime")
    def last_state_loss_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lastStateLossTime"))

    @last_state_loss_time.setter
    def last_state_loss_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8231dcf50e77cf1ee446370cf6928a44541f88c697d93083b3a689ec8ec907f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastStateLossTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeTypeId")
    def node_type_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeTypeId"))

    @node_type_id.setter
    def node_type_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a89e11b8be534b4b5895304b4dd4fe96ac534fcbc2a927e0b36618ffd4cf218)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeTypeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numWorkers")
    def num_workers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numWorkers"))

    @num_workers.setter
    def num_workers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b46e5794e77b1bbcec07c55c73897265149baaaabee7d7048394cf689171853)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numWorkers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__994b0113cc2fa911489f930406504359074bdae43b79ac4c0c29496b9455f46a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeEngine")
    def runtime_engine(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeEngine"))

    @runtime_engine.setter
    def runtime_engine(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ead89abcdf59b03adf4dc779a3c799bd85570b05863989331228e18f7e55e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeEngine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="singleUserName")
    def single_user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "singleUserName"))

    @single_user_name.setter
    def single_user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db9fed6955c4c1293eb883b568f70f0aac7521b8643fc0fbd44e11e80766e883)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "singleUserName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sparkConf")
    def spark_conf(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "sparkConf"))

    @spark_conf.setter
    def spark_conf(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a5964b2f9852a185cc73ab239b6a5533748228d79616c030552e41adb1d2b9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sparkConf", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sparkContextId")
    def spark_context_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sparkContextId"))

    @spark_context_id.setter
    def spark_context_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f3d92cd03a85dcb7426ce01271fe2f09641a6654688f34e060cd70f77142b31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sparkContextId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sparkEnvVars")
    def spark_env_vars(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "sparkEnvVars"))

    @spark_env_vars.setter
    def spark_env_vars(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2c53088af566f99b77ed7f2dd3337a5e88233c60063334f71ee716ed3eb98d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sparkEnvVars", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sparkVersion")
    def spark_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sparkVersion"))

    @spark_version.setter
    def spark_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90f543155bdbd65346fc98df0cb083657cb39018d8c9e1792add9739377e0648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sparkVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshPublicKeys")
    def ssh_public_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sshPublicKeys"))

    @ssh_public_keys.setter
    def ssh_public_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e2699b0367fcad350bcf6075d12344ae7871b99a3b821eab3770b085ec447e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshPublicKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78d22a1303211a380039011beb0c35ac0674bd7d57c65f5dfb3395ecc2755937)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a854ee23e87c62eda14bf26ee1590d053d1092f6f42a27b2166893ece13f1854)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stateMessage")
    def state_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateMessage"))

    @state_message.setter
    def state_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e2075cbefc297d76bdac99cc6fe03073d1a8d0333c3ed1603e03ceed3cfd23e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stateMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terminatedTime")
    def terminated_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "terminatedTime"))

    @terminated_time.setter
    def terminated_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c10cb6cf47b99c23078bc0c5439a8c25ab24d0cdbd091f5f948723f318a267a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terminatedTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfo]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfo]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfo]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de71b6a68f36f3ef0532897aa74bbd6221489bfa57fb4b6cafaa8efe2a1626dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpec",
    jsii_struct_bases=[],
    name_mapping={
        "apply_policy_default_values": "applyPolicyDefaultValues",
        "autoscale": "autoscale",
        "autotermination_minutes": "autoterminationMinutes",
        "aws_attributes": "awsAttributes",
        "azure_attributes": "azureAttributes",
        "cluster_log_conf": "clusterLogConf",
        "cluster_name": "clusterName",
        "custom_tags": "customTags",
        "data_security_mode": "dataSecurityMode",
        "docker_image": "dockerImage",
        "driver_instance_pool_id": "driverInstancePoolId",
        "driver_node_type_id": "driverNodeTypeId",
        "enable_elastic_disk": "enableElasticDisk",
        "enable_local_disk_encryption": "enableLocalDiskEncryption",
        "gcp_attributes": "gcpAttributes",
        "init_scripts": "initScripts",
        "instance_pool_id": "instancePoolId",
        "node_type_id": "nodeTypeId",
        "num_workers": "numWorkers",
        "policy_id": "policyId",
        "runtime_engine": "runtimeEngine",
        "single_user_name": "singleUserName",
        "spark_conf": "sparkConf",
        "spark_env_vars": "sparkEnvVars",
        "spark_version": "sparkVersion",
        "ssh_public_keys": "sshPublicKeys",
        "workload_type": "workloadType",
    },
)
class DataDatabricksClusterPluginframeworkClusterInfoSpec:
    def __init__(
        self,
        *,
        apply_policy_default_values: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        autoscale: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecAutoscale", typing.Dict[builtins.str, typing.Any]]] = None,
        autotermination_minutes: typing.Optional[jsii.Number] = None,
        aws_attributes: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecAwsAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
        azure_attributes: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_log_conf: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConf", typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        custom_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        data_security_mode: typing.Optional[builtins.str] = None,
        docker_image: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImage", typing.Dict[builtins.str, typing.Any]]] = None,
        driver_instance_pool_id: typing.Optional[builtins.str] = None,
        driver_node_type_id: typing.Optional[builtins.str] = None,
        enable_elastic_disk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_local_disk_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcp_attributes: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecGcpAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
        init_scripts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScripts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        instance_pool_id: typing.Optional[builtins.str] = None,
        node_type_id: typing.Optional[builtins.str] = None,
        num_workers: typing.Optional[jsii.Number] = None,
        policy_id: typing.Optional[builtins.str] = None,
        runtime_engine: typing.Optional[builtins.str] = None,
        single_user_name: typing.Optional[builtins.str] = None,
        spark_conf: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        spark_env_vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        spark_version: typing.Optional[builtins.str] = None,
        ssh_public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        workload_type: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadType", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param apply_policy_default_values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#apply_policy_default_values DataDatabricksClusterPluginframework#apply_policy_default_values}.
        :param autoscale: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#autoscale DataDatabricksClusterPluginframework#autoscale}.
        :param autotermination_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#autotermination_minutes DataDatabricksClusterPluginframework#autotermination_minutes}.
        :param aws_attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#aws_attributes DataDatabricksClusterPluginframework#aws_attributes}.
        :param azure_attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#azure_attributes DataDatabricksClusterPluginframework#azure_attributes}.
        :param cluster_log_conf: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_log_conf DataDatabricksClusterPluginframework#cluster_log_conf}.
        :param cluster_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_name DataDatabricksClusterPluginframework#cluster_name}.
        :param custom_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#custom_tags DataDatabricksClusterPluginframework#custom_tags}.
        :param data_security_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#data_security_mode DataDatabricksClusterPluginframework#data_security_mode}.
        :param docker_image: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#docker_image DataDatabricksClusterPluginframework#docker_image}.
        :param driver_instance_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#driver_instance_pool_id DataDatabricksClusterPluginframework#driver_instance_pool_id}.
        :param driver_node_type_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#driver_node_type_id DataDatabricksClusterPluginframework#driver_node_type_id}.
        :param enable_elastic_disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#enable_elastic_disk DataDatabricksClusterPluginframework#enable_elastic_disk}.
        :param enable_local_disk_encryption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#enable_local_disk_encryption DataDatabricksClusterPluginframework#enable_local_disk_encryption}.
        :param gcp_attributes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#gcp_attributes DataDatabricksClusterPluginframework#gcp_attributes}.
        :param init_scripts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#init_scripts DataDatabricksClusterPluginframework#init_scripts}.
        :param instance_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#instance_pool_id DataDatabricksClusterPluginframework#instance_pool_id}.
        :param node_type_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#node_type_id DataDatabricksClusterPluginframework#node_type_id}.
        :param num_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#num_workers DataDatabricksClusterPluginframework#num_workers}.
        :param policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#policy_id DataDatabricksClusterPluginframework#policy_id}.
        :param runtime_engine: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#runtime_engine DataDatabricksClusterPluginframework#runtime_engine}.
        :param single_user_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#single_user_name DataDatabricksClusterPluginframework#single_user_name}.
        :param spark_conf: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spark_conf DataDatabricksClusterPluginframework#spark_conf}.
        :param spark_env_vars: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spark_env_vars DataDatabricksClusterPluginframework#spark_env_vars}.
        :param spark_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spark_version DataDatabricksClusterPluginframework#spark_version}.
        :param ssh_public_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ssh_public_keys DataDatabricksClusterPluginframework#ssh_public_keys}.
        :param workload_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#workload_type DataDatabricksClusterPluginframework#workload_type}.
        '''
        if isinstance(autoscale, dict):
            autoscale = DataDatabricksClusterPluginframeworkClusterInfoSpecAutoscale(**autoscale)
        if isinstance(aws_attributes, dict):
            aws_attributes = DataDatabricksClusterPluginframeworkClusterInfoSpecAwsAttributes(**aws_attributes)
        if isinstance(azure_attributes, dict):
            azure_attributes = DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributes(**azure_attributes)
        if isinstance(cluster_log_conf, dict):
            cluster_log_conf = DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConf(**cluster_log_conf)
        if isinstance(docker_image, dict):
            docker_image = DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImage(**docker_image)
        if isinstance(gcp_attributes, dict):
            gcp_attributes = DataDatabricksClusterPluginframeworkClusterInfoSpecGcpAttributes(**gcp_attributes)
        if isinstance(workload_type, dict):
            workload_type = DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadType(**workload_type)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db20201a5eb214e4657510411068f40edc3eaff70bc4f09280338ea07418c262)
            check_type(argname="argument apply_policy_default_values", value=apply_policy_default_values, expected_type=type_hints["apply_policy_default_values"])
            check_type(argname="argument autoscale", value=autoscale, expected_type=type_hints["autoscale"])
            check_type(argname="argument autotermination_minutes", value=autotermination_minutes, expected_type=type_hints["autotermination_minutes"])
            check_type(argname="argument aws_attributes", value=aws_attributes, expected_type=type_hints["aws_attributes"])
            check_type(argname="argument azure_attributes", value=azure_attributes, expected_type=type_hints["azure_attributes"])
            check_type(argname="argument cluster_log_conf", value=cluster_log_conf, expected_type=type_hints["cluster_log_conf"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument custom_tags", value=custom_tags, expected_type=type_hints["custom_tags"])
            check_type(argname="argument data_security_mode", value=data_security_mode, expected_type=type_hints["data_security_mode"])
            check_type(argname="argument docker_image", value=docker_image, expected_type=type_hints["docker_image"])
            check_type(argname="argument driver_instance_pool_id", value=driver_instance_pool_id, expected_type=type_hints["driver_instance_pool_id"])
            check_type(argname="argument driver_node_type_id", value=driver_node_type_id, expected_type=type_hints["driver_node_type_id"])
            check_type(argname="argument enable_elastic_disk", value=enable_elastic_disk, expected_type=type_hints["enable_elastic_disk"])
            check_type(argname="argument enable_local_disk_encryption", value=enable_local_disk_encryption, expected_type=type_hints["enable_local_disk_encryption"])
            check_type(argname="argument gcp_attributes", value=gcp_attributes, expected_type=type_hints["gcp_attributes"])
            check_type(argname="argument init_scripts", value=init_scripts, expected_type=type_hints["init_scripts"])
            check_type(argname="argument instance_pool_id", value=instance_pool_id, expected_type=type_hints["instance_pool_id"])
            check_type(argname="argument node_type_id", value=node_type_id, expected_type=type_hints["node_type_id"])
            check_type(argname="argument num_workers", value=num_workers, expected_type=type_hints["num_workers"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument runtime_engine", value=runtime_engine, expected_type=type_hints["runtime_engine"])
            check_type(argname="argument single_user_name", value=single_user_name, expected_type=type_hints["single_user_name"])
            check_type(argname="argument spark_conf", value=spark_conf, expected_type=type_hints["spark_conf"])
            check_type(argname="argument spark_env_vars", value=spark_env_vars, expected_type=type_hints["spark_env_vars"])
            check_type(argname="argument spark_version", value=spark_version, expected_type=type_hints["spark_version"])
            check_type(argname="argument ssh_public_keys", value=ssh_public_keys, expected_type=type_hints["ssh_public_keys"])
            check_type(argname="argument workload_type", value=workload_type, expected_type=type_hints["workload_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if apply_policy_default_values is not None:
            self._values["apply_policy_default_values"] = apply_policy_default_values
        if autoscale is not None:
            self._values["autoscale"] = autoscale
        if autotermination_minutes is not None:
            self._values["autotermination_minutes"] = autotermination_minutes
        if aws_attributes is not None:
            self._values["aws_attributes"] = aws_attributes
        if azure_attributes is not None:
            self._values["azure_attributes"] = azure_attributes
        if cluster_log_conf is not None:
            self._values["cluster_log_conf"] = cluster_log_conf
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if custom_tags is not None:
            self._values["custom_tags"] = custom_tags
        if data_security_mode is not None:
            self._values["data_security_mode"] = data_security_mode
        if docker_image is not None:
            self._values["docker_image"] = docker_image
        if driver_instance_pool_id is not None:
            self._values["driver_instance_pool_id"] = driver_instance_pool_id
        if driver_node_type_id is not None:
            self._values["driver_node_type_id"] = driver_node_type_id
        if enable_elastic_disk is not None:
            self._values["enable_elastic_disk"] = enable_elastic_disk
        if enable_local_disk_encryption is not None:
            self._values["enable_local_disk_encryption"] = enable_local_disk_encryption
        if gcp_attributes is not None:
            self._values["gcp_attributes"] = gcp_attributes
        if init_scripts is not None:
            self._values["init_scripts"] = init_scripts
        if instance_pool_id is not None:
            self._values["instance_pool_id"] = instance_pool_id
        if node_type_id is not None:
            self._values["node_type_id"] = node_type_id
        if num_workers is not None:
            self._values["num_workers"] = num_workers
        if policy_id is not None:
            self._values["policy_id"] = policy_id
        if runtime_engine is not None:
            self._values["runtime_engine"] = runtime_engine
        if single_user_name is not None:
            self._values["single_user_name"] = single_user_name
        if spark_conf is not None:
            self._values["spark_conf"] = spark_conf
        if spark_env_vars is not None:
            self._values["spark_env_vars"] = spark_env_vars
        if spark_version is not None:
            self._values["spark_version"] = spark_version
        if ssh_public_keys is not None:
            self._values["ssh_public_keys"] = ssh_public_keys
        if workload_type is not None:
            self._values["workload_type"] = workload_type

    @builtins.property
    def apply_policy_default_values(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#apply_policy_default_values DataDatabricksClusterPluginframework#apply_policy_default_values}.'''
        result = self._values.get("apply_policy_default_values")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def autoscale(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecAutoscale"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#autoscale DataDatabricksClusterPluginframework#autoscale}.'''
        result = self._values.get("autoscale")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecAutoscale"], result)

    @builtins.property
    def autotermination_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#autotermination_minutes DataDatabricksClusterPluginframework#autotermination_minutes}.'''
        result = self._values.get("autotermination_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def aws_attributes(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecAwsAttributes"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#aws_attributes DataDatabricksClusterPluginframework#aws_attributes}.'''
        result = self._values.get("aws_attributes")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecAwsAttributes"], result)

    @builtins.property
    def azure_attributes(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributes"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#azure_attributes DataDatabricksClusterPluginframework#azure_attributes}.'''
        result = self._values.get("azure_attributes")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributes"], result)

    @builtins.property
    def cluster_log_conf(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConf"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_log_conf DataDatabricksClusterPluginframework#cluster_log_conf}.'''
        result = self._values.get("cluster_log_conf")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConf"], result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_name DataDatabricksClusterPluginframework#cluster_name}.'''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#custom_tags DataDatabricksClusterPluginframework#custom_tags}.'''
        result = self._values.get("custom_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def data_security_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#data_security_mode DataDatabricksClusterPluginframework#data_security_mode}.'''
        result = self._values.get("data_security_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_image(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImage"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#docker_image DataDatabricksClusterPluginframework#docker_image}.'''
        result = self._values.get("docker_image")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImage"], result)

    @builtins.property
    def driver_instance_pool_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#driver_instance_pool_id DataDatabricksClusterPluginframework#driver_instance_pool_id}.'''
        result = self._values.get("driver_instance_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def driver_node_type_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#driver_node_type_id DataDatabricksClusterPluginframework#driver_node_type_id}.'''
        result = self._values.get("driver_node_type_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_elastic_disk(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#enable_elastic_disk DataDatabricksClusterPluginframework#enable_elastic_disk}.'''
        result = self._values.get("enable_elastic_disk")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_local_disk_encryption(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#enable_local_disk_encryption DataDatabricksClusterPluginframework#enable_local_disk_encryption}.'''
        result = self._values.get("enable_local_disk_encryption")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcp_attributes(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecGcpAttributes"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#gcp_attributes DataDatabricksClusterPluginframework#gcp_attributes}.'''
        result = self._values.get("gcp_attributes")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecGcpAttributes"], result)

    @builtins.property
    def init_scripts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScripts"]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#init_scripts DataDatabricksClusterPluginframework#init_scripts}.'''
        result = self._values.get("init_scripts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScripts"]]], result)

    @builtins.property
    def instance_pool_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#instance_pool_id DataDatabricksClusterPluginframework#instance_pool_id}.'''
        result = self._values.get("instance_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_type_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#node_type_id DataDatabricksClusterPluginframework#node_type_id}.'''
        result = self._values.get("node_type_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_workers(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#num_workers DataDatabricksClusterPluginframework#num_workers}.'''
        result = self._values.get("num_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def policy_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#policy_id DataDatabricksClusterPluginframework#policy_id}.'''
        result = self._values.get("policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_engine(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#runtime_engine DataDatabricksClusterPluginframework#runtime_engine}.'''
        result = self._values.get("runtime_engine")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def single_user_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#single_user_name DataDatabricksClusterPluginframework#single_user_name}.'''
        result = self._values.get("single_user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spark_conf(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spark_conf DataDatabricksClusterPluginframework#spark_conf}.'''
        result = self._values.get("spark_conf")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def spark_env_vars(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spark_env_vars DataDatabricksClusterPluginframework#spark_env_vars}.'''
        result = self._values.get("spark_env_vars")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def spark_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spark_version DataDatabricksClusterPluginframework#spark_version}.'''
        result = self._values.get("spark_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_public_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ssh_public_keys DataDatabricksClusterPluginframework#ssh_public_keys}.'''
        result = self._values.get("ssh_public_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def workload_type(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadType"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#workload_type DataDatabricksClusterPluginframework#workload_type}.'''
        result = self._values.get("workload_type")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecAutoscale",
    jsii_struct_bases=[],
    name_mapping={"max_workers": "maxWorkers", "min_workers": "minWorkers"},
)
class DataDatabricksClusterPluginframeworkClusterInfoSpecAutoscale:
    def __init__(
        self,
        *,
        max_workers: typing.Optional[jsii.Number] = None,
        min_workers: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#max_workers DataDatabricksClusterPluginframework#max_workers}.
        :param min_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#min_workers DataDatabricksClusterPluginframework#min_workers}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3dce34e0f1a374930c166da3a2598697d61432db0283a358b40cb3b33ddc35d)
            check_type(argname="argument max_workers", value=max_workers, expected_type=type_hints["max_workers"])
            check_type(argname="argument min_workers", value=min_workers, expected_type=type_hints["min_workers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_workers is not None:
            self._values["max_workers"] = max_workers
        if min_workers is not None:
            self._values["min_workers"] = min_workers

    @builtins.property
    def max_workers(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#max_workers DataDatabricksClusterPluginframework#max_workers}.'''
        result = self._values.get("max_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_workers(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#min_workers DataDatabricksClusterPluginframework#min_workers}.'''
        result = self._values.get("min_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoSpecAutoscale(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoSpecAutoscaleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecAutoscaleOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__037b54cbc850d94dab621742c9f0aa6b08007d29a863f6fd3d6274e68670d867)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxWorkers")
    def reset_max_workers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxWorkers", []))

    @jsii.member(jsii_name="resetMinWorkers")
    def reset_min_workers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinWorkers", []))

    @builtins.property
    @jsii.member(jsii_name="maxWorkersInput")
    def max_workers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxWorkersInput"))

    @builtins.property
    @jsii.member(jsii_name="minWorkersInput")
    def min_workers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minWorkersInput"))

    @builtins.property
    @jsii.member(jsii_name="maxWorkers")
    def max_workers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxWorkers"))

    @max_workers.setter
    def max_workers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d25e51137f6f7a8b714856f2a0246c9e1bf58452fccfaa49a6cce2027ec07674)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxWorkers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minWorkers")
    def min_workers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minWorkers"))

    @min_workers.setter
    def min_workers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56af967207ab53da9384f95815e195a24f4e7db62f262155bfab71de4d34a389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minWorkers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecAutoscale]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecAutoscale]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecAutoscale]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30cb061b9372ee2962917cbf13dc4f2b2f86ed422fbaaf683b54968efccc823e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecAwsAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "availability": "availability",
        "ebs_volume_count": "ebsVolumeCount",
        "ebs_volume_iops": "ebsVolumeIops",
        "ebs_volume_size": "ebsVolumeSize",
        "ebs_volume_throughput": "ebsVolumeThroughput",
        "ebs_volume_type": "ebsVolumeType",
        "first_on_demand": "firstOnDemand",
        "instance_profile_arn": "instanceProfileArn",
        "spot_bid_price_percent": "spotBidPricePercent",
        "zone_id": "zoneId",
    },
)
class DataDatabricksClusterPluginframeworkClusterInfoSpecAwsAttributes:
    def __init__(
        self,
        *,
        availability: typing.Optional[builtins.str] = None,
        ebs_volume_count: typing.Optional[jsii.Number] = None,
        ebs_volume_iops: typing.Optional[jsii.Number] = None,
        ebs_volume_size: typing.Optional[jsii.Number] = None,
        ebs_volume_throughput: typing.Optional[jsii.Number] = None,
        ebs_volume_type: typing.Optional[builtins.str] = None,
        first_on_demand: typing.Optional[jsii.Number] = None,
        instance_profile_arn: typing.Optional[builtins.str] = None,
        spot_bid_price_percent: typing.Optional[jsii.Number] = None,
        zone_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#availability DataDatabricksClusterPluginframework#availability}.
        :param ebs_volume_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_count DataDatabricksClusterPluginframework#ebs_volume_count}.
        :param ebs_volume_iops: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_iops DataDatabricksClusterPluginframework#ebs_volume_iops}.
        :param ebs_volume_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_size DataDatabricksClusterPluginframework#ebs_volume_size}.
        :param ebs_volume_throughput: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_throughput DataDatabricksClusterPluginframework#ebs_volume_throughput}.
        :param ebs_volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_type DataDatabricksClusterPluginframework#ebs_volume_type}.
        :param first_on_demand: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#first_on_demand DataDatabricksClusterPluginframework#first_on_demand}.
        :param instance_profile_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#instance_profile_arn DataDatabricksClusterPluginframework#instance_profile_arn}.
        :param spot_bid_price_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spot_bid_price_percent DataDatabricksClusterPluginframework#spot_bid_price_percent}.
        :param zone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#zone_id DataDatabricksClusterPluginframework#zone_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fabcd2dc5bb56ffac7fa9e7816081645ddec5d2b7c27fde171634e88534ed440)
            check_type(argname="argument availability", value=availability, expected_type=type_hints["availability"])
            check_type(argname="argument ebs_volume_count", value=ebs_volume_count, expected_type=type_hints["ebs_volume_count"])
            check_type(argname="argument ebs_volume_iops", value=ebs_volume_iops, expected_type=type_hints["ebs_volume_iops"])
            check_type(argname="argument ebs_volume_size", value=ebs_volume_size, expected_type=type_hints["ebs_volume_size"])
            check_type(argname="argument ebs_volume_throughput", value=ebs_volume_throughput, expected_type=type_hints["ebs_volume_throughput"])
            check_type(argname="argument ebs_volume_type", value=ebs_volume_type, expected_type=type_hints["ebs_volume_type"])
            check_type(argname="argument first_on_demand", value=first_on_demand, expected_type=type_hints["first_on_demand"])
            check_type(argname="argument instance_profile_arn", value=instance_profile_arn, expected_type=type_hints["instance_profile_arn"])
            check_type(argname="argument spot_bid_price_percent", value=spot_bid_price_percent, expected_type=type_hints["spot_bid_price_percent"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability is not None:
            self._values["availability"] = availability
        if ebs_volume_count is not None:
            self._values["ebs_volume_count"] = ebs_volume_count
        if ebs_volume_iops is not None:
            self._values["ebs_volume_iops"] = ebs_volume_iops
        if ebs_volume_size is not None:
            self._values["ebs_volume_size"] = ebs_volume_size
        if ebs_volume_throughput is not None:
            self._values["ebs_volume_throughput"] = ebs_volume_throughput
        if ebs_volume_type is not None:
            self._values["ebs_volume_type"] = ebs_volume_type
        if first_on_demand is not None:
            self._values["first_on_demand"] = first_on_demand
        if instance_profile_arn is not None:
            self._values["instance_profile_arn"] = instance_profile_arn
        if spot_bid_price_percent is not None:
            self._values["spot_bid_price_percent"] = spot_bid_price_percent
        if zone_id is not None:
            self._values["zone_id"] = zone_id

    @builtins.property
    def availability(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#availability DataDatabricksClusterPluginframework#availability}.'''
        result = self._values.get("availability")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ebs_volume_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_count DataDatabricksClusterPluginframework#ebs_volume_count}.'''
        result = self._values.get("ebs_volume_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ebs_volume_iops(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_iops DataDatabricksClusterPluginframework#ebs_volume_iops}.'''
        result = self._values.get("ebs_volume_iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ebs_volume_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_size DataDatabricksClusterPluginframework#ebs_volume_size}.'''
        result = self._values.get("ebs_volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ebs_volume_throughput(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_throughput DataDatabricksClusterPluginframework#ebs_volume_throughput}.'''
        result = self._values.get("ebs_volume_throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ebs_volume_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_type DataDatabricksClusterPluginframework#ebs_volume_type}.'''
        result = self._values.get("ebs_volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def first_on_demand(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#first_on_demand DataDatabricksClusterPluginframework#first_on_demand}.'''
        result = self._values.get("first_on_demand")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def instance_profile_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#instance_profile_arn DataDatabricksClusterPluginframework#instance_profile_arn}.'''
        result = self._values.get("instance_profile_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spot_bid_price_percent(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spot_bid_price_percent DataDatabricksClusterPluginframework#spot_bid_price_percent}.'''
        result = self._values.get("spot_bid_price_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def zone_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#zone_id DataDatabricksClusterPluginframework#zone_id}.'''
        result = self._values.get("zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoSpecAwsAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoSpecAwsAttributesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecAwsAttributesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33fe19b79794e91d7d4a7524db935c77dc21336540947a87feb7bdd26439fc13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAvailability")
    def reset_availability(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailability", []))

    @jsii.member(jsii_name="resetEbsVolumeCount")
    def reset_ebs_volume_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEbsVolumeCount", []))

    @jsii.member(jsii_name="resetEbsVolumeIops")
    def reset_ebs_volume_iops(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEbsVolumeIops", []))

    @jsii.member(jsii_name="resetEbsVolumeSize")
    def reset_ebs_volume_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEbsVolumeSize", []))

    @jsii.member(jsii_name="resetEbsVolumeThroughput")
    def reset_ebs_volume_throughput(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEbsVolumeThroughput", []))

    @jsii.member(jsii_name="resetEbsVolumeType")
    def reset_ebs_volume_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEbsVolumeType", []))

    @jsii.member(jsii_name="resetFirstOnDemand")
    def reset_first_on_demand(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirstOnDemand", []))

    @jsii.member(jsii_name="resetInstanceProfileArn")
    def reset_instance_profile_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceProfileArn", []))

    @jsii.member(jsii_name="resetSpotBidPricePercent")
    def reset_spot_bid_price_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpotBidPricePercent", []))

    @jsii.member(jsii_name="resetZoneId")
    def reset_zone_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZoneId", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityInput")
    def availability_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeCountInput")
    def ebs_volume_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ebsVolumeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeIopsInput")
    def ebs_volume_iops_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ebsVolumeIopsInput"))

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeSizeInput")
    def ebs_volume_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ebsVolumeSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeThroughputInput")
    def ebs_volume_throughput_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ebsVolumeThroughputInput"))

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeTypeInput")
    def ebs_volume_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ebsVolumeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="firstOnDemandInput")
    def first_on_demand_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "firstOnDemandInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceProfileArnInput")
    def instance_profile_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceProfileArnInput"))

    @builtins.property
    @jsii.member(jsii_name="spotBidPricePercentInput")
    def spot_bid_price_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "spotBidPricePercentInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneIdInput")
    def zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="availability")
    def availability(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availability"))

    @availability.setter
    def availability(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20fc6d4798b1319276c713456a5d70bc6ac1640b525b802aad23aa20ce37bf0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availability", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeCount")
    def ebs_volume_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ebsVolumeCount"))

    @ebs_volume_count.setter
    def ebs_volume_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8129e655f0407d393db243fbed63e4c35ec2ce87ac5c717b555007ebb41a410f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ebsVolumeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeIops")
    def ebs_volume_iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ebsVolumeIops"))

    @ebs_volume_iops.setter
    def ebs_volume_iops(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aad17a6943ba7f17e83e2e5cf7a705ec2a0404f0f70400bb479ec8a8ec03f728)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ebsVolumeIops", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeSize")
    def ebs_volume_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ebsVolumeSize"))

    @ebs_volume_size.setter
    def ebs_volume_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f57ae6b45c0c94ac56730f90f9ca1b9388e1f56c1c31d86bff09891e03260b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ebsVolumeSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeThroughput")
    def ebs_volume_throughput(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ebsVolumeThroughput"))

    @ebs_volume_throughput.setter
    def ebs_volume_throughput(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f65045a9e5be0b46fc05a7bb64f4f20092dc382e0f018aa77aae4cc91b61474)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ebsVolumeThroughput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeType")
    def ebs_volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ebsVolumeType"))

    @ebs_volume_type.setter
    def ebs_volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__334674cd04e22bf6b49b1ce1128e257a39c5400a953f51d2924ef8a08a6c13fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ebsVolumeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firstOnDemand")
    def first_on_demand(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "firstOnDemand"))

    @first_on_demand.setter
    def first_on_demand(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2935a11948adc3a11033a2bdd3aa65106a35e8f34270595f278e76fa9312cf69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstOnDemand", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceProfileArn")
    def instance_profile_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceProfileArn"))

    @instance_profile_arn.setter
    def instance_profile_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1af9a16396f544375018537bf78130b74562b18edab32f3b815b5427f42cda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceProfileArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="spotBidPricePercent")
    def spot_bid_price_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "spotBidPricePercent"))

    @spot_bid_price_percent.setter
    def spot_bid_price_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e08c01fa01dab1d7d0082867ef8809c4226a42e7c64ed60ae52d54b4cbdb52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spotBidPricePercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c2d8e9747ecb8848d880f04c18cc7df40fc746a1ff3160367036641da41543e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecAwsAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecAwsAttributes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecAwsAttributes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7766f7603c61c73afff0ed991f2621f207e200fdff80221bd560ccb993b02d02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "availability": "availability",
        "first_on_demand": "firstOnDemand",
        "log_analytics_info": "logAnalyticsInfo",
        "spot_bid_max_price": "spotBidMaxPrice",
    },
)
class DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributes:
    def __init__(
        self,
        *,
        availability: typing.Optional[builtins.str] = None,
        first_on_demand: typing.Optional[jsii.Number] = None,
        log_analytics_info: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesLogAnalyticsInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        spot_bid_max_price: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param availability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#availability DataDatabricksClusterPluginframework#availability}.
        :param first_on_demand: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#first_on_demand DataDatabricksClusterPluginframework#first_on_demand}.
        :param log_analytics_info: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#log_analytics_info DataDatabricksClusterPluginframework#log_analytics_info}.
        :param spot_bid_max_price: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spot_bid_max_price DataDatabricksClusterPluginframework#spot_bid_max_price}.
        '''
        if isinstance(log_analytics_info, dict):
            log_analytics_info = DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesLogAnalyticsInfo(**log_analytics_info)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e28ae651fe851d1651b6712902927f06bad4ddcb1a499b4cf8c892a14e92e4d7)
            check_type(argname="argument availability", value=availability, expected_type=type_hints["availability"])
            check_type(argname="argument first_on_demand", value=first_on_demand, expected_type=type_hints["first_on_demand"])
            check_type(argname="argument log_analytics_info", value=log_analytics_info, expected_type=type_hints["log_analytics_info"])
            check_type(argname="argument spot_bid_max_price", value=spot_bid_max_price, expected_type=type_hints["spot_bid_max_price"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability is not None:
            self._values["availability"] = availability
        if first_on_demand is not None:
            self._values["first_on_demand"] = first_on_demand
        if log_analytics_info is not None:
            self._values["log_analytics_info"] = log_analytics_info
        if spot_bid_max_price is not None:
            self._values["spot_bid_max_price"] = spot_bid_max_price

    @builtins.property
    def availability(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#availability DataDatabricksClusterPluginframework#availability}.'''
        result = self._values.get("availability")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def first_on_demand(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#first_on_demand DataDatabricksClusterPluginframework#first_on_demand}.'''
        result = self._values.get("first_on_demand")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def log_analytics_info(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesLogAnalyticsInfo"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#log_analytics_info DataDatabricksClusterPluginframework#log_analytics_info}.'''
        result = self._values.get("log_analytics_info")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesLogAnalyticsInfo"], result)

    @builtins.property
    def spot_bid_max_price(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spot_bid_max_price DataDatabricksClusterPluginframework#spot_bid_max_price}.'''
        result = self._values.get("spot_bid_max_price")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesLogAnalyticsInfo",
    jsii_struct_bases=[],
    name_mapping={
        "log_analytics_primary_key": "logAnalyticsPrimaryKey",
        "log_analytics_workspace_id": "logAnalyticsWorkspaceId",
    },
)
class DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesLogAnalyticsInfo:
    def __init__(
        self,
        *,
        log_analytics_primary_key: typing.Optional[builtins.str] = None,
        log_analytics_workspace_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param log_analytics_primary_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#log_analytics_primary_key DataDatabricksClusterPluginframework#log_analytics_primary_key}.
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#log_analytics_workspace_id DataDatabricksClusterPluginframework#log_analytics_workspace_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74174c05ba93c4887792a99d203d3dc5bc3109fb28c6084caa895e6ac148c6f2)
            check_type(argname="argument log_analytics_primary_key", value=log_analytics_primary_key, expected_type=type_hints["log_analytics_primary_key"])
            check_type(argname="argument log_analytics_workspace_id", value=log_analytics_workspace_id, expected_type=type_hints["log_analytics_workspace_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_analytics_primary_key is not None:
            self._values["log_analytics_primary_key"] = log_analytics_primary_key
        if log_analytics_workspace_id is not None:
            self._values["log_analytics_workspace_id"] = log_analytics_workspace_id

    @builtins.property
    def log_analytics_primary_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#log_analytics_primary_key DataDatabricksClusterPluginframework#log_analytics_primary_key}.'''
        result = self._values.get("log_analytics_primary_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_analytics_workspace_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#log_analytics_workspace_id DataDatabricksClusterPluginframework#log_analytics_workspace_id}.'''
        result = self._values.get("log_analytics_workspace_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesLogAnalyticsInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesLogAnalyticsInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesLogAnalyticsInfoOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ce14dbed9ca3c6768cc7afeeea30b48e570f0127d1e23dc21b41f9c3e3cb9b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLogAnalyticsPrimaryKey")
    def reset_log_analytics_primary_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogAnalyticsPrimaryKey", []))

    @jsii.member(jsii_name="resetLogAnalyticsWorkspaceId")
    def reset_log_analytics_workspace_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogAnalyticsWorkspaceId", []))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsPrimaryKeyInput")
    def log_analytics_primary_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logAnalyticsPrimaryKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsWorkspaceIdInput")
    def log_analytics_workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logAnalyticsWorkspaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsPrimaryKey")
    def log_analytics_primary_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logAnalyticsPrimaryKey"))

    @log_analytics_primary_key.setter
    def log_analytics_primary_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7afadd0b766e49a85d1d58c35db872805fd6d7eaa1898787b42fd65d2b6938da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAnalyticsPrimaryKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsWorkspaceId")
    def log_analytics_workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logAnalyticsWorkspaceId"))

    @log_analytics_workspace_id.setter
    def log_analytics_workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f4607eb53dd96babff5f46e7edcfe5ec23222ec437b7573e3bedd2090268a85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAnalyticsWorkspaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesLogAnalyticsInfo]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesLogAnalyticsInfo]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesLogAnalyticsInfo]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57d1db3e33139a70d6c79c78cbb2abe12397e2f875092099f05dd9948224dcea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d444c0c053a5ea7025c14ed0fbe7f82f512127d11df5848c05f236f6a0aa5deb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLogAnalyticsInfo")
    def put_log_analytics_info(
        self,
        *,
        log_analytics_primary_key: typing.Optional[builtins.str] = None,
        log_analytics_workspace_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param log_analytics_primary_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#log_analytics_primary_key DataDatabricksClusterPluginframework#log_analytics_primary_key}.
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#log_analytics_workspace_id DataDatabricksClusterPluginframework#log_analytics_workspace_id}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesLogAnalyticsInfo(
            log_analytics_primary_key=log_analytics_primary_key,
            log_analytics_workspace_id=log_analytics_workspace_id,
        )

        return typing.cast(None, jsii.invoke(self, "putLogAnalyticsInfo", [value]))

    @jsii.member(jsii_name="resetAvailability")
    def reset_availability(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailability", []))

    @jsii.member(jsii_name="resetFirstOnDemand")
    def reset_first_on_demand(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirstOnDemand", []))

    @jsii.member(jsii_name="resetLogAnalyticsInfo")
    def reset_log_analytics_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogAnalyticsInfo", []))

    @jsii.member(jsii_name="resetSpotBidMaxPrice")
    def reset_spot_bid_max_price(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpotBidMaxPrice", []))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsInfo")
    def log_analytics_info(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesLogAnalyticsInfoOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesLogAnalyticsInfoOutputReference, jsii.get(self, "logAnalyticsInfo"))

    @builtins.property
    @jsii.member(jsii_name="availabilityInput")
    def availability_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="firstOnDemandInput")
    def first_on_demand_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "firstOnDemandInput"))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsInfoInput")
    def log_analytics_info_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesLogAnalyticsInfo]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesLogAnalyticsInfo]], jsii.get(self, "logAnalyticsInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="spotBidMaxPriceInput")
    def spot_bid_max_price_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "spotBidMaxPriceInput"))

    @builtins.property
    @jsii.member(jsii_name="availability")
    def availability(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availability"))

    @availability.setter
    def availability(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__857407d351c1b83da0cf097e6a579f9df0a948be7efb78cce022da398e695493)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availability", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firstOnDemand")
    def first_on_demand(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "firstOnDemand"))

    @first_on_demand.setter
    def first_on_demand(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__709779ed41e834999793f93b1e0dd072fbad0eb1f7724b7be27f2877d6e4ab04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstOnDemand", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="spotBidMaxPrice")
    def spot_bid_max_price(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "spotBidMaxPrice"))

    @spot_bid_max_price.setter
    def spot_bid_max_price(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__916c296d94fee4a51104aeb4a24a7aa554eafd7bb645469e6eade920c5abb63a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spotBidMaxPrice", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16641524954fbcfbe98d01890b2d2833aa30c3429b9acda36d1426a8732745e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConf",
    jsii_struct_bases=[],
    name_mapping={"dbfs": "dbfs", "s3": "s3"},
)
class DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConf:
    def __init__(
        self,
        *,
        dbfs: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfDbfs", typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfS3", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dbfs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#dbfs DataDatabricksClusterPluginframework#dbfs}.
        :param s3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#s3 DataDatabricksClusterPluginframework#s3}.
        '''
        if isinstance(dbfs, dict):
            dbfs = DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfDbfs(**dbfs)
        if isinstance(s3, dict):
            s3 = DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfS3(**s3)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9398c0016cec098a6456319a427a4a3ce6df4001751c1bc48fa30b3681f46f36)
            check_type(argname="argument dbfs", value=dbfs, expected_type=type_hints["dbfs"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dbfs is not None:
            self._values["dbfs"] = dbfs
        if s3 is not None:
            self._values["s3"] = s3

    @builtins.property
    def dbfs(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfDbfs"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#dbfs DataDatabricksClusterPluginframework#dbfs}.'''
        result = self._values.get("dbfs")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfDbfs"], result)

    @builtins.property
    def s3(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfS3"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#s3 DataDatabricksClusterPluginframework#s3}.'''
        result = self._values.get("s3")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfS3"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConf(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfDbfs",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination"},
)
class DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfDbfs:
    def __init__(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21ecb9491e599037e46f35983a68a07aaed5b582081c71af65bebe1c610f339a)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
        }

    @builtins.property
    def destination(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfDbfs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfDbfsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfDbfsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c34de45a263831229d4c4ae31a6e5caa61d0ca8b73a6833f4de8050519d2420)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff0b08fc58a34f1ccb47d156dff4e1380f67954383a518a101aaf6521c57d9af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfDbfs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfDbfs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfDbfs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__082c9e7cdf3cadc5fe9025cb41e8ae16eee356c7d94fb62067c3b7bc84d3e16f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfec64213c181a7d822cee487f48ebf979cffa42cadcd35e76437a96940222fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDbfs")
    def put_dbfs(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfDbfs(
            destination=destination
        )

        return typing.cast(None, jsii.invoke(self, "putDbfs", [value]))

    @jsii.member(jsii_name="putS3")
    def put_s3(
        self,
        *,
        destination: builtins.str,
        canned_acl: typing.Optional[builtins.str] = None,
        enable_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_type: typing.Optional[builtins.str] = None,
        endpoint: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        :param canned_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#canned_acl DataDatabricksClusterPluginframework#canned_acl}.
        :param enable_encryption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#enable_encryption DataDatabricksClusterPluginframework#enable_encryption}.
        :param encryption_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#encryption_type DataDatabricksClusterPluginframework#encryption_type}.
        :param endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#endpoint DataDatabricksClusterPluginframework#endpoint}.
        :param kms_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#kms_key DataDatabricksClusterPluginframework#kms_key}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#region DataDatabricksClusterPluginframework#region}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfS3(
            destination=destination,
            canned_acl=canned_acl,
            enable_encryption=enable_encryption,
            encryption_type=encryption_type,
            endpoint=endpoint,
            kms_key=kms_key,
            region=region,
        )

        return typing.cast(None, jsii.invoke(self, "putS3", [value]))

    @jsii.member(jsii_name="resetDbfs")
    def reset_dbfs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDbfs", []))

    @jsii.member(jsii_name="resetS3")
    def reset_s3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3", []))

    @builtins.property
    @jsii.member(jsii_name="dbfs")
    def dbfs(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfDbfsOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfDbfsOutputReference, jsii.get(self, "dbfs"))

    @builtins.property
    @jsii.member(jsii_name="s3")
    def s3(
        self,
    ) -> "DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfS3OutputReference":
        return typing.cast("DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfS3OutputReference", jsii.get(self, "s3"))

    @builtins.property
    @jsii.member(jsii_name="dbfsInput")
    def dbfs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfDbfs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfDbfs]], jsii.get(self, "dbfsInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Input")
    def s3_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfS3"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfS3"]], jsii.get(self, "s3Input"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConf]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConf]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConf]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10c34673b353e015d7be31b57e8c7b74c0a16b5c87403614279369dc4e1cec35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfS3",
    jsii_struct_bases=[],
    name_mapping={
        "destination": "destination",
        "canned_acl": "cannedAcl",
        "enable_encryption": "enableEncryption",
        "encryption_type": "encryptionType",
        "endpoint": "endpoint",
        "kms_key": "kmsKey",
        "region": "region",
    },
)
class DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfS3:
    def __init__(
        self,
        *,
        destination: builtins.str,
        canned_acl: typing.Optional[builtins.str] = None,
        enable_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_type: typing.Optional[builtins.str] = None,
        endpoint: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        :param canned_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#canned_acl DataDatabricksClusterPluginframework#canned_acl}.
        :param enable_encryption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#enable_encryption DataDatabricksClusterPluginframework#enable_encryption}.
        :param encryption_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#encryption_type DataDatabricksClusterPluginframework#encryption_type}.
        :param endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#endpoint DataDatabricksClusterPluginframework#endpoint}.
        :param kms_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#kms_key DataDatabricksClusterPluginframework#kms_key}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#region DataDatabricksClusterPluginframework#region}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e4c53055320b0ee563d3bf019d060b481a3786c3538c4954343e6a87fb1843a)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument canned_acl", value=canned_acl, expected_type=type_hints["canned_acl"])
            check_type(argname="argument enable_encryption", value=enable_encryption, expected_type=type_hints["enable_encryption"])
            check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
        }
        if canned_acl is not None:
            self._values["canned_acl"] = canned_acl
        if enable_encryption is not None:
            self._values["enable_encryption"] = enable_encryption
        if encryption_type is not None:
            self._values["encryption_type"] = encryption_type
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def destination(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def canned_acl(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#canned_acl DataDatabricksClusterPluginframework#canned_acl}.'''
        result = self._values.get("canned_acl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_encryption(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#enable_encryption DataDatabricksClusterPluginframework#enable_encryption}.'''
        result = self._values.get("enable_encryption")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#encryption_type DataDatabricksClusterPluginframework#encryption_type}.'''
        result = self._values.get("encryption_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#endpoint DataDatabricksClusterPluginframework#endpoint}.'''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#kms_key DataDatabricksClusterPluginframework#kms_key}.'''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#region DataDatabricksClusterPluginframework#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfS3(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfS3OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfS3OutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b30230369dadec1a0041c2081faeb95f9ffdcf4ad3f19bbecef16302ff8257)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCannedAcl")
    def reset_canned_acl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCannedAcl", []))

    @jsii.member(jsii_name="resetEnableEncryption")
    def reset_enable_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableEncryption", []))

    @jsii.member(jsii_name="resetEncryptionType")
    def reset_encryption_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionType", []))

    @jsii.member(jsii_name="resetEndpoint")
    def reset_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpoint", []))

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @builtins.property
    @jsii.member(jsii_name="cannedAclInput")
    def canned_acl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cannedAclInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="enableEncryptionInput")
    def enable_encryption_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionTypeInput")
    def encryption_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointInput")
    def endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="cannedAcl")
    def canned_acl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cannedAcl"))

    @canned_acl.setter
    def canned_acl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48081131b7181b3a7b23000b9f9dd1f6c0bb232ada17585f9a890ee2a281a7cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cannedAcl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ccc9359f56f66462ac505c93345518c12883858b00212e40126467a9608e87e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableEncryption")
    def enable_encryption(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableEncryption"))

    @enable_encryption.setter
    def enable_encryption(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6132a63c7fb79f45632176c55b17bd8f3c920bb3833099e0be2e6509f91477cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableEncryption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionType")
    def encryption_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionType"))

    @encryption_type.setter
    def encryption_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81be120fb6bef5e74358e910c871d5dd6673c50105cc3c4ec24aaa4711746460)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @endpoint.setter
    def endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0bfe0efd5078f005ab4c4f310056f9e1c2860a23630247907d2a338f69dc2f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b578cfaec5c68bc391db3936762f363b3bf851e1de924f7991839562149af2be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5384a8177792dbfe25203a570032c9b81345e2a275add3857da018b07d7efc3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfS3]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfS3]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfS3]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9ae16a9af6c4caf04744e70e6062bf532fbe50d7118b1385af105bda4fdd45c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImage",
    jsii_struct_bases=[],
    name_mapping={"basic_auth": "basicAuth", "url": "url"},
)
class DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImage:
    def __init__(
        self,
        *,
        basic_auth: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageBasicAuth", typing.Dict[builtins.str, typing.Any]]] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param basic_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#basic_auth DataDatabricksClusterPluginframework#basic_auth}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#url DataDatabricksClusterPluginframework#url}.
        '''
        if isinstance(basic_auth, dict):
            basic_auth = DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageBasicAuth(**basic_auth)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b94ff5751d88129dd2787b481ff670159fad3b803fb061477fba8358d6bf7723)
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if basic_auth is not None:
            self._values["basic_auth"] = basic_auth
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def basic_auth(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageBasicAuth"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#basic_auth DataDatabricksClusterPluginframework#basic_auth}.'''
        result = self._values.get("basic_auth")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageBasicAuth"], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#url DataDatabricksClusterPluginframework#url}.'''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageBasicAuth",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageBasicAuth:
    def __init__(
        self,
        *,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#password DataDatabricksClusterPluginframework#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#username DataDatabricksClusterPluginframework#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49c32318a52f41dcbad0a5b61e22ffd1b97eeba7dfa1432ee7d22bca36d21b82)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if password is not None:
            self._values["password"] = password
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#password DataDatabricksClusterPluginframework#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#username DataDatabricksClusterPluginframework#username}.'''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageBasicAuth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageBasicAuthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageBasicAuthOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5983a1a4198044964b3bf1b2d13612611497a4ab6c0cc942150dda409da56943)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad2504f6ddb86e188ce430af33e7be4f0c1a8fb2979f7a5eb8502b68fb8cce20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__283ed7f1b37b97f1ce5e308a3f6fc3f6e12c899edae04dd35bb093f396956174)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageBasicAuth]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageBasicAuth]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageBasicAuth]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00536c513e977c774e03d06faf80e92c5c1a63d0158ceca07bd92a0df6125a37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a238b8e5ad4537cf52f1909dcea29b06f773e1e18f9412ee29d0020f3a2c12c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBasicAuth")
    def put_basic_auth(
        self,
        *,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#password DataDatabricksClusterPluginframework#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#username DataDatabricksClusterPluginframework#username}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageBasicAuth(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putBasicAuth", [value]))

    @jsii.member(jsii_name="resetBasicAuth")
    def reset_basic_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasicAuth", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @builtins.property
    @jsii.member(jsii_name="basicAuth")
    def basic_auth(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageBasicAuthOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageBasicAuthOutputReference, jsii.get(self, "basicAuth"))

    @builtins.property
    @jsii.member(jsii_name="basicAuthInput")
    def basic_auth_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageBasicAuth]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageBasicAuth]], jsii.get(self, "basicAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca10577bef89251c8cb7c8751936960e3538a73663ec98c1fbecd99fc7994694)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImage]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImage]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImage]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d408203b92dfc1a390db58ac5674a25715193203f5f40879e1d470042448736e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecGcpAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "availability": "availability",
        "boot_disk_size": "bootDiskSize",
        "google_service_account": "googleServiceAccount",
        "local_ssd_count": "localSsdCount",
        "use_preemptible_executors": "usePreemptibleExecutors",
        "zone_id": "zoneId",
    },
)
class DataDatabricksClusterPluginframeworkClusterInfoSpecGcpAttributes:
    def __init__(
        self,
        *,
        availability: typing.Optional[builtins.str] = None,
        boot_disk_size: typing.Optional[jsii.Number] = None,
        google_service_account: typing.Optional[builtins.str] = None,
        local_ssd_count: typing.Optional[jsii.Number] = None,
        use_preemptible_executors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        zone_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#availability DataDatabricksClusterPluginframework#availability}.
        :param boot_disk_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#boot_disk_size DataDatabricksClusterPluginframework#boot_disk_size}.
        :param google_service_account: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#google_service_account DataDatabricksClusterPluginframework#google_service_account}.
        :param local_ssd_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#local_ssd_count DataDatabricksClusterPluginframework#local_ssd_count}.
        :param use_preemptible_executors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#use_preemptible_executors DataDatabricksClusterPluginframework#use_preemptible_executors}.
        :param zone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#zone_id DataDatabricksClusterPluginframework#zone_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea47501e2027f605aaf68ee194ce245d8efb1e7f5bf9989ecff2caa200b5d36d)
            check_type(argname="argument availability", value=availability, expected_type=type_hints["availability"])
            check_type(argname="argument boot_disk_size", value=boot_disk_size, expected_type=type_hints["boot_disk_size"])
            check_type(argname="argument google_service_account", value=google_service_account, expected_type=type_hints["google_service_account"])
            check_type(argname="argument local_ssd_count", value=local_ssd_count, expected_type=type_hints["local_ssd_count"])
            check_type(argname="argument use_preemptible_executors", value=use_preemptible_executors, expected_type=type_hints["use_preemptible_executors"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability is not None:
            self._values["availability"] = availability
        if boot_disk_size is not None:
            self._values["boot_disk_size"] = boot_disk_size
        if google_service_account is not None:
            self._values["google_service_account"] = google_service_account
        if local_ssd_count is not None:
            self._values["local_ssd_count"] = local_ssd_count
        if use_preemptible_executors is not None:
            self._values["use_preemptible_executors"] = use_preemptible_executors
        if zone_id is not None:
            self._values["zone_id"] = zone_id

    @builtins.property
    def availability(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#availability DataDatabricksClusterPluginframework#availability}.'''
        result = self._values.get("availability")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def boot_disk_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#boot_disk_size DataDatabricksClusterPluginframework#boot_disk_size}.'''
        result = self._values.get("boot_disk_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def google_service_account(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#google_service_account DataDatabricksClusterPluginframework#google_service_account}.'''
        result = self._values.get("google_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_ssd_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#local_ssd_count DataDatabricksClusterPluginframework#local_ssd_count}.'''
        result = self._values.get("local_ssd_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def use_preemptible_executors(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#use_preemptible_executors DataDatabricksClusterPluginframework#use_preemptible_executors}.'''
        result = self._values.get("use_preemptible_executors")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def zone_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#zone_id DataDatabricksClusterPluginframework#zone_id}.'''
        result = self._values.get("zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoSpecGcpAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoSpecGcpAttributesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecGcpAttributesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd032a517f6752d39ff662f6b7ee9db1ec737d440dcd4c25e8868a4cd28f4868)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAvailability")
    def reset_availability(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailability", []))

    @jsii.member(jsii_name="resetBootDiskSize")
    def reset_boot_disk_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskSize", []))

    @jsii.member(jsii_name="resetGoogleServiceAccount")
    def reset_google_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoogleServiceAccount", []))

    @jsii.member(jsii_name="resetLocalSsdCount")
    def reset_local_ssd_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalSsdCount", []))

    @jsii.member(jsii_name="resetUsePreemptibleExecutors")
    def reset_use_preemptible_executors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsePreemptibleExecutors", []))

    @jsii.member(jsii_name="resetZoneId")
    def reset_zone_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZoneId", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityInput")
    def availability_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeInput")
    def boot_disk_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootDiskSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="googleServiceAccountInput")
    def google_service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "googleServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="localSsdCountInput")
    def local_ssd_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "localSsdCountInput"))

    @builtins.property
    @jsii.member(jsii_name="usePreemptibleExecutorsInput")
    def use_preemptible_executors_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "usePreemptibleExecutorsInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneIdInput")
    def zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="availability")
    def availability(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availability"))

    @availability.setter
    def availability(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47a65ed1a6e5a17bdceddf8930f52824884b0f39252b3085567d9f8f22eb99f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availability", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bootDiskSize")
    def boot_disk_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bootDiskSize"))

    @boot_disk_size.setter
    def boot_disk_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33121aa90f3a95aed8b0a7117957403211d9a023750fa6db22602146eaf7bb11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="googleServiceAccount")
    def google_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "googleServiceAccount"))

    @google_service_account.setter
    def google_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ec50644b2f6a0221ecf3ef05a162a9c79bcc534307ec83b636c09e151a874bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "googleServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localSsdCount")
    def local_ssd_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "localSsdCount"))

    @local_ssd_count.setter
    def local_ssd_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b58c0f24e36d08058e370e4c603d01f137cb1966f2e48bd6c6cfaca71b3129ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localSsdCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="usePreemptibleExecutors")
    def use_preemptible_executors(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "usePreemptibleExecutors"))

    @use_preemptible_executors.setter
    def use_preemptible_executors(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9ccb09662637fb5d761accd1c6b40489f1deb78fb1e46cb48d7846f29500d06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usePreemptibleExecutors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3b7fbed91266578a5919d4e3a7a952849147b1ef160e126991fb687c8835652)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecGcpAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecGcpAttributes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecGcpAttributes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7ff7994d078080082bfc362e39d2041eea0d79b1b326301db7234195896afd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecInitScripts",
    jsii_struct_bases=[],
    name_mapping={
        "abfss": "abfss",
        "dbfs": "dbfs",
        "file": "file",
        "gcs": "gcs",
        "s3": "s3",
        "volumes": "volumes",
        "workspace": "workspace",
    },
)
class DataDatabricksClusterPluginframeworkClusterInfoSpecInitScripts:
    def __init__(
        self,
        *,
        abfss: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsAbfss", typing.Dict[builtins.str, typing.Any]]] = None,
        dbfs: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsDbfs", typing.Dict[builtins.str, typing.Any]]] = None,
        file: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsFile", typing.Dict[builtins.str, typing.Any]]] = None,
        gcs: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsS3", typing.Dict[builtins.str, typing.Any]]] = None,
        volumes: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsVolumes", typing.Dict[builtins.str, typing.Any]]] = None,
        workspace: typing.Optional[typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsWorkspace", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param abfss: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#abfss DataDatabricksClusterPluginframework#abfss}.
        :param dbfs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#dbfs DataDatabricksClusterPluginframework#dbfs}.
        :param file: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#file DataDatabricksClusterPluginframework#file}.
        :param gcs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#gcs DataDatabricksClusterPluginframework#gcs}.
        :param s3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#s3 DataDatabricksClusterPluginframework#s3}.
        :param volumes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#volumes DataDatabricksClusterPluginframework#volumes}.
        :param workspace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#workspace DataDatabricksClusterPluginframework#workspace}.
        '''
        if isinstance(abfss, dict):
            abfss = DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsAbfss(**abfss)
        if isinstance(dbfs, dict):
            dbfs = DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsDbfs(**dbfs)
        if isinstance(file, dict):
            file = DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsFile(**file)
        if isinstance(gcs, dict):
            gcs = DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsGcs(**gcs)
        if isinstance(s3, dict):
            s3 = DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsS3(**s3)
        if isinstance(volumes, dict):
            volumes = DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsVolumes(**volumes)
        if isinstance(workspace, dict):
            workspace = DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsWorkspace(**workspace)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baca042086b02a841c794eca79b4fa029e83564b8ceeb3e12aa09f4f0c0794f9)
            check_type(argname="argument abfss", value=abfss, expected_type=type_hints["abfss"])
            check_type(argname="argument dbfs", value=dbfs, expected_type=type_hints["dbfs"])
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument gcs", value=gcs, expected_type=type_hints["gcs"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
            check_type(argname="argument workspace", value=workspace, expected_type=type_hints["workspace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if abfss is not None:
            self._values["abfss"] = abfss
        if dbfs is not None:
            self._values["dbfs"] = dbfs
        if file is not None:
            self._values["file"] = file
        if gcs is not None:
            self._values["gcs"] = gcs
        if s3 is not None:
            self._values["s3"] = s3
        if volumes is not None:
            self._values["volumes"] = volumes
        if workspace is not None:
            self._values["workspace"] = workspace

    @builtins.property
    def abfss(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsAbfss"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#abfss DataDatabricksClusterPluginframework#abfss}.'''
        result = self._values.get("abfss")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsAbfss"], result)

    @builtins.property
    def dbfs(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsDbfs"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#dbfs DataDatabricksClusterPluginframework#dbfs}.'''
        result = self._values.get("dbfs")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsDbfs"], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsFile"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#file DataDatabricksClusterPluginframework#file}.'''
        result = self._values.get("file")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsFile"], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsGcs"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#gcs DataDatabricksClusterPluginframework#gcs}.'''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsGcs"], result)

    @builtins.property
    def s3(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsS3"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#s3 DataDatabricksClusterPluginframework#s3}.'''
        result = self._values.get("s3")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsS3"], result)

    @builtins.property
    def volumes(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsVolumes"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#volumes DataDatabricksClusterPluginframework#volumes}.'''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsVolumes"], result)

    @builtins.property
    def workspace(
        self,
    ) -> typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsWorkspace"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#workspace DataDatabricksClusterPluginframework#workspace}.'''
        result = self._values.get("workspace")
        return typing.cast(typing.Optional["DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsWorkspace"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScripts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsAbfss",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination"},
)
class DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsAbfss:
    def __init__(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90c01b98fbdc9fa305eb2b374abc28134268b6cb1db3f3df6b4132dbe93c0be5)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
        }

    @builtins.property
    def destination(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsAbfss(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsAbfssOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsAbfssOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3fabfebce9c073506edfe1cdd44f299f649aa9c6b17fc0c8939946f7a067f50)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c297d7fc2f3f059929863799ce902caada00bbd52eba4299b2c56dce08a909e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsAbfss]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsAbfss]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsAbfss]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a92e4a555d99662c79bc626c196baa14ed8a28b28272074461258bed075302b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsDbfs",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination"},
)
class DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsDbfs:
    def __init__(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c78f964223c25bd64858cf2bcdbfb631bd0235d0a682bd12c760183f0e600ad4)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
        }

    @builtins.property
    def destination(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsDbfs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsDbfsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsDbfsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4605813d5b00894414785f1e8bd5cbc56f8b6c0c56a208e7fedbfcf526444f1c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f80abf94a93dd1f97fb7a1da76cf3684003b2fab223035c3b37843dc20d3b4cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsDbfs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsDbfs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsDbfs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e5c77fffc2ef2222f5c3693080584b79f610e30f7bf540873008c6c1c7cad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsFile",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination"},
)
class DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsFile:
    def __init__(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__475ff1e254c68313d4029f29d8ee0b4a3017a696ecfc49e7fb173600ada14c45)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
        }

    @builtins.property
    def destination(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsFileOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19a4ae2834fbf0cdad7bf3bb7f903e67b1cfcd2a56ef834b37aed3cc7c362acf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc29aa4ae6c646bf981b0a863cc737eb582ddd1cde8cef3a196573351437ab5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsFile]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsFile]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsFile]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef5662bfe362d2f01a6d2b573172678134c91c8819e3319ccba4a65a25369053)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsGcs",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination"},
)
class DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsGcs:
    def __init__(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42e0cf48685956c79ef30499491b4689caa7cd58d8370131abcc9c163acd5326)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
        }

    @builtins.property
    def destination(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsGcsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6846041c1bc0e45e00b01a98baa9083ba15f1da50e12143fe1f48f983c20782e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2de6e2bd95280166cf0e13347c5d105a13bda8993261cc8c7a0eb299893dc0e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsGcs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsGcs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsGcs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9554d02c16ebc9063975bc4e3f73a93e0f209a448614d4f6f7402ddf29b2a21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f912899134fed3fcc158fe60169bd0ac0d5b9ac0ec88450ef964a40b8677d7dc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb2d6244856889f82d5ceb78c750ec63f197d23fd0cec0594fa14fba7f1f1b8f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb0e7f0c5adc4ffe45e998ab25fe490a9a6ee121a39c678cff120aaa58ab4ba7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cc2354a434fd7152cea25312339202b92b688b823a8815c424e1b77d91606be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb37e3cc56e62c979ae6249298cb5e8440179afcf45c896b912ff29d3c1994d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksClusterPluginframeworkClusterInfoSpecInitScripts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksClusterPluginframeworkClusterInfoSpecInitScripts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksClusterPluginframeworkClusterInfoSpecInitScripts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b42ee9187fc038fcfece35e1f2f844e65f9ca688665bf200727f857b3239df59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b0c182fcff2251cfc237336a6fc2a8f3bbe2297e63e244e68af5b402b74bcc5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAbfss")
    def put_abfss(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsAbfss(
            destination=destination
        )

        return typing.cast(None, jsii.invoke(self, "putAbfss", [value]))

    @jsii.member(jsii_name="putDbfs")
    def put_dbfs(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsDbfs(
            destination=destination
        )

        return typing.cast(None, jsii.invoke(self, "putDbfs", [value]))

    @jsii.member(jsii_name="putFile")
    def put_file(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsFile(
            destination=destination
        )

        return typing.cast(None, jsii.invoke(self, "putFile", [value]))

    @jsii.member(jsii_name="putGcs")
    def put_gcs(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsGcs(
            destination=destination
        )

        return typing.cast(None, jsii.invoke(self, "putGcs", [value]))

    @jsii.member(jsii_name="putS3")
    def put_s3(
        self,
        *,
        destination: builtins.str,
        canned_acl: typing.Optional[builtins.str] = None,
        enable_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_type: typing.Optional[builtins.str] = None,
        endpoint: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        :param canned_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#canned_acl DataDatabricksClusterPluginframework#canned_acl}.
        :param enable_encryption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#enable_encryption DataDatabricksClusterPluginframework#enable_encryption}.
        :param encryption_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#encryption_type DataDatabricksClusterPluginframework#encryption_type}.
        :param endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#endpoint DataDatabricksClusterPluginframework#endpoint}.
        :param kms_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#kms_key DataDatabricksClusterPluginframework#kms_key}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#region DataDatabricksClusterPluginframework#region}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsS3(
            destination=destination,
            canned_acl=canned_acl,
            enable_encryption=enable_encryption,
            encryption_type=encryption_type,
            endpoint=endpoint,
            kms_key=kms_key,
            region=region,
        )

        return typing.cast(None, jsii.invoke(self, "putS3", [value]))

    @jsii.member(jsii_name="putVolumes")
    def put_volumes(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsVolumes(
            destination=destination
        )

        return typing.cast(None, jsii.invoke(self, "putVolumes", [value]))

    @jsii.member(jsii_name="putWorkspace")
    def put_workspace(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsWorkspace(
            destination=destination
        )

        return typing.cast(None, jsii.invoke(self, "putWorkspace", [value]))

    @jsii.member(jsii_name="resetAbfss")
    def reset_abfss(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAbfss", []))

    @jsii.member(jsii_name="resetDbfs")
    def reset_dbfs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDbfs", []))

    @jsii.member(jsii_name="resetFile")
    def reset_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFile", []))

    @jsii.member(jsii_name="resetGcs")
    def reset_gcs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcs", []))

    @jsii.member(jsii_name="resetS3")
    def reset_s3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3", []))

    @jsii.member(jsii_name="resetVolumes")
    def reset_volumes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumes", []))

    @jsii.member(jsii_name="resetWorkspace")
    def reset_workspace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkspace", []))

    @builtins.property
    @jsii.member(jsii_name="abfss")
    def abfss(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsAbfssOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsAbfssOutputReference, jsii.get(self, "abfss"))

    @builtins.property
    @jsii.member(jsii_name="dbfs")
    def dbfs(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsDbfsOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsDbfsOutputReference, jsii.get(self, "dbfs"))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsFileOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="gcs")
    def gcs(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsGcsOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="s3")
    def s3(
        self,
    ) -> "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsS3OutputReference":
        return typing.cast("DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsS3OutputReference", jsii.get(self, "s3"))

    @builtins.property
    @jsii.member(jsii_name="volumes")
    def volumes(
        self,
    ) -> "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsVolumesOutputReference":
        return typing.cast("DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsVolumesOutputReference", jsii.get(self, "volumes"))

    @builtins.property
    @jsii.member(jsii_name="workspace")
    def workspace(
        self,
    ) -> "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsWorkspaceOutputReference":
        return typing.cast("DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsWorkspaceOutputReference", jsii.get(self, "workspace"))

    @builtins.property
    @jsii.member(jsii_name="abfssInput")
    def abfss_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsAbfss]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsAbfss]], jsii.get(self, "abfssInput"))

    @builtins.property
    @jsii.member(jsii_name="dbfsInput")
    def dbfs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsDbfs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsDbfs]], jsii.get(self, "dbfsInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsFile]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsFile]], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsInput")
    def gcs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsGcs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsGcs]], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Input")
    def s3_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsS3"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsS3"]], jsii.get(self, "s3Input"))

    @builtins.property
    @jsii.member(jsii_name="volumesInput")
    def volumes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsVolumes"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsVolumes"]], jsii.get(self, "volumesInput"))

    @builtins.property
    @jsii.member(jsii_name="workspaceInput")
    def workspace_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsWorkspace"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsWorkspace"]], jsii.get(self, "workspaceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScripts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScripts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScripts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bb5611c34420b5b9f7ec4521f0e4edd4e6141b1b5e37f0a435544f298488469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsS3",
    jsii_struct_bases=[],
    name_mapping={
        "destination": "destination",
        "canned_acl": "cannedAcl",
        "enable_encryption": "enableEncryption",
        "encryption_type": "encryptionType",
        "endpoint": "endpoint",
        "kms_key": "kmsKey",
        "region": "region",
    },
)
class DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsS3:
    def __init__(
        self,
        *,
        destination: builtins.str,
        canned_acl: typing.Optional[builtins.str] = None,
        enable_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_type: typing.Optional[builtins.str] = None,
        endpoint: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        :param canned_acl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#canned_acl DataDatabricksClusterPluginframework#canned_acl}.
        :param enable_encryption: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#enable_encryption DataDatabricksClusterPluginframework#enable_encryption}.
        :param encryption_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#encryption_type DataDatabricksClusterPluginframework#encryption_type}.
        :param endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#endpoint DataDatabricksClusterPluginframework#endpoint}.
        :param kms_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#kms_key DataDatabricksClusterPluginframework#kms_key}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#region DataDatabricksClusterPluginframework#region}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfb2c071d67c60af8fd036a88a029eb1f648b23d9bd694642acfd7c4dd428617)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument canned_acl", value=canned_acl, expected_type=type_hints["canned_acl"])
            check_type(argname="argument enable_encryption", value=enable_encryption, expected_type=type_hints["enable_encryption"])
            check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
        }
        if canned_acl is not None:
            self._values["canned_acl"] = canned_acl
        if enable_encryption is not None:
            self._values["enable_encryption"] = enable_encryption
        if encryption_type is not None:
            self._values["encryption_type"] = encryption_type
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def destination(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def canned_acl(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#canned_acl DataDatabricksClusterPluginframework#canned_acl}.'''
        result = self._values.get("canned_acl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_encryption(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#enable_encryption DataDatabricksClusterPluginframework#enable_encryption}.'''
        result = self._values.get("enable_encryption")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#encryption_type DataDatabricksClusterPluginframework#encryption_type}.'''
        result = self._values.get("encryption_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#endpoint DataDatabricksClusterPluginframework#endpoint}.'''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#kms_key DataDatabricksClusterPluginframework#kms_key}.'''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#region DataDatabricksClusterPluginframework#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsS3(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsS3OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsS3OutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4edc13e3aa3adc1f61320463e547d1c106658c1ca63a67b4c1df53b1ddbf02a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCannedAcl")
    def reset_canned_acl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCannedAcl", []))

    @jsii.member(jsii_name="resetEnableEncryption")
    def reset_enable_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableEncryption", []))

    @jsii.member(jsii_name="resetEncryptionType")
    def reset_encryption_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionType", []))

    @jsii.member(jsii_name="resetEndpoint")
    def reset_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpoint", []))

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @builtins.property
    @jsii.member(jsii_name="cannedAclInput")
    def canned_acl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cannedAclInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="enableEncryptionInput")
    def enable_encryption_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionTypeInput")
    def encryption_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointInput")
    def endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="cannedAcl")
    def canned_acl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cannedAcl"))

    @canned_acl.setter
    def canned_acl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09f88cb6067fa1c65fffae0d38dbb2538e5e10d46f6c3a183e8f122122a86e54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cannedAcl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b995db290d90afe8f0f3c28bf258ce5d41c2bb8f329c9ccdab98909c4e911c91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableEncryption")
    def enable_encryption(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableEncryption"))

    @enable_encryption.setter
    def enable_encryption(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41238c5be7d78f31435d9fe51fb27706669eb9e025089acd13ab39bd1da027ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableEncryption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionType")
    def encryption_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionType"))

    @encryption_type.setter
    def encryption_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a839623d08decdb9118cb6f4e9211facb9f6e8ec504687b4dffc05efd5c417c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @endpoint.setter
    def endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5bd5f5abdee109559c461730e2adb2420ae0b41662273d85eef7c0fd5f16c00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6209c73d803f6bc1341d5cde27f87aedbd3d87ae22d64c039c597bc12abf9ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22cd9eb283e79e390d277d3116ad406cdc3df621e061026852927fc24548a8d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsS3]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsS3]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsS3]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b0a20538d58e619c876fe15ec0cd40f28db57fe749d4a2fa2bfddf1b28a39a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsVolumes",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination"},
)
class DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsVolumes:
    def __init__(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bcc0e162b7dfa2df41fc8054ba5fce67737f1e092935668a986edac851b24b0)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
        }

    @builtins.property
    def destination(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsVolumesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsVolumesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdfad2f83996555ea64d8bbe965e515fbdfe62e1ebd30d8aca5ef475bf3339fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5671f50edc74c068abf6a1302c8c691db0ea52f099abccd0a5a81eb6dcd3479f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsVolumes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsVolumes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsVolumes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22125d9473c3db59fc4a8171647268dc77201909210567bdf2a74bc914a227f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsWorkspace",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination"},
)
class DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsWorkspace:
    def __init__(self, *, destination: builtins.str) -> None:
        '''
        :param destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__961c53888ff137f5e77233e22f021cb219e770028266581876a882d7f3399dfa)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
        }

    @builtins.property
    def destination(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#destination DataDatabricksClusterPluginframework#destination}.'''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsWorkspace(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsWorkspaceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsWorkspaceOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27cafb156627fcd72ed7b58d8a68379860cae30c2cca2aaac8ae08cde5c6b245)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a98e2c2431f0e143281286e46b9daa0a07df02d0987dd392b0eb260a3f1f80b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsWorkspace]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsWorkspace]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsWorkspace]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__726caf50679267ef1be4d028d5e51eb8d271120dc8d5bb2cbdbf163f5ef011d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksClusterPluginframeworkClusterInfoSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__501102455f95620d0084520e687bdf14b36596a7be99b9977881223dabf63f64)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscale")
    def put_autoscale(
        self,
        *,
        max_workers: typing.Optional[jsii.Number] = None,
        min_workers: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#max_workers DataDatabricksClusterPluginframework#max_workers}.
        :param min_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#min_workers DataDatabricksClusterPluginframework#min_workers}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoSpecAutoscale(
            max_workers=max_workers, min_workers=min_workers
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscale", [value]))

    @jsii.member(jsii_name="putAwsAttributes")
    def put_aws_attributes(
        self,
        *,
        availability: typing.Optional[builtins.str] = None,
        ebs_volume_count: typing.Optional[jsii.Number] = None,
        ebs_volume_iops: typing.Optional[jsii.Number] = None,
        ebs_volume_size: typing.Optional[jsii.Number] = None,
        ebs_volume_throughput: typing.Optional[jsii.Number] = None,
        ebs_volume_type: typing.Optional[builtins.str] = None,
        first_on_demand: typing.Optional[jsii.Number] = None,
        instance_profile_arn: typing.Optional[builtins.str] = None,
        spot_bid_price_percent: typing.Optional[jsii.Number] = None,
        zone_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#availability DataDatabricksClusterPluginframework#availability}.
        :param ebs_volume_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_count DataDatabricksClusterPluginframework#ebs_volume_count}.
        :param ebs_volume_iops: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_iops DataDatabricksClusterPluginframework#ebs_volume_iops}.
        :param ebs_volume_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_size DataDatabricksClusterPluginframework#ebs_volume_size}.
        :param ebs_volume_throughput: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_throughput DataDatabricksClusterPluginframework#ebs_volume_throughput}.
        :param ebs_volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#ebs_volume_type DataDatabricksClusterPluginframework#ebs_volume_type}.
        :param first_on_demand: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#first_on_demand DataDatabricksClusterPluginframework#first_on_demand}.
        :param instance_profile_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#instance_profile_arn DataDatabricksClusterPluginframework#instance_profile_arn}.
        :param spot_bid_price_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spot_bid_price_percent DataDatabricksClusterPluginframework#spot_bid_price_percent}.
        :param zone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#zone_id DataDatabricksClusterPluginframework#zone_id}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoSpecAwsAttributes(
            availability=availability,
            ebs_volume_count=ebs_volume_count,
            ebs_volume_iops=ebs_volume_iops,
            ebs_volume_size=ebs_volume_size,
            ebs_volume_throughput=ebs_volume_throughput,
            ebs_volume_type=ebs_volume_type,
            first_on_demand=first_on_demand,
            instance_profile_arn=instance_profile_arn,
            spot_bid_price_percent=spot_bid_price_percent,
            zone_id=zone_id,
        )

        return typing.cast(None, jsii.invoke(self, "putAwsAttributes", [value]))

    @jsii.member(jsii_name="putAzureAttributes")
    def put_azure_attributes(
        self,
        *,
        availability: typing.Optional[builtins.str] = None,
        first_on_demand: typing.Optional[jsii.Number] = None,
        log_analytics_info: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesLogAnalyticsInfo, typing.Dict[builtins.str, typing.Any]]] = None,
        spot_bid_max_price: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param availability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#availability DataDatabricksClusterPluginframework#availability}.
        :param first_on_demand: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#first_on_demand DataDatabricksClusterPluginframework#first_on_demand}.
        :param log_analytics_info: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#log_analytics_info DataDatabricksClusterPluginframework#log_analytics_info}.
        :param spot_bid_max_price: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#spot_bid_max_price DataDatabricksClusterPluginframework#spot_bid_max_price}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributes(
            availability=availability,
            first_on_demand=first_on_demand,
            log_analytics_info=log_analytics_info,
            spot_bid_max_price=spot_bid_max_price,
        )

        return typing.cast(None, jsii.invoke(self, "putAzureAttributes", [value]))

    @jsii.member(jsii_name="putClusterLogConf")
    def put_cluster_log_conf(
        self,
        *,
        dbfs: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfDbfs, typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfS3, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dbfs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#dbfs DataDatabricksClusterPluginframework#dbfs}.
        :param s3: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#s3 DataDatabricksClusterPluginframework#s3}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConf(
            dbfs=dbfs, s3=s3
        )

        return typing.cast(None, jsii.invoke(self, "putClusterLogConf", [value]))

    @jsii.member(jsii_name="putDockerImage")
    def put_docker_image(
        self,
        *,
        basic_auth: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageBasicAuth, typing.Dict[builtins.str, typing.Any]]] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param basic_auth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#basic_auth DataDatabricksClusterPluginframework#basic_auth}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#url DataDatabricksClusterPluginframework#url}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImage(
            basic_auth=basic_auth, url=url
        )

        return typing.cast(None, jsii.invoke(self, "putDockerImage", [value]))

    @jsii.member(jsii_name="putGcpAttributes")
    def put_gcp_attributes(
        self,
        *,
        availability: typing.Optional[builtins.str] = None,
        boot_disk_size: typing.Optional[jsii.Number] = None,
        google_service_account: typing.Optional[builtins.str] = None,
        local_ssd_count: typing.Optional[jsii.Number] = None,
        use_preemptible_executors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        zone_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param availability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#availability DataDatabricksClusterPluginframework#availability}.
        :param boot_disk_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#boot_disk_size DataDatabricksClusterPluginframework#boot_disk_size}.
        :param google_service_account: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#google_service_account DataDatabricksClusterPluginframework#google_service_account}.
        :param local_ssd_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#local_ssd_count DataDatabricksClusterPluginframework#local_ssd_count}.
        :param use_preemptible_executors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#use_preemptible_executors DataDatabricksClusterPluginframework#use_preemptible_executors}.
        :param zone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#zone_id DataDatabricksClusterPluginframework#zone_id}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoSpecGcpAttributes(
            availability=availability,
            boot_disk_size=boot_disk_size,
            google_service_account=google_service_account,
            local_ssd_count=local_ssd_count,
            use_preemptible_executors=use_preemptible_executors,
            zone_id=zone_id,
        )

        return typing.cast(None, jsii.invoke(self, "putGcpAttributes", [value]))

    @jsii.member(jsii_name="putInitScripts")
    def put_init_scripts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecInitScripts, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9bae80cc0789a6c6cd5c620d346ab23efed8bb627eaafffe897cbe5810b4b7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInitScripts", [value]))

    @jsii.member(jsii_name="putWorkloadType")
    def put_workload_type(
        self,
        *,
        clients: typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeClients", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param clients: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#clients DataDatabricksClusterPluginframework#clients}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadType(
            clients=clients
        )

        return typing.cast(None, jsii.invoke(self, "putWorkloadType", [value]))

    @jsii.member(jsii_name="resetApplyPolicyDefaultValues")
    def reset_apply_policy_default_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplyPolicyDefaultValues", []))

    @jsii.member(jsii_name="resetAutoscale")
    def reset_autoscale(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscale", []))

    @jsii.member(jsii_name="resetAutoterminationMinutes")
    def reset_autotermination_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoterminationMinutes", []))

    @jsii.member(jsii_name="resetAwsAttributes")
    def reset_aws_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAttributes", []))

    @jsii.member(jsii_name="resetAzureAttributes")
    def reset_azure_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureAttributes", []))

    @jsii.member(jsii_name="resetClusterLogConf")
    def reset_cluster_log_conf(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterLogConf", []))

    @jsii.member(jsii_name="resetClusterName")
    def reset_cluster_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterName", []))

    @jsii.member(jsii_name="resetCustomTags")
    def reset_custom_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomTags", []))

    @jsii.member(jsii_name="resetDataSecurityMode")
    def reset_data_security_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataSecurityMode", []))

    @jsii.member(jsii_name="resetDockerImage")
    def reset_docker_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerImage", []))

    @jsii.member(jsii_name="resetDriverInstancePoolId")
    def reset_driver_instance_pool_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDriverInstancePoolId", []))

    @jsii.member(jsii_name="resetDriverNodeTypeId")
    def reset_driver_node_type_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDriverNodeTypeId", []))

    @jsii.member(jsii_name="resetEnableElasticDisk")
    def reset_enable_elastic_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableElasticDisk", []))

    @jsii.member(jsii_name="resetEnableLocalDiskEncryption")
    def reset_enable_local_disk_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableLocalDiskEncryption", []))

    @jsii.member(jsii_name="resetGcpAttributes")
    def reset_gcp_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcpAttributes", []))

    @jsii.member(jsii_name="resetInitScripts")
    def reset_init_scripts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitScripts", []))

    @jsii.member(jsii_name="resetInstancePoolId")
    def reset_instance_pool_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstancePoolId", []))

    @jsii.member(jsii_name="resetNodeTypeId")
    def reset_node_type_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeTypeId", []))

    @jsii.member(jsii_name="resetNumWorkers")
    def reset_num_workers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumWorkers", []))

    @jsii.member(jsii_name="resetPolicyId")
    def reset_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyId", []))

    @jsii.member(jsii_name="resetRuntimeEngine")
    def reset_runtime_engine(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeEngine", []))

    @jsii.member(jsii_name="resetSingleUserName")
    def reset_single_user_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSingleUserName", []))

    @jsii.member(jsii_name="resetSparkConf")
    def reset_spark_conf(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkConf", []))

    @jsii.member(jsii_name="resetSparkEnvVars")
    def reset_spark_env_vars(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkEnvVars", []))

    @jsii.member(jsii_name="resetSparkVersion")
    def reset_spark_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkVersion", []))

    @jsii.member(jsii_name="resetSshPublicKeys")
    def reset_ssh_public_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshPublicKeys", []))

    @jsii.member(jsii_name="resetWorkloadType")
    def reset_workload_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkloadType", []))

    @builtins.property
    @jsii.member(jsii_name="autoscale")
    def autoscale(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoSpecAutoscaleOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoSpecAutoscaleOutputReference, jsii.get(self, "autoscale"))

    @builtins.property
    @jsii.member(jsii_name="awsAttributes")
    def aws_attributes(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoSpecAwsAttributesOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoSpecAwsAttributesOutputReference, jsii.get(self, "awsAttributes"))

    @builtins.property
    @jsii.member(jsii_name="azureAttributes")
    def azure_attributes(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesOutputReference, jsii.get(self, "azureAttributes"))

    @builtins.property
    @jsii.member(jsii_name="clusterLogConf")
    def cluster_log_conf(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfOutputReference, jsii.get(self, "clusterLogConf"))

    @builtins.property
    @jsii.member(jsii_name="dockerImage")
    def docker_image(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageOutputReference, jsii.get(self, "dockerImage"))

    @builtins.property
    @jsii.member(jsii_name="gcpAttributes")
    def gcp_attributes(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoSpecGcpAttributesOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoSpecGcpAttributesOutputReference, jsii.get(self, "gcpAttributes"))

    @builtins.property
    @jsii.member(jsii_name="initScripts")
    def init_scripts(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsList:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsList, jsii.get(self, "initScripts"))

    @builtins.property
    @jsii.member(jsii_name="workloadType")
    def workload_type(
        self,
    ) -> "DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeOutputReference":
        return typing.cast("DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeOutputReference", jsii.get(self, "workloadType"))

    @builtins.property
    @jsii.member(jsii_name="applyPolicyDefaultValuesInput")
    def apply_policy_default_values_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "applyPolicyDefaultValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="autoscaleInput")
    def autoscale_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecAutoscale]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecAutoscale]], jsii.get(self, "autoscaleInput"))

    @builtins.property
    @jsii.member(jsii_name="autoterminationMinutesInput")
    def autotermination_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "autoterminationMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="awsAttributesInput")
    def aws_attributes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecAwsAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecAwsAttributes]], jsii.get(self, "awsAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="azureAttributesInput")
    def azure_attributes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributes]], jsii.get(self, "azureAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterLogConfInput")
    def cluster_log_conf_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConf]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConf]], jsii.get(self, "clusterLogConfInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterNameInput")
    def cluster_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="customTagsInput")
    def custom_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "customTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSecurityModeInput")
    def data_security_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSecurityModeInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerImageInput")
    def docker_image_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImage]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImage]], jsii.get(self, "dockerImageInput"))

    @builtins.property
    @jsii.member(jsii_name="driverInstancePoolIdInput")
    def driver_instance_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "driverInstancePoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="driverNodeTypeIdInput")
    def driver_node_type_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "driverNodeTypeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="enableElasticDiskInput")
    def enable_elastic_disk_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableElasticDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="enableLocalDiskEncryptionInput")
    def enable_local_disk_encryption_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableLocalDiskEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpAttributesInput")
    def gcp_attributes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecGcpAttributes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecGcpAttributes]], jsii.get(self, "gcpAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="initScriptsInput")
    def init_scripts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksClusterPluginframeworkClusterInfoSpecInitScripts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksClusterPluginframeworkClusterInfoSpecInitScripts]]], jsii.get(self, "initScriptsInput"))

    @builtins.property
    @jsii.member(jsii_name="instancePoolIdInput")
    def instance_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instancePoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeIdInput")
    def node_type_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeTypeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="numWorkersInput")
    def num_workers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numWorkersInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdInput")
    def policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeEngineInput")
    def runtime_engine_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeEngineInput"))

    @builtins.property
    @jsii.member(jsii_name="singleUserNameInput")
    def single_user_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "singleUserNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkConfInput")
    def spark_conf_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "sparkConfInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkEnvVarsInput")
    def spark_env_vars_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "sparkEnvVarsInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkVersionInput")
    def spark_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sparkVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="sshPublicKeysInput")
    def ssh_public_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sshPublicKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadTypeInput")
    def workload_type_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadType"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadType"]], jsii.get(self, "workloadTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="applyPolicyDefaultValues")
    def apply_policy_default_values(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "applyPolicyDefaultValues"))

    @apply_policy_default_values.setter
    def apply_policy_default_values(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ea942f6e7dff05eb71ddcae48ab3f57859fa594b927f41583076c0c604c0708)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applyPolicyDefaultValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoterminationMinutes")
    def autotermination_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autoterminationMinutes"))

    @autotermination_minutes.setter
    def autotermination_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a3ed779334b68316e58b2200df7bdd794c52ee0f4e9370c2e6431497a6b8b0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoterminationMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @cluster_name.setter
    def cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5367b8142419b7e10a4a1d5b592e9b414215f04f083fae646f3fb2b1651f02e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customTags")
    def custom_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "customTags"))

    @custom_tags.setter
    def custom_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c6be79202ae8e212ac55ed867f7ba4ea854f1ba05c413d1b5aaf564821604e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataSecurityMode")
    def data_security_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSecurityMode"))

    @data_security_mode.setter
    def data_security_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96eefd840d2ecc6d04bb9d4006a3a8cb919b9d77e0f4f426bc627ea30c26c061)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSecurityMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="driverInstancePoolId")
    def driver_instance_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "driverInstancePoolId"))

    @driver_instance_pool_id.setter
    def driver_instance_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d28c4afc96c7054c598a4567d85f99f061dab9e0d7ca4479d15e90f9b35de07f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverInstancePoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="driverNodeTypeId")
    def driver_node_type_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "driverNodeTypeId"))

    @driver_node_type_id.setter
    def driver_node_type_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__384efcabb1ef45a825b5d559c411eb6536b6386452e5763054425545e32176c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverNodeTypeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableElasticDisk")
    def enable_elastic_disk(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableElasticDisk"))

    @enable_elastic_disk.setter
    def enable_elastic_disk(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69ed8220899823ea456f694cf483818b68598e2de4fb49fc85b52570fa2b32ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableElasticDisk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableLocalDiskEncryption")
    def enable_local_disk_encryption(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableLocalDiskEncryption"))

    @enable_local_disk_encryption.setter
    def enable_local_disk_encryption(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fef4fc9dac036608a164d489f707ae9ccd84dd747c97caf33c04fcf042e1a99b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableLocalDiskEncryption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instancePoolId")
    def instance_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instancePoolId"))

    @instance_pool_id.setter
    def instance_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__170de453a59253837449ea685e4403b23b2c0d7ade0cf74f8db5e554e8f707c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instancePoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeTypeId")
    def node_type_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeTypeId"))

    @node_type_id.setter
    def node_type_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b91302e0d391e0ecfbd330c3cce2082d523c2b23edd0ab65075915f952f2918)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeTypeId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numWorkers")
    def num_workers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numWorkers"))

    @num_workers.setter
    def num_workers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3756fef17e2d7e24ca664fbf12bacc96b4d99c8a8b02561413930c40d3b3591e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numWorkers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a31e10197843c6c2ce7e6c7cd8bc47884aa5fe3afaa68e872f658aa6b16c29d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeEngine")
    def runtime_engine(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeEngine"))

    @runtime_engine.setter
    def runtime_engine(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d64b0dc40bc072f8947c9ebd1531529c95403e74c762ba22e8cd82ee08c2643)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeEngine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="singleUserName")
    def single_user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "singleUserName"))

    @single_user_name.setter
    def single_user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa6d91cce342e6b43425910b0a079407710fd3ac42fa0158a6118b1da34a3fa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "singleUserName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sparkConf")
    def spark_conf(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "sparkConf"))

    @spark_conf.setter
    def spark_conf(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d93efaf5e9f19a7e397e0a6d7cd736b5410e58aaea69c015cfa0431ecb6156f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sparkConf", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sparkEnvVars")
    def spark_env_vars(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "sparkEnvVars"))

    @spark_env_vars.setter
    def spark_env_vars(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__637a5538c7225b70e3b4517797ea675a8dcc6bc1032b6fe87082ae41534b1c59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sparkEnvVars", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sparkVersion")
    def spark_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sparkVersion"))

    @spark_version.setter
    def spark_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bb4b956f53710063be2c93a596535ba88389d4cf22f6847ca63dc8eecc65bd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sparkVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshPublicKeys")
    def ssh_public_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sshPublicKeys"))

    @ssh_public_keys.setter
    def ssh_public_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de4bf9e66b324c7a53cbd1fa2a6c5c28ef670510b27637b53a46bec5f6d7fb10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshPublicKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpec]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpec]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpec]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13811e02216a0d6b935ef078c89d09cb328fcd738f045f4cf2bed701ccd969f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadType",
    jsii_struct_bases=[],
    name_mapping={"clients": "clients"},
)
class DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadType:
    def __init__(
        self,
        *,
        clients: typing.Union["DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeClients", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param clients: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#clients DataDatabricksClusterPluginframework#clients}.
        '''
        if isinstance(clients, dict):
            clients = DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeClients(**clients)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b7812dc08116bf00cd618d9ef78537742ff28e968060a008b590356a370a0d)
            check_type(argname="argument clients", value=clients, expected_type=type_hints["clients"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "clients": clients,
        }

    @builtins.property
    def clients(
        self,
    ) -> "DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeClients":
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#clients DataDatabricksClusterPluginframework#clients}.'''
        result = self._values.get("clients")
        assert result is not None, "Required property 'clients' is missing"
        return typing.cast("DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeClients", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeClients",
    jsii_struct_bases=[],
    name_mapping={"jobs": "jobs", "notebooks": "notebooks"},
)
class DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeClients:
    def __init__(
        self,
        *,
        jobs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        notebooks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param jobs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#jobs DataDatabricksClusterPluginframework#jobs}.
        :param notebooks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#notebooks DataDatabricksClusterPluginframework#notebooks}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa44f95bb795714b946eaf95df7860663e0e13689073f7290e804f48c6df72b0)
            check_type(argname="argument jobs", value=jobs, expected_type=type_hints["jobs"])
            check_type(argname="argument notebooks", value=notebooks, expected_type=type_hints["notebooks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if jobs is not None:
            self._values["jobs"] = jobs
        if notebooks is not None:
            self._values["notebooks"] = notebooks

    @builtins.property
    def jobs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#jobs DataDatabricksClusterPluginframework#jobs}.'''
        result = self._values.get("jobs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def notebooks(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#notebooks DataDatabricksClusterPluginframework#notebooks}.'''
        result = self._values.get("notebooks")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeClients(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeClientsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeClientsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__831cc81d47f8970529e9a5e1be953ea63dba13180cad6a9e01b3d04fda108274)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetJobs")
    def reset_jobs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJobs", []))

    @jsii.member(jsii_name="resetNotebooks")
    def reset_notebooks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotebooks", []))

    @builtins.property
    @jsii.member(jsii_name="jobsInput")
    def jobs_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "jobsInput"))

    @builtins.property
    @jsii.member(jsii_name="notebooksInput")
    def notebooks_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "notebooksInput"))

    @builtins.property
    @jsii.member(jsii_name="jobs")
    def jobs(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "jobs"))

    @jobs.setter
    def jobs(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3889e55e3f4e76639a2c69092fb150d0f7e220b8ccaad978a1db75f2cd5785b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notebooks")
    def notebooks(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "notebooks"))

    @notebooks.setter
    def notebooks(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe95479d227b895f23fea9935c52bcdbf1f3ff240f55b8c25d3bc2d2b9679d5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notebooks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeClients]:
        return typing.cast(typing.Optional[DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeClients], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeClients],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25cb7ccbd24f2dbc82288964294a36c5a0f37bb5ffc4de7f84603f290151a079)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cf463d2c852ebc6b0301818a0dc28fb4731130d5e82cec13f5f28eed1598ae0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClients")
    def put_clients(
        self,
        *,
        jobs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        notebooks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param jobs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#jobs DataDatabricksClusterPluginframework#jobs}.
        :param notebooks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#notebooks DataDatabricksClusterPluginframework#notebooks}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeClients(
            jobs=jobs, notebooks=notebooks
        )

        return typing.cast(None, jsii.invoke(self, "putClients", [value]))

    @builtins.property
    @jsii.member(jsii_name="clients")
    def clients(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeClientsOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeClientsOutputReference, jsii.get(self, "clients"))

    @builtins.property
    @jsii.member(jsii_name="clientsInput")
    def clients_input(
        self,
    ) -> typing.Optional[DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeClients]:
        return typing.cast(typing.Optional[DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeClients], jsii.get(self, "clientsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadType]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadType]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadType]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__358f3ca3aea587ce182a1c669452449dc3a0ae1cd42364d3d7882cb2696d7fc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoTerminationReason",
    jsii_struct_bases=[],
    name_mapping={"code": "code", "parameters": "parameters", "type": "type"},
)
class DataDatabricksClusterPluginframeworkClusterInfoTerminationReason:
    def __init__(
        self,
        *,
        code: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#code DataDatabricksClusterPluginframework#code}.
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#parameters DataDatabricksClusterPluginframework#parameters}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#type DataDatabricksClusterPluginframework#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c641f134117317598001465ea80d24f55cfae4aeb879e81082f9ec1954a069a0)
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if code is not None:
            self._values["code"] = code
        if parameters is not None:
            self._values["parameters"] = parameters
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#code DataDatabricksClusterPluginframework#code}.'''
        result = self._values.get("code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#parameters DataDatabricksClusterPluginframework#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#type DataDatabricksClusterPluginframework#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoTerminationReason(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoTerminationReasonOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoTerminationReasonOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__691238dcbfa9756a9b787f1d43193c5fca61690b4aac6bcfc8f3d51b98b9473b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCode")
    def reset_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCode", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="codeInput")
    def code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "codeInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "code"))

    @code.setter
    def code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10960a3bb0fdf9e1adf97ce8512e5dd8f98bd04d58ddd26163dddb490110bb2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "code", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c9ea0734e811b8aa7b9d88b4e6bf081b920d7443824ae94cd1c954a795dccb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f0bd96c652360f21d2e8a031af47f77177aaec06eb2feb83975d8152db67128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoTerminationReason]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoTerminationReason]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoTerminationReason]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__557d67a1c1aaee93d2d9314a76e28f4b12f90c6e82a42f6639140aa3415a57ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoWorkloadType",
    jsii_struct_bases=[],
    name_mapping={"clients": "clients"},
)
class DataDatabricksClusterPluginframeworkClusterInfoWorkloadType:
    def __init__(
        self,
        *,
        clients: typing.Union["DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeClients", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param clients: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#clients DataDatabricksClusterPluginframework#clients}.
        '''
        if isinstance(clients, dict):
            clients = DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeClients(**clients)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98fdee78259b2fe42d26b1bf085bcb7b4ca181e7991bcbac8220ea2e8285b49e)
            check_type(argname="argument clients", value=clients, expected_type=type_hints["clients"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "clients": clients,
        }

    @builtins.property
    def clients(
        self,
    ) -> "DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeClients":
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#clients DataDatabricksClusterPluginframework#clients}.'''
        result = self._values.get("clients")
        assert result is not None, "Required property 'clients' is missing"
        return typing.cast("DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeClients", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoWorkloadType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeClients",
    jsii_struct_bases=[],
    name_mapping={"jobs": "jobs", "notebooks": "notebooks"},
)
class DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeClients:
    def __init__(
        self,
        *,
        jobs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        notebooks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param jobs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#jobs DataDatabricksClusterPluginframework#jobs}.
        :param notebooks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#notebooks DataDatabricksClusterPluginframework#notebooks}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d41135970e4598ed428b97979b7e65c6868b9c17f07d5241882977ba0fd1840)
            check_type(argname="argument jobs", value=jobs, expected_type=type_hints["jobs"])
            check_type(argname="argument notebooks", value=notebooks, expected_type=type_hints["notebooks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if jobs is not None:
            self._values["jobs"] = jobs
        if notebooks is not None:
            self._values["notebooks"] = notebooks

    @builtins.property
    def jobs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#jobs DataDatabricksClusterPluginframework#jobs}.'''
        result = self._values.get("jobs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def notebooks(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#notebooks DataDatabricksClusterPluginframework#notebooks}.'''
        result = self._values.get("notebooks")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeClients(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeClientsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeClientsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0d4261b1db0060db04b029cd1e874bd615a7bdd87164ca0a01dc5918fc02d24)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetJobs")
    def reset_jobs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJobs", []))

    @jsii.member(jsii_name="resetNotebooks")
    def reset_notebooks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotebooks", []))

    @builtins.property
    @jsii.member(jsii_name="jobsInput")
    def jobs_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "jobsInput"))

    @builtins.property
    @jsii.member(jsii_name="notebooksInput")
    def notebooks_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "notebooksInput"))

    @builtins.property
    @jsii.member(jsii_name="jobs")
    def jobs(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "jobs"))

    @jobs.setter
    def jobs(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__864f611252ba965037c3c5395deb3ee28d7b6f0e705a017bc4b84674168d4595)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notebooks")
    def notebooks(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "notebooks"))

    @notebooks.setter
    def notebooks(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6af103f9d85312178c6a0ab512f2458e085f16d97df76deb9700b7ab9027f31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notebooks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeClients]:
        return typing.cast(typing.Optional[DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeClients], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeClients],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eed678efe00d380710b37993a14085e965836619371022682800cd476e8df9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07a1ef093f582e96eabec1031b9da96d175f2954e0a0cd9207fa431399c14a41)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClients")
    def put_clients(
        self,
        *,
        jobs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        notebooks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param jobs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#jobs DataDatabricksClusterPluginframework#jobs}.
        :param notebooks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#notebooks DataDatabricksClusterPluginframework#notebooks}.
        '''
        value = DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeClients(
            jobs=jobs, notebooks=notebooks
        )

        return typing.cast(None, jsii.invoke(self, "putClients", [value]))

    @builtins.property
    @jsii.member(jsii_name="clients")
    def clients(
        self,
    ) -> DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeClientsOutputReference:
        return typing.cast(DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeClientsOutputReference, jsii.get(self, "clients"))

    @builtins.property
    @jsii.member(jsii_name="clientsInput")
    def clients_input(
        self,
    ) -> typing.Optional[DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeClients]:
        return typing.cast(typing.Optional[DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeClients], jsii.get(self, "clientsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoWorkloadType]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoWorkloadType]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoWorkloadType]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__913a884cdecf9e57fab27106d48c704b38dc3337fca1db35298db7dfeb7b958c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.dataDatabricksClusterPluginframework.DataDatabricksClusterPluginframeworkConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cluster_id": "clusterId",
        "cluster_info": "clusterInfo",
        "cluster_name": "clusterName",
    },
)
class DataDatabricksClusterPluginframeworkConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        cluster_id: typing.Optional[builtins.str] = None,
        cluster_info: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfo, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_id DataDatabricksClusterPluginframework#cluster_id}.
        :param cluster_info: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_info DataDatabricksClusterPluginframework#cluster_info}.
        :param cluster_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_name DataDatabricksClusterPluginframework#cluster_name}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(cluster_info, dict):
            cluster_info = DataDatabricksClusterPluginframeworkClusterInfo(**cluster_info)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebd962bd6567e2d6784b6e7f34d4438ced4e7abe32770cad2e73697338fbe37a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument cluster_info", value=cluster_info, expected_type=type_hints["cluster_info"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if cluster_id is not None:
            self._values["cluster_id"] = cluster_id
        if cluster_info is not None:
            self._values["cluster_info"] = cluster_info
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def cluster_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_id DataDatabricksClusterPluginframework#cluster_id}.'''
        result = self._values.get("cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_info(
        self,
    ) -> typing.Optional[DataDatabricksClusterPluginframeworkClusterInfo]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_info DataDatabricksClusterPluginframework#cluster_info}.'''
        result = self._values.get("cluster_info")
        return typing.cast(typing.Optional[DataDatabricksClusterPluginframeworkClusterInfo], result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/data-sources/cluster_pluginframework#cluster_name DataDatabricksClusterPluginframework#cluster_name}.'''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataDatabricksClusterPluginframeworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataDatabricksClusterPluginframework",
    "DataDatabricksClusterPluginframeworkClusterInfo",
    "DataDatabricksClusterPluginframeworkClusterInfoAutoscale",
    "DataDatabricksClusterPluginframeworkClusterInfoAutoscaleOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoAwsAttributes",
    "DataDatabricksClusterPluginframeworkClusterInfoAwsAttributesOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoAzureAttributes",
    "DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesLogAnalyticsInfo",
    "DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesLogAnalyticsInfoOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoClusterLogConf",
    "DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfDbfs",
    "DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfDbfsOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfS3",
    "DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfS3OutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoClusterLogStatus",
    "DataDatabricksClusterPluginframeworkClusterInfoClusterLogStatusOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoDockerImage",
    "DataDatabricksClusterPluginframeworkClusterInfoDockerImageBasicAuth",
    "DataDatabricksClusterPluginframeworkClusterInfoDockerImageBasicAuthOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoDockerImageOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoDriver",
    "DataDatabricksClusterPluginframeworkClusterInfoDriverNodeAwsAttributes",
    "DataDatabricksClusterPluginframeworkClusterInfoDriverNodeAwsAttributesOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoDriverOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoExecutors",
    "DataDatabricksClusterPluginframeworkClusterInfoExecutorsList",
    "DataDatabricksClusterPluginframeworkClusterInfoExecutorsNodeAwsAttributes",
    "DataDatabricksClusterPluginframeworkClusterInfoExecutorsNodeAwsAttributesOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoExecutorsOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoGcpAttributes",
    "DataDatabricksClusterPluginframeworkClusterInfoGcpAttributesOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoInitScripts",
    "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsAbfss",
    "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsAbfssOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsDbfs",
    "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsDbfsOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsFile",
    "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsFileOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsGcs",
    "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsGcsOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsList",
    "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsS3",
    "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsS3OutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsVolumes",
    "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsVolumesOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsWorkspace",
    "DataDatabricksClusterPluginframeworkClusterInfoInitScriptsWorkspaceOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoSpec",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecAutoscale",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecAutoscaleOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecAwsAttributes",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecAwsAttributesOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributes",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesLogAnalyticsInfo",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesLogAnalyticsInfoOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConf",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfDbfs",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfDbfsOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfS3",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfS3OutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImage",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageBasicAuth",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageBasicAuthOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecGcpAttributes",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecGcpAttributesOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScripts",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsAbfss",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsAbfssOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsDbfs",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsDbfsOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsFile",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsFileOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsGcs",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsGcsOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsList",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsS3",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsS3OutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsVolumes",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsVolumesOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsWorkspace",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsWorkspaceOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadType",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeClients",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeClientsOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoTerminationReason",
    "DataDatabricksClusterPluginframeworkClusterInfoTerminationReasonOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoWorkloadType",
    "DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeClients",
    "DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeClientsOutputReference",
    "DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeOutputReference",
    "DataDatabricksClusterPluginframeworkConfig",
]

publication.publish()

def _typecheckingstub__e366a91d00295d072b70f1a4e627cc9579b8fe5cafd12a160382a2fdb2e5d65c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cluster_id: typing.Optional[builtins.str] = None,
    cluster_info: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02b3fe730f0239a2886dd2b2b7a984548fb31f98aaafab93756102ed31ab2240(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61117428e448e89f7262a790000b078ad9011cd3953b9bffcb89483abb2ab8f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52288c752f765542de324754ed21ed43bffa4f75f8df8101044aeb301d1c828f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__861fb60b7278f74f5f9f4062c027552fb238d79c232e98fa917a2f033314f72d(
    *,
    autoscale: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoAutoscale, typing.Dict[builtins.str, typing.Any]]] = None,
    autotermination_minutes: typing.Optional[jsii.Number] = None,
    aws_attributes: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoAwsAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
    azure_attributes: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoAzureAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_cores: typing.Optional[jsii.Number] = None,
    cluster_id: typing.Optional[builtins.str] = None,
    cluster_log_conf: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoClusterLogConf, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_log_status: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoClusterLogStatus, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_memory_mb: typing.Optional[jsii.Number] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    cluster_source: typing.Optional[builtins.str] = None,
    creator_user_name: typing.Optional[builtins.str] = None,
    custom_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    data_security_mode: typing.Optional[builtins.str] = None,
    default_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    docker_image: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoDockerImage, typing.Dict[builtins.str, typing.Any]]] = None,
    driver: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoDriver, typing.Dict[builtins.str, typing.Any]]] = None,
    driver_instance_pool_id: typing.Optional[builtins.str] = None,
    driver_node_type_id: typing.Optional[builtins.str] = None,
    enable_elastic_disk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_local_disk_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    executors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoExecutors, typing.Dict[builtins.str, typing.Any]]]]] = None,
    gcp_attributes: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoGcpAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
    init_scripts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoInitScripts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    instance_pool_id: typing.Optional[builtins.str] = None,
    jdbc_port: typing.Optional[jsii.Number] = None,
    last_restarted_time: typing.Optional[jsii.Number] = None,
    last_state_loss_time: typing.Optional[jsii.Number] = None,
    node_type_id: typing.Optional[builtins.str] = None,
    num_workers: typing.Optional[jsii.Number] = None,
    policy_id: typing.Optional[builtins.str] = None,
    runtime_engine: typing.Optional[builtins.str] = None,
    single_user_name: typing.Optional[builtins.str] = None,
    spark_conf: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    spark_context_id: typing.Optional[jsii.Number] = None,
    spark_env_vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    spark_version: typing.Optional[builtins.str] = None,
    spec: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    ssh_public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    start_time: typing.Optional[jsii.Number] = None,
    state: typing.Optional[builtins.str] = None,
    state_message: typing.Optional[builtins.str] = None,
    terminated_time: typing.Optional[jsii.Number] = None,
    termination_reason: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoTerminationReason, typing.Dict[builtins.str, typing.Any]]] = None,
    workload_type: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoWorkloadType, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a491b50ffd2d0df548ca1223d74097008523070bca7e61f2e5f1da760d7a3147(
    *,
    max_workers: typing.Optional[jsii.Number] = None,
    min_workers: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4904f1c6baabcf0658ccb5df187cdfedb6169cb7437bba2961aaa95f040d89dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__698fef5441edbb1daa034e43e877a7cc57217ed46a88e950e46db7e4650cbb06(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a0b80199c9b0ae6e3b956f6c7ab6bdcb5489b8a5035275127838aa8724c36f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a7b63e7ea72a41861d5a7bf6014139dffd087ddd7f574daff618deb0efa1cb4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoAutoscale]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__142a1d57ec24d0655a019d4b468ec67298c2703f1a99e6e94b46bdd27a719d64(
    *,
    availability: typing.Optional[builtins.str] = None,
    ebs_volume_count: typing.Optional[jsii.Number] = None,
    ebs_volume_iops: typing.Optional[jsii.Number] = None,
    ebs_volume_size: typing.Optional[jsii.Number] = None,
    ebs_volume_throughput: typing.Optional[jsii.Number] = None,
    ebs_volume_type: typing.Optional[builtins.str] = None,
    first_on_demand: typing.Optional[jsii.Number] = None,
    instance_profile_arn: typing.Optional[builtins.str] = None,
    spot_bid_price_percent: typing.Optional[jsii.Number] = None,
    zone_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e62c8bbe0639e01091d2bc211f2d291012684b198071a0713dc3a254e3eedd63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__904e31f6e42c22cd19debbf895213aa321fc9103a539ae6324024bde1107d51b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c352d5197c4f3ba78d2c2374be9a15c0c0aef00d6ddc6e153c230a9dfe92fb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__275f0b10442867b91c0ad06d8fc05383f9ea2fb7eb5f6dfadfe4962274c56406(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a6ed9e1d7216b331270b577ac951111df47814d211a960cfbdb96611b8aca44(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f29e53e21a527c4c8cf5c00ca3dc12211f9b16a0d39f973ff6945532812796f1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ccb26e151487a86d2747fe756daebd4b3e04841a8f7dfb18283cc0b2d94a02d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0698a8228e86d65933796913d83382a52c64526737d1f5d8ef2deb7fe7a5edb5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f087f005c035cb88bda9a0af8d925b4f411a6a3aed8a16d509fbc0604db80fde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9950ef57c2924fb82aeed6ee9475c9af8d6d4af6bca5400408edcf2b21f8bd45(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__720ce8cc362784d56407b7c1575bc3303dfe3dd8a5a296911412314190882324(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a65d5eb6afd08bf75467f438521c07659a3d9fabd8c23d57f42f66b88f6fb8ea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoAwsAttributes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c61c05d47a38992ce40e850f42c3a434cf5738de3592f9c72427efe14ac1c06(
    *,
    availability: typing.Optional[builtins.str] = None,
    first_on_demand: typing.Optional[jsii.Number] = None,
    log_analytics_info: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesLogAnalyticsInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    spot_bid_max_price: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1311071d7443791899381b56ddcd2a9b3069ad7a310808fd13999544a9c25e(
    *,
    log_analytics_primary_key: typing.Optional[builtins.str] = None,
    log_analytics_workspace_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b283e45fbdfc87a748b46573663aa317e9036b00e97eebc85f450a2d315c1a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3eafc6f7bf090d0434c663c16cc3c8800f2fd4c568c5cde0e2d44e3d733503(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__857c25e4590e5b05ab53b20a8ae6ef252e1d38e128405e448985784b8ca141b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe46080c75b16c4e6380646f1ee6277bd6315a2688d0b5f9abc0a86be8f38ec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoAzureAttributesLogAnalyticsInfo]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195c567bbe2f4f15052c871cd81cda0ae5d6ee7dd8e27d211942088dec87c439(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__793c0d8feafc6317e8b50bbdfed29f9c383be8e49c1d16cdc11412b3b0266dea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c6c35766ca77c3b1f6d39b7ac874f087b59dbcb49565de189e6aba968248245(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f47b453c963543e03cc475bd9e42ca0a0266bfd5d79d9f18260fe691b7075b71(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3339022c88de46316fdcc079352dcec63e7ee29a0bd5210e79b8da44c8048074(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoAzureAttributes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95302eabb56e430f0bf11cc230528c1cfb77d2e95370bbefedf10acded5c032c(
    *,
    dbfs: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfDbfs, typing.Dict[builtins.str, typing.Any]]] = None,
    s3: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfS3, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d5183648012b17b641618704764a775971084023ff2e2f60068931610606a91(
    *,
    destination: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f0850c0d411624f7c6e9e0198d082bf2d71a71b6cfd4297980f41e92492696(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f93007cafddd4b565fb8a01fef8c3af31433dce3aa0f543b02c252d476dba353(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c572f2de82973a2681abe43a44c2495ac11eaedb847e626c991179bf2314bfb5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfDbfs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cede6b0bb78cb04c20315c1a9ff59e1a05a47ddae8298b7e7f7c7c22a3cbaec0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ffee980eddf2c3afa00bf8f51affbe4a315f9b95c02abd1926a9e6153fb421(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoClusterLogConf]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c98e750f3ea6c7db093fc50b5b184f8d691236b029681782c353f0c94bd6bf63(
    *,
    destination: builtins.str,
    canned_acl: typing.Optional[builtins.str] = None,
    enable_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_type: typing.Optional[builtins.str] = None,
    endpoint: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf7cf385061a94ce6b175b9d54c96a3d78b9a78635b83847e19967be564b626e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975ca4c0ba52e9415f2c50e90f2ceb956c430634e0c55ba0fb8f4a184ab8f0b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad34fa87b4b77d11ed4df63fb8fbde5d9d0ec619edd24df6374df2c5dfa50f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a925b7763e61f59762e328046864ab4f84e4594a5382e69bfabd9eebc434d7f7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e4cb417d29e2b0ad71a2768a6b5d259f815b0b6511fc84dff2ff8136978e54a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__370d3d8c80313b4583ec17e8d6213a9b4d0ea92b64b6a026c28ccba2a94d764e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99577b4567caa6106c489cf26e9efee1b0ec0bb1eb2e31f16eba943ec4cafc8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__951d1731f36f0e1090f807ac5955e36582e17705cbd37807556ee5178cb8900d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f697b98e3928d89e790f67e79925331a10b2b83ed2d7afff2444f56e252db75e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoClusterLogConfS3]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__144ff888cfde69b59c8d604dc20588fea18685c93aa5241e44e12024973ce3c4(
    *,
    last_attempted: typing.Optional[jsii.Number] = None,
    last_exception: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa0f79b2abaa42e43734c8d32d1029b225f0f2456669c010dcc1f8a552d1f786(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8bf40e64683ad0905d9ca42023c302661389a39afb755e521e4b453a07ef9e3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dbc676216696d2dc7b36d8817c9d865a8e8aa657893bdc97b37b62f97530d29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d270a2fb60128fa29e9d9653fb4ef00f5252efe4b761af762cdfe1bc021ca4be(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoClusterLogStatus]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c456f251d379d56612b7038692260e5ac27b29a34ff0fe6b3c6825f3c4466c(
    *,
    basic_auth: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoDockerImageBasicAuth, typing.Dict[builtins.str, typing.Any]]] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef22e7d121df0b664ce9a72f8022ccf0cb5087301aff9cb0ab689abba37a7c69(
    *,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b255db7c5e0ec9495a169e0bda6a701ba707183bc24e3b6f7de929d2b4619ffe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25492122a1c428af1290c8a2b7b5cc683da028513abe10e41bb4caebd426be1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67eee541ad5cc79b66d632ba12ad32d1696415284768f18738f79fbcb2073538(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c089fd9c55b2744e67f2002099e877b779f7935dbe31fa4b8aa2b9567b4347(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoDockerImageBasicAuth]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3d04ed0d16050f818adb5ebf739f656524cff2952c064517257145e916b8c7d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91a866d2e2d518cc072bc2b58df06ab0de1c4e6f4ef887095a71d6b5f461d403(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79b8c4fd40b12ec57488eb9f8b598ca03f32c6d72288d4f03affb7db614ab98e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoDockerImage]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f12dfa1954f4075bd8e49fb94e5ad113456f1677ac842a9ecbabe277d9dc1d17(
    *,
    host_private_ip: typing.Optional[builtins.str] = None,
    instance_id: typing.Optional[builtins.str] = None,
    node_aws_attributes: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoDriverNodeAwsAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
    node_id: typing.Optional[builtins.str] = None,
    private_ip: typing.Optional[builtins.str] = None,
    public_dns: typing.Optional[builtins.str] = None,
    start_timestamp: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d3706d6dd90dcc8863899ab883c718b81d62c5bce028d897b4fbbe319fdde9(
    *,
    is_spot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10b6aa1544838285c98c2d17e7ac7686c85f52c042c231829013c97f8230cb11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__402c40df8534fbd26162e2568120209f1ec61dcf219ca5d65ad7ce290b016fb7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d8a488bd8b841fde7057767c68f1d99353d3a82c28fd668afb9bc45ee9a329b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoDriverNodeAwsAttributes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16ea6c3c9dcb431d4b459ce055cb786e689c91794f39295e3d5b8b4f14f88ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bc9832d7a4fc77fc89b980baff9aae4b433cdc76ed1c092978450d7c4157169(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba8b315ed569bad79802068ecf82a3a31cfbc8570736e9e4c2391277989c8294(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f5f70a44436e99478c8f8a0d69ea081aa3d5da0fdcf0c56f875d44788339ccf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07a3590d6b33307133e8d4daf582d83b59415eab17ac250a56a8a0878f66f35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__727a1b84d6a7a0e1759726220cfffbd6512babefe99938f66e9b68adafdbc3c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3400957b0156361f120e26ed9a28daef28d365639d25aed144e3bf50d828ba72(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c2b182ae64f20614470d9d93679b96d1fc60f919b08b2b3bc3c030481fdf058(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoDriver]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__527830bf026ed34bc1a58b28d476acee9190e64d04fb46e330442043f1f8e18e(
    *,
    host_private_ip: typing.Optional[builtins.str] = None,
    instance_id: typing.Optional[builtins.str] = None,
    node_aws_attributes: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoExecutorsNodeAwsAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
    node_id: typing.Optional[builtins.str] = None,
    private_ip: typing.Optional[builtins.str] = None,
    public_dns: typing.Optional[builtins.str] = None,
    start_timestamp: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a70242f8a83aaaa9ff98a200bc4f72a63a73601f400d612668a7356cb1e1d257(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9efe5234a0846553ba75fd9ad89ce73ffb15fe7a3179b281c2e13ef4181b7416(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d6c7d971b4ff09f7a93cde40ec04ab125415a498270c33571f1660adc812b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0b7ebc812a2f3b41330b1b8c2edddb5ef9a2226ef09b961b9ccfee4b6e9b91d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f47a31d54c847e6a5fc30098f133045c7902b3a9c5aee160136064ffb78a161(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a91a2d500dc583e77be07e054482e7dcc01e11c2ca0364f06e7bd9e248b8393(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksClusterPluginframeworkClusterInfoExecutors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6599b2ad6fa5701bcc1d263460d9f484583068dfc7577eca94d2505cb05a963c(
    *,
    is_spot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca078e16956a155c8735d749ded6fab1d1b206142574f870d3e93618810d2a10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__618585335e6fc3e3397fcb7a7f0cf28213cd3225820d9caa849e2fbb711e622d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6f4cbb932676d7439d719e62c53ca1ee101002e6962446d6a8cf7d6b1eb5959(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoExecutorsNodeAwsAttributes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be2509eeda1d6f056844116457d4b94d70834d99ffa5854a40c98d185a3d80b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d162a495528ee7c2b6dd52b5d6e466c52e856e13ac37ce3281c91c11bc7ea203(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4f7e015edfd774ffaa788e9463a35645b34f5f29ea9afaeee5dcd94db0b274d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c91e5ebeeb5a7bdc297ce1c615504409b6eda6b83a7b103df4db42f7c2a1a122(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__957b21c3b8245b6c2ffe06ba2f994e742d20f96543634c3a9c1b6084cbbe486f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff45f15b0fcfa53aadac758eb91ddb25eb5acdddbd96003ad3c8b1cc4f7aaddc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ea7e0ba22b0ed78efcea6ddfc3d643bef41c502b041e24b66ccd7ea6ad8351f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7994183f60724fdd848b8695bd3c3e5711ee844b428b463daff53799703660db(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoExecutors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e234c304877129e2e44796e3f391a8d7e1e166f10819be4bae34253b8134c5(
    *,
    availability: typing.Optional[builtins.str] = None,
    boot_disk_size: typing.Optional[jsii.Number] = None,
    google_service_account: typing.Optional[builtins.str] = None,
    local_ssd_count: typing.Optional[jsii.Number] = None,
    use_preemptible_executors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    zone_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e2038a23a7a1b8f208680f8085906a233afb460f684098c8167b62ed7253c06(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e1631a07717f17c5a8b064f9cf1ba6277cbf74c85bdbb0a0d1c945865f27cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b4900d5d495c7edc0be74159063b7343d41f30208be44f60fd17c2dd360085(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c47f502c4d26ccef7f90ea0b7d27fc3cc38be8cc0823fdc5385ef304c0837832(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfa8433e6fef7b00ff052453373acdc77a3d916e44636386fe506b448eb37cd1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34686f25ca3bf072d5640ed2062919a3edf81a636518f4183b8c86917818774d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18352a40af64067c1a17f467af7a6840b128d63e9bae360d26cdea8f8452c114(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a5d1ce6612e303973e56874427a7edccadea09d0b8029330f7854af989af3c9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoGcpAttributes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdebcd61f45adbf2793b3fc06eb847644a66b2cc1b4820c03d0b11c99bf6b5a0(
    *,
    abfss: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoInitScriptsAbfss, typing.Dict[builtins.str, typing.Any]]] = None,
    dbfs: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoInitScriptsDbfs, typing.Dict[builtins.str, typing.Any]]] = None,
    file: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoInitScriptsFile, typing.Dict[builtins.str, typing.Any]]] = None,
    gcs: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoInitScriptsGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    s3: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoInitScriptsS3, typing.Dict[builtins.str, typing.Any]]] = None,
    volumes: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoInitScriptsVolumes, typing.Dict[builtins.str, typing.Any]]] = None,
    workspace: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoInitScriptsWorkspace, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd5cf140713279fde4bc68194f26b0ea8de43a9616101eebddf3ccfb4beb55e9(
    *,
    destination: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce2fb7319f9ef6e9adfe7747de5bc6896b18de02e1089b64dab30ca86272e04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a62c80d402e379c52b569c478bca3b6b0f7bb38798aaaa2ad514e40bca093c07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4de0b3faa37b872174a7b9a8018957972b1b47f9e8d1b1afaa9d7583987cfba7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsAbfss]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2df5244fd02fa27eb67a79ec5aaa7a0f36153d1f521d05b268dc0bb57689f61d(
    *,
    destination: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5890865c8d22dd7f9b9b0faf2ccbe4efe6a824fa087797fa981cab0a75d127b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0570727dd09562ccb38ebf652eace60576226dd83f71ce2bc4d2185b0381c02b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1054870082d88e8f93af9819e52918e06bd4f14f9c1e7464e5401b1f0f0d6f4f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsDbfs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab8fdc6bfc9116cd6638882688b3046bf92328073c5b28ee1017d7336c6f27e6(
    *,
    destination: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2564ec85c7b18ed5cd098baa60849d81ae0d9ed1243dd532e944717f7c611aaa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__671e21decced6cf92d4fb216e6528eb8e7f42773b92e9d29b807facbc766df1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__796fd6fac516654e3bc7ac86e2be0119684150a68faa45cf8db530c0f9c29be9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsFile]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__737a0aba020e61008cf1e15fd913b513817b6fe0831a6e118fbfb94b81f7ff2b(
    *,
    destination: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cfaf90092a5dd754100a36b010ce85094b9be983bb6fdb5e68751d36df84ee7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b4fc6a4faed5cd84c7ed59ebfb87d93a99a3378be17d869bef1995be75445fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d148b4783f0b6e99357c0ec596c0d89a40054e9a947bbb4f3e89f481b1e1e52a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsGcs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15efa0fbd5e3c101af6003ea70667d1702cc3ddf7d9597cd161849dd588e062f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93af346a236377577fe1ea7b9a8b4d0a47d874e14cfc7ba8cf4e711dab465078(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bffc4802a8bc3e070f72ac78a6465c98350ac87835c124dc7bfe79ee8389396b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a08a918accf5cb0f644f8db4d8827e66cd2904b8243d95c8429c3c62be2ea5a5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07896b2f6f77d53c7796d813a4c47767135ee42ee510d7e27610a6d709a28f8b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54d16d7335750f005a8cd85b44a353f73f6752bf37931b3cfa49a0031f02f924(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksClusterPluginframeworkClusterInfoInitScripts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eee1594b96f24a52d67e8af14a2779e123cb08ff734b137b2b071f4a3f12cbe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ada2af8560ace81d6e1375f0babbaaadb05e816be21d80623f9f690ab6590f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScripts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f277518e0bc6240e9b14ac1119e0595ee9308cd11be6eb21bd518dbcc081ed6(
    *,
    destination: builtins.str,
    canned_acl: typing.Optional[builtins.str] = None,
    enable_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_type: typing.Optional[builtins.str] = None,
    endpoint: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f301b41e8f5cf3028428113faf05ebe12e85cb38f0cc0d30bdf63f02fbcae69(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__413ad66f45a91c3dffcf3243364bb3ba100d1c670efe06bcf303bc7a3d73beaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ba7e9d686913cae2d2d7bd0f694d7ffa5c9925628e64753c49a9a772abdbffb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a9ae850d8e2d4ecf9f32d60528dda71ddc8949ead99733a2dee477b8c5141b7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0394331140382874e473f275b8445fc47aee275dfa67dad093eda01266bb9ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58f219c68752d1665c17237b551d14addaa51ab1bb2f638f7f9f793cedc33ab8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5205bb1c6c365b19e57bf28df45ebb1ada8a736c4d88fccf750d0b719e0c0140(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e48ab1f12275ed858ef90bed7aea2c6466b96bfcc52002a977c3039e0cdacce6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68afdea31ca27cc03f0c0f1d4ef971db11bdc580a954b22e251cf86b5caab46e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsS3]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba1bd655324811f9686b5812f1885ba184ae3f5826076eb21059d01bacf2b1d(
    *,
    destination: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1fc1ab8829ddfa45d85e6ed5898fd5c2f9ad062f979fd5104af8cf788e98fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82f7dbf039d9805beee10e2f04619773bfcd49f11d8564d6847b7a8643295ade(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f825d95205d5149442f0ac045fce6a99eb593f8b8ad3f07d227b7c790494bf8d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsVolumes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64af70f1b395584c409d0b282e3589b791d488d6d1ffd77735b2cdddd178b88(
    *,
    destination: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a39020c23721d0aac2a1e399507dc10e8a7e9d88fad23f2cc1cfadd8a4c636(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e2933af3bc8d0d4aaa570eeea248421abed0e983a37bc75e22d3014aa3c6f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c9b60834509e8b28a873dccbe89fce3c9f0cd963cb9d63eccb5d9a656704b2b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoInitScriptsWorkspace]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c04e1c7ad9ad820d25b577c85ddeb0f1bf52116d206a078d91947f62f1def3c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ccabe9b9cf5c52869126b2984e8fae528eb60ec8a0782cc92fccf0aa6e5ebf2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoExecutors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05cbc00fead3aab4bc78f0e8cc74469e450ff985c8cadba3db384808fae17781(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoInitScripts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__310f1f473f9753944e6e04c4af062243ae850ef62bac42bf466103215f846362(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbbfe0f01efa30fdaf179559c934858b30b134ac22ee3e231541d6b2a3bdccce(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59723baccb3d1dfcad18093dbb8d9bd6a0746a22238695c8ba4b3c1efaccc667(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4367343ef7436ad3d6ddf1fa2c7754b40eb80e671062995aa565b41a89c5cf07(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09483fc6783cbb6e5992dec7011f7e92bb5716c1039900a46e251b40b17eef0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b15fa9ea543b7cd4e309389b88f67c98b87b1d40ea37ae5d8b8282b0358f8a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7434234e6f1bda86d8f65ca2ee26d28ebed6e0965517febc7b2940277798a198(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64272a38b946c47f84fe5313867f58850278ad98f38cb2713c446e594de2ec37(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__666b0de308e50fffdd84df5a2df90d9c1e68ba45545a5da5492d421c85c122f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ed07a0699bdc2bd8021149ee36d83f5f32e821c34ae49b96a2454f6d29ea13(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d5f43f9446948a5f74859746784a142955e4c9f9592eb2d878f6bbea16b2316(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a47a4c171939f992a05afb0e0bb6aa9b77323692e4516b5c5886eb46193826d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8626138e188822af894108765c4839364bf84bb40c54a312bf6d7437e601116(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74e10213ceb110c5210e4196c237c1907d35a0adf4bcbcf6664623dc41db4c97(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e82ccb0c92b2ce9002867a657fb39219621fe046d15fe273fadcbac20578b14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c53cb6398b6c33990a96d9e0130c70a2c456773d94989f8a275ad802defec244(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25467021e336701e11df5a1f0f6709328b0fadf4cb5ca60bbf5015a36d62ea04(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8231dcf50e77cf1ee446370cf6928a44541f88c697d93083b3a689ec8ec907f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a89e11b8be534b4b5895304b4dd4fe96ac534fcbc2a927e0b36618ffd4cf218(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b46e5794e77b1bbcec07c55c73897265149baaaabee7d7048394cf689171853(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__994b0113cc2fa911489f930406504359074bdae43b79ac4c0c29496b9455f46a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ead89abcdf59b03adf4dc779a3c799bd85570b05863989331228e18f7e55e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db9fed6955c4c1293eb883b568f70f0aac7521b8643fc0fbd44e11e80766e883(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a5964b2f9852a185cc73ab239b6a5533748228d79616c030552e41adb1d2b9d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3d92cd03a85dcb7426ce01271fe2f09641a6654688f34e060cd70f77142b31(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2c53088af566f99b77ed7f2dd3337a5e88233c60063334f71ee716ed3eb98d7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90f543155bdbd65346fc98df0cb083657cb39018d8c9e1792add9739377e0648(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2699b0367fcad350bcf6075d12344ae7871b99a3b821eab3770b085ec447e1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78d22a1303211a380039011beb0c35ac0674bd7d57c65f5dfb3395ecc2755937(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a854ee23e87c62eda14bf26ee1590d053d1092f6f42a27b2166893ece13f1854(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e2075cbefc297d76bdac99cc6fe03073d1a8d0333c3ed1603e03ceed3cfd23e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c10cb6cf47b99c23078bc0c5439a8c25ab24d0cdbd091f5f948723f318a267a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de71b6a68f36f3ef0532897aa74bbd6221489bfa57fb4b6cafaa8efe2a1626dc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfo]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db20201a5eb214e4657510411068f40edc3eaff70bc4f09280338ea07418c262(
    *,
    apply_policy_default_values: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    autoscale: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecAutoscale, typing.Dict[builtins.str, typing.Any]]] = None,
    autotermination_minutes: typing.Optional[jsii.Number] = None,
    aws_attributes: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecAwsAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
    azure_attributes: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_log_conf: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConf, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    custom_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    data_security_mode: typing.Optional[builtins.str] = None,
    docker_image: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImage, typing.Dict[builtins.str, typing.Any]]] = None,
    driver_instance_pool_id: typing.Optional[builtins.str] = None,
    driver_node_type_id: typing.Optional[builtins.str] = None,
    enable_elastic_disk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_local_disk_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcp_attributes: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecGcpAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
    init_scripts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecInitScripts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    instance_pool_id: typing.Optional[builtins.str] = None,
    node_type_id: typing.Optional[builtins.str] = None,
    num_workers: typing.Optional[jsii.Number] = None,
    policy_id: typing.Optional[builtins.str] = None,
    runtime_engine: typing.Optional[builtins.str] = None,
    single_user_name: typing.Optional[builtins.str] = None,
    spark_conf: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    spark_env_vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    spark_version: typing.Optional[builtins.str] = None,
    ssh_public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    workload_type: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadType, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3dce34e0f1a374930c166da3a2598697d61432db0283a358b40cb3b33ddc35d(
    *,
    max_workers: typing.Optional[jsii.Number] = None,
    min_workers: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__037b54cbc850d94dab621742c9f0aa6b08007d29a863f6fd3d6274e68670d867(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d25e51137f6f7a8b714856f2a0246c9e1bf58452fccfaa49a6cce2027ec07674(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56af967207ab53da9384f95815e195a24f4e7db62f262155bfab71de4d34a389(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30cb061b9372ee2962917cbf13dc4f2b2f86ed422fbaaf683b54968efccc823e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecAutoscale]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fabcd2dc5bb56ffac7fa9e7816081645ddec5d2b7c27fde171634e88534ed440(
    *,
    availability: typing.Optional[builtins.str] = None,
    ebs_volume_count: typing.Optional[jsii.Number] = None,
    ebs_volume_iops: typing.Optional[jsii.Number] = None,
    ebs_volume_size: typing.Optional[jsii.Number] = None,
    ebs_volume_throughput: typing.Optional[jsii.Number] = None,
    ebs_volume_type: typing.Optional[builtins.str] = None,
    first_on_demand: typing.Optional[jsii.Number] = None,
    instance_profile_arn: typing.Optional[builtins.str] = None,
    spot_bid_price_percent: typing.Optional[jsii.Number] = None,
    zone_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33fe19b79794e91d7d4a7524db935c77dc21336540947a87feb7bdd26439fc13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20fc6d4798b1319276c713456a5d70bc6ac1640b525b802aad23aa20ce37bf0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8129e655f0407d393db243fbed63e4c35ec2ce87ac5c717b555007ebb41a410f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad17a6943ba7f17e83e2e5cf7a705ec2a0404f0f70400bb479ec8a8ec03f728(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f57ae6b45c0c94ac56730f90f9ca1b9388e1f56c1c31d86bff09891e03260b4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f65045a9e5be0b46fc05a7bb64f4f20092dc382e0f018aa77aae4cc91b61474(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__334674cd04e22bf6b49b1ce1128e257a39c5400a953f51d2924ef8a08a6c13fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2935a11948adc3a11033a2bdd3aa65106a35e8f34270595f278e76fa9312cf69(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1af9a16396f544375018537bf78130b74562b18edab32f3b815b5427f42cda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e08c01fa01dab1d7d0082867ef8809c4226a42e7c64ed60ae52d54b4cbdb52(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c2d8e9747ecb8848d880f04c18cc7df40fc746a1ff3160367036641da41543e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7766f7603c61c73afff0ed991f2621f207e200fdff80221bd560ccb993b02d02(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecAwsAttributes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e28ae651fe851d1651b6712902927f06bad4ddcb1a499b4cf8c892a14e92e4d7(
    *,
    availability: typing.Optional[builtins.str] = None,
    first_on_demand: typing.Optional[jsii.Number] = None,
    log_analytics_info: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesLogAnalyticsInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    spot_bid_max_price: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74174c05ba93c4887792a99d203d3dc5bc3109fb28c6084caa895e6ac148c6f2(
    *,
    log_analytics_primary_key: typing.Optional[builtins.str] = None,
    log_analytics_workspace_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ce14dbed9ca3c6768cc7afeeea30b48e570f0127d1e23dc21b41f9c3e3cb9b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7afadd0b766e49a85d1d58c35db872805fd6d7eaa1898787b42fd65d2b6938da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f4607eb53dd96babff5f46e7edcfe5ec23222ec437b7573e3bedd2090268a85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57d1db3e33139a70d6c79c78cbb2abe12397e2f875092099f05dd9948224dcea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributesLogAnalyticsInfo]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d444c0c053a5ea7025c14ed0fbe7f82f512127d11df5848c05f236f6a0aa5deb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__857407d351c1b83da0cf097e6a579f9df0a948be7efb78cce022da398e695493(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__709779ed41e834999793f93b1e0dd072fbad0eb1f7724b7be27f2877d6e4ab04(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__916c296d94fee4a51104aeb4a24a7aa554eafd7bb645469e6eade920c5abb63a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16641524954fbcfbe98d01890b2d2833aa30c3429b9acda36d1426a8732745e7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecAzureAttributes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9398c0016cec098a6456319a427a4a3ce6df4001751c1bc48fa30b3681f46f36(
    *,
    dbfs: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfDbfs, typing.Dict[builtins.str, typing.Any]]] = None,
    s3: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfS3, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21ecb9491e599037e46f35983a68a07aaed5b582081c71af65bebe1c610f339a(
    *,
    destination: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c34de45a263831229d4c4ae31a6e5caa61d0ca8b73a6833f4de8050519d2420(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff0b08fc58a34f1ccb47d156dff4e1380f67954383a518a101aaf6521c57d9af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__082c9e7cdf3cadc5fe9025cb41e8ae16eee356c7d94fb62067c3b7bc84d3e16f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfDbfs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfec64213c181a7d822cee487f48ebf979cffa42cadcd35e76437a96940222fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10c34673b353e015d7be31b57e8c7b74c0a16b5c87403614279369dc4e1cec35(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConf]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e4c53055320b0ee563d3bf019d060b481a3786c3538c4954343e6a87fb1843a(
    *,
    destination: builtins.str,
    canned_acl: typing.Optional[builtins.str] = None,
    enable_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_type: typing.Optional[builtins.str] = None,
    endpoint: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b30230369dadec1a0041c2081faeb95f9ffdcf4ad3f19bbecef16302ff8257(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48081131b7181b3a7b23000b9f9dd1f6c0bb232ada17585f9a890ee2a281a7cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ccc9359f56f66462ac505c93345518c12883858b00212e40126467a9608e87e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6132a63c7fb79f45632176c55b17bd8f3c920bb3833099e0be2e6509f91477cb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81be120fb6bef5e74358e910c871d5dd6673c50105cc3c4ec24aaa4711746460(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0bfe0efd5078f005ab4c4f310056f9e1c2860a23630247907d2a338f69dc2f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b578cfaec5c68bc391db3936762f363b3bf851e1de924f7991839562149af2be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5384a8177792dbfe25203a570032c9b81345e2a275add3857da018b07d7efc3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9ae16a9af6c4caf04744e70e6062bf532fbe50d7118b1385af105bda4fdd45c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecClusterLogConfS3]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b94ff5751d88129dd2787b481ff670159fad3b803fb061477fba8358d6bf7723(
    *,
    basic_auth: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageBasicAuth, typing.Dict[builtins.str, typing.Any]]] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49c32318a52f41dcbad0a5b61e22ffd1b97eeba7dfa1432ee7d22bca36d21b82(
    *,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5983a1a4198044964b3bf1b2d13612611497a4ab6c0cc942150dda409da56943(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad2504f6ddb86e188ce430af33e7be4f0c1a8fb2979f7a5eb8502b68fb8cce20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__283ed7f1b37b97f1ce5e308a3f6fc3f6e12c899edae04dd35bb093f396956174(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00536c513e977c774e03d06faf80e92c5c1a63d0158ceca07bd92a0df6125a37(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImageBasicAuth]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a238b8e5ad4537cf52f1909dcea29b06f773e1e18f9412ee29d0020f3a2c12c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca10577bef89251c8cb7c8751936960e3538a73663ec98c1fbecd99fc7994694(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d408203b92dfc1a390db58ac5674a25715193203f5f40879e1d470042448736e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecDockerImage]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea47501e2027f605aaf68ee194ce245d8efb1e7f5bf9989ecff2caa200b5d36d(
    *,
    availability: typing.Optional[builtins.str] = None,
    boot_disk_size: typing.Optional[jsii.Number] = None,
    google_service_account: typing.Optional[builtins.str] = None,
    local_ssd_count: typing.Optional[jsii.Number] = None,
    use_preemptible_executors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    zone_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd032a517f6752d39ff662f6b7ee9db1ec737d440dcd4c25e8868a4cd28f4868(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a65ed1a6e5a17bdceddf8930f52824884b0f39252b3085567d9f8f22eb99f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33121aa90f3a95aed8b0a7117957403211d9a023750fa6db22602146eaf7bb11(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ec50644b2f6a0221ecf3ef05a162a9c79bcc534307ec83b636c09e151a874bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b58c0f24e36d08058e370e4c603d01f137cb1966f2e48bd6c6cfaca71b3129ac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9ccb09662637fb5d761accd1c6b40489f1deb78fb1e46cb48d7846f29500d06(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3b7fbed91266578a5919d4e3a7a952849147b1ef160e126991fb687c8835652(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ff7994d078080082bfc362e39d2041eea0d79b1b326301db7234195896afd0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecGcpAttributes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baca042086b02a841c794eca79b4fa029e83564b8ceeb3e12aa09f4f0c0794f9(
    *,
    abfss: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsAbfss, typing.Dict[builtins.str, typing.Any]]] = None,
    dbfs: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsDbfs, typing.Dict[builtins.str, typing.Any]]] = None,
    file: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsFile, typing.Dict[builtins.str, typing.Any]]] = None,
    gcs: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    s3: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsS3, typing.Dict[builtins.str, typing.Any]]] = None,
    volumes: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsVolumes, typing.Dict[builtins.str, typing.Any]]] = None,
    workspace: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsWorkspace, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90c01b98fbdc9fa305eb2b374abc28134268b6cb1db3f3df6b4132dbe93c0be5(
    *,
    destination: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3fabfebce9c073506edfe1cdd44f299f649aa9c6b17fc0c8939946f7a067f50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c297d7fc2f3f059929863799ce902caada00bbd52eba4299b2c56dce08a909e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a92e4a555d99662c79bc626c196baa14ed8a28b28272074461258bed075302b8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsAbfss]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c78f964223c25bd64858cf2bcdbfb631bd0235d0a682bd12c760183f0e600ad4(
    *,
    destination: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4605813d5b00894414785f1e8bd5cbc56f8b6c0c56a208e7fedbfcf526444f1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f80abf94a93dd1f97fb7a1da76cf3684003b2fab223035c3b37843dc20d3b4cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e5c77fffc2ef2222f5c3693080584b79f610e30f7bf540873008c6c1c7cad9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsDbfs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__475ff1e254c68313d4029f29d8ee0b4a3017a696ecfc49e7fb173600ada14c45(
    *,
    destination: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19a4ae2834fbf0cdad7bf3bb7f903e67b1cfcd2a56ef834b37aed3cc7c362acf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc29aa4ae6c646bf981b0a863cc737eb582ddd1cde8cef3a196573351437ab5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef5662bfe362d2f01a6d2b573172678134c91c8819e3319ccba4a65a25369053(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsFile]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42e0cf48685956c79ef30499491b4689caa7cd58d8370131abcc9c163acd5326(
    *,
    destination: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6846041c1bc0e45e00b01a98baa9083ba15f1da50e12143fe1f48f983c20782e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2de6e2bd95280166cf0e13347c5d105a13bda8993261cc8c7a0eb299893dc0e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9554d02c16ebc9063975bc4e3f73a93e0f209a448614d4f6f7402ddf29b2a21(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsGcs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f912899134fed3fcc158fe60169bd0ac0d5b9ac0ec88450ef964a40b8677d7dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb2d6244856889f82d5ceb78c750ec63f197d23fd0cec0594fa14fba7f1f1b8f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0e7f0c5adc4ffe45e998ab25fe490a9a6ee121a39c678cff120aaa58ab4ba7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc2354a434fd7152cea25312339202b92b688b823a8815c424e1b77d91606be(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb37e3cc56e62c979ae6249298cb5e8440179afcf45c896b912ff29d3c1994d6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b42ee9187fc038fcfece35e1f2f844e65f9ca688665bf200727f857b3239df59(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataDatabricksClusterPluginframeworkClusterInfoSpecInitScripts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b0c182fcff2251cfc237336a6fc2a8f3bbe2297e63e244e68af5b402b74bcc5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb5611c34420b5b9f7ec4521f0e4edd4e6141b1b5e37f0a435544f298488469(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScripts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb2c071d67c60af8fd036a88a029eb1f648b23d9bd694642acfd7c4dd428617(
    *,
    destination: builtins.str,
    canned_acl: typing.Optional[builtins.str] = None,
    enable_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_type: typing.Optional[builtins.str] = None,
    endpoint: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4edc13e3aa3adc1f61320463e547d1c106658c1ca63a67b4c1df53b1ddbf02a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09f88cb6067fa1c65fffae0d38dbb2538e5e10d46f6c3a183e8f122122a86e54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b995db290d90afe8f0f3c28bf258ce5d41c2bb8f329c9ccdab98909c4e911c91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41238c5be7d78f31435d9fe51fb27706669eb9e025089acd13ab39bd1da027ea(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a839623d08decdb9118cb6f4e9211facb9f6e8ec504687b4dffc05efd5c417c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5bd5f5abdee109559c461730e2adb2420ae0b41662273d85eef7c0fd5f16c00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6209c73d803f6bc1341d5cde27f87aedbd3d87ae22d64c039c597bc12abf9ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22cd9eb283e79e390d277d3116ad406cdc3df621e061026852927fc24548a8d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b0a20538d58e619c876fe15ec0cd40f28db57fe749d4a2fa2bfddf1b28a39a0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsS3]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bcc0e162b7dfa2df41fc8054ba5fce67737f1e092935668a986edac851b24b0(
    *,
    destination: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdfad2f83996555ea64d8bbe965e515fbdfe62e1ebd30d8aca5ef475bf3339fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5671f50edc74c068abf6a1302c8c691db0ea52f099abccd0a5a81eb6dcd3479f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22125d9473c3db59fc4a8171647268dc77201909210567bdf2a74bc914a227f2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsVolumes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__961c53888ff137f5e77233e22f021cb219e770028266581876a882d7f3399dfa(
    *,
    destination: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27cafb156627fcd72ed7b58d8a68379860cae30c2cca2aaac8ae08cde5c6b245(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a98e2c2431f0e143281286e46b9daa0a07df02d0987dd392b0eb260a3f1f80b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__726caf50679267ef1be4d028d5e51eb8d271120dc8d5bb2cbdbf163f5ef011d6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecInitScriptsWorkspace]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__501102455f95620d0084520e687bdf14b36596a7be99b9977881223dabf63f64(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9bae80cc0789a6c6cd5c620d346ab23efed8bb627eaafffe897cbe5810b4b7f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecInitScripts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea942f6e7dff05eb71ddcae48ab3f57859fa594b927f41583076c0c604c0708(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a3ed779334b68316e58b2200df7bdd794c52ee0f4e9370c2e6431497a6b8b0b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5367b8142419b7e10a4a1d5b592e9b414215f04f083fae646f3fb2b1651f02e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6be79202ae8e212ac55ed867f7ba4ea854f1ba05c413d1b5aaf564821604e6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96eefd840d2ecc6d04bb9d4006a3a8cb919b9d77e0f4f426bc627ea30c26c061(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d28c4afc96c7054c598a4567d85f99f061dab9e0d7ca4479d15e90f9b35de07f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__384efcabb1ef45a825b5d559c411eb6536b6386452e5763054425545e32176c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69ed8220899823ea456f694cf483818b68598e2de4fb49fc85b52570fa2b32ce(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fef4fc9dac036608a164d489f707ae9ccd84dd747c97caf33c04fcf042e1a99b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__170de453a59253837449ea685e4403b23b2c0d7ade0cf74f8db5e554e8f707c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b91302e0d391e0ecfbd330c3cce2082d523c2b23edd0ab65075915f952f2918(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3756fef17e2d7e24ca664fbf12bacc96b4d99c8a8b02561413930c40d3b3591e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a31e10197843c6c2ce7e6c7cd8bc47884aa5fe3afaa68e872f658aa6b16c29d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d64b0dc40bc072f8947c9ebd1531529c95403e74c762ba22e8cd82ee08c2643(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa6d91cce342e6b43425910b0a079407710fd3ac42fa0158a6118b1da34a3fa6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d93efaf5e9f19a7e397e0a6d7cd736b5410e58aaea69c015cfa0431ecb6156f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__637a5538c7225b70e3b4517797ea675a8dcc6bc1032b6fe87082ae41534b1c59(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bb4b956f53710063be2c93a596535ba88389d4cf22f6847ca63dc8eecc65bd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de4bf9e66b324c7a53cbd1fa2a6c5c28ef670510b27637b53a46bec5f6d7fb10(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13811e02216a0d6b935ef078c89d09cb328fcd738f045f4cf2bed701ccd969f5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpec]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b7812dc08116bf00cd618d9ef78537742ff28e968060a008b590356a370a0d(
    *,
    clients: typing.Union[DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeClients, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa44f95bb795714b946eaf95df7860663e0e13689073f7290e804f48c6df72b0(
    *,
    jobs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    notebooks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__831cc81d47f8970529e9a5e1be953ea63dba13180cad6a9e01b3d04fda108274(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3889e55e3f4e76639a2c69092fb150d0f7e220b8ccaad978a1db75f2cd5785b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe95479d227b895f23fea9935c52bcdbf1f3ff240f55b8c25d3bc2d2b9679d5e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25cb7ccbd24f2dbc82288964294a36c5a0f37bb5ffc4de7f84603f290151a079(
    value: typing.Optional[DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadTypeClients],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cf463d2c852ebc6b0301818a0dc28fb4731130d5e82cec13f5f28eed1598ae0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__358f3ca3aea587ce182a1c669452449dc3a0ae1cd42364d3d7882cb2696d7fc1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoSpecWorkloadType]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c641f134117317598001465ea80d24f55cfae4aeb879e81082f9ec1954a069a0(
    *,
    code: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__691238dcbfa9756a9b787f1d43193c5fca61690b4aac6bcfc8f3d51b98b9473b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10960a3bb0fdf9e1adf97ce8512e5dd8f98bd04d58ddd26163dddb490110bb2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c9ea0734e811b8aa7b9d88b4e6bf081b920d7443824ae94cd1c954a795dccb6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f0bd96c652360f21d2e8a031af47f77177aaec06eb2feb83975d8152db67128(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__557d67a1c1aaee93d2d9314a76e28f4b12f90c6e82a42f6639140aa3415a57ba(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoTerminationReason]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98fdee78259b2fe42d26b1bf085bcb7b4ca181e7991bcbac8220ea2e8285b49e(
    *,
    clients: typing.Union[DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeClients, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d41135970e4598ed428b97979b7e65c6868b9c17f07d5241882977ba0fd1840(
    *,
    jobs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    notebooks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d4261b1db0060db04b029cd1e874bd615a7bdd87164ca0a01dc5918fc02d24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864f611252ba965037c3c5395deb3ee28d7b6f0e705a017bc4b84674168d4595(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6af103f9d85312178c6a0ab512f2458e085f16d97df76deb9700b7ab9027f31(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eed678efe00d380710b37993a14085e965836619371022682800cd476e8df9d(
    value: typing.Optional[DataDatabricksClusterPluginframeworkClusterInfoWorkloadTypeClients],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07a1ef093f582e96eabec1031b9da96d175f2954e0a0cd9207fa431399c14a41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__913a884cdecf9e57fab27106d48c704b38dc3337fca1db35298db7dfeb7b958c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataDatabricksClusterPluginframeworkClusterInfoWorkloadType]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebd962bd6567e2d6784b6e7f34d4438ced4e7abe32770cad2e73697338fbe37a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_id: typing.Optional[builtins.str] = None,
    cluster_info: typing.Optional[typing.Union[DataDatabricksClusterPluginframeworkClusterInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
