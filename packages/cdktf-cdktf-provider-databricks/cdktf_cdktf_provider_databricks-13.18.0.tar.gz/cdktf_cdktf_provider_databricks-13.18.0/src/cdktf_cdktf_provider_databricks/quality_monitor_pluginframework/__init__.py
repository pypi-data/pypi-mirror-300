r'''
# `databricks_quality_monitor_pluginframework`

Refer to the Terraform Registry for docs: [`databricks_quality_monitor_pluginframework`](https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework).
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


class QualityMonitorPluginframework(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.qualityMonitorPluginframework.QualityMonitorPluginframework",
):
    '''Represents a {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework databricks_quality_monitor_pluginframework}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        assets_dir: builtins.str,
        output_schema_name: builtins.str,
        table_name: builtins.str,
        baseline_table_name: typing.Optional[builtins.str] = None,
        custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QualityMonitorPluginframeworkCustomMetrics", typing.Dict[builtins.str, typing.Any]]]]] = None,
        data_classification_config: typing.Optional[typing.Union["QualityMonitorPluginframeworkDataClassificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        inference_log: typing.Optional[typing.Union["QualityMonitorPluginframeworkInferenceLog", typing.Dict[builtins.str, typing.Any]]] = None,
        latest_monitor_failure_msg: typing.Optional[builtins.str] = None,
        notifications: typing.Optional[typing.Union["QualityMonitorPluginframeworkNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
        schedule: typing.Optional[typing.Union["QualityMonitorPluginframeworkSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        skip_builtin_dashboard: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        slicing_exprs: typing.Optional[typing.Sequence[builtins.str]] = None,
        snapshot: typing.Optional[typing.Union["QualityMonitorPluginframeworkSnapshot", typing.Dict[builtins.str, typing.Any]]] = None,
        time_series: typing.Optional[typing.Union["QualityMonitorPluginframeworkTimeSeries", typing.Dict[builtins.str, typing.Any]]] = None,
        warehouse_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework databricks_quality_monitor_pluginframework} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param assets_dir: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#assets_dir QualityMonitorPluginframework#assets_dir}.
        :param output_schema_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#output_schema_name QualityMonitorPluginframework#output_schema_name}.
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#table_name QualityMonitorPluginframework#table_name}.
        :param baseline_table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#baseline_table_name QualityMonitorPluginframework#baseline_table_name}.
        :param custom_metrics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#custom_metrics QualityMonitorPluginframework#custom_metrics}.
        :param data_classification_config: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#data_classification_config QualityMonitorPluginframework#data_classification_config}.
        :param inference_log: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#inference_log QualityMonitorPluginframework#inference_log}.
        :param latest_monitor_failure_msg: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#latest_monitor_failure_msg QualityMonitorPluginframework#latest_monitor_failure_msg}.
        :param notifications: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#notifications QualityMonitorPluginframework#notifications}.
        :param schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#schedule QualityMonitorPluginframework#schedule}.
        :param skip_builtin_dashboard: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#skip_builtin_dashboard QualityMonitorPluginframework#skip_builtin_dashboard}.
        :param slicing_exprs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#slicing_exprs QualityMonitorPluginframework#slicing_exprs}.
        :param snapshot: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#snapshot QualityMonitorPluginframework#snapshot}.
        :param time_series: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#time_series QualityMonitorPluginframework#time_series}.
        :param warehouse_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#warehouse_id QualityMonitorPluginframework#warehouse_id}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3289d7d5dd8d92207a6f0e7f8bbf30a54d841c2d53d29f1eef22fc9282cbf7e6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = QualityMonitorPluginframeworkConfig(
            assets_dir=assets_dir,
            output_schema_name=output_schema_name,
            table_name=table_name,
            baseline_table_name=baseline_table_name,
            custom_metrics=custom_metrics,
            data_classification_config=data_classification_config,
            inference_log=inference_log,
            latest_monitor_failure_msg=latest_monitor_failure_msg,
            notifications=notifications,
            schedule=schedule,
            skip_builtin_dashboard=skip_builtin_dashboard,
            slicing_exprs=slicing_exprs,
            snapshot=snapshot,
            time_series=time_series,
            warehouse_id=warehouse_id,
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
        '''Generates CDKTF code for importing a QualityMonitorPluginframework resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the QualityMonitorPluginframework to import.
        :param import_from_id: The id of the existing QualityMonitorPluginframework that should be imported. Refer to the {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the QualityMonitorPluginframework to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1b139cc985976b94b035828ffc3fa89922e8e7a6b55d3915e4f7ac547e4aa99)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCustomMetrics")
    def put_custom_metrics(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QualityMonitorPluginframeworkCustomMetrics", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__489c441c51fffb0c838b63b568f63afa3ce9c2f82846dba1de8307feefc7dab0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomMetrics", [value]))

    @jsii.member(jsii_name="putDataClassificationConfig")
    def put_data_classification_config(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#enabled QualityMonitorPluginframework#enabled}.
        '''
        value = QualityMonitorPluginframeworkDataClassificationConfig(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putDataClassificationConfig", [value]))

    @jsii.member(jsii_name="putInferenceLog")
    def put_inference_log(
        self,
        *,
        granularities: typing.Sequence[builtins.str],
        model_id_col: builtins.str,
        prediction_col: builtins.str,
        problem_type: builtins.str,
        timestamp_col: builtins.str,
        label_col: typing.Optional[builtins.str] = None,
        prediction_proba_col: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param granularities: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#granularities QualityMonitorPluginframework#granularities}.
        :param model_id_col: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#model_id_col QualityMonitorPluginframework#model_id_col}.
        :param prediction_col: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#prediction_col QualityMonitorPluginframework#prediction_col}.
        :param problem_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#problem_type QualityMonitorPluginframework#problem_type}.
        :param timestamp_col: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#timestamp_col QualityMonitorPluginframework#timestamp_col}.
        :param label_col: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#label_col QualityMonitorPluginframework#label_col}.
        :param prediction_proba_col: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#prediction_proba_col QualityMonitorPluginframework#prediction_proba_col}.
        '''
        value = QualityMonitorPluginframeworkInferenceLog(
            granularities=granularities,
            model_id_col=model_id_col,
            prediction_col=prediction_col,
            problem_type=problem_type,
            timestamp_col=timestamp_col,
            label_col=label_col,
            prediction_proba_col=prediction_proba_col,
        )

        return typing.cast(None, jsii.invoke(self, "putInferenceLog", [value]))

    @jsii.member(jsii_name="putNotifications")
    def put_notifications(
        self,
        *,
        on_failure: typing.Optional[typing.Union["QualityMonitorPluginframeworkNotificationsOnFailure", typing.Dict[builtins.str, typing.Any]]] = None,
        on_new_classification_tag_detected: typing.Optional[typing.Union["QualityMonitorPluginframeworkNotificationsOnNewClassificationTagDetected", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param on_failure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#on_failure QualityMonitorPluginframework#on_failure}.
        :param on_new_classification_tag_detected: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#on_new_classification_tag_detected QualityMonitorPluginframework#on_new_classification_tag_detected}.
        '''
        value = QualityMonitorPluginframeworkNotifications(
            on_failure=on_failure,
            on_new_classification_tag_detected=on_new_classification_tag_detected,
        )

        return typing.cast(None, jsii.invoke(self, "putNotifications", [value]))

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        *,
        quartz_cron_expression: builtins.str,
        timezone_id: builtins.str,
    ) -> None:
        '''
        :param quartz_cron_expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#quartz_cron_expression QualityMonitorPluginframework#quartz_cron_expression}.
        :param timezone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#timezone_id QualityMonitorPluginframework#timezone_id}.
        '''
        value = QualityMonitorPluginframeworkSchedule(
            quartz_cron_expression=quartz_cron_expression, timezone_id=timezone_id
        )

        return typing.cast(None, jsii.invoke(self, "putSchedule", [value]))

    @jsii.member(jsii_name="putSnapshot")
    def put_snapshot(self) -> None:
        value = QualityMonitorPluginframeworkSnapshot()

        return typing.cast(None, jsii.invoke(self, "putSnapshot", [value]))

    @jsii.member(jsii_name="putTimeSeries")
    def put_time_series(
        self,
        *,
        granularities: typing.Sequence[builtins.str],
        timestamp_col: builtins.str,
    ) -> None:
        '''
        :param granularities: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#granularities QualityMonitorPluginframework#granularities}.
        :param timestamp_col: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#timestamp_col QualityMonitorPluginframework#timestamp_col}.
        '''
        value = QualityMonitorPluginframeworkTimeSeries(
            granularities=granularities, timestamp_col=timestamp_col
        )

        return typing.cast(None, jsii.invoke(self, "putTimeSeries", [value]))

    @jsii.member(jsii_name="resetBaselineTableName")
    def reset_baseline_table_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBaselineTableName", []))

    @jsii.member(jsii_name="resetCustomMetrics")
    def reset_custom_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomMetrics", []))

    @jsii.member(jsii_name="resetDataClassificationConfig")
    def reset_data_classification_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataClassificationConfig", []))

    @jsii.member(jsii_name="resetInferenceLog")
    def reset_inference_log(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInferenceLog", []))

    @jsii.member(jsii_name="resetLatestMonitorFailureMsg")
    def reset_latest_monitor_failure_msg(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLatestMonitorFailureMsg", []))

    @jsii.member(jsii_name="resetNotifications")
    def reset_notifications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotifications", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @jsii.member(jsii_name="resetSkipBuiltinDashboard")
    def reset_skip_builtin_dashboard(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipBuiltinDashboard", []))

    @jsii.member(jsii_name="resetSlicingExprs")
    def reset_slicing_exprs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSlicingExprs", []))

    @jsii.member(jsii_name="resetSnapshot")
    def reset_snapshot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshot", []))

    @jsii.member(jsii_name="resetTimeSeries")
    def reset_time_series(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeSeries", []))

    @jsii.member(jsii_name="resetWarehouseId")
    def reset_warehouse_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWarehouseId", []))

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
    @jsii.member(jsii_name="customMetrics")
    def custom_metrics(self) -> "QualityMonitorPluginframeworkCustomMetricsList":
        return typing.cast("QualityMonitorPluginframeworkCustomMetricsList", jsii.get(self, "customMetrics"))

    @builtins.property
    @jsii.member(jsii_name="dashboardId")
    def dashboard_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dashboardId"))

    @builtins.property
    @jsii.member(jsii_name="dataClassificationConfig")
    def data_classification_config(
        self,
    ) -> "QualityMonitorPluginframeworkDataClassificationConfigOutputReference":
        return typing.cast("QualityMonitorPluginframeworkDataClassificationConfigOutputReference", jsii.get(self, "dataClassificationConfig"))

    @builtins.property
    @jsii.member(jsii_name="driftMetricsTableName")
    def drift_metrics_table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "driftMetricsTableName"))

    @builtins.property
    @jsii.member(jsii_name="inferenceLog")
    def inference_log(
        self,
    ) -> "QualityMonitorPluginframeworkInferenceLogOutputReference":
        return typing.cast("QualityMonitorPluginframeworkInferenceLogOutputReference", jsii.get(self, "inferenceLog"))

    @builtins.property
    @jsii.member(jsii_name="monitorVersion")
    def monitor_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "monitorVersion"))

    @builtins.property
    @jsii.member(jsii_name="notifications")
    def notifications(
        self,
    ) -> "QualityMonitorPluginframeworkNotificationsOutputReference":
        return typing.cast("QualityMonitorPluginframeworkNotificationsOutputReference", jsii.get(self, "notifications"))

    @builtins.property
    @jsii.member(jsii_name="profileMetricsTableName")
    def profile_metrics_table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "profileMetricsTableName"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> "QualityMonitorPluginframeworkScheduleOutputReference":
        return typing.cast("QualityMonitorPluginframeworkScheduleOutputReference", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="snapshot")
    def snapshot(self) -> "QualityMonitorPluginframeworkSnapshotOutputReference":
        return typing.cast("QualityMonitorPluginframeworkSnapshotOutputReference", jsii.get(self, "snapshot"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeSeries")
    def time_series(self) -> "QualityMonitorPluginframeworkTimeSeriesOutputReference":
        return typing.cast("QualityMonitorPluginframeworkTimeSeriesOutputReference", jsii.get(self, "timeSeries"))

    @builtins.property
    @jsii.member(jsii_name="assetsDirInput")
    def assets_dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assetsDirInput"))

    @builtins.property
    @jsii.member(jsii_name="baselineTableNameInput")
    def baseline_table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baselineTableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="customMetricsInput")
    def custom_metrics_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QualityMonitorPluginframeworkCustomMetrics"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QualityMonitorPluginframeworkCustomMetrics"]]], jsii.get(self, "customMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataClassificationConfigInput")
    def data_classification_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "QualityMonitorPluginframeworkDataClassificationConfig"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "QualityMonitorPluginframeworkDataClassificationConfig"]], jsii.get(self, "dataClassificationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="inferenceLogInput")
    def inference_log_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "QualityMonitorPluginframeworkInferenceLog"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "QualityMonitorPluginframeworkInferenceLog"]], jsii.get(self, "inferenceLogInput"))

    @builtins.property
    @jsii.member(jsii_name="latestMonitorFailureMsgInput")
    def latest_monitor_failure_msg_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "latestMonitorFailureMsgInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationsInput")
    def notifications_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "QualityMonitorPluginframeworkNotifications"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "QualityMonitorPluginframeworkNotifications"]], jsii.get(self, "notificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="outputSchemaNameInput")
    def output_schema_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputSchemaNameInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "QualityMonitorPluginframeworkSchedule"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "QualityMonitorPluginframeworkSchedule"]], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="skipBuiltinDashboardInput")
    def skip_builtin_dashboard_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipBuiltinDashboardInput"))

    @builtins.property
    @jsii.member(jsii_name="slicingExprsInput")
    def slicing_exprs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "slicingExprsInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotInput")
    def snapshot_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "QualityMonitorPluginframeworkSnapshot"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "QualityMonitorPluginframeworkSnapshot"]], jsii.get(self, "snapshotInput"))

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeSeriesInput")
    def time_series_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "QualityMonitorPluginframeworkTimeSeries"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "QualityMonitorPluginframeworkTimeSeries"]], jsii.get(self, "timeSeriesInput"))

    @builtins.property
    @jsii.member(jsii_name="warehouseIdInput")
    def warehouse_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "warehouseIdInput"))

    @builtins.property
    @jsii.member(jsii_name="assetsDir")
    def assets_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "assetsDir"))

    @assets_dir.setter
    def assets_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed534d050fb6423e788ce018773e255be237b456b9197428ea588d6c00404259)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetsDir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="baselineTableName")
    def baseline_table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baselineTableName"))

    @baseline_table_name.setter
    def baseline_table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f9f500c61f04d8bce195f7fd905dfd5a0bb1be0582dde768b8b9aaacf79bd9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baselineTableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="latestMonitorFailureMsg")
    def latest_monitor_failure_msg(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "latestMonitorFailureMsg"))

    @latest_monitor_failure_msg.setter
    def latest_monitor_failure_msg(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bdf8cda7aa28829dd8814fafdbec70c46c78fa87f160173caa8d67b42a29963)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "latestMonitorFailureMsg", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputSchemaName")
    def output_schema_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputSchemaName"))

    @output_schema_name.setter
    def output_schema_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c401256871bc17f4fd2fbd4feb1417a4d1dbde29f634d791d4430ca4c6e53a5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputSchemaName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipBuiltinDashboard")
    def skip_builtin_dashboard(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipBuiltinDashboard"))

    @skip_builtin_dashboard.setter
    def skip_builtin_dashboard(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f53d2576f33c0fbf67b56ed2c4dce1ca6bc4fa97ebddf33a551f175838128449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipBuiltinDashboard", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="slicingExprs")
    def slicing_exprs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "slicingExprs"))

    @slicing_exprs.setter
    def slicing_exprs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e23a97fe4e66ff938a85539c4878675f44c72e738870423d8302dd1b2a8dde6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "slicingExprs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd7c8b013c3e0b9a43fb0f4e521d9e2979ca6e8dfbc96738cf8cfd7604f0543b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="warehouseId")
    def warehouse_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "warehouseId"))

    @warehouse_id.setter
    def warehouse_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14796fa283a9f5734af501cbd2d0f5d620f1c76ba400cc26bfd54c1309113367)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "warehouseId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.qualityMonitorPluginframework.QualityMonitorPluginframeworkConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "assets_dir": "assetsDir",
        "output_schema_name": "outputSchemaName",
        "table_name": "tableName",
        "baseline_table_name": "baselineTableName",
        "custom_metrics": "customMetrics",
        "data_classification_config": "dataClassificationConfig",
        "inference_log": "inferenceLog",
        "latest_monitor_failure_msg": "latestMonitorFailureMsg",
        "notifications": "notifications",
        "schedule": "schedule",
        "skip_builtin_dashboard": "skipBuiltinDashboard",
        "slicing_exprs": "slicingExprs",
        "snapshot": "snapshot",
        "time_series": "timeSeries",
        "warehouse_id": "warehouseId",
    },
)
class QualityMonitorPluginframeworkConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        assets_dir: builtins.str,
        output_schema_name: builtins.str,
        table_name: builtins.str,
        baseline_table_name: typing.Optional[builtins.str] = None,
        custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QualityMonitorPluginframeworkCustomMetrics", typing.Dict[builtins.str, typing.Any]]]]] = None,
        data_classification_config: typing.Optional[typing.Union["QualityMonitorPluginframeworkDataClassificationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        inference_log: typing.Optional[typing.Union["QualityMonitorPluginframeworkInferenceLog", typing.Dict[builtins.str, typing.Any]]] = None,
        latest_monitor_failure_msg: typing.Optional[builtins.str] = None,
        notifications: typing.Optional[typing.Union["QualityMonitorPluginframeworkNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
        schedule: typing.Optional[typing.Union["QualityMonitorPluginframeworkSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        skip_builtin_dashboard: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        slicing_exprs: typing.Optional[typing.Sequence[builtins.str]] = None,
        snapshot: typing.Optional[typing.Union["QualityMonitorPluginframeworkSnapshot", typing.Dict[builtins.str, typing.Any]]] = None,
        time_series: typing.Optional[typing.Union["QualityMonitorPluginframeworkTimeSeries", typing.Dict[builtins.str, typing.Any]]] = None,
        warehouse_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param assets_dir: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#assets_dir QualityMonitorPluginframework#assets_dir}.
        :param output_schema_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#output_schema_name QualityMonitorPluginframework#output_schema_name}.
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#table_name QualityMonitorPluginframework#table_name}.
        :param baseline_table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#baseline_table_name QualityMonitorPluginframework#baseline_table_name}.
        :param custom_metrics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#custom_metrics QualityMonitorPluginframework#custom_metrics}.
        :param data_classification_config: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#data_classification_config QualityMonitorPluginframework#data_classification_config}.
        :param inference_log: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#inference_log QualityMonitorPluginframework#inference_log}.
        :param latest_monitor_failure_msg: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#latest_monitor_failure_msg QualityMonitorPluginframework#latest_monitor_failure_msg}.
        :param notifications: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#notifications QualityMonitorPluginframework#notifications}.
        :param schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#schedule QualityMonitorPluginframework#schedule}.
        :param skip_builtin_dashboard: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#skip_builtin_dashboard QualityMonitorPluginframework#skip_builtin_dashboard}.
        :param slicing_exprs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#slicing_exprs QualityMonitorPluginframework#slicing_exprs}.
        :param snapshot: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#snapshot QualityMonitorPluginframework#snapshot}.
        :param time_series: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#time_series QualityMonitorPluginframework#time_series}.
        :param warehouse_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#warehouse_id QualityMonitorPluginframework#warehouse_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(data_classification_config, dict):
            data_classification_config = QualityMonitorPluginframeworkDataClassificationConfig(**data_classification_config)
        if isinstance(inference_log, dict):
            inference_log = QualityMonitorPluginframeworkInferenceLog(**inference_log)
        if isinstance(notifications, dict):
            notifications = QualityMonitorPluginframeworkNotifications(**notifications)
        if isinstance(schedule, dict):
            schedule = QualityMonitorPluginframeworkSchedule(**schedule)
        if isinstance(snapshot, dict):
            snapshot = QualityMonitorPluginframeworkSnapshot(**snapshot)
        if isinstance(time_series, dict):
            time_series = QualityMonitorPluginframeworkTimeSeries(**time_series)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__887a63f681d6ce3c9facef2f4ff1011377c454e76ba7548445c90b5ff63fccb5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument assets_dir", value=assets_dir, expected_type=type_hints["assets_dir"])
            check_type(argname="argument output_schema_name", value=output_schema_name, expected_type=type_hints["output_schema_name"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument baseline_table_name", value=baseline_table_name, expected_type=type_hints["baseline_table_name"])
            check_type(argname="argument custom_metrics", value=custom_metrics, expected_type=type_hints["custom_metrics"])
            check_type(argname="argument data_classification_config", value=data_classification_config, expected_type=type_hints["data_classification_config"])
            check_type(argname="argument inference_log", value=inference_log, expected_type=type_hints["inference_log"])
            check_type(argname="argument latest_monitor_failure_msg", value=latest_monitor_failure_msg, expected_type=type_hints["latest_monitor_failure_msg"])
            check_type(argname="argument notifications", value=notifications, expected_type=type_hints["notifications"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument skip_builtin_dashboard", value=skip_builtin_dashboard, expected_type=type_hints["skip_builtin_dashboard"])
            check_type(argname="argument slicing_exprs", value=slicing_exprs, expected_type=type_hints["slicing_exprs"])
            check_type(argname="argument snapshot", value=snapshot, expected_type=type_hints["snapshot"])
            check_type(argname="argument time_series", value=time_series, expected_type=type_hints["time_series"])
            check_type(argname="argument warehouse_id", value=warehouse_id, expected_type=type_hints["warehouse_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "assets_dir": assets_dir,
            "output_schema_name": output_schema_name,
            "table_name": table_name,
        }
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
        if baseline_table_name is not None:
            self._values["baseline_table_name"] = baseline_table_name
        if custom_metrics is not None:
            self._values["custom_metrics"] = custom_metrics
        if data_classification_config is not None:
            self._values["data_classification_config"] = data_classification_config
        if inference_log is not None:
            self._values["inference_log"] = inference_log
        if latest_monitor_failure_msg is not None:
            self._values["latest_monitor_failure_msg"] = latest_monitor_failure_msg
        if notifications is not None:
            self._values["notifications"] = notifications
        if schedule is not None:
            self._values["schedule"] = schedule
        if skip_builtin_dashboard is not None:
            self._values["skip_builtin_dashboard"] = skip_builtin_dashboard
        if slicing_exprs is not None:
            self._values["slicing_exprs"] = slicing_exprs
        if snapshot is not None:
            self._values["snapshot"] = snapshot
        if time_series is not None:
            self._values["time_series"] = time_series
        if warehouse_id is not None:
            self._values["warehouse_id"] = warehouse_id

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
    def assets_dir(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#assets_dir QualityMonitorPluginframework#assets_dir}.'''
        result = self._values.get("assets_dir")
        assert result is not None, "Required property 'assets_dir' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def output_schema_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#output_schema_name QualityMonitorPluginframework#output_schema_name}.'''
        result = self._values.get("output_schema_name")
        assert result is not None, "Required property 'output_schema_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#table_name QualityMonitorPluginframework#table_name}.'''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def baseline_table_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#baseline_table_name QualityMonitorPluginframework#baseline_table_name}.'''
        result = self._values.get("baseline_table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_metrics(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QualityMonitorPluginframeworkCustomMetrics"]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#custom_metrics QualityMonitorPluginframework#custom_metrics}.'''
        result = self._values.get("custom_metrics")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QualityMonitorPluginframeworkCustomMetrics"]]], result)

    @builtins.property
    def data_classification_config(
        self,
    ) -> typing.Optional["QualityMonitorPluginframeworkDataClassificationConfig"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#data_classification_config QualityMonitorPluginframework#data_classification_config}.'''
        result = self._values.get("data_classification_config")
        return typing.cast(typing.Optional["QualityMonitorPluginframeworkDataClassificationConfig"], result)

    @builtins.property
    def inference_log(
        self,
    ) -> typing.Optional["QualityMonitorPluginframeworkInferenceLog"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#inference_log QualityMonitorPluginframework#inference_log}.'''
        result = self._values.get("inference_log")
        return typing.cast(typing.Optional["QualityMonitorPluginframeworkInferenceLog"], result)

    @builtins.property
    def latest_monitor_failure_msg(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#latest_monitor_failure_msg QualityMonitorPluginframework#latest_monitor_failure_msg}.'''
        result = self._values.get("latest_monitor_failure_msg")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notifications(
        self,
    ) -> typing.Optional["QualityMonitorPluginframeworkNotifications"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#notifications QualityMonitorPluginframework#notifications}.'''
        result = self._values.get("notifications")
        return typing.cast(typing.Optional["QualityMonitorPluginframeworkNotifications"], result)

    @builtins.property
    def schedule(self) -> typing.Optional["QualityMonitorPluginframeworkSchedule"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#schedule QualityMonitorPluginframework#schedule}.'''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional["QualityMonitorPluginframeworkSchedule"], result)

    @builtins.property
    def skip_builtin_dashboard(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#skip_builtin_dashboard QualityMonitorPluginframework#skip_builtin_dashboard}.'''
        result = self._values.get("skip_builtin_dashboard")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def slicing_exprs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#slicing_exprs QualityMonitorPluginframework#slicing_exprs}.'''
        result = self._values.get("slicing_exprs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def snapshot(self) -> typing.Optional["QualityMonitorPluginframeworkSnapshot"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#snapshot QualityMonitorPluginframework#snapshot}.'''
        result = self._values.get("snapshot")
        return typing.cast(typing.Optional["QualityMonitorPluginframeworkSnapshot"], result)

    @builtins.property
    def time_series(self) -> typing.Optional["QualityMonitorPluginframeworkTimeSeries"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#time_series QualityMonitorPluginframework#time_series}.'''
        result = self._values.get("time_series")
        return typing.cast(typing.Optional["QualityMonitorPluginframeworkTimeSeries"], result)

    @builtins.property
    def warehouse_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#warehouse_id QualityMonitorPluginframework#warehouse_id}.'''
        result = self._values.get("warehouse_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QualityMonitorPluginframeworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.qualityMonitorPluginframework.QualityMonitorPluginframeworkCustomMetrics",
    jsii_struct_bases=[],
    name_mapping={
        "definition": "definition",
        "input_columns": "inputColumns",
        "name": "name",
        "output_data_type": "outputDataType",
        "type": "type",
    },
)
class QualityMonitorPluginframeworkCustomMetrics:
    def __init__(
        self,
        *,
        definition: builtins.str,
        input_columns: typing.Sequence[builtins.str],
        name: builtins.str,
        output_data_type: builtins.str,
        type: builtins.str,
    ) -> None:
        '''
        :param definition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#definition QualityMonitorPluginframework#definition}.
        :param input_columns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#input_columns QualityMonitorPluginframework#input_columns}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#name QualityMonitorPluginframework#name}.
        :param output_data_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#output_data_type QualityMonitorPluginframework#output_data_type}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#type QualityMonitorPluginframework#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1215a1df0ba590a5d3f47dca8dd30baad1bc76347a6dc16d011e24046ff479ad)
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument input_columns", value=input_columns, expected_type=type_hints["input_columns"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument output_data_type", value=output_data_type, expected_type=type_hints["output_data_type"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "definition": definition,
            "input_columns": input_columns,
            "name": name,
            "output_data_type": output_data_type,
            "type": type,
        }

    @builtins.property
    def definition(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#definition QualityMonitorPluginframework#definition}.'''
        result = self._values.get("definition")
        assert result is not None, "Required property 'definition' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def input_columns(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#input_columns QualityMonitorPluginframework#input_columns}.'''
        result = self._values.get("input_columns")
        assert result is not None, "Required property 'input_columns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#name QualityMonitorPluginframework#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def output_data_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#output_data_type QualityMonitorPluginframework#output_data_type}.'''
        result = self._values.get("output_data_type")
        assert result is not None, "Required property 'output_data_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#type QualityMonitorPluginframework#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QualityMonitorPluginframeworkCustomMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QualityMonitorPluginframeworkCustomMetricsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.qualityMonitorPluginframework.QualityMonitorPluginframeworkCustomMetricsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71d574230aec86b2075e2aac1eb8ef9e82aaf1e7c4c09bd0223a86e29d3f3efa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QualityMonitorPluginframeworkCustomMetricsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3498206e9770dbd51699ddd2775aa2b3f51a2a12abf1aa0dd02e1e0f573530b4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QualityMonitorPluginframeworkCustomMetricsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5a5801243a57d6118ded397e4b767c575539081c19f00cdb0ee11e747cbd701)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea3e051ba41283b8f2bf9cab6eb0f76827a3d8ad8c1aa1c5807987f712b0710f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c14aa23751447d2361f4d2c34b9c395919b01709bfc89f1246279dcf46ca8f4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QualityMonitorPluginframeworkCustomMetrics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QualityMonitorPluginframeworkCustomMetrics]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QualityMonitorPluginframeworkCustomMetrics]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa3d039318bc176f59685308e5e80ed45a8f8176ca3e00450fc16b9a6032c909)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QualityMonitorPluginframeworkCustomMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.qualityMonitorPluginframework.QualityMonitorPluginframeworkCustomMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a0e3790211e25bb892d70bca7fa2d7a86f76a06c8393544ed54a515c2645eb2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="definitionInput")
    def definition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "definitionInput"))

    @builtins.property
    @jsii.member(jsii_name="inputColumnsInput")
    def input_columns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inputColumnsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="outputDataTypeInput")
    def output_data_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputDataTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "definition"))

    @definition.setter
    def definition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1150b1f21e80e03f53b84341cd37774f22080a8e238f04c8fd66d5dbe249830e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputColumns")
    def input_columns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inputColumns"))

    @input_columns.setter
    def input_columns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aee05da818599b1c776c8b662d0c4dd14e1b9698b17d6d43c644e66a81800f07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputColumns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef2d832b53dda79835155bcdb917d2b7ee345520dcf73b5ea35dbb4df762241c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputDataType")
    def output_data_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputDataType"))

    @output_data_type.setter
    def output_data_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54a69a3ec9d6c69f706e96ffabc0b153992de2fd2771b570b5284a1afe04fc4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputDataType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71a39263bfdb5c784c5b681ad0db6175e299d9121e9b46b605c354a5f1e59ef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkCustomMetrics]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkCustomMetrics]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkCustomMetrics]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__189e0e34f35d36771703a3d91fd5ff7c49c9c09b1b1e03e36322a036fed2be3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.qualityMonitorPluginframework.QualityMonitorPluginframeworkDataClassificationConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class QualityMonitorPluginframeworkDataClassificationConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#enabled QualityMonitorPluginframework#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16b77b3f07f8f65d804baf91f77e5a0fa72fb1dbd1c6ff1183de64cb17aa820f)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#enabled QualityMonitorPluginframework#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QualityMonitorPluginframeworkDataClassificationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QualityMonitorPluginframeworkDataClassificationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.qualityMonitorPluginframework.QualityMonitorPluginframeworkDataClassificationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f30a9363757029ae559901a22ce665317867ccc53af1619c64f776f5bb2b8b53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eae24bfa24df683546cfb8efb271c2287c662821a07fa7e16a2f77a3efdaa37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkDataClassificationConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkDataClassificationConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkDataClassificationConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5389d14a30c579129f85e731adae11fe4972cb2a0be2b8e16aaaf45f2541099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.qualityMonitorPluginframework.QualityMonitorPluginframeworkInferenceLog",
    jsii_struct_bases=[],
    name_mapping={
        "granularities": "granularities",
        "model_id_col": "modelIdCol",
        "prediction_col": "predictionCol",
        "problem_type": "problemType",
        "timestamp_col": "timestampCol",
        "label_col": "labelCol",
        "prediction_proba_col": "predictionProbaCol",
    },
)
class QualityMonitorPluginframeworkInferenceLog:
    def __init__(
        self,
        *,
        granularities: typing.Sequence[builtins.str],
        model_id_col: builtins.str,
        prediction_col: builtins.str,
        problem_type: builtins.str,
        timestamp_col: builtins.str,
        label_col: typing.Optional[builtins.str] = None,
        prediction_proba_col: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param granularities: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#granularities QualityMonitorPluginframework#granularities}.
        :param model_id_col: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#model_id_col QualityMonitorPluginframework#model_id_col}.
        :param prediction_col: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#prediction_col QualityMonitorPluginframework#prediction_col}.
        :param problem_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#problem_type QualityMonitorPluginframework#problem_type}.
        :param timestamp_col: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#timestamp_col QualityMonitorPluginframework#timestamp_col}.
        :param label_col: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#label_col QualityMonitorPluginframework#label_col}.
        :param prediction_proba_col: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#prediction_proba_col QualityMonitorPluginframework#prediction_proba_col}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c62db492114110c5f002c2666546e530c2d22f301ad202d31b3b7ed8004c5eb4)
            check_type(argname="argument granularities", value=granularities, expected_type=type_hints["granularities"])
            check_type(argname="argument model_id_col", value=model_id_col, expected_type=type_hints["model_id_col"])
            check_type(argname="argument prediction_col", value=prediction_col, expected_type=type_hints["prediction_col"])
            check_type(argname="argument problem_type", value=problem_type, expected_type=type_hints["problem_type"])
            check_type(argname="argument timestamp_col", value=timestamp_col, expected_type=type_hints["timestamp_col"])
            check_type(argname="argument label_col", value=label_col, expected_type=type_hints["label_col"])
            check_type(argname="argument prediction_proba_col", value=prediction_proba_col, expected_type=type_hints["prediction_proba_col"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "granularities": granularities,
            "model_id_col": model_id_col,
            "prediction_col": prediction_col,
            "problem_type": problem_type,
            "timestamp_col": timestamp_col,
        }
        if label_col is not None:
            self._values["label_col"] = label_col
        if prediction_proba_col is not None:
            self._values["prediction_proba_col"] = prediction_proba_col

    @builtins.property
    def granularities(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#granularities QualityMonitorPluginframework#granularities}.'''
        result = self._values.get("granularities")
        assert result is not None, "Required property 'granularities' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def model_id_col(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#model_id_col QualityMonitorPluginframework#model_id_col}.'''
        result = self._values.get("model_id_col")
        assert result is not None, "Required property 'model_id_col' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prediction_col(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#prediction_col QualityMonitorPluginframework#prediction_col}.'''
        result = self._values.get("prediction_col")
        assert result is not None, "Required property 'prediction_col' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def problem_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#problem_type QualityMonitorPluginframework#problem_type}.'''
        result = self._values.get("problem_type")
        assert result is not None, "Required property 'problem_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def timestamp_col(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#timestamp_col QualityMonitorPluginframework#timestamp_col}.'''
        result = self._values.get("timestamp_col")
        assert result is not None, "Required property 'timestamp_col' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def label_col(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#label_col QualityMonitorPluginframework#label_col}.'''
        result = self._values.get("label_col")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prediction_proba_col(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#prediction_proba_col QualityMonitorPluginframework#prediction_proba_col}.'''
        result = self._values.get("prediction_proba_col")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QualityMonitorPluginframeworkInferenceLog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QualityMonitorPluginframeworkInferenceLogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.qualityMonitorPluginframework.QualityMonitorPluginframeworkInferenceLogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5ec4e2cc05554f1e9acb8d5df3cb65e8dd1ddcff42bf73763c65082219bdb40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLabelCol")
    def reset_label_col(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabelCol", []))

    @jsii.member(jsii_name="resetPredictionProbaCol")
    def reset_prediction_proba_col(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPredictionProbaCol", []))

    @builtins.property
    @jsii.member(jsii_name="granularitiesInput")
    def granularities_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "granularitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="labelColInput")
    def label_col_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelColInput"))

    @builtins.property
    @jsii.member(jsii_name="modelIdColInput")
    def model_id_col_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelIdColInput"))

    @builtins.property
    @jsii.member(jsii_name="predictionColInput")
    def prediction_col_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "predictionColInput"))

    @builtins.property
    @jsii.member(jsii_name="predictionProbaColInput")
    def prediction_proba_col_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "predictionProbaColInput"))

    @builtins.property
    @jsii.member(jsii_name="problemTypeInput")
    def problem_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "problemTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampColInput")
    def timestamp_col_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timestampColInput"))

    @builtins.property
    @jsii.member(jsii_name="granularities")
    def granularities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "granularities"))

    @granularities.setter
    def granularities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36d7afc8b8216d640149c4588bfc9514fbac6ed3af5c60b56ef96294cbae0276)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "granularities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labelCol")
    def label_col(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "labelCol"))

    @label_col.setter
    def label_col(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8306834dcf3f19a65b4e098322176be8736147d352f9d0d7396500f2ad0c7533)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labelCol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelIdCol")
    def model_id_col(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelIdCol"))

    @model_id_col.setter
    def model_id_col(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__143de0093289e50e1f5b1433f362540db75203df24a3a047d4bbcc3663d42e26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelIdCol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="predictionCol")
    def prediction_col(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "predictionCol"))

    @prediction_col.setter
    def prediction_col(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43649fb4ad03da08f2f519cf034b29eeb240c7d60c0c707cc34f8c577d87fdf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "predictionCol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="predictionProbaCol")
    def prediction_proba_col(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "predictionProbaCol"))

    @prediction_proba_col.setter
    def prediction_proba_col(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc1a9c456ecc21d7eed76f53b23cc5f98b4502975a2d74a68d2340b8899e71a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "predictionProbaCol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="problemType")
    def problem_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "problemType"))

    @problem_type.setter
    def problem_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9332999fda28e8299c164feaf4fcefb9b4be71886347e54eea9bc26acad009fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "problemType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampCol")
    def timestamp_col(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampCol"))

    @timestamp_col.setter
    def timestamp_col(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__466d51918d2fcb2903314f973ec59169469af5aeb2948942bf22512a9ab2c92e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampCol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkInferenceLog]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkInferenceLog]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkInferenceLog]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8043d4acdd614df46d3e5d69039b2763d29ac53c38e976ff9a68b3af4865cf79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.qualityMonitorPluginframework.QualityMonitorPluginframeworkNotifications",
    jsii_struct_bases=[],
    name_mapping={
        "on_failure": "onFailure",
        "on_new_classification_tag_detected": "onNewClassificationTagDetected",
    },
)
class QualityMonitorPluginframeworkNotifications:
    def __init__(
        self,
        *,
        on_failure: typing.Optional[typing.Union["QualityMonitorPluginframeworkNotificationsOnFailure", typing.Dict[builtins.str, typing.Any]]] = None,
        on_new_classification_tag_detected: typing.Optional[typing.Union["QualityMonitorPluginframeworkNotificationsOnNewClassificationTagDetected", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param on_failure: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#on_failure QualityMonitorPluginframework#on_failure}.
        :param on_new_classification_tag_detected: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#on_new_classification_tag_detected QualityMonitorPluginframework#on_new_classification_tag_detected}.
        '''
        if isinstance(on_failure, dict):
            on_failure = QualityMonitorPluginframeworkNotificationsOnFailure(**on_failure)
        if isinstance(on_new_classification_tag_detected, dict):
            on_new_classification_tag_detected = QualityMonitorPluginframeworkNotificationsOnNewClassificationTagDetected(**on_new_classification_tag_detected)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af91c350897ed51046e39034c6b71a0f2d13eae7e3eb07f3630fe4da57b4d367)
            check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
            check_type(argname="argument on_new_classification_tag_detected", value=on_new_classification_tag_detected, expected_type=type_hints["on_new_classification_tag_detected"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if on_new_classification_tag_detected is not None:
            self._values["on_new_classification_tag_detected"] = on_new_classification_tag_detected

    @builtins.property
    def on_failure(
        self,
    ) -> typing.Optional["QualityMonitorPluginframeworkNotificationsOnFailure"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#on_failure QualityMonitorPluginframework#on_failure}.'''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional["QualityMonitorPluginframeworkNotificationsOnFailure"], result)

    @builtins.property
    def on_new_classification_tag_detected(
        self,
    ) -> typing.Optional["QualityMonitorPluginframeworkNotificationsOnNewClassificationTagDetected"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#on_new_classification_tag_detected QualityMonitorPluginframework#on_new_classification_tag_detected}.'''
        result = self._values.get("on_new_classification_tag_detected")
        return typing.cast(typing.Optional["QualityMonitorPluginframeworkNotificationsOnNewClassificationTagDetected"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QualityMonitorPluginframeworkNotifications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.qualityMonitorPluginframework.QualityMonitorPluginframeworkNotificationsOnFailure",
    jsii_struct_bases=[],
    name_mapping={"email_addresses": "emailAddresses"},
)
class QualityMonitorPluginframeworkNotificationsOnFailure:
    def __init__(
        self,
        *,
        email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param email_addresses: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#email_addresses QualityMonitorPluginframework#email_addresses}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f356bdd0abacdf293be3c0a77b26f7916f9da5e40deb75c4708b80478548f5d5)
            check_type(argname="argument email_addresses", value=email_addresses, expected_type=type_hints["email_addresses"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if email_addresses is not None:
            self._values["email_addresses"] = email_addresses

    @builtins.property
    def email_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#email_addresses QualityMonitorPluginframework#email_addresses}.'''
        result = self._values.get("email_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QualityMonitorPluginframeworkNotificationsOnFailure(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QualityMonitorPluginframeworkNotificationsOnFailureOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.qualityMonitorPluginframework.QualityMonitorPluginframeworkNotificationsOnFailureOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af4977b7145565fd72e5efa286c40dde5a3dec95c1c9780558ba270a85f3855f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEmailAddresses")
    def reset_email_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailAddresses", []))

    @builtins.property
    @jsii.member(jsii_name="emailAddressesInput")
    def email_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emailAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="emailAddresses")
    def email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "emailAddresses"))

    @email_addresses.setter
    def email_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fcef04f64c80efbafdfeac826e19fd2ba9d5176d88f0a6e208417b65a1617fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkNotificationsOnFailure]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkNotificationsOnFailure]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkNotificationsOnFailure]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c939662dbcbd80430497929dd90ba1a5637fa5a2dab447ff8773afab2f79ec3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.qualityMonitorPluginframework.QualityMonitorPluginframeworkNotificationsOnNewClassificationTagDetected",
    jsii_struct_bases=[],
    name_mapping={"email_addresses": "emailAddresses"},
)
class QualityMonitorPluginframeworkNotificationsOnNewClassificationTagDetected:
    def __init__(
        self,
        *,
        email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param email_addresses: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#email_addresses QualityMonitorPluginframework#email_addresses}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0f878be720c2bd01839efde06e8b6efb7bdb96c262c91fa0086a571ecc4b991)
            check_type(argname="argument email_addresses", value=email_addresses, expected_type=type_hints["email_addresses"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if email_addresses is not None:
            self._values["email_addresses"] = email_addresses

    @builtins.property
    def email_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#email_addresses QualityMonitorPluginframework#email_addresses}.'''
        result = self._values.get("email_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QualityMonitorPluginframeworkNotificationsOnNewClassificationTagDetected(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QualityMonitorPluginframeworkNotificationsOnNewClassificationTagDetectedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.qualityMonitorPluginframework.QualityMonitorPluginframeworkNotificationsOnNewClassificationTagDetectedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbe3dd30f5833e46926e65eeece8a0a7eb232aef0817a884d2b8d270e1484b9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEmailAddresses")
    def reset_email_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailAddresses", []))

    @builtins.property
    @jsii.member(jsii_name="emailAddressesInput")
    def email_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emailAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="emailAddresses")
    def email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "emailAddresses"))

    @email_addresses.setter
    def email_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__912ad1b05a04165bbbba9cae63b803e4ea3e2f977cc5c689d88316a17776b404)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkNotificationsOnNewClassificationTagDetected]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkNotificationsOnNewClassificationTagDetected]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkNotificationsOnNewClassificationTagDetected]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a71276526fc74701e65a55f5e4e81bdd64155e2ca8ed3dc08de0b36b04ff3826)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QualityMonitorPluginframeworkNotificationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.qualityMonitorPluginframework.QualityMonitorPluginframeworkNotificationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59eff81a072dc85f3d44b390403dbba992a0694f5d62fb989baafce39869447f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOnFailure")
    def put_on_failure(
        self,
        *,
        email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param email_addresses: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#email_addresses QualityMonitorPluginframework#email_addresses}.
        '''
        value = QualityMonitorPluginframeworkNotificationsOnFailure(
            email_addresses=email_addresses
        )

        return typing.cast(None, jsii.invoke(self, "putOnFailure", [value]))

    @jsii.member(jsii_name="putOnNewClassificationTagDetected")
    def put_on_new_classification_tag_detected(
        self,
        *,
        email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param email_addresses: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#email_addresses QualityMonitorPluginframework#email_addresses}.
        '''
        value = QualityMonitorPluginframeworkNotificationsOnNewClassificationTagDetected(
            email_addresses=email_addresses
        )

        return typing.cast(None, jsii.invoke(self, "putOnNewClassificationTagDetected", [value]))

    @jsii.member(jsii_name="resetOnFailure")
    def reset_on_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnFailure", []))

    @jsii.member(jsii_name="resetOnNewClassificationTagDetected")
    def reset_on_new_classification_tag_detected(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnNewClassificationTagDetected", []))

    @builtins.property
    @jsii.member(jsii_name="onFailure")
    def on_failure(
        self,
    ) -> QualityMonitorPluginframeworkNotificationsOnFailureOutputReference:
        return typing.cast(QualityMonitorPluginframeworkNotificationsOnFailureOutputReference, jsii.get(self, "onFailure"))

    @builtins.property
    @jsii.member(jsii_name="onNewClassificationTagDetected")
    def on_new_classification_tag_detected(
        self,
    ) -> QualityMonitorPluginframeworkNotificationsOnNewClassificationTagDetectedOutputReference:
        return typing.cast(QualityMonitorPluginframeworkNotificationsOnNewClassificationTagDetectedOutputReference, jsii.get(self, "onNewClassificationTagDetected"))

    @builtins.property
    @jsii.member(jsii_name="onFailureInput")
    def on_failure_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkNotificationsOnFailure]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkNotificationsOnFailure]], jsii.get(self, "onFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="onNewClassificationTagDetectedInput")
    def on_new_classification_tag_detected_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkNotificationsOnNewClassificationTagDetected]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkNotificationsOnNewClassificationTagDetected]], jsii.get(self, "onNewClassificationTagDetectedInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkNotifications]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkNotifications]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkNotifications]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f75e746e7e49b89fc2c8015027033cb262f7278d8dd7ca2d720f36bd6b570297)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.qualityMonitorPluginframework.QualityMonitorPluginframeworkSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "quartz_cron_expression": "quartzCronExpression",
        "timezone_id": "timezoneId",
    },
)
class QualityMonitorPluginframeworkSchedule:
    def __init__(
        self,
        *,
        quartz_cron_expression: builtins.str,
        timezone_id: builtins.str,
    ) -> None:
        '''
        :param quartz_cron_expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#quartz_cron_expression QualityMonitorPluginframework#quartz_cron_expression}.
        :param timezone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#timezone_id QualityMonitorPluginframework#timezone_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35800dd979f7be41fd9a08ca5e630c1ade511a2fd82df2dceb3cc472dc351d8d)
            check_type(argname="argument quartz_cron_expression", value=quartz_cron_expression, expected_type=type_hints["quartz_cron_expression"])
            check_type(argname="argument timezone_id", value=timezone_id, expected_type=type_hints["timezone_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "quartz_cron_expression": quartz_cron_expression,
            "timezone_id": timezone_id,
        }

    @builtins.property
    def quartz_cron_expression(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#quartz_cron_expression QualityMonitorPluginframework#quartz_cron_expression}.'''
        result = self._values.get("quartz_cron_expression")
        assert result is not None, "Required property 'quartz_cron_expression' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def timezone_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#timezone_id QualityMonitorPluginframework#timezone_id}.'''
        result = self._values.get("timezone_id")
        assert result is not None, "Required property 'timezone_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QualityMonitorPluginframeworkSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QualityMonitorPluginframeworkScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.qualityMonitorPluginframework.QualityMonitorPluginframeworkScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e52450d9c75f65967d7f86da133ff8ce7cc67e741f6e0c10a562fa315fe7c6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="pauseStatus")
    def pause_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pauseStatus"))

    @builtins.property
    @jsii.member(jsii_name="quartzCronExpressionInput")
    def quartz_cron_expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "quartzCronExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="timezoneIdInput")
    def timezone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timezoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="quartzCronExpression")
    def quartz_cron_expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "quartzCronExpression"))

    @quartz_cron_expression.setter
    def quartz_cron_expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4cdc4d3b9ffda916abd566d9a5946d5b72e830b32ebf09038eacf4a75283730)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quartzCronExpression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timezoneId")
    def timezone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezoneId"))

    @timezone_id.setter
    def timezone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__affe992c026eb064eb2ec5c625c1f6abc0858074a1aa4ee3d2a38e5b67ab9451)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezoneId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkSchedule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkSchedule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkSchedule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cabf8735ec1e5032a34fc3e7df01d80c0955d78cf8f89c0f90419eb3dd1ebb18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.qualityMonitorPluginframework.QualityMonitorPluginframeworkSnapshot",
    jsii_struct_bases=[],
    name_mapping={},
)
class QualityMonitorPluginframeworkSnapshot:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QualityMonitorPluginframeworkSnapshot(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QualityMonitorPluginframeworkSnapshotOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.qualityMonitorPluginframework.QualityMonitorPluginframeworkSnapshotOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__01ee976489e25b8c366b8d559939bc86092ba14dc631af15692d157fcd7f7880)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkSnapshot]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkSnapshot]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkSnapshot]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c8b98f6dffa96fb61f6bb9ffc740df3fd03e89f9423c98d42e4ccaf547f647)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.qualityMonitorPluginframework.QualityMonitorPluginframeworkTimeSeries",
    jsii_struct_bases=[],
    name_mapping={"granularities": "granularities", "timestamp_col": "timestampCol"},
)
class QualityMonitorPluginframeworkTimeSeries:
    def __init__(
        self,
        *,
        granularities: typing.Sequence[builtins.str],
        timestamp_col: builtins.str,
    ) -> None:
        '''
        :param granularities: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#granularities QualityMonitorPluginframework#granularities}.
        :param timestamp_col: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#timestamp_col QualityMonitorPluginframework#timestamp_col}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b127ab459dada4b553878256ea8ff1e18301135bca101a81dc203b6c1760ae51)
            check_type(argname="argument granularities", value=granularities, expected_type=type_hints["granularities"])
            check_type(argname="argument timestamp_col", value=timestamp_col, expected_type=type_hints["timestamp_col"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "granularities": granularities,
            "timestamp_col": timestamp_col,
        }

    @builtins.property
    def granularities(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#granularities QualityMonitorPluginframework#granularities}.'''
        result = self._values.get("granularities")
        assert result is not None, "Required property 'granularities' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def timestamp_col(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.53.0/docs/resources/quality_monitor_pluginframework#timestamp_col QualityMonitorPluginframework#timestamp_col}.'''
        result = self._values.get("timestamp_col")
        assert result is not None, "Required property 'timestamp_col' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QualityMonitorPluginframeworkTimeSeries(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QualityMonitorPluginframeworkTimeSeriesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.qualityMonitorPluginframework.QualityMonitorPluginframeworkTimeSeriesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__687bf9adb210300110dfc39bfdd99da015d2b5c653f768063a09708453728509)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="granularitiesInput")
    def granularities_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "granularitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampColInput")
    def timestamp_col_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timestampColInput"))

    @builtins.property
    @jsii.member(jsii_name="granularities")
    def granularities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "granularities"))

    @granularities.setter
    def granularities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__078d2c89acdfa5f6b24afe549f7205b45d289ea9cf8c5aaaf7011e97325f3114)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "granularities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampCol")
    def timestamp_col(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampCol"))

    @timestamp_col.setter
    def timestamp_col(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fd53dd39a92e9ac0d520eb1370473295fe46193f0eec412dd4bc85ac207dff5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampCol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkTimeSeries]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkTimeSeries]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkTimeSeries]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__576a08e9e3bbdad6195e995c300e27a55540fbc9c7ebc0eb8523092e012afcf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "QualityMonitorPluginframework",
    "QualityMonitorPluginframeworkConfig",
    "QualityMonitorPluginframeworkCustomMetrics",
    "QualityMonitorPluginframeworkCustomMetricsList",
    "QualityMonitorPluginframeworkCustomMetricsOutputReference",
    "QualityMonitorPluginframeworkDataClassificationConfig",
    "QualityMonitorPluginframeworkDataClassificationConfigOutputReference",
    "QualityMonitorPluginframeworkInferenceLog",
    "QualityMonitorPluginframeworkInferenceLogOutputReference",
    "QualityMonitorPluginframeworkNotifications",
    "QualityMonitorPluginframeworkNotificationsOnFailure",
    "QualityMonitorPluginframeworkNotificationsOnFailureOutputReference",
    "QualityMonitorPluginframeworkNotificationsOnNewClassificationTagDetected",
    "QualityMonitorPluginframeworkNotificationsOnNewClassificationTagDetectedOutputReference",
    "QualityMonitorPluginframeworkNotificationsOutputReference",
    "QualityMonitorPluginframeworkSchedule",
    "QualityMonitorPluginframeworkScheduleOutputReference",
    "QualityMonitorPluginframeworkSnapshot",
    "QualityMonitorPluginframeworkSnapshotOutputReference",
    "QualityMonitorPluginframeworkTimeSeries",
    "QualityMonitorPluginframeworkTimeSeriesOutputReference",
]

