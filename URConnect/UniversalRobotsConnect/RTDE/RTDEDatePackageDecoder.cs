using System;
using System.Collections;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace UniversalRobotsConnect
{
    class RTDEDatePackageDecoder
    {
        private List<KeyValuePair<string, string>> _rtdeOutputConfiguration;
        private ConcurrentQueue<byte[]> _rtdeDataPackageQueue;
        private ConcurrentQueue<RobotModel> _updateModelQueue;

        public RTDEDatePackageDecoder(List<KeyValuePair<string, string>> rtdeOutputConfiguration, ConcurrentQueue<byte[]> rtdeDataPackageQueue, ConcurrentQueue<RobotModel> robotData)
        {
            this._rtdeOutputConfiguration = rtdeOutputConfiguration;
            this._rtdeDataPackageQueue = rtdeDataPackageQueue;
            this._updateModelQueue = robotData;

            Thread rtdeDataDecoderThread = new Thread(RtdeDataDecoder);
            rtdeDataDecoderThread.Start();
        }

        private void RtdeDataDecoder()
        {
            while (true)
            {
                byte[] rtdeDataPackage; 
                if (_rtdeDataPackageQueue.Count > 0)
                {
                    bool success = _rtdeDataPackageQueue.TryDequeue(out rtdeDataPackage);
                    if (success)
                    {
                        //Console.WriteLine("De Queued a RTDE Data package - now need to decode");
                        var localRobotModel = DecodeRTDEDataPackage(rtdeDataPackage);
                        _updateModelQueue.Enqueue(localRobotModel);
                    }
                    if (_rtdeDataPackageQueue.Count > 5)
                    {
                        Console.WriteLine($"RTDE DATA Packages in queue: {_rtdeDataPackageQueue.Count}");
                    }
                }
                Thread.Sleep(2);
            }
        }


        private RobotModel DecodeRTDEDataPackage(byte[] payloadArray)
        {
            DateTime startDecodeTime = DateTime.Now;
            RobotModel localRobotModel = new RobotModel();

            int payloadArrayIndex = 0;
            foreach (KeyValuePair<string, string> keyValuePair in _rtdeOutputConfiguration)
            {

                if (keyValuePair.Value == "DOUBLE")
                {
                    DecodeKeyValuePair(keyValuePair.Key, GetDoubleFromPayloadArray(payloadArray, ref payloadArrayIndex), ref localRobotModel);
                }
                else if (keyValuePair.Value == "UINT64")
                {
                    DecodeKeyValuePair(keyValuePair.Key, GetUint64FromPayloadArray(payloadArray, ref payloadArrayIndex), ref localRobotModel);
                }
                else if (keyValuePair.Value == "VECTOR6D")
                {
                    DecodeKeyValuePair(keyValuePair.Key, GetVector6DFromPayloadArray(payloadArray, ref payloadArrayIndex), ref localRobotModel);
                }
                else if (keyValuePair.Value == "INT32")
                {
                    DecodeKeyValuePair(keyValuePair.Key, GetInt32FromPayloadArray(payloadArray, ref payloadArrayIndex), ref localRobotModel);
                }
                else if (keyValuePair.Value == "VECTOR6INT32")
                {
                    DecodeKeyValuePair(keyValuePair.Key, GetVector6DInt32FromPayloadArray(payloadArray, ref payloadArrayIndex), ref localRobotModel);
                }
                else if (keyValuePair.Value == "VECTOR3D")
                {
                    DecodeKeyValuePair(keyValuePair.Key, GetVector3DFromPayloadArray(payloadArray, ref payloadArrayIndex), ref localRobotModel);
                }
                else if (keyValuePair.Value == "UINT32")
                {
                    DecodeKeyValuePair(keyValuePair.Key, GetUInt32FromPayloadArray(payloadArray, ref payloadArrayIndex), ref localRobotModel);
                }
                else
                {
                    throw new NotImplementedException("Got a datatype in RTDE Data Package with a value of " + keyValuePair.Value + " that we did not expect");
                }
                //    //DateTime finishDecodeTime = DateTime.Now;
                //    //TimeSpan decodetime = finishDecodeTime - startDecodeTime;
                //    //if (decodetime.TotalMilliseconds > 3)
                //    //{
                //    //    Console.WriteLine($"{keyValuePair.Key} Took too long to decode {decodetime.TotalMilliseconds} milliseconds");
                //    //}
            }

            if (payloadArrayIndex != payloadArray.Length)
            {
                //log.Error("Did not decode all the data");
                throw new ArgumentOutOfRangeException("Did not decode all the data");
            }
            
            DateTime finishDecodeTime = DateTime.Now;
            TimeSpan decodetime = finishDecodeTime - startDecodeTime;
            if (decodetime.TotalMilliseconds > 4)
            {
                Console.WriteLine($"RTDE DATA Package took too long to decode {decodetime.TotalMilliseconds} milliseconds");
            }
            return localRobotModel;
        }

        private void DecodeKeyValuePair(string key, object value, ref RobotModel localRobotModel)
        {
            double timestamp;   //Set last as we are using this for a clock
            switch (key)
            {
                case "timestamp":
                    timestamp = (double)value;
                    //double delta = timestamp - _robotModel.RobotTimestamp;
                    //if (0.0079 > delta || delta > 0.0081)
                    //{
                    //    Debug.WriteLine($"Robot Time Error of {delta} milliseconds");
                    //    //log.Error($"{delta * 1000} Milliseconds since last RTDE");
                    //}
                    localRobotModel.RobotTimestamp = timestamp;
                    break;
                case "target_q":
                    localRobotModel.TargetQ = (double[])value;
                    break;
                case "target_qd":
                    localRobotModel.TargetQD = (double[])value;
                    break;
                case "target_qdd":
                    localRobotModel.TargetQDD = (double[])value;
                    break;
                case "target_current":
                    localRobotModel.TargetCurrent = (double[])value;
                    break;
                case "target_moment":
                    localRobotModel.TargetMoment = (double[])value;
                    break;
                case "actual_q":
                    localRobotModel.ActualQ = (double[])value;
                    break;
                case "actual_qd":
                    localRobotModel.ActualQD = (double[])value;
                    break;
                case "actual_current":
                    localRobotModel.ActualCurrent = (double[])value;
                    break;
                case "joint_control_output":
                    localRobotModel.JointControlOutput = (double[])value;
                    break;
                case "actual_TCP_pose":
                    localRobotModel.ActualTCPPose = (double[])value;
                    break;
                case "actual_TCP_speed":
                    localRobotModel.ActualTCPSpeed = (double[])value;
                    break;
                case "actual_TCP_force":
                    localRobotModel.ActualTCPForce = (double[])value;
                    break;
                case "target_TCP_pose":
                    localRobotModel.TargetTCPPose = (double[])value;
                    break;
                case "target_TCP_speed":
                    localRobotModel.TargetTCPSpeed = (double[])value;
                    break;
                case "actual_digital_input_bits":
                    byte[] bytes = BitConverter.GetBytes((UInt64)value);
                    localRobotModel.DigitalInputbits.AllBits = new BitArray(new byte[] { (byte)bytes[0] });
                    localRobotModel.ConfigurableInputBits.AllBits = new BitArray(new byte[] { (byte)bytes[1] });
                    break;
                case "joint_temperatures":
                    localRobotModel.JointTemperatures = (double[])value;
                    break;
                case "actual_execution_time":
                    localRobotModel.ActualExecutionTime = (double)value;
                    break;
                case "robot_mode":
                    localRobotModel.RobotMode = (RobotMode)(int)value;
                    break;
                case "joint_mode":
                    localRobotModel.JointMode = (double[])value;
                    break;
                case "safety_mode":
                    localRobotModel.SafetyMode = (SafetyMode)(int)value;
                    break;
                case "actual_tool_accelerometer":
                    localRobotModel.ActualToolAccelerometer = (double[])value;
                    break;
                case "speed_scaling":
                    localRobotModel.SpeedScaling = (double)value;
                    break;
                case "target_speed_fraction":
                    localRobotModel.TargetSpeedFraction = (double)value;
                    break;
                case "actual_momentum":
                    localRobotModel.ActualMomentum = (double)value;
                    break;
                case "actual_main_voltage":
                    localRobotModel.ActualMainVoltage = (double)value;
                    break;
                case "actual_robot_voltage":
                    localRobotModel.ActualRobotVoltage = (double)value;
                    break;
                case "actual_robot_current":
                    localRobotModel.ActualRobotCurrent = (double)value;
                    break;
                case "actual_joint_voltage":
                    localRobotModel.ActualJointVoltage = (double[])value;
                    break;
                case "actual_digital_output_bits":
                    byte[] outputBytes = BitConverter.GetBytes((UInt64)value);
                    localRobotModel.DigitalOutputBits.AllBits = new BitArray(new byte[] { (byte)outputBytes[0] });
                    localRobotModel.ConfigurableOutputBits.AllBits = new BitArray(new byte[] { (byte)outputBytes[1] });
                    break;
                case "runtime_state":
                    localRobotModel.RuntimeState = (RuntimeState)(uint)value;
                    break;
                case "robot_status_bits":
                    BitArray statusBitArray = new BitArray(new byte[] { (byte)(UInt32)value });
                    localRobotModel.RobotStatus.PowerOn = statusBitArray[0];
                    localRobotModel.RobotStatus.ProgramRunning = statusBitArray[1];
                    localRobotModel.RobotStatus.TeachButtonPressed = statusBitArray[2];
                    localRobotModel.RobotStatus.PowerButtonPressed = statusBitArray[3];
                    break;
                case "safety_status_bits":
                    byte[] bytearray = BitConverter.GetBytes((UInt32)value);
                    BitArray safetystatusBitArray1 = new BitArray(new byte[] { (byte)bytearray[0] });
                    localRobotModel.SafetyStatus.NormalMode = safetystatusBitArray1[0];
                    localRobotModel.SafetyStatus.ReducedMode = safetystatusBitArray1[1];
                    localRobotModel.SafetyStatus.ProtectiveStopped = safetystatusBitArray1[2];
                    localRobotModel.SafetyStatus.RecoveryMode = safetystatusBitArray1[3];
                    localRobotModel.SafetyStatus.SafeguardStopped = safetystatusBitArray1[4];
                    localRobotModel.SafetyStatus.SystemEmergencyStopped = safetystatusBitArray1[5];
                    localRobotModel.SafetyStatus.RobotEmergencyStopped = safetystatusBitArray1[6];
                    localRobotModel.SafetyStatus.EmergencyStopped = safetystatusBitArray1[7];
                    BitArray safetystatusBitArray2 = new BitArray(new byte[] { (byte)bytearray[1] });
                    localRobotModel.SafetyStatus.Violation = safetystatusBitArray2[0];
                    localRobotModel.SafetyStatus.Fault = safetystatusBitArray2[1];
                    localRobotModel.SafetyStatus.StoppedDueToSafety = safetystatusBitArray2[2];
                    break;

                case "analog_io_types":
                    throw new NotImplementedException("analog_io_types");
                    //localRobotModel.AnalogIOTypes = (UInt32) value;   //ToDo - this is voltage or current for Analog IO - handle nicely
                    break;
                case "standard_analog_input0":
                    localRobotModel.StandardAnalogInput0 = (double)value;
                    break;

                case "standard_analog_input1":
                    localRobotModel.StandardAnalogInput1 = (double)value;
                    break;
                case "standard_analog_output0":
                    localRobotModel.StandardAnalogOutput0 = (double)value;
                    break;
                case "standard_analog_output1":
                    localRobotModel.StandardAnalogOutput = (double)value;
                    break;
                case "io_current":
                    localRobotModel.IOCurrent = (double)value;
                    break;
                case "euromap67_input_bits":
                    throw new NotImplementedException("euromap67_input_bits");
                    break;
                case "euromap67_output_bits":
                    throw new NotImplementedException("euromap67_output_bits");
                    break;
                case "euromap67_24V_voltage":
                    throw new NotImplementedException("euromap67_24V_voltage");
                    break;
                case "euromap67_24V_current":
                    throw new NotImplementedException("euromap67_24V_current");
                    break;
                case "tool_mode":
                    throw new NotImplementedException("tool_mode");
                    //localRobotModel.ToolMode = (UInt32) value;    //Todo - dont know what this is .. need to figure out
                    break;
                case "tool_analog_input_types":
                    throw new NotImplementedException("tool_analog_input_types");
                    //localRobotModel.ToolAnalogInputTypes = (UInt32) value;    //ToDo - this is voltage or current for Analog Input at the tool - handle nicely
                    break;
                case "tool_analog_input0":
                    localRobotModel.ToolAnalogInput0 = (double)value;
                    break;
                case "tool_analog_input1":
                    localRobotModel.ToolAnalogInput1 = (double)value;
                    break;
                case "tool_output_voltage":
                    localRobotModel.ToolOutputVoltage = (int)value;
                    break;
                case "tool_output_current":
                    localRobotModel.ToolOutputCurrent = (double)value;
                    break;
                case "tcp_force_scalar":
                    localRobotModel.TCPForceScalar = (double)value;
                    break;
                #region outputBitRegisters

                case "output_bit_registers0_to_31":
                    localRobotModel.OutputBitRegister.SetOutputBitRegisters0to31 = new BitArray(BitConverter.GetBytes((UInt32)value));
                    break;
                case "output_bit_registers32_to_63":
                    localRobotModel.OutputBitRegister.SetOutputBitRegisters32to63 = new BitArray(BitConverter.GetBytes((UInt32)value));
                    break;

                #endregion

                #region outputIntRegisters
                case "output_int_register_0":
                    localRobotModel.OutputIntRegister.Register0 = (int)value;
                    break;
                case "output_int_register_1":
                    localRobotModel.OutputIntRegister.Register1 = (int)value;
                    break;
                case "output_int_register_2":
                    localRobotModel.OutputIntRegister.Register2 = (int)value;
                    break;
                case "output_int_register_3":
                    localRobotModel.OutputIntRegister.Register3 = (int)value;
                    break;
                case "output_int_register_4":
                    localRobotModel.OutputIntRegister.Register4 = (int)value;
                    break;
                case "output_int_register_5":
                    localRobotModel.OutputIntRegister.Register5 = (int)value;
                    break;
                case "output_int_register_6":
                    localRobotModel.OutputIntRegister.Register6 = (int)value;
                    break;
                case "output_int_register_7":
                    localRobotModel.OutputIntRegister.Register7 = (int)value;
                    break;
                case "output_int_register_8":
                    localRobotModel.OutputIntRegister.Register8 = (int)value;
                    break;
                case "output_int_register_9":
                    localRobotModel.OutputIntRegister.Register9 = (int)value;
                    break;
                case "output_int_register_10":
                    localRobotModel.OutputIntRegister.Register10 = (int)value;
                    break;
                case "output_int_register_11":
                    localRobotModel.OutputIntRegister.Register11 = (int)value;
                    break;
                case "output_int_register_12":
                    localRobotModel.OutputIntRegister.Register12 = (int)value;
                    break;
                case "output_int_register_13":
                    localRobotModel.OutputIntRegister.Register13 = (int)value;
                    break;
                case "output_int_register_14":
                    localRobotModel.OutputIntRegister.Register14 = (int)value;
                    break;
                case "output_int_register_15":
                    localRobotModel.OutputIntRegister.Register15 = (int)value;
                    break;
                case "output_int_register_16":
                    localRobotModel.OutputIntRegister.Register16 = (int)value;
                    break;
                case "output_int_register_17":
                    localRobotModel.OutputIntRegister.Register17 = (int)value;
                    break;
                case "output_int_register_18":
                    localRobotModel.OutputIntRegister.Register18 = (int)value;
                    break;
                case "output_int_register_19":
                    localRobotModel.OutputIntRegister.Register19 = (int)value;
                    break;
                case "output_int_register_20":
                    localRobotModel.OutputIntRegister.Register20 = (int)value;
                    break;
                case "output_int_register_21":
                    localRobotModel.OutputIntRegister.Register21 = (int)value;
                    break;
                case "output_int_register_22":
                    localRobotModel.OutputIntRegister.Register22 = (int)value;
                    break;
                case "output_int_register_23":
                    localRobotModel.OutputIntRegister.Register23 = (int)value;
                    break;

                #endregion

                #region outputDoubleRegisters
                case "output_double_register_0":
                    localRobotModel.OutputDoubleRegister.Register0 = (double)value;
                    break;
                case "output_double_register_1":
                    localRobotModel.OutputDoubleRegister.Register1 = (double)value;
                    break;
                case "output_double_register_2":
                    localRobotModel.OutputDoubleRegister.Register2 = (double)value;
                    break;
                case "output_double_register_3":
                    localRobotModel.OutputDoubleRegister.Register3 = (double)value;
                    break;
                case "output_double_register_4":
                    localRobotModel.OutputDoubleRegister.Register4 = (double)value;
                    break;
                case "output_double_register_5":
                    localRobotModel.OutputDoubleRegister.Register5 = (double)value;
                    break;
                case "output_double_register_6":
                    localRobotModel.OutputDoubleRegister.Register6 = (double)value;
                    break;
                case "output_double_register_7":
                    localRobotModel.OutputDoubleRegister.Register7 = (double)value;
                    break;
                case "output_double_register_8":
                    localRobotModel.OutputDoubleRegister.Register8 = (double)value;
                    break;
                case "output_double_register_9":
                    localRobotModel.OutputDoubleRegister.Register9 = (double)value;
                    break;
                case "output_double_register_10":
                    localRobotModel.OutputDoubleRegister.Register10 = (double)value;
                    break;
                case "output_double_register_11":
                    localRobotModel.OutputDoubleRegister.Register11 = (double)value;
                    break;
                case "output_double_register_12":
                    localRobotModel.OutputDoubleRegister.Register12 = (double)value;
                    break;
                case "output_double_register_13":
                    localRobotModel.OutputDoubleRegister.Register13 = (double)value;
                    break;
                case "output_double_register_14":
                    localRobotModel.OutputDoubleRegister.Register14 = (double)value;
                    break;
                case "output_double_register_15":
                    localRobotModel.OutputDoubleRegister.Register15 = (double)value;
                    break;
                case "output_double_register_16":
                    localRobotModel.OutputDoubleRegister.Register16 = (double)value;
                    break;
                case "output_double_register_17":
                    localRobotModel.OutputDoubleRegister.Register17 = (double)value;
                    break;
                case "output_double_register_18":
                    localRobotModel.OutputDoubleRegister.Register18 = (double)value;
                    break;
                case "output_double_register_19":
                    localRobotModel.OutputDoubleRegister.Register19 = (double)value;
                    break;
                case "output_double_register_20":
                    localRobotModel.OutputDoubleRegister.Register20 = (double)value;
                    break;
                case "output_double_register_21":
                    localRobotModel.OutputDoubleRegister.Register21 = (double)value;
                    break;
                case "output_double_register_22":
                    localRobotModel.OutputDoubleRegister.Register22 = (double)value;
                    break;
                case "output_double_register_23":
                    localRobotModel.OutputDoubleRegister.Register23 = (double)value;
                    break;


                #endregion
                default:
                    throw new NotImplementedException("Did not find any handling for " + key);
            }
        }



        private object GetVector3DFromPayloadArray(byte[] payloadArray, ref int payloadArrayIndex)
        {
            var x = GetDoubleFromPayloadArray(payloadArray, ref payloadArrayIndex);
            var y = GetDoubleFromPayloadArray(payloadArray, ref payloadArrayIndex);
            var z = GetDoubleFromPayloadArray(payloadArray, ref payloadArrayIndex);
            return new double[] { x, y, z };
        }

        private object GetVector6DInt32FromPayloadArray(byte[] payloadArray, ref int payloadArrayIndex)
        {
            var x = GetInt32FromPayloadArray(payloadArray, ref payloadArrayIndex);
            var y = GetInt32FromPayloadArray(payloadArray, ref payloadArrayIndex);
            var z = GetInt32FromPayloadArray(payloadArray, ref payloadArrayIndex);
            var rx = GetInt32FromPayloadArray(payloadArray, ref payloadArrayIndex);
            var ry = GetInt32FromPayloadArray(payloadArray, ref payloadArrayIndex);
            var rz = GetInt32FromPayloadArray(payloadArray, ref payloadArrayIndex);
            return new double[]
            {
                x, y, z, rx, ry, rz
            };
        }


        private double[] GetVector6DFromPayloadArray(byte[] payloadArray, ref int payloadArrayIndex)
        {
            var x = GetDoubleFromPayloadArray(payloadArray, ref payloadArrayIndex);
            var y = GetDoubleFromPayloadArray(payloadArray, ref payloadArrayIndex);
            var z = GetDoubleFromPayloadArray(payloadArray, ref payloadArrayIndex);
            var rx = GetDoubleFromPayloadArray(payloadArray, ref payloadArrayIndex);
            var ry = GetDoubleFromPayloadArray(payloadArray, ref payloadArrayIndex);
            var rz = GetDoubleFromPayloadArray(payloadArray, ref payloadArrayIndex);
            return new double[] { x, y, z, rx, ry, rz };
        }

        private double GetDoubleFromPayloadArray(byte[] payloadArray, ref int payloadArrayIndex)
        {
            byte[] bytes = new byte[8];
            Array.Copy(payloadArray, payloadArrayIndex, bytes, 0, 8);
            bytes = CheckEndian(bytes);
            payloadArrayIndex = payloadArrayIndex + 8;
            return BitConverter.ToDouble(bytes, 0);
        }

        private UInt32 GetUInt32FromPayloadArray(byte[] payloadArray, ref int payloadArrayIndex)
        {
            byte[] bytes = new byte[4];
            Array.Copy(payloadArray, payloadArrayIndex, bytes, 0, 4);
            bytes = CheckEndian(bytes);
            payloadArrayIndex = payloadArrayIndex + 4;
            return BitConverter.ToUInt32(bytes, 0);
        }

        private Int32 GetInt32FromPayloadArray(byte[] payloadArray, ref int payloadArrayIndex)
        {
            byte[] bytes = new byte[4];
            Array.Copy(payloadArray, payloadArrayIndex, bytes, 0, 4);
            bytes = CheckEndian(bytes);
            payloadArrayIndex = payloadArrayIndex + 4;
            return BitConverter.ToInt32(bytes, 0);
        }

        private UInt64 GetUint64FromPayloadArray(byte[] payloadArray, ref int payloadArrayIndex)
        {
            byte[] bytes = new byte[8];
            Array.Copy(payloadArray, payloadArrayIndex, bytes, 0, 8);
            bytes = CheckEndian(bytes);
            payloadArrayIndex = payloadArrayIndex + 8;
            return BitConverter.ToUInt64(bytes, 0);
        }

        internal static byte[] CheckEndian(byte[] input)    //dublet .. flyt til utilities 
        {
            if (BitConverter.IsLittleEndian)
                Array.Reverse(input);
            return input;
        }
    }
}
