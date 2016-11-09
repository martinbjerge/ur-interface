using System;
using System.Collections;
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
using RobotServer.Types;

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
        private static readonly log4net.ILog log = log4net.LogManager.GetLogger(typeof(RTDE));

        private const int port = 30004;

        private TcpClient _client;
        private NetworkStream _stream;
        private RTDEReceiver _rtdeReceiver;
        private RTDESender _rtdeSender;
        private RobotModel _robotModel;
        private List<KeyValuePair<string, string>> _rtdeOutputConfiguration;

        public void SendData(byte[] data)
        {
            _rtdeSender.SendData(data);
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
            _client = new TcpClient(_robotModel.IpAddress.ToString(), port);    
            _stream = _client.GetStream();
            _rtdeOutputConfiguration = new List<KeyValuePair<string, string>>();

            _rtdeReceiver = new RTDEReceiver(_stream, _robotModel, _rtdeOutputConfiguration);
            _rtdeSender = new RTDESender(_stream, _rtdeOutputConfiguration);
            _rtdeReceiver.DataReceived += OnDataReceived;


            GetControllerVersion();
            NegotiateProtocolVersion();
            SetupRtdeInterface();
            StartRTDEInterface();


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
            _rtdeOutputConfiguration.Add(new KeyValuePair<string, string>("timestam" +
                                                                          "p", null));  //Always get the robot timestamp
            //FileStream fileStream = new FileStream(@"Resources\rtde_configuration.xml", FileMode.Open);
            XmlReader xmlReader = XmlReader.Create(@"C:\SourceCode\ur-interface\URConnect\RobotServer\bin\Debug\Resources\rtde_configuration.xml");
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
            _rtdeSender.SendData(package);
        }

        private void StartRTDEInterface()
        {
            log.Debug("Starting RTDE Interface");
            byte[] myBytes = new byte[0];
            byte[] package = CreatePackage((byte) UR_RTDE_Command.RTDE_CONTROL_PACKAGE_START, myBytes);
            _rtdeSender.SendData(package);
        }

        private void PauseRTDEInterface()
        {
            log.Debug("Pausing RTDE Interface");
            byte[] myBytes = new byte[0];
            byte[] package = CreatePackage((byte)UR_RTDE_Command.RTDE_CONTROL_PACKAGE_PAUSE, myBytes);
            _rtdeSender.SendData(package);
        }

    }
}
