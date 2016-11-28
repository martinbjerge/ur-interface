using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using log4net;
using UniversalRobotsConnect.Types;

namespace UniversalRobotsConnect
{
    class RTDEReceiver
    {
        private static readonly ILog log = LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        internal event EventHandler<DataReceivedEventArgs> DataReceived;
        private NetworkStream _stream;
        private Thread _receiverThread;
        private RobotModel _robotModel;
        private List<KeyValuePair<string, string>> _rtdeOutputConfiguration;
        private List<KeyValuePair<string, string>> _rtdeInputConfiguration;
        private List<byte[]> _packageList = new List<byte[]>();
        private Thread _packageDecoderThread;

        internal RTDEReceiver(NetworkStream stream, RobotModel robotModel, List<KeyValuePair<string, string>> rtdeOutputConfiguration, List<KeyValuePair<string, string>> rtdeInputConfiguration)
        {
            _robotModel = robotModel;
            _stream = stream;
            _rtdeOutputConfiguration = rtdeOutputConfiguration;
            _rtdeInputConfiguration = rtdeInputConfiguration;
            _packageDecoderThread = new Thread(PacageDecoder);
            _packageDecoderThread.Start();
            _receiverThread = new Thread(Run);
            _receiverThread.Start();
        }

        private void Run()
        {
            //// main thread loop for receiving data...
            while (true)
            {
                if (_stream.DataAvailable)
                {
                    if (_stream.CanRead)
                    {
                        byte[] myReadBuffer = new byte[65000];
                        int numberOfBytesRead = 0;
                        do
                        {
                            numberOfBytesRead = _stream.Read(myReadBuffer, 0, myReadBuffer.Length);
                        }
                        while (_stream.DataAvailable);

                        byte[] package =  new byte[numberOfBytesRead];
                        Array.Copy(myReadBuffer, package, numberOfBytesRead);
                        _packageList.Add(package);
                    }
                    else
                    {
                        Debug.WriteLine("Sorry.  You cannot read from this NetworkStream.");
                        throw new SystemException();
                    }
                }
            }
        }

        private void PacageDecoder()
        {
            while (true)
            {
                if (_packageList.Count > 0)
                {
                    if (_packageList[0] != null)
                    {
                        DecodePacage(_packageList[0]);
                        _packageList.RemoveAt(0);
                    }
                }
                Thread.Sleep(2);
            }
        }

        private void DecodePacage(byte[] recievedPackage)
        {
            byte[] sizeArray = new byte[2];
            UR_RTDE_Command type = (UR_RTDE_Command) recievedPackage[2];
            Array.Copy(recievedPackage, sizeArray, 2);
            sizeArray = CheckEndian(sizeArray);
            ushort size = BitConverter.ToUInt16(sizeArray, 0);
            if ((size > 3) && (size == recievedPackage.Length) )
            {
                byte[] payloadArray = new byte[size - 3];
                Array.Copy(recievedPackage, 3, payloadArray, 0, size - 3);

                switch (type)
                {
                    case UR_RTDE_Command.RTDE_REQUEST_PROTOCOL_VERSION:
                        _robotModel.RTDEProtocolVersion = DecodeProtocolVersion(payloadArray);
                        break;
                    case UR_RTDE_Command.RTDE_GET_URCONTROL_VERSION:
                        DecodeUniversalRobotsControllerVersion(payloadArray);
                        break;
                    case UR_RTDE_Command.RTDE_CONTROL_PACKAGE_SETUP_OUTPUTS:
                        DecodeRTDESetupPackage(payloadArray, _rtdeOutputConfiguration);
                        break;
                    case UR_RTDE_Command.RTDE_CONTROL_PACKAGE_SETUP_INPUTS:
                        DecodeRTDESetupPackage(payloadArray, _rtdeInputConfiguration);
                        break;
                    case UR_RTDE_Command.RTDE_DATA_PACKAGE:
                        DecodeRTDEDataPackage(payloadArray);
                        break;
                    case UR_RTDE_Command.RTDE_CONTROL_PACKAGE_START:
                        _robotModel.RTDEConnectionState = DecodeRTDEControlPackageStart(payloadArray);
                        break;
                    case UR_RTDE_Command.RTDE_CONTROL_PACKAGE_PAUSE:
                        _robotModel.RTDEConnectionState = DecodeRTDEControlPacagePause(payloadArray);
                        break;
                    default:
                        log.Error("Package type not implemented " + type);
                        //throw new NotImplementedException("Package type not implemented " + type);  
                        break;
                }
            }
            else
            {
                //log.Error("Got a packet of unexpected size");  
                //throw new Exception("Got a packet of unexpected size");
            }
        }

        

