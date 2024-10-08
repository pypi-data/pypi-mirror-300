from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
import math
import traceback
from typing import List
import helics as h
from esdl import esdl

from dots_infrastructure import Common
from dots_infrastructure.Constants import TimeRequestType
from dots_infrastructure.DataClasses import CalculationServiceInput, CalculationServiceOutput, HelicsCalculationInformation, HelicsFederateInformation, HelicsMessageFederateInformation, SimulatorConfiguration, TimeStepInformation
from dots_infrastructure.EsdlHelper import EsdlHelper
from dots_infrastructure.Logger import LOGGER
from dots_infrastructure import CalculationServiceHelperFunctions
from dots_infrastructure.influxdb_connector import InfluxDBConnector

class HelicsFederateExecutor:

    def __init__(self):
        self.simulator_configuration = CalculationServiceHelperFunctions.get_simulator_configuration_from_environment()

    def init_federate_info(self, info : HelicsFederateInformation, simulation_config : SimulatorConfiguration):
        federate_info = h.helicsCreateFederateInfo()
        h.helicsFederateInfoSetCoreName(federate_info, self.simulator_configuration.model_id) # might have to set different core names for esdl and calculation core
        h.helicsFederateInfoSetBroker(federate_info, self.simulator_configuration.broker_ip)
        h.helicsFederateInfoSetBrokerPort(federate_info, self.simulator_configuration.broker_port)
        h.helicsFederateInfoSetTimeProperty(federate_info, h.HelicsProperty.TIME_PERIOD, info.time_period_in_seconds)
        h.helicsFederateInfoSetTimeProperty(federate_info, h.HelicsProperty.TIME_OFFSET, info.offset)
        h.helicsFederateInfoSetFlagOption(federate_info, h.HelicsFederateFlag.UNINTERRUPTIBLE, info.uninterruptible)
        h.helicsFederateInfoSetFlagOption(federate_info, h.HelicsFederateFlag.WAIT_FOR_CURRENT_TIME_UPDATE, info.wait_for_current_time_update)
        h.helicsFederateInfoSetFlagOption(federate_info, h.HelicsFlag.TERMINATE_ON_ERROR, info.terminate_on_error)
        h.helicsFederateInfoSetCoreType(federate_info, h.HelicsCoreType.ZMQ)
        h.helicsFederateInfoSetIntegerProperty(federate_info, h.HelicsProperty.INT_LOG_LEVEL, simulation_config.log_level)
        return federate_info

class HelicsEsdlMessageFederateExecutor(HelicsFederateExecutor):
    def __init__(self, info : HelicsMessageFederateInformation):
        super().__init__()
        self.helics_message_federate_information = info

    def init_federate(self):
        federate_info = self.init_federate_info(self.helics_message_federate_information, self.simulator_configuration)
        self.message_federate = h.helicsCreateMessageFederate(f"{self.simulator_configuration.model_id}", federate_info)
        self.message_enpoint = h.helicsFederateRegisterEndpoint(self.message_federate, self.helics_message_federate_information.endpoint_name)

    def wait_for_esdl_file(self) -> EsdlHelper:
        self.message_federate.enter_executing_mode()
        h.helicsFederateRequestTime(self.message_federate, h.HELICS_TIME_MAXTIME)
        esdl_file_base64 = h.helicsMessageGetString(h.helicsEndpointGetMessage(self.message_enpoint))
        Common.destroy_federate(self.message_federate)
        esdl_helper = EsdlHelper(esdl_file_base64)

        return esdl_helper

