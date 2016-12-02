using System;
using System.Collections;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Xml;
using log4net;


namespace UniversalRobotsConnect
{
    enum UR_RTDE_Command:byte
    {
        RTDE_REQUEST_PROTOCOL_VERSION = 86,
        RTDE_GET_URCONTROL_VERSION = 118,
        RTDE_TEXT_MESSAGE = 77,
        RTDE_DATA_PACKAGE = 85,
        RTDE_CONTROL_PACKAGE_SETUP_OUTPUTS = 79,
        RTDE_CONTROL_PACKAGE_SETUP_INPUTS = 73,
        RTDE_CONTROL_PACKAGE_START = 83,
        RTDE_CONTROL_PACKAGE_PAUSE = 80
    }

    public class RTDE
    {
        private static readonly ILog log = LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        private const int port = 30004;

        private TcpClient _client;
        private NetworkStream _stream;
        private RTDEReceiver _rtdeReceiver;
        private RTDESender _rtdeSender;
        private RobotModel _robotModel;
        private List<KeyValuePair<string, string>> _rtdeOutputConfiguration;
        private List<KeyValuePair<string, string>> _rtdeInputConfiguration;
        private BitArray _configurableDigitalOutputBitArray = new BitArray(8);
        private BitArray _standardDigitalOutputBitArray = new BitArray(8);
        private int[] _rtdeInputInts = new int[24];
        private double[] _rtdeInputDoubles = new double[24];

        public RTDE(RobotModel robotModel, ConcurrentQueue<RobotModel> robotData)
        {
            _robotModel = robotModel;
            _client = new TcpClient(_robotModel.IpAddress.ToString(), port);
            _stream = _client.GetStream();
            _rtdeOutputConfiguration = new List<KeyValuePair<string, string>>();
            _rtdeInputConfiguration = new List<KeyValuePair<string, string>>();

            _rtdeReceiver = new RTDEReceiver(_stream, _robotModel, _rtdeOutputConfiguration, _rtdeInputConfiguration, robotData);
            _rtdeSender = new RTDESender(_stream/*, _rtdeOutputConfiguration*/);
            _rtdeReceiver.DataReceived += OnDataReceived;


            GetControllerVersion();
            while (_robotModel.URControlVersion == null)
            {
                Thread.Sleep(10);
            }
            NegotiateProtocolVersion();
            while (_robotModel.RTDEProtocolVersion != 1)
            {
                Thread.Sleep(10);
            }

            SetupRtdeInterface();
            Thread.Sleep(300);
            StartRTDEInterface();
            while (_robotModel.RTDEConnectionState != ConnectionState.Started)
            {
                Thread.Sleep(10);
            }

        }

        public void SendData(byte[] data)
        {
            byte[] testBytes = CreatePackage((byte)UR_RTDE_Command.RTDE_DATA_PACKAGE, data);
            _rtdeSender.SendData(testBytes);

            log.Debug($"Send RTDE to robot");
        }

        public void SendData(string payload)
        {
            SendData(Encoding.UTF8.GetBytes(payload));
        }


        public void SetConfigurableDigitalOutput(int bitNumber, bool value)
        {
            _configurableDigitalOutputBitArray[bitNumber] = value;
            SendRTDEDataPackage();
        }

        
        public void SetStandardDigitalOutput(int bitNumber, bool value)
        {
            _standardDigitalOutputBitArray[bitNumber] = value;
            SendRTDEDataPackage();
        }

        public void SetInputIntRegister(int intNumber, int value)
        {
            _rtdeInputInts[intNumber] = value;
            SendRTDEDataPackage();
        }

        public void SetInputDoubleRegister(int doubleNumber, double value)
        {
            _rtdeInputDoubles[doubleNumber] = value;
            SendRTDEDataPackage();
        }

