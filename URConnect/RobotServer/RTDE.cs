using System;
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

namespace RobotServer
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

    class RTDE
    {
        private const int port = 30004;

        private TcpClient _client;
        private NetworkStream _stream;
        private Receiver _receiver;
        private Sender _sender;
        private RobotModel _robotModel;
        private List<KeyValuePair<string, string>> _rtdeOutputConfiguration;

        public void SendData(byte[] data)
        {
            _sender.SendData(data);
        }

        // Consumers register to receive data.
        public event EventHandler<DataReceivedEventArgs> DataReceived;

        

        private void OnDataReceived(object sender, DataReceivedEventArgs e)
        {
            var handler = DataReceived;
            if (handler != null) DataReceived(this, e);  // re-raise event
        }

        


        public RTDE(RobotModel robotModel)
        {
            _robotModel = robotModel;
            _client = new TcpClient(_robotModel.IpAddress.ToString(), port);          /////////////////////////////////////////////////////////////////////////////
            _stream = _client.GetStream();
            _rtdeOutputConfiguration = new List<KeyValuePair<string, string>>();

            _receiver = new Receiver(_stream, _robotModel, _rtdeOutputConfiguration);
            _sender = new Sender(_stream, _rtdeOutputConfiguration);
            _receiver.DataReceived += OnDataReceived;


            //StartListening();
            GetControllerVersion();
            Thread.Sleep(150);
            NegotiateProtocolVersion();
            Thread.Sleep(150);
            SetupRtdeInterface();
            Thread.Sleep(150);
            StartRTDEInterface();
            Thread.Sleep(10000);
            PauseRTDEInterface();
            Thread.Sleep(2000);
            StartRTDEInterface();

        }

        

        private void GetControllerVersion()
        {
            byte [] myBytes = new byte[0];
            byte[] testBytes = CreatePackage((byte)UR_RTDE_Command.RTDE_GET_URCONTROL_VERSION , myBytes);

            _sender.SendData(testBytes);
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
            //byte[] testBytes = new byte[] { 0, 5, 86, 0, 1};

            byte[] payload = GetByteArray((UInt16) 1);

            byte[] package = CreatePackage(86, payload);

            //string encodedText = "\x00\x05V\x00\x01";
            //byte[] byteArray = Encoding.ASCII.GetBytes(encodedText);
            _sender.SendData(package);
        }

        private void SetupRtdeInterface()
        {

            _rtdeOutputConfiguration.Add(new KeyValuePair<string, string>("timestamp", null));  //Always get the robot timestamp
            //FileStream fileStream = new FileStream(@"Resources\rtde_configuration.xml", FileMode.Open);
            XmlReader xmlReader = XmlReader.Create(@"Resources\rtde_configuration.xml");
            xmlReader.ReadToFollowing("receive");
            if (xmlReader.ReadToDescendant("field"))
            {
                do
                {
                    var name = xmlReader.GetAttribute("name");
                    var value = xmlReader.GetAttribute("type");
                    _rtdeOutputConfiguration.Add(new KeyValuePair<string, string>(name, value));
                } while (xmlReader.ReadToNextSibling("field"));
                    
            }
           
            //_rtdeOutputConfiguration.Add(new KeyValuePair<string, string>("actual_digital_output_bits", null));

            StringBuilder stringBuilder = new StringBuilder();
            int index = 1;
            foreach (KeyValuePair<string, string> keyValuePair in _rtdeOutputConfiguration)
            {
                stringBuilder.Append(keyValuePair.Key);
                if (index <_rtdeOutputConfiguration.Count)
                {
                    stringBuilder.Append(",");
                }
                index++;
            }

            byte[] payload = GetByteArray(stringBuilder.ToString());

            //byte[] payload = GetByteArray("timestamp,actual_digital_output_bits");
            byte[] package = CreatePackage(79, payload); 
            _sender.SendData(package);
        }

        private void StartRTDEInterface()
        {
            byte[] myBytes = new byte[0];
            byte[] package = CreatePackage((byte) UR_RTDE_Command.RTDE_CONTROL_PACKAGE_START, myBytes);
            _sender.SendData(package);
        }

        private void PauseRTDEInterface()
        {
            byte[] myBytes = new byte[0];
            byte[] package = CreatePackage((byte)UR_RTDE_Command.RTDE_CONTROL_PACKAGE_PAUSE, myBytes);
            _sender.SendData(package);
        }

    }



    sealed class Receiver
    {
        internal event EventHandler<DataReceivedEventArgs> DataReceived;
        private NetworkStream _stream;
        private Thread _thread;
        private RobotModel _robotModel;
        private List<KeyValuePair<string, string>> _rtdeOutputConfiguration;

        internal Receiver(NetworkStream stream, RobotModel robotModel, List<KeyValuePair<string,string>> rtdeOutputConfiguration)
        {
            _robotModel = robotModel;
            _stream = stream;
            _rtdeOutputConfiguration = rtdeOutputConfiguration;
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
                        byte[] myReadBuffer = new byte[1024];
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
                    DecodeRTDESetupPackage(payloadArray);
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
                    throw new NotImplementedException("Package type not implemented");
            }
        }

        private void DecodeRTDEDataPackage(byte[] payloadArray)
        {
            int payloadArrayIndex = 0;
            foreach (KeyValuePair<string, string> keyValuePair in _rtdeOutputConfiguration)
            {
                if (keyValuePair.Value == "DOUBLE")
                {
                    byte[] bytes = new byte[8];
                    Array.Copy(payloadArray, payloadArrayIndex, bytes, 0, 8);
                    bytes = CheckEndian(bytes);
                    payloadArrayIndex = payloadArrayIndex + 8;
                    UpdateModel(keyValuePair.Key, BitConverter.ToDouble(bytes, 0));
                }
                else if (keyValuePair.Value == "UINT64")
                {
                    byte[] bytes = new byte[8];
                    Array.Copy(payloadArray, payloadArrayIndex, bytes, 0, 8);
                    bytes = CheckEndian(bytes);
                    payloadArrayIndex = payloadArrayIndex + 8;
                    UpdateModel(keyValuePair.Key, (byte)BitConverter.ToUInt64(bytes, 0));
                }
                else if (keyValuePair.Value == "VECTOR6D")
                {
                    byte[] bytes = new byte[8];
                    Array.Copy(payloadArray, payloadArrayIndex, bytes, 0, 8);
                    bytes = CheckEndian(bytes);
                    payloadArrayIndex = payloadArrayIndex + 8;
                    var x = BitConverter.ToDouble(bytes,0);
                    Array.Copy(payloadArray, payloadArrayIndex, bytes, 0, 8);
                    bytes = CheckEndian(bytes);
                    payloadArrayIndex = payloadArrayIndex + 8;
                    var y = BitConverter.ToDouble(bytes, 0);
                    Array.Copy(payloadArray, payloadArrayIndex, bytes, 0, 8);
                    bytes = CheckEndian(bytes);
                    payloadArrayIndex = payloadArrayIndex + 8;
                    var z = BitConverter.ToDouble(bytes, 0);
                    Array.Copy(payloadArray, payloadArrayIndex, bytes, 0, 8);
                    bytes = CheckEndian(bytes);
                    payloadArrayIndex = payloadArrayIndex + 8;
                    var rx = BitConverter.ToDouble(bytes, 0);
                    Array.Copy(payloadArray, payloadArrayIndex, bytes, 0, 8);
                    bytes = CheckEndian(bytes);
                    payloadArrayIndex = payloadArrayIndex + 8;
                    var ry = BitConverter.ToDouble(bytes, 0);
                    Array.Copy(payloadArray, payloadArrayIndex, bytes, 0, 8);
                    bytes = CheckEndian(bytes);
                    payloadArrayIndex = payloadArrayIndex + 8;
                    var rz = BitConverter.ToDouble(bytes, 0);
                    UpdateModel(keyValuePair.Key, new Vector6D(x,y,z,rx, ry, rz));
                }
                else if (keyValuePair.Value == "INT32")
                {
                    byte[] bytes = new byte[4];
                    Array.Copy(payloadArray, payloadArrayIndex, bytes, 0, 4);
                    bytes = CheckEndian(bytes);
                    payloadArrayIndex = payloadArrayIndex + 4;
                    UpdateModel(keyValuePair.Key, BitConverter.ToUInt32(bytes, 0));
                }
                else
                {
                    throw new NotImplementedException("Got a datatype in RTDE Data Package with a value of " + keyValuePair.Value + " that we did not expect");
                }
            }
        }

        private void UpdateModel(string key, object value)
        {
            switch (key)
            {
                case "timestamp":
                    _robotModel.RobotTimestamp = (double)value;
                    break;

                case "actual_digital_output_bits":
                    _robotModel.ActualDigitalOutputBits = (byte)value;
                    Debug.WriteLine("Digital output bits: " + _robotModel.ActualDigitalOutputBits);
                    break;
                case "actual_TCP_pose":
                    _robotModel.ActualTCPPose = (Vector6D) value;
                    break;
                case "robot_mode":
                    _robotModel.RobotMode = (RobotMode)value;
                    break;
                case "safety_mode":
                    _robotModel.SafetyMode = (SafetyMode) value;
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

        private void DecodeRTDESetupPackage(byte[] payloadArray)
        {
            var str = Encoding.Default.GetString(payloadArray);
            string[] values = str.Split(',');
            List<KeyValuePair<string,string>> updatedKeyValueList = new List<KeyValuePair<string, string>>();
            int index = 0;
            foreach (KeyValuePair<string, string> keyValuePair in _rtdeOutputConfiguration)
            {
                var newKeyValuePair = new KeyValuePair<string, string>(keyValuePair.Key, values[index]);
                updatedKeyValueList.Add(newKeyValuePair);
                index++;
            }
            _rtdeOutputConfiguration = updatedKeyValueList;
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
            if (myReadBuffer[2]=='v')
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

    sealed class Sender
    {
        private byte[] _dataToSend = new byte[0];
        private NetworkStream _stream;
        private Thread _thread;
        List<KeyValuePair<string, string>>_rtdeOutputConfiguration;

        internal void SendData(byte[] data)
        {
            _dataToSend = data;
        }

        internal Sender(NetworkStream stream, List<KeyValuePair<string, string>> rtdeOutputConfiguration )
        {
            _stream = stream;
            _rtdeOutputConfiguration = rtdeOutputConfiguration;
            _thread = new Thread(Run);
            _thread.Start();
        }

        private void Run()
        {
            while (true)
            {
                if (_dataToSend.Length > 0)
                {
                    Thread.Sleep(10);
                    _stream.Write(_dataToSend, 0, _dataToSend.Length);
                    //_stream.Flush();
                    //string test = Encoding.ASCII.GetString(_dataToSend);
                    //Debug.WriteLine("Send to Robot: " + test);
                    _dataToSend = new byte[0];
                }
                
            }
        }
    }
}