class HelicsCombinationFederateExecutor(HelicsFederateExecutor):

    def __init__(self, info : HelicsCalculationInformation):
        super().__init__()
        self.input_dict : dict[str, List[CalculationServiceInput]] = {}
        self.output_dict : dict[str, List[CalculationServiceOutput]] = {}
        self.helics_value_federate_info = info
        self.energy_system : esdl.EnergySystem = None
        self.combination_federate : h.HelicsCombinationFederate = None
        self.commands_message_enpoint : h.HelicsEndpoint = None

    def init_outputs(self, info : HelicsCalculationInformation, combination_federate : h.HelicsCombinationFederate):
        outputs = CalculationServiceHelperFunctions.generate_publications_from_value_descriptions(info.outputs, self.simulator_configuration)
        for output in outputs:
            key = f'{output.esdl_asset_type}/{output.output_name}/{output.output_esdl_id}'
            if output.global_flag:
                pub = h.helicsFederateRegisterGlobalPublication(combination_federate, key, output.output_type, output.output_unit)
            else:
                pub = h.helicsFederateRegisterPublication(combination_federate, key, output.output_type, output.output_unit)
            output.helics_publication = pub
            if output.output_esdl_id in self.output_dict:
                self.output_dict[output.output_esdl_id].append(output)
            else:
                self.output_dict[output.output_esdl_id] = [output]

    def init_inputs(self, info : HelicsCalculationInformation, esdl_helper : EsdlHelper, combination_federate : h.HelicsCombinationFederate):
        inputs : List[CalculationServiceInput] = []
        for esdl_id in self.simulator_configuration.esdl_ids:
            inputs_for_esdl_object = esdl_helper.get_connected_input_esdl_objects(esdl_id, self.simulator_configuration.calculation_services, info.inputs)
            inputs.extend(inputs_for_esdl_object)
            self.input_dict[esdl_id] = inputs_for_esdl_object

        for input in inputs:
            sub_key = f'{input.esdl_asset_type}/{input.input_name}/{input.input_esdl_id}'
            LOGGER.debug(f"Subscribing to publication with key: {sub_key}")
            sub = h.helicsFederateRegisterSubscription(combination_federate, sub_key, input.input_unit)
            input.helics_input = sub
            input.helics_sub_key = sub_key

        self.commands_message_enpoint = h.helicsFederateRegisterEndpoint(combination_federate, "commands")

    def init_federate(self, esdl_helper : EsdlHelper):

        federate_info = self.init_federate_info(self.helics_value_federate_info, self.simulator_configuration)
        combination_federate = h.helicsCreateCombinationFederate(f"{self.simulator_configuration.model_id}/{self.helics_value_federate_info.calculation_name}", federate_info)

        self.init_inputs(self.helics_value_federate_info, esdl_helper, combination_federate)
        self.init_outputs(self.helics_value_federate_info, combination_federate)
        self.combination_federate = combination_federate
        self.energy_system = esdl_helper.energy_system

    def get_helics_value(self, helics_sub : CalculationServiceInput):
        LOGGER.debug(f"Getting value for subscription: {helics_sub.input_name} with type: {helics_sub.input_type}")
        input_type = helics_sub.input_type
        sub = helics_sub.helics_input
        ret_val = None
        if h.helicsInputIsUpdated(sub):
            if input_type == h.HelicsDataType.BOOLEAN:
                ret_val = h.helicsInputGetBoolean(sub)
            elif input_type == h.HelicsDataType.COMPLEX_VECTOR:
                ret_val = h.helicsInputGetComplexVector(sub)
            elif input_type == h.HelicsDataType.DOUBLE:
                ret_val = h.helicsInputGetDouble(sub)
            elif input_type == h.HelicsDataType.COMPLEX:
                ret_val = h.helicsInputGetComplex(sub)
            elif input_type == h.HelicsDataType.INT:
                ret_val = h.helicsInputGetInteger(sub)
            elif input_type == h.HelicsDataType.JSON:
                ret_val = h.helicsInputGetString(sub)
            elif input_type == h.HelicsDataType.NAMED_POINT:
                ret_val = h.helicsInputGetNamedPoint(sub)
            elif input_type == h.HelicsDataType.STRING:
                ret_val = h.helicsInputGetString(sub)
            elif input_type == h.HelicsDataType.RAW:
                ret_val = h.helicsInputGetRawValue(sub)
            elif input_type == h.HelicsDataType.TIME:
                ret_val = h.helicsInputGetTime(sub)
            elif input_type == h.HelicsDataType.VECTOR:
                ret_val = h.helicsInputGetVector(sub)
            elif input_type == h.HelicsDataType.ANY:
                ret_val = h.helicsInputGetBytes(sub)
            else:
                raise ValueError("Unsupported Helics Data Type")
        return ret_val

    def publish_helics_value(self, helics_output : CalculationServiceOutput, value):
        LOGGER.debug(f"Publishing value: {value} for publication: {helics_output.output_name} with type: {helics_output.output_type}")
        pub = helics_output.helics_publication
        output_type = helics_output.output_type
        if output_type == h.HelicsDataType.BOOLEAN:
            h.helicsPublicationPublishBoolean(pub, value)
        elif output_type == h.HelicsDataType.COMPLEX_VECTOR:
            h.helicsPublicationPublishComplexVector(pub, value)
        elif output_type == h.HelicsDataType.DOUBLE:
            h.helicsPublicationPublishDouble(pub, value)
        elif output_type == h.HelicsDataType.COMPLEX:
            h.helicsPublicationPublishComplex(pub, value)
        elif output_type == h.HelicsDataType.INT:
            h.helicsPublicationPublishInteger(pub, value)
        elif output_type == h.HelicsDataType.JSON:
            h.helicsPublicationPublishString(pub, value)
        elif output_type == h.HelicsDataType.NAMED_POINT:
            h.helicsPublicationPublishNamedPoint(pub, value)
        elif output_type == h.HelicsDataType.STRING:
            h.helicsPublicationPublishString(pub, value)
        elif output_type == h.HelicsDataType.RAW:
            h.helicsPublicationPublishRaw(pub, value)
        elif output_type == h.HelicsDataType.TIME:
            h.helicsPublicationPublishTime(pub, value)
        elif output_type == h.HelicsDataType.VECTOR:
            h.helicsPublicationPublishVector(pub, value)
        elif output_type == h.HelicsDataType.ANY:
            h.helicsPublicationPublishBytes(pub, value)
        else:
            raise ValueError("Unsupported Helics Data Type")

    def start_combination_federate(self):
        self.enter_simulation_loop()
        Common.destroy_federate(self.combination_federate)

    def _compute_time_step_number(self, granted_time : h.HelicsTime, period : float):
        if period == 0:
            raise Exception(f"Period cannot be zero for calculation {self.helics_value_federate_info.calculation_name}")
        return int(math.floor(granted_time / period))

    def _get_calculation_service_max_timestamp(self, simulation_duration_in_seconds : int, period : float):
        return int(math.floor(simulation_duration_in_seconds / period))
    
    def _init_calculation_params(self):
        ret_val = {}
        for esdl_id in self.simulator_configuration.esdl_ids:
            if esdl_id in self.input_dict:
                inputs = self.input_dict[esdl_id]
                for helics_input in inputs:
                    ret_val[helics_input.helics_sub_key] = None
        return ret_val

    def enter_simulation_loop(self):
        LOGGER.info(f"Entering HELICS execution mode {self.helics_value_federate_info.calculation_name}")
        h.helicsFederateEnterExecutingMode(self.combination_federate)
        LOGGER.info(f"Entered HELICS execution mode {self.helics_value_federate_info.calculation_name}")
        federate_name = h.helicsFederateGetName(self.combination_federate)

        total_interval = self.simulator_configuration.simulation_duration_in_seconds
        update_interval = int(h.helicsFederateGetTimeProperty(self.combination_federate, h.HELICS_PROPERTY_TIME_PERIOD))
        max_time_step_number = self._get_calculation_service_max_timestamp(total_interval, update_interval)
        granted_time = 0
        terminate_requested = False
        calculation_params = self._init_calculation_params()
        while granted_time < total_interval and not terminate_requested:
            requested_time = self._get_request_time(update_interval, granted_time)
            LOGGER.debug(f"Requesting time: {requested_time} for calculation {self.helics_value_federate_info.calculation_name}")
            granted_time = h.helicsFederateRequestTime(self.combination_federate, requested_time)
            LOGGER.debug(f"Time granted: {granted_time} for calculation {self.helics_value_federate_info.calculation_name}")

            simulator_time = self.simulator_configuration.start_time + timedelta(seconds = granted_time)
            time_step_number = self._compute_time_step_number(granted_time, update_interval)
            time_step_information = TimeStepInformation(time_step_number, max_time_step_number)
            for esdl_id in self.simulator_configuration.esdl_ids:
                if not terminate_requested:
                    if esdl_id in self.input_dict:
                        inputs = self.input_dict[esdl_id]
                        for helics_input in inputs:
                            if calculation_params[helics_input.helics_sub_key] == None:
                                calculation_params[helics_input.helics_sub_key] = self.get_helics_value(helics_input)
                    try:
                        if CalculationServiceHelperFunctions.dictionary_has_values_for_all_keys(calculation_params):
                            LOGGER.info(f"Executing calculation {self.helics_value_federate_info.calculation_name} for esdl_id {esdl_id} at time {granted_time}")
                            pub_values = self.helics_value_federate_info.calculation_function(calculation_params, simulator_time, time_step_information, esdl_id, self.energy_system)
                            LOGGER.info(f"Finished calculation {self.helics_value_federate_info.calculation_name} for esdl_id {esdl_id} at time {granted_time}")
                            LOGGER.debug(f"Publishing Values: {self.output_dict}")

                            if len(self.helics_value_federate_info.outputs) > 0:
                                outputs = self.output_dict[esdl_id]
                                for output in outputs:
                                    value_to_publish = pub_values[output.output_name]
                                    self.publish_helics_value(output, value_to_publish)
                            calculation_params = CalculationServiceHelperFunctions.clear_dictionary_values(calculation_params)
                    except Exception:
                        LOGGER.info(f"Exception occurred for esdl_id {esdl_id} at time {granted_time} terminating simulation...")
                        traceback.print_exc()
                        Common.terminate_simulation(self.combination_federate, self.commands_message_enpoint)
                        terminate_requested = True

            LOGGER.info(f"Finished {granted_time} of {total_interval} and terminate requested {terminate_requested} for federate with name {federate_name}")

            terminate_requested = Common.terminate_requested_at_commands_endpoint(self.commands_message_enpoint)

        LOGGER.info(f"Finalizing federate at {granted_time} of {total_interval} and terminate requested {terminate_requested} with name {federate_name}")

    def _get_request_time(self, update_interval, granted_time):
        requested_time = 0
        if self.helics_value_federate_info.time_request_type == TimeRequestType.PERIOD and granted_time > 0:
            requested_time = granted_time + update_interval
        if self.helics_value_federate_info.time_request_type == TimeRequestType.ON_INPUT:
            requested_time = h.HELICS_TIME_MAXTIME
        return requested_time