        private void DecodeRTDEDataPackage(byte[] payloadArray)
        {
            int payloadArrayIndex = 0;
            foreach (KeyValuePair<string, string> keyValuePair in _rtdeOutputConfiguration)
            {
                if (keyValuePair.Value == "DOUBLE")
                {
                    UpdateModel(keyValuePair.Key, GetDoubleFromPayloadArray(payloadArray, ref payloadArrayIndex));
                }
                else if (keyValuePair.Value == "UINT64")
                {
                    UpdateModel(keyValuePair.Key, GetUint64FromPayloadArray(payloadArray, ref payloadArrayIndex));
                }
                else if (keyValuePair.Value == "VECTOR6D")
                {
                    UpdateModel(keyValuePair.Key, GetVector6DFromPayloadArray(payloadArray, ref payloadArrayIndex));
                }
                else if (keyValuePair.Value == "INT32")
                {
                    UpdateModel(keyValuePair.Key, GetInt32FromPayloadArray(payloadArray, ref payloadArrayIndex));
                }
                else if (keyValuePair.Value == "VECTOR6INT32")
                {
                    UpdateModel(keyValuePair.Key, GetVector6DInt32FromPayloadArray(payloadArray, ref payloadArrayIndex));
                }
                else if (keyValuePair.Value == "VECTOR3D")
                {
                    UpdateModel(keyValuePair.Key, GetVector3DFromPayloadArray(payloadArray, ref payloadArrayIndex));
                }
                else if (keyValuePair.Value == "UINT32")
                {
                    UpdateModel(keyValuePair.Key, GetUInt32FromPayloadArray(payloadArray, ref payloadArrayIndex));
                }
                else
                {
                    throw new NotImplementedException("Got a datatype in RTDE Data Package with a value of " + keyValuePair.Value + " that we did not expect");
                }
            }
            if (payloadArrayIndex != payloadArray.Length)
            {
                log.Error("Did not decode all the data");
                throw new ArgumentOutOfRangeException("Did not decode all the data");
            }
        }

        private object GetVector3DFromPayloadArray(byte[] payloadArray, ref int payloadArrayIndex)
        {
            var x = GetDoubleFromPayloadArray(payloadArray, ref payloadArrayIndex);
            var y = GetDoubleFromPayloadArray(payloadArray, ref payloadArrayIndex);
            var z = GetDoubleFromPayloadArray(payloadArray, ref payloadArrayIndex);
            return new double[] { x, y, z};
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
            return new double[] { x, y, z, rx, ry, rz};
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