        private void SendRTDEDataPackage()
        {
            List<byte> payloadByteList = new List<byte>();
            payloadByteList.Add(1);

            foreach (KeyValuePair<string, string> keyValuePair in _rtdeInputConfiguration)
            {
                #region Bigass Switch

                switch (keyValuePair.Key)
                {
                    case "standard_digital_output_mask":
                        payloadByteList.Add(255);
                        break;
                    case "standard_digital_output":
                        payloadByteList.Add(BitArrayToByteArray(_standardDigitalOutputBitArray)[0]);
                        break;
                    case "configurable_digital_output_mask":
                        payloadByteList.Add(255);
                        break;
                    case "configurable_digital_output":
                        payloadByteList.Add(BitArrayToByteArray(_configurableDigitalOutputBitArray)[0]);
                        break;
                    case "input_int_register_0":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputInts[0]));
                        break;
                    case "input_int_register_1":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputInts[1]));
                        break;
                    case "input_int_register_2":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputInts[2]));
                        break;
                    case "input_int_register_3":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputInts[3]));
                        break;
                    case "input_int_register_4":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputInts[4]));
                        break;
                    case "input_int_register_5":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputInts[5]));
                        break;
                    case "input_int_register_6":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputInts[6]));
                        break;
                    case "input_int_register_7":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputInts[7]));
                        break;
                    case "input_int_register_8":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputInts[8]));
                        break;
                    case "input_int_register_9":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputInts[9]));
                        break;
                    case "input_int_register_10":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputInts[10]));
                        break;
                    case "input_int_register_11":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputInts[11]));
                        break;
                    case "input_int_register_12":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputInts[12]));
                        break;
                    case "input_int_register_13":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputInts[13]));
                        break;
                    case "input_int_register_14":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputInts[14]));
                        break;
                    case "input_int_register_15":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputInts[15]));
                        break;
                    case "input_int_register_16":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputInts[16]));
                        break;
                    case "input_int_register_17":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputInts[17]));
                        break;
                    case "input_int_register_18":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputInts[18]));
                        break;
                    case "input_int_register_19":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputInts[19]));
                        break;
                    case "input_int_register_20":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputInts[20]));
                        break;
                    case "input_int_register_21":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputInts[21]));
                        break;
                    case "input_int_register_22":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputInts[22]));
                        break;
                    case "input_int_register_23":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputInts[23]));
                        break;
                    case "input_double_register_0":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputDoubles[0]));
                        break;
                    case "input_double_register_1":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputDoubles[1]));
                        break;
                    case "input_double_register_2":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputDoubles[2]));
                        break;
                    case "input_double_register_3":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputDoubles[3]));
                        break;
                    case "input_double_register_4":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputDoubles[4]));
                        break;
                    case "input_double_register_5":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputDoubles[5]));
                        break;
                    case "input_double_register_6":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputDoubles[6]));
                        break;
                    case "input_double_register_7":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputDoubles[7]));
                        break;
                    case "input_double_register_8":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputDoubles[8]));
                        break;
                    case "input_double_register_9":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputDoubles[9]));
                        break;
                    case "input_double_register_10":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputDoubles[10]));
                        break;
                    case "input_double_register_11":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputDoubles[11]));
                        break;
                    case "input_double_register_12":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputDoubles[12]));
                        break;
                    case "input_double_register_13":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputDoubles[13]));
                        break;
                    case "input_double_register_14":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputDoubles[14]));
                        break;
                    case "input_double_register_15":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputDoubles[15]));
                        break;
                    case "input_double_register_16":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputDoubles[16]));
                        break;
                    case "input_double_register_17":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputDoubles[17]));
                        break;
                    case "input_double_register_18":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputDoubles[18]));
                        break;
                    case "input_double_register_19":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputDoubles[19]));
                        break;
                    case "input_double_register_20":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputDoubles[20]));
                        break;
                    case "input_double_register_21":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputDoubles[21]));
                        break;
                    case "input_double_register_22":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputDoubles[22]));
                        break;
                    case "input_double_register_23":
                        payloadByteList.AddRange(BitConverter.GetBytes(_rtdeInputDoubles[23]));
                        break;

                    default:
                        log.Error("Got a datatype not expected");
                        throw new NotImplementedException("check your rtde config - we did not support that input datatype");


                        
                        
                }
                #endregion
            }
            byte[] myPackage = CreatePackage((byte)UR_RTDE_Command.RTDE_DATA_PACKAGE, payloadByteList.ToArray());
            _rtdeSender.SendData(myPackage);
        }


        private static byte[] BitArrayToByteArray(BitArray bits)
        {
            byte[] ret = new byte[(bits.Length - 1) / 8 + 1];
            bits.CopyTo(ret, 0);
            return ret;
        }

        // Consumers register to receive data.
        private event EventHandler<DataReceivedEventArgs> DataReceived;

        private void OnDataReceived(object sender, DataReceivedEventArgs e)
        {
            var handler = DataReceived;
            if (handler != null) DataReceived(this, e);  // re-raise event
        }

        


       

        

        private void GetControllerVersion()
        {
            log.Debug("Get Controller Version from Robot");
            byte [] myBytes = new byte[0];
            byte[] testBytes = CreatePackage((byte)UR_RTDE_Command.RTDE_GET_URCONTROL_VERSION , myBytes);
            _rtdeSender.SendData(testBytes);
        }

        

        private byte[] CreatePackage(byte type, byte[] payload)
        {
            UInt16 packageSize = (ushort) (payload.Length + 3);

            byte[] package = new byte[packageSize];
            int packageIndex = 3;
            foreach (byte b in payload)
            {
                package[packageIndex] = b;
                packageIndex++;
            }
            byte[] header = GetHeader(packageSize, type);
            package[0] = header[0];
            package[1] = header[1];
            package[2] = header[2];

            return package;
        }

        private byte[] GetHeader(ushort packageSize, byte type)
        {
            byte[] header = new byte[3];
            byte[] size = GetByteArray(packageSize);
            header[0] = size[0];
            header[1] = size[1];
            header[2] = type;
            return header;
        }

        private byte[] GetByteArray(object obj)
        {
            if (obj is UInt16)
            {
                byte[] byteArray = BitConverter.GetBytes((UInt16)obj);
                byteArray = CheckEndian(byteArray);
                return byteArray;
            }
            if (obj is string)
            {
                string input = (string)obj;
                char[] charArray = new char[((string)obj).Length];
                int index = 0;
                foreach (char c in input)
                {
                    charArray[index] = input[index];
                    index++;
                }
                byte[] byteArray = Encoding.UTF8.GetBytes(charArray);
                return byteArray;
            }
            else
            {
                throw new NotImplementedException("Datetype Not implemented for conversion");
            }
        }

        private byte[] CheckEndian(byte[] input)
        {
            if (BitConverter.IsLittleEndian)
                Array.Reverse(input);
            return input;
        }

        private void NegotiateProtocolVersion() //Version 1
        {
            log.Debug("Negotiate Protocol Version with Robot");
            byte[] payload = GetByteArray((UInt16) 1);

            byte[] package = CreatePackage(86, payload);

            //string encodedText = "\x00\x05V\x00\x01";
            //byte[] byteArray = Encoding.ASCII.GetBytes(encodedText);
            _rtdeSender.SendData(package);
        }

        private void SetupRtdeInterface()
        {
            log.Debug("Setting up RTDE Interface");

            GetRTDEConfigFromFile("receive", _rtdeOutputConfiguration);
            _rtdeOutputConfiguration.Insert(0, new KeyValuePair<string, string>("timestamp", null));  //Always get the robot timestamp
            
            byte[] outputPayload = GetByteArray(GetRTDEPayloadString(_rtdeOutputConfiguration));
            byte[] outputPackage = CreatePackage((byte) UR_RTDE_Command.RTDE_CONTROL_PACKAGE_SETUP_OUTPUTS, outputPayload); 
            _rtdeSender.SendData(outputPackage);

            GetRTDEConfigFromFile("send", _rtdeInputConfiguration);
            if (_rtdeInputConfiguration.Count > 0)
            {
                byte[] inputPayload = GetByteArray(GetRTDEPayloadString(_rtdeInputConfiguration));
                byte[] inputPackage = CreatePackage((byte)UR_RTDE_Command.RTDE_CONTROL_PACKAGE_SETUP_INPUTS, inputPayload);
                _rtdeSender.SendData(inputPackage);
            }
        }

        private string GetRTDEPayloadString(List<KeyValuePair<string, string>> rtdeConfiguration)
        {
            StringBuilder payloadStringBuilder = new StringBuilder();
            int index = 1;
            foreach (KeyValuePair<string, string> keyValuePair in rtdeConfiguration)
            {
                payloadStringBuilder.Append(keyValuePair.Key);
                if (index < rtdeConfiguration.Count)
                {
                    payloadStringBuilder.Append(",");
                }
                index++;
            }
            return payloadStringBuilder.ToString();
        }

        private void GetRTDEConfigFromFile(string xmlKey, List<KeyValuePair<string, string>> rtdeConfiguration)
        {
            //List<KeyValuePair<string,string>> values = new List<KeyValuePair<string, string>>();
            XmlReader xmlReader = XmlReader.Create(@"C:\SourceCode\ur-interface\URConnect\UniversalRobotsConnect\bin\Debug\Resources\rtde_configuration.xml");
            xmlReader.ReadToFollowing(xmlKey);
            if (xmlReader.ReadToDescendant("field"))
            {
                do
                {
                    var name = xmlReader.GetAttribute("name");
                    var value = xmlReader.GetAttribute("type");
                    rtdeConfiguration.Add(new KeyValuePair<string, string>(name, value));
                } while (xmlReader.ReadToNextSibling("field"));
            }
            //return rtdeConfiguration;
        }

        private void StartRTDEInterface()
        {
            log.Debug("Starting RTDE Interface");
            byte[] myBytes = new byte[0];
            byte[] package = CreatePackage((byte) UR_RTDE_Command.RTDE_CONTROL_PACKAGE_START, myBytes);
            _rtdeReceiver.RtdePackageSize = GetRtdeDatePackageSize(_rtdeOutputConfiguration);
            _rtdeSender.SendData(package);
        }

        private void PauseRTDEInterface()
        {
            log.Debug("Pausing RTDE Interface");
            byte[] myBytes = new byte[0];
            byte[] package = CreatePackage((byte)UR_RTDE_Command.RTDE_CONTROL_PACKAGE_PAUSE, myBytes);
            _rtdeReceiver.RtdePackageSize = 0;
            _rtdeSender.SendData(package);
        }

        private int GetRtdeDatePackageSize(List<KeyValuePair<string, string>> rtdeOutputConfiguration)
        {
            int packageSize = 11;    //Header is 3 bytes - timestamp will be 8 bytes
            foreach (var keyValuePair in rtdeOutputConfiguration)
            {
                if (keyValuePair.Key != "timestamp")
                {
                    switch (keyValuePair.Value)
                    {
                        case "DOUBLE":
                            packageSize = packageSize + 8;
                            break;
                        case "UINT64":
                            packageSize = packageSize + 8;
                            break;
                        case "VECTOR6D":
                            packageSize = packageSize + 48;
                            break;
                        case "INT32":
                            packageSize = packageSize + 4;
                            break;
                        case "VECTOR6INT32":
                            packageSize = packageSize + 24;
                            break;
                        case "VECTOR3D":
                            packageSize = packageSize + 24;
                            break;
                        case "UINT32":
                            packageSize = packageSize + 4;
                            break;
                        default:
                            throw new ArgumentException("Datatype in rtde output not known");
                    }
                }

            }

            return packageSize;
        }


    }
}