class HelicsSimulationExecutor:

    def __init__(self):
        self.simulator_configuration = CalculationServiceHelperFunctions.get_simulator_configuration_from_environment()
        self.calculations: List[HelicsCombinationFederateExecutor] = []
        self.energy_system = None
        self.influx_connector = InfluxDBConnector(self.simulator_configuration.influx_host, self.simulator_configuration.influx_port, self.simulator_configuration.influx_username, self.simulator_configuration.influx_password, self.simulator_configuration.influx_database_name)

    def add_calculation(self, info : HelicsCalculationInformation):
        if info.inputs == None:
            info.inputs = []
        if info.outputs == None:
            info.outputs = []
        self.calculations.append(HelicsCombinationFederateExecutor(info))

    def _get_esdl_from_so(self):
        esdl_message_federate = HelicsEsdlMessageFederateExecutor(HelicsMessageFederateInformation(60, TimeRequestType.ON_INPUT, 60, False, False, True, 'esdl'))
        esdl_message_federate.init_federate()
        esdl_helper = esdl_message_federate.wait_for_esdl_file()
        return esdl_helper

    def _init_influxdb(self, esdl_helper : EsdlHelper):
        esdl_objects = esdl_helper.esdl_object_mapping
        self.influx_connector.init_profile_output_data(self.simulator_configuration.simulation_id, self.simulator_configuration.model_id, self.simulator_configuration.esdl_type, esdl_objects)
        self.influx_connector.connect()

    def init_calculation_service(self, energy_system : esdl.EnergySystem):
        pass

    def init_simulation(self) -> esdl.EnergySystem:
        esdl_helper = self._get_esdl_from_so()
        self._init_influxdb(esdl_helper)
        self.init_calculation_service(esdl_helper.energy_system)
        return esdl_helper

    def start_simulation(self):
        esdl_helper = self.init_simulation()
        self.exe = ThreadPoolExecutor(len(self.calculations))
        for calculation in self.calculations:
            calculation.init_federate(esdl_helper)
        for calculation in self.calculations:
            self.exe.submit(calculation.start_combination_federate)

    def stop_simulation(self):
        self.exe.shutdown()
        LOGGER.debug(f"Writing data to influx for calculation service {self.simulator_configuration.model_id}")
        self.influx_connector.write_output()