publication.publish()

def _typecheckingstub__3289d7d5dd8d92207a6f0e7f8bbf30a54d841c2d53d29f1eef22fc9282cbf7e6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    assets_dir: builtins.str,
    output_schema_name: builtins.str,
    table_name: builtins.str,
    baseline_table_name: typing.Optional[builtins.str] = None,
    custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QualityMonitorPluginframeworkCustomMetrics, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_classification_config: typing.Optional[typing.Union[QualityMonitorPluginframeworkDataClassificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    inference_log: typing.Optional[typing.Union[QualityMonitorPluginframeworkInferenceLog, typing.Dict[builtins.str, typing.Any]]] = None,
    latest_monitor_failure_msg: typing.Optional[builtins.str] = None,
    notifications: typing.Optional[typing.Union[QualityMonitorPluginframeworkNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    schedule: typing.Optional[typing.Union[QualityMonitorPluginframeworkSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    skip_builtin_dashboard: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    slicing_exprs: typing.Optional[typing.Sequence[builtins.str]] = None,
    snapshot: typing.Optional[typing.Union[QualityMonitorPluginframeworkSnapshot, typing.Dict[builtins.str, typing.Any]]] = None,
    time_series: typing.Optional[typing.Union[QualityMonitorPluginframeworkTimeSeries, typing.Dict[builtins.str, typing.Any]]] = None,
    warehouse_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__c1b139cc985976b94b035828ffc3fa89922e8e7a6b55d3915e4f7ac547e4aa99(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__489c441c51fffb0c838b63b568f63afa3ce9c2f82846dba1de8307feefc7dab0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QualityMonitorPluginframeworkCustomMetrics, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed534d050fb6423e788ce018773e255be237b456b9197428ea588d6c00404259(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f9f500c61f04d8bce195f7fd905dfd5a0bb1be0582dde768b8b9aaacf79bd9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bdf8cda7aa28829dd8814fafdbec70c46c78fa87f160173caa8d67b42a29963(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c401256871bc17f4fd2fbd4feb1417a4d1dbde29f634d791d4430ca4c6e53a5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f53d2576f33c0fbf67b56ed2c4dce1ca6bc4fa97ebddf33a551f175838128449(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e23a97fe4e66ff938a85539c4878675f44c72e738870423d8302dd1b2a8dde6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7c8b013c3e0b9a43fb0f4e521d9e2979ca6e8dfbc96738cf8cfd7604f0543b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14796fa283a9f5734af501cbd2d0f5d620f1c76ba400cc26bfd54c1309113367(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__887a63f681d6ce3c9facef2f4ff1011377c454e76ba7548445c90b5ff63fccb5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    assets_dir: builtins.str,
    output_schema_name: builtins.str,
    table_name: builtins.str,
    baseline_table_name: typing.Optional[builtins.str] = None,
    custom_metrics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QualityMonitorPluginframeworkCustomMetrics, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_classification_config: typing.Optional[typing.Union[QualityMonitorPluginframeworkDataClassificationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    inference_log: typing.Optional[typing.Union[QualityMonitorPluginframeworkInferenceLog, typing.Dict[builtins.str, typing.Any]]] = None,
    latest_monitor_failure_msg: typing.Optional[builtins.str] = None,
    notifications: typing.Optional[typing.Union[QualityMonitorPluginframeworkNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    schedule: typing.Optional[typing.Union[QualityMonitorPluginframeworkSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    skip_builtin_dashboard: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    slicing_exprs: typing.Optional[typing.Sequence[builtins.str]] = None,
    snapshot: typing.Optional[typing.Union[QualityMonitorPluginframeworkSnapshot, typing.Dict[builtins.str, typing.Any]]] = None,
    time_series: typing.Optional[typing.Union[QualityMonitorPluginframeworkTimeSeries, typing.Dict[builtins.str, typing.Any]]] = None,
    warehouse_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1215a1df0ba590a5d3f47dca8dd30baad1bc76347a6dc16d011e24046ff479ad(
    *,
    definition: builtins.str,
    input_columns: typing.Sequence[builtins.str],
    name: builtins.str,
    output_data_type: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71d574230aec86b2075e2aac1eb8ef9e82aaf1e7c4c09bd0223a86e29d3f3efa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3498206e9770dbd51699ddd2775aa2b3f51a2a12abf1aa0dd02e1e0f573530b4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5a5801243a57d6118ded397e4b767c575539081c19f00cdb0ee11e747cbd701(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea3e051ba41283b8f2bf9cab6eb0f76827a3d8ad8c1aa1c5807987f712b0710f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c14aa23751447d2361f4d2c34b9c395919b01709bfc89f1246279dcf46ca8f4f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3d039318bc176f59685308e5e80ed45a8f8176ca3e00450fc16b9a6032c909(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QualityMonitorPluginframeworkCustomMetrics]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a0e3790211e25bb892d70bca7fa2d7a86f76a06c8393544ed54a515c2645eb2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1150b1f21e80e03f53b84341cd37774f22080a8e238f04c8fd66d5dbe249830e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee05da818599b1c776c8b662d0c4dd14e1b9698b17d6d43c644e66a81800f07(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef2d832b53dda79835155bcdb917d2b7ee345520dcf73b5ea35dbb4df762241c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54a69a3ec9d6c69f706e96ffabc0b153992de2fd2771b570b5284a1afe04fc4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71a39263bfdb5c784c5b681ad0db6175e299d9121e9b46b605c354a5f1e59ef6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__189e0e34f35d36771703a3d91fd5ff7c49c9c09b1b1e03e36322a036fed2be3f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkCustomMetrics]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b77b3f07f8f65d804baf91f77e5a0fa72fb1dbd1c6ff1183de64cb17aa820f(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f30a9363757029ae559901a22ce665317867ccc53af1619c64f776f5bb2b8b53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eae24bfa24df683546cfb8efb271c2287c662821a07fa7e16a2f77a3efdaa37(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5389d14a30c579129f85e731adae11fe4972cb2a0be2b8e16aaaf45f2541099(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkDataClassificationConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62db492114110c5f002c2666546e530c2d22f301ad202d31b3b7ed8004c5eb4(
    *,
    granularities: typing.Sequence[builtins.str],
    model_id_col: builtins.str,
    prediction_col: builtins.str,
    problem_type: builtins.str,
    timestamp_col: builtins.str,
    label_col: typing.Optional[builtins.str] = None,
    prediction_proba_col: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ec4e2cc05554f1e9acb8d5df3cb65e8dd1ddcff42bf73763c65082219bdb40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36d7afc8b8216d640149c4588bfc9514fbac6ed3af5c60b56ef96294cbae0276(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8306834dcf3f19a65b4e098322176be8736147d352f9d0d7396500f2ad0c7533(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__143de0093289e50e1f5b1433f362540db75203df24a3a047d4bbcc3663d42e26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43649fb4ad03da08f2f519cf034b29eeb240c7d60c0c707cc34f8c577d87fdf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1a9c456ecc21d7eed76f53b23cc5f98b4502975a2d74a68d2340b8899e71a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9332999fda28e8299c164feaf4fcefb9b4be71886347e54eea9bc26acad009fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466d51918d2fcb2903314f973ec59169469af5aeb2948942bf22512a9ab2c92e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8043d4acdd614df46d3e5d69039b2763d29ac53c38e976ff9a68b3af4865cf79(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkInferenceLog]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af91c350897ed51046e39034c6b71a0f2d13eae7e3eb07f3630fe4da57b4d367(
    *,
    on_failure: typing.Optional[typing.Union[QualityMonitorPluginframeworkNotificationsOnFailure, typing.Dict[builtins.str, typing.Any]]] = None,
    on_new_classification_tag_detected: typing.Optional[typing.Union[QualityMonitorPluginframeworkNotificationsOnNewClassificationTagDetected, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f356bdd0abacdf293be3c0a77b26f7916f9da5e40deb75c4708b80478548f5d5(
    *,
    email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af4977b7145565fd72e5efa286c40dde5a3dec95c1c9780558ba270a85f3855f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fcef04f64c80efbafdfeac826e19fd2ba9d5176d88f0a6e208417b65a1617fb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c939662dbcbd80430497929dd90ba1a5637fa5a2dab447ff8773afab2f79ec3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkNotificationsOnFailure]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0f878be720c2bd01839efde06e8b6efb7bdb96c262c91fa0086a571ecc4b991(
    *,
    email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe3dd30f5833e46926e65eeece8a0a7eb232aef0817a884d2b8d270e1484b9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__912ad1b05a04165bbbba9cae63b803e4ea3e2f977cc5c689d88316a17776b404(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71276526fc74701e65a55f5e4e81bdd64155e2ca8ed3dc08de0b36b04ff3826(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkNotificationsOnNewClassificationTagDetected]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59eff81a072dc85f3d44b390403dbba992a0694f5d62fb989baafce39869447f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f75e746e7e49b89fc2c8015027033cb262f7278d8dd7ca2d720f36bd6b570297(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkNotifications]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35800dd979f7be41fd9a08ca5e630c1ade511a2fd82df2dceb3cc472dc351d8d(
    *,
    quartz_cron_expression: builtins.str,
    timezone_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e52450d9c75f65967d7f86da133ff8ce7cc67e741f6e0c10a562fa315fe7c6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4cdc4d3b9ffda916abd566d9a5946d5b72e830b32ebf09038eacf4a75283730(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__affe992c026eb064eb2ec5c625c1f6abc0858074a1aa4ee3d2a38e5b67ab9451(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cabf8735ec1e5032a34fc3e7df01d80c0955d78cf8f89c0f90419eb3dd1ebb18(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkSchedule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01ee976489e25b8c366b8d559939bc86092ba14dc631af15692d157fcd7f7880(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c8b98f6dffa96fb61f6bb9ffc740df3fd03e89f9423c98d42e4ccaf547f647(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkSnapshot]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b127ab459dada4b553878256ea8ff1e18301135bca101a81dc203b6c1760ae51(
    *,
    granularities: typing.Sequence[builtins.str],
    timestamp_col: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__687bf9adb210300110dfc39bfdd99da015d2b5c653f768063a09708453728509(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__078d2c89acdfa5f6b24afe549f7205b45d289ea9cf8c5aaaf7011e97325f3114(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd53dd39a92e9ac0d520eb1370473295fe46193f0eec412dd4bc85ac207dff5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__576a08e9e3bbdad6195e995c300e27a55540fbc9c7ebc0eb8523092e012afcf6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QualityMonitorPluginframeworkTimeSeries]],
) -> None:
    """Type checking stubs"""
    pass