        private void UpdateModel(string key, object value)
        {
            switch (key)
            {
                case "timestamp":
                    double timestamp = (double) value;
                    double delta = timestamp - _robotModel.RobotTimestamp;
                    if (delta > 0.0081)
                    {
                        //log.Error($"{delta*1000} Milliseconds since last RTDE");
                    }
                    _robotModel.RobotTimestamp = (double)value;
                    break;
                case "target_q":
                    _robotModel.TargetQ = (double[])value;
                    break;
                case "target_qd":
                    _robotModel.TargetQD = (double[])value;
                    break;
                case "target_qdd":
                    _robotModel.TargetQDD = (double[])value;
                    break;
                case "target_current":
                    _robotModel.TargetCurrent = (double[])value;
                    break;
                case "target_moment":
                    _robotModel.TargetMoment = (double[])value;
                    break;
                case "actual_q":
                    _robotModel.ActualQ = (double[])value;
                    break;
                case "actual_qd":
                    _robotModel.ActualQD = (double[])value;
                    break;
                case "actual_current":
                    _robotModel.ActualCurrent = (double[])value;
                    break;
                case "joint_control_output":
                    _robotModel.JointControlOutput = (double[])value;
                    break;
                case "actual_TCP_pose":
                    _robotModel.ActualTCPPose = (double[])value;
                    break;
                case "actual_TCP_speed":
                    _robotModel.ActualTCPSpeed = (double[])value;
                    break;
                case "actual_TCP_force":
                    _robotModel.ActualTCPForce = (double[])value;
                    break;
                case "target_TCP_pose":
                    _robotModel.TargetTCPPose = (double[])value;
                    break;
                case "target_TCP_speed":
                    _robotModel.TargetTCPSpeed = (double[])value;
                    break;
                case "actual_digital_input_bits":
                    byte[] bytes = BitConverter.GetBytes((UInt64) value);
                    _robotModel.DigitalInputbits.SetBits = new BitArray(new byte[] { (byte) bytes[0]});
                    _robotModel.ConfigurableInputBits.SetBits = new BitArray(new byte[] { (byte) bytes[1]});
                    break;
                case "joint_temperatures":
                    _robotModel.JointTemperatures = (double[])value;
                    break;
                case "actual_execution_time":
                    _robotModel.ActualExecutionTime = (double)value;
                    break;
                case "robot_mode":
                    _robotModel.RobotMode = (RobotMode)(int)value;
                    break;
                case "joint_mode":
                    _robotModel.JointMode = (double[])value;               
                    break;
                case "safety_mode":
                    _robotModel.SafetyMode = (SafetyMode)(int)value;
                    break;
                case "actual_tool_accelerometer":
                    _robotModel.ActualToolAccelerometer = (double[])value;
                    break;
                case "speed_scaling":
                    _robotModel.SpeedScaling = (double)value;
                    break;
                case "target_speed_fraction":
                    _robotModel.TargetSpeedFraction = (double)value;
                    break;
                case "actual_momentum":
                    _robotModel.ActualMomentum = (double)value;
                    break;
                case "actual_main_voltage":
                    _robotModel.ActualMainVoltage = (double)value;
                    break;
                case "actual_robot_voltage":
                    _robotModel.ActualRobotVoltage = (double)value;
                    break;
                case "actual_robot_current":
                    _robotModel.ActualRobotCurrent = (double)value;
                    break;
                case "actual_joint_voltage":
                    _robotModel.ActualJointVoltage = (double[])value;
                    break;
                case "actual_digital_output_bits":
                    byte[] outputBytes = BitConverter.GetBytes((UInt64)value);
                    _robotModel.DigitalOutputBits.SetBits = new BitArray(new byte[] { (byte)outputBytes[0] });
                    _robotModel.ConfigurableOutputBits.SetBits = new BitArray(new byte[] { (byte)outputBytes[1] });
                    break;
                case "runtime_state":
                    _robotModel.RuntimeState = (RuntimeState)(uint) value;
                    break;
                case "robot_status_bits":
                    BitArray statusBitArray = new BitArray(new byte[] { (byte)(UInt32)value });
                    _robotModel.RobotStatus.PowerOn = statusBitArray[0];
                    _robotModel.RobotStatus.ProgramRunning = statusBitArray[1];
                    _robotModel.RobotStatus.TeachButtonPressed = statusBitArray[2];
                    _robotModel.RobotStatus.PowerButtonPressed = statusBitArray[3];
                    break;
                case "safety_status_bits":
                    byte[] bytearray = BitConverter.GetBytes((UInt32)value);
                    BitArray safetystatusBitArray1 = new BitArray(new byte[] { (byte) bytearray[0] });
                    _robotModel.SafetyStatus.NormalMode = safetystatusBitArray1[0];
                    _robotModel.SafetyStatus.ReducedMode = safetystatusBitArray1[1];
                    _robotModel.SafetyStatus.ProtectiveStopped = safetystatusBitArray1[2];
                    _robotModel.SafetyStatus.RecoveryMode = safetystatusBitArray1[3];
                    _robotModel.SafetyStatus.SafeguardStopped = safetystatusBitArray1[4];
                    _robotModel.SafetyStatus.SystemEmergencyStopped = safetystatusBitArray1[5];
                    _robotModel.SafetyStatus.RobotEmergencyStopped = safetystatusBitArray1[6];
                    _robotModel.SafetyStatus.EmergencyStopped = safetystatusBitArray1[7];
                    BitArray safetystatusBitArray2 = new BitArray(new byte[] { (byte)bytearray[1] });
                    _robotModel.SafetyStatus.Violation = safetystatusBitArray2[0];
                    _robotModel.SafetyStatus.Fault = safetystatusBitArray2[1];
                    _robotModel.SafetyStatus.StoppedDueToSafety = safetystatusBitArray2[2];
                    break;
                case "standard_analog_input0":
                    _robotModel.StandardAnalogInput0 = (double)value;
                    break;

                case "standard_analog_input1":
                    _robotModel.StandardAnalogInput1 = (double)value;
                    break;
                case "standard_analog_output0":
                    _robotModel.StandardAnalogOutput0 = (double)value;
                    break;
                case "standard_analog_output1":
                    _robotModel.StandardAnalogOutput = (double)value;
                    break;
                case "io_current":
                    _robotModel.IOCurrent = (double)value;
                    break;
                    

                case "tool_analog_input0":
                    _robotModel.ToolAnalogInput0 = (double)value;
                    break;
                case "tool_analog_input1":
                    _robotModel.ToolAnalogInput1 = (double)value;
                    break;
                case "tool_output_voltage":
                    _robotModel.ToolOutputVoltage = (int)value;
                    break;
                case "tool_output_current":
                    _robotModel.ToolOutputCurrent = (double)value;
                    break;
                case "tcp_force_scalar":
                    _robotModel.TCPForceScalar = (double)value;
                    break;

                #region outputBitRegisters

                case "output_bit_registers0_to_31":
                    _robotModel.OutputBitRegister.SetOutputBitRegisters0to31 = new BitArray(BitConverter.GetBytes((UInt32)value));
                    break;
                case "output_bit_registers32_to_63":
                    _robotModel.OutputBitRegister.SetOutputBitRegisters32to63 = new BitArray(BitConverter.GetBytes((UInt32)value));
                    break;

                #endregion

                #region outputIntRegisters
                case "output_int_register_0":
                    _robotModel.OutputIntRegister.Register0 = (int) value;
                    break;
                //case "output_int_register_1":
                //    _robotModel.SetOutputIntRegister(1, (int)value);
                //    break;
                //case "output_int_register_2":
                //    _robotModel.SetOutputIntRegister(2, (int)value);
                //    break;
                //case "output_int_register_3":
                //    _robotModel.SetOutputIntRegister(3, (int)value);
                //    break;
                //case "output_int_register_4":
                //    _robotModel.SetOutputIntRegister(4, (int)value);
                //    break;
                //case "output_int_register_5":
                //    _robotModel.SetOutputIntRegister(5, (int)value);
                //    break;
                //case "output_int_register_6":
                //    _robotModel.SetOutputIntRegister(6, (int)value);
                //    break;
                //case "output_int_register_7":
                //    _robotModel.SetOutputIntRegister(7, (int)value);
                //    break;
                //case "output_int_register_8":
                //    _robotModel.SetOutputIntRegister(8, (int)value);
                //    break;
                //case "output_int_register_9":
                //    _robotModel.SetOutputIntRegister(9, (int)value);
                //    break;
                //case "output_int_register_10":
                //    _robotModel.SetOutputIntRegister(10, (int)value);
                //    break;
                //case "output_int_register_11":
                //    _robotModel.SetOutputIntRegister(11, (int)value);
                //    break;
                //case "output_int_register_12":
                //    _robotModel.SetOutputIntRegister(12, (int)value);
                //    break;
                //case "output_int_register_13":
                //    _robotModel.SetOutputIntRegister(13, (int)value);
                //    break;
                //case "output_int_register_14":
                //    _robotModel.SetOutputIntRegister(14, (int)value);
                //    break;
                //case "output_int_register_15":
                //    _robotModel.SetOutputIntRegister(15, (int)value);
                //    break;
                //case "output_int_register_16":
                //    _robotModel.SetOutputIntRegister(16, (int)value);
                //    break;
                //case "output_int_register_17":
                //    _robotModel.SetOutputIntRegister(17, (int)value);
                //    break;
                //case "output_int_register_18":
                //    _robotModel.SetOutputIntRegister(18, (int)value);
                //    break;
                //case "output_int_register_19":
                //    _robotModel.SetOutputIntRegister(19, (int)value);
                //    break;
                //case "output_int_register_20":
                //    _robotModel.SetOutputIntRegister(20, (int)value);
                //    break;
                //case "output_int_register_21":
                //    _robotModel.SetOutputIntRegister(21, (int)value);
                //    break;
                //case "output_int_register_22":
                //    _robotModel.SetOutputIntRegister(22, (int)value);
                //    break;
                //case "output_int_register_23":
                //    _robotModel.SetOutputIntRegister(23, (int)value);
                //    break;

                #endregion

                #region outputDoubleRegisters
                case "output_double_register_0":
                    _robotModel.OutputDoubleRegister.Register0 = (double) value;
                    break;
                //case "output_double_register_1":
                //    _robotModel.SetOutputDoubleRegister(1, (double)value);
                //    break;
                //case "output_double_register_2":
                //    _robotModel.SetOutputDoubleRegister(2, (double)value);
                //    break;
                //case "output_double_register_3":
                //    _robotModel.SetOutputDoubleRegister(3, (double)value);
                //    break;
                //case "output_double_register_4":
                //    _robotModel.SetOutputDoubleRegister(4, (double)value);
                //    break;
                //case "output_double_register_5":
                //    _robotModel.SetOutputDoubleRegister(5, (double)value);
                //    break;
                //case "output_double_register_6":
                //    _robotModel.SetOutputDoubleRegister(6, (double)value);
                //    break;
                //case "output_double_register_7":
                //    _robotModel.SetOutputDoubleRegister(7, (double)value);
                //    break;
                //case "output_double_register_8":
                //    _robotModel.SetOutputDoubleRegister(8, (double)value);
                //    break;
                //case "output_double_register_9":
                //    _robotModel.SetOutputDoubleRegister(9, (double)value);
                //    break;
                //case "output_double_register_10":
                //    _robotModel.SetOutputDoubleRegister(10, (double)value);
                //    break;
                //case "output_double_register_11":
                //    _robotModel.SetOutputDoubleRegister(11, (double)value);
                //    break;
                //case "output_double_register_12":
                //    _robotModel.SetOutputDoubleRegister(12, (double)value);
                //    break;
                //case "output_double_register_13":
                //    _robotModel.SetOutputDoubleRegister(13, (double)value);
                //    break;
                //case "output_double_register_14":
                //    _robotModel.SetOutputDoubleRegister(14, (double)value);
                //    break;
                //case "output_double_register_15":
                //    _robotModel.SetOutputDoubleRegister(15, (double)value);
                //    break;
                //case "output_double_register_16":
                //    _robotModel.SetOutputDoubleRegister(16, (double)value);
                //    break;
                //case "output_double_register_17":
                //    _robotModel.SetOutputDoubleRegister(17, (double)value);
                //    break;
                //case "output_double_register_18":
                //    _robotModel.SetOutputDoubleRegister(18, (double)value);
                //    break;
                //case "output_double_register_19":
                //    _robotModel.SetOutputDoubleRegister(19, (double)value);
                //    break;
                //case "output_double_register_20":
                //    _robotModel.SetOutputDoubleRegister(20, (double)value);
                //    break;
                //case "output_double_register_21":
                //    _robotModel.SetOutputDoubleRegister(21, (double)value);
                //    break;
                //case "output_double_register_22":
                //    _robotModel.SetOutputDoubleRegister(22, (double)value);
                //    break;
                //case "output_double_register_23":
                //    _robotModel.SetOutputDoubleRegister(23, (double)value);
                //    break;


                #endregion


                default:
                    throw new NotImplementedException("Did not find any handling for " + key);
            }
        }



