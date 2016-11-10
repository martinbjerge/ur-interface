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
        private Thread _thread;
        private RobotModel _robotModel;
        private List<KeyValuePair<string, string>> _rtdeOutputConfiguration;
        private List<KeyValuePair<string, string>> _rtdeInputConfiguration;

        internal RTDEReceiver(NetworkStream stream, RobotModel robotModel, List<KeyValuePair<string, string>> rtdeOutputConfiguration, List<KeyValuePair<string, string>> rtdeInputConfiguration)
        {
            _robotModel = robotModel;
            _stream = stream;
            _rtdeOutputConfiguration = rtdeOutputConfiguration;
            _rtdeInputConfiguration = rtdeInputConfiguration;
            _thread = new Thread(Run);
            _thread.Start();
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
                        byte[] myReadBuffer = new byte[64000];
                        StringBuilder myCompleteMessage = new StringBuilder();
                        int numberOfBytesRead = 0;

                        // Incoming message may be larger than the buffer size.
                        do
                        {
                            numberOfBytesRead = _stream.Read(myReadBuffer, 0, myReadBuffer.Length);
                            myCompleteMessage.AppendFormat("{0}", Encoding.ASCII.GetString(myReadBuffer, 0, numberOfBytesRead));
                        }
                        while (_stream.DataAvailable);

                        DecodePacage(myReadBuffer);
                        //MessageDecode(myReadBuffer);
                    }
                    else
                    {
                        Debug.WriteLine("Sorry.  You cannot read from this NetworkStream.");
                        throw new SystemException();
                    }
                }
            }
        }

        private void DecodePacage(byte[] recievedPackage)
        {
            byte[] sizeArray = new byte[2];
            byte type = recievedPackage[2];
            Array.Copy(recievedPackage, sizeArray, 2);
            sizeArray = CheckEndian(sizeArray);
            ushort size = BitConverter.ToUInt16(sizeArray, 0);
            if (size > 3)
            {
                byte[] payloadArray = new byte[size - 3];
                Array.Copy(recievedPackage, 3, payloadArray, 0, size - 3);

                switch (type)
                {
                    case (byte)UR_RTDE_Command.RTDE_REQUEST_PROTOCOL_VERSION:
                        _robotModel.RTDEProtocolVersion = DecodeProtocolVersion(payloadArray);
                        break;
                    case (byte)UR_RTDE_Command.RTDE_GET_URCONTROL_VERSION:
                        DecodeUniversalRobotsControllerVersion(payloadArray);
                        break;
                    case (byte)UR_RTDE_Command.RTDE_CONTROL_PACKAGE_SETUP_OUTPUTS:
                        DecodeRTDESetupPackage(payloadArray, _rtdeOutputConfiguration);
                        break;
                    case (byte)UR_RTDE_Command.RTDE_CONTROL_PACKAGE_SETUP_INPUTS:
                        DecodeRTDESetupPackage(payloadArray, _rtdeInputConfiguration);
                        break;
                    case (byte)UR_RTDE_Command.RTDE_DATA_PACKAGE:
                        DecodeRTDEDataPackage(payloadArray);
                        break;
                    case (byte)UR_RTDE_Command.RTDE_CONTROL_PACKAGE_START:
                        _robotModel.RTDEConnectionState = DecodeRTDEControlPackageStart(payloadArray);
                        break;
                    case (byte)UR_RTDE_Command.RTDE_CONTROL_PACKAGE_PAUSE:
                        _robotModel.RTDEConnectionState = DecodeRTDEControlPacagePause(payloadArray);
                        break;
                    default:
                        throw new NotImplementedException("Package type not implemented " + (UR_RTDE_Command)type);
                }
            }
            else
            {
                log.Error("Got a packet too small");
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
            return new Vector3D(x, y, z);
        }

        private object GetVector6DInt32FromPayloadArray(byte[] payloadArray, ref int payloadArrayIndex)
        {
            var x = GetInt32FromPayloadArray(payloadArray, ref payloadArrayIndex);
            var y = GetInt32FromPayloadArray(payloadArray, ref payloadArrayIndex);
            var z = GetInt32FromPayloadArray(payloadArray, ref payloadArrayIndex);
            var rx = GetInt32FromPayloadArray(payloadArray, ref payloadArrayIndex);
            var ry = GetInt32FromPayloadArray(payloadArray, ref payloadArrayIndex);
            var rz = GetInt32FromPayloadArray(payloadArray, ref payloadArrayIndex);
            return new Vector6D(x, y, z, rx, ry, rz);
        }


        private Vector6D GetVector6DFromPayloadArray(byte[] payloadArray, ref int payloadArrayIndex)
        {
            var x = GetDoubleFromPayloadArray(payloadArray, ref payloadArrayIndex);
            var y = GetDoubleFromPayloadArray(payloadArray, ref payloadArrayIndex);
            var z = GetDoubleFromPayloadArray(payloadArray, ref payloadArrayIndex);
            var rx = GetDoubleFromPayloadArray(payloadArray, ref payloadArrayIndex);
            var ry = GetDoubleFromPayloadArray(payloadArray, ref payloadArrayIndex);
            var rz = GetDoubleFromPayloadArray(payloadArray, ref payloadArrayIndex);
            return new Vector6D(x, y, z, rx, ry, rz);
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
                    _robotModel.RobotTimestamp = (double)value;
                    break;
                case "target_q":
                    _robotModel.TargetQ = (Vector6D)value;
                    break;
                case "target_qd":
                    _robotModel.TargetQD = (Vector6D)value;
                    break;
                case "target_qdd":
                    _robotModel.TargetQDD = (Vector6D)value;
                    break;
                case "target_current":
                    _robotModel.TargetCurrent = (Vector6D)value;
                    break;
                case "target_moment":
                    _robotModel.TargetMoment = (Vector6D)value;
                    break;
                case "actual_q":
                    _robotModel.ActualQ = (Vector6D)value;
                    break;
                case "actual_qd":
                    _robotModel.ActualQD = (Vector6D)value;
                    break;
                case "actual_current":
                    _robotModel.ActualCurrent = (Vector6D)value;
                    break;
                case "joint_control_output":
                    _robotModel.JointControlOutput = (Vector6D)value;
                    break;
                case "actual_TCP_pose":
                    _robotModel.ActualTCPPose = (Vector6D)value;
                    break;
                case "actual_TCP_speed":
                    _robotModel.ActualTCPSpeed = (Vector6D)value;
                    break;
                case "actual_TCP_force":
                    _robotModel.ActualTCPForce = (Vector6D)value;
                    break;
                case "target_TCP_pose":
                    _robotModel.TargetTCPPose = (Vector6D)value;
                    break;
                case "target_TCP_speed":
                    _robotModel.TargetTCPSpeed = (Vector6D)value;
                    break;
                case "actual_digital_input_bits":
                    BitArray inputBits = new BitArray(new byte[] { (byte)(UInt64)value });
                    _robotModel.DigitalInputBit0 = inputBits[0];
                    _robotModel.DigitalInputBit1 = inputBits[1];
                    _robotModel.DigitalInputBit2 = inputBits[2];
                    _robotModel.DigitalInputBit3 = inputBits[3];
                    _robotModel.DigitalInputBit4 = inputBits[4];
                    _robotModel.DigitalInputBit5 = inputBits[5];
                    _robotModel.DigitalInputBit6 = inputBits[6];
                    _robotModel.DigitalInputBit7 = inputBits[7];
                    break;
                case "joint_temperatures":
                    _robotModel.JointTemperatures = (Vector6D)value;
                    break;
                case "actual_execution_time":
                    _robotModel.ActualExecutionTime = (double)value;
                    break;
                case "robot_mode":
                    _robotModel.RobotMode = (RobotMode)(int)value;
                    break;
                case "joint_mode":
                    _robotModel.JointMode = (Vector6D)value;                //ToDo - split modes for each joint
                    break;
                case "safety_mode":
                    _robotModel.SafetyMode = (SafetyMode)(int)value;
                    break;
                case "actual_tool_accelerometer":
                    _robotModel.ActualToolAccelerometer = (Vector3D)value;
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
                    _robotModel.ActualJointVoltage = (Vector6D)value;
                    break;
                case "actual_digital_output_bits":
                    BitArray bitArray = new BitArray(new byte[] { (byte)(UInt64)value });
                    _robotModel.DigitalOutputBit0 = bitArray[0];
                    _robotModel.DigitalOutputBit1 = bitArray[1];
                    _robotModel.DigitalOutputBit2 = bitArray[2];
                    _robotModel.DigitalOutputBit3 = bitArray[3];
                    _robotModel.DigitalOutputBit4 = bitArray[4];
                    _robotModel.DigitalOutputBit5 = bitArray[5];
                    _robotModel.DigitalOutputBit6 = bitArray[6];
                    _robotModel.DigitalOutputBit7 = bitArray[7];
                    break;
                case "runtime_state":
                    _robotModel.RuntimeState = (uint) value;
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
            List<KeyValuePair<string, string>> updatedKeyValueList = new List<KeyValuePair<string, string>>();
            int index = 0;
            foreach (KeyValuePair<string, string> keyValuePair in rtdeConfiguration)
            {
                var newKeyValuePair = new KeyValuePair<string, string>(keyValuePair.Key, values[index]);
                updatedKeyValueList.Add(newKeyValuePair);
                index++;
            }
            rtdeConfiguration = updatedKeyValueList;        //dangerous reference override
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