        private ConnectionState DecodeRTDEControlPacagePause(byte[] payloadArray)
        {
            if (payloadArray[0] == 1)
            {
                return ConnectionState.Paused;
            }
            else
            {
                throw new NotImplementedException();
            }
        }

        private ConnectionState DecodeRTDEControlPackageStart(byte[] payloadArray)
        {
            if (payloadArray[0] == 1)
            {
                return ConnectionState.Started;
            }
            else
            {
                throw new NotImplementedException();
            }

        }

        private void DecodeRTDESetupPackage(byte[] payloadArray, List<KeyValuePair<string,string>> rtdeConfiguration )
        {
            var str = Encoding.Default.GetString(payloadArray);
            string[] values = str.Split(',');
           
            for (int i = 0; i < rtdeConfiguration.Count; i++)
            {
                if (rtdeConfiguration[i].Value != values[i])
                {
                    rtdeConfiguration[i] = new KeyValuePair<string, string>(rtdeConfiguration[i].Key, values[i]);
                }
            }
        }

        

        private void DecodeUniversalRobotsControllerVersion(byte[] payload)
        {
            byte[] majorArray = new byte[4];
            Array.Copy(payload, 0, majorArray, 0, 4);
            majorArray = CheckEndian(majorArray);
            UInt32 major = BitConverter.ToUInt32(majorArray, 0);
            byte[] minorArray = new byte[4];
            Array.Copy(payload, 4, minorArray, 0, 4);
            minorArray = CheckEndian(minorArray);
            UInt32 minor = BitConverter.ToUInt32(minorArray, 0);
            byte[] bugfixArray = new byte[4];
            Array.Copy(payload, 8, bugfixArray, 0, 4);
            bugfixArray = CheckEndian(bugfixArray);
            UInt32 bugfix = BitConverter.ToUInt32(bugfixArray, 0);
            byte[] buildArray = new byte[4];
            Array.Copy(payload, 12, buildArray, 0, 4);
            buildArray = CheckEndian(buildArray);
            UInt32 build = BitConverter.ToUInt32(buildArray, 0);
        }

        private int DecodeProtocolVersion(byte[] payload)
        {
            return payload[0];
        }

        private byte[] CheckEndian(byte[] input)    //dublet .. flyt til utilities 
        {
            if (BitConverter.IsLittleEndian)
                Array.Reverse(input);
            return input;
        }

        private void ControllerVersionDecoder(byte[] myReadBuffer)
        {
            if (myReadBuffer[2] == 'v')
            {
                Debug.WriteLine("Found Controller Version Number: {0}.{1}.{2}.{3}", myReadBuffer[6], myReadBuffer[10], myReadBuffer[14], myReadBuffer[18]);
            }
            if (myReadBuffer[2] == 'V')
            {
                Debug.WriteLine("Negotiated Protocol Number: {0}", myReadBuffer[3]);
            }
            else
            {
                string text = Encoding.ASCII.GetString(myReadBuffer);
                Debug.WriteLine(text);
            }
        }

    }
}
