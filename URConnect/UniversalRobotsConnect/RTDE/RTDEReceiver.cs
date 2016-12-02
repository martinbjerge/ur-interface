using System;
using System.Collections;
using System.Collections.Concurrent;
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
        //private List<byte[]> _packageList = new List<byte[]>();
        ConcurrentQueue<byte[]> _rtdeDataPackageQueue = new ConcurrentQueue<byte[]>();
        private RTDEDatePackageDecoder _rtdeDataPackageDecoder;
        // private ConcurrentQueue<RobotModel> _robotData;
        private DateTime lastRtdeDataPackTime = DateTime.Now;

        private Thread _packageDecoderThread;
        private bool readFixedRTDEPackageSize = false;


        internal RTDEReceiver(NetworkStream stream, RobotModel robotModel, List<KeyValuePair<string, string>> rtdeOutputConfiguration, List<KeyValuePair<string, string>> rtdeInputConfiguration, ConcurrentQueue<RobotModel> robotData)
        {
            _robotModel = robotModel;
            _stream = stream;
            _rtdeOutputConfiguration = rtdeOutputConfiguration;
            _rtdeInputConfiguration = rtdeInputConfiguration;
            //_robotData = robotData;
            _rtdeDataPackageDecoder = new RTDEDatePackageDecoder(_rtdeOutputConfiguration, _rtdeDataPackageQueue, robotData);
            
            //_packageDecoderThread = new Thread(SocketPacageDecoder);
            //_packageDecoderThread.Start();
            _receiverThread = new Thread(Run);
            _receiverThread.Start();
        }

        public int RtdePackageSize { get; set; }


        private void Run()
        {
            List<byte> bytelist = new List<byte>();

            while (true)
            {
                DateTime startTime = DateTime.Now;
                if (_stream.DataAvailable)
                {
                    if (_stream.CanRead)
                    {
                        if (readFixedRTDEPackageSize)
                        {
                            bytelist.Add((byte)_stream.ReadByte());
                            if (bytelist.Count == RtdePackageSize)
                            {
                                DecodeRtdePacage(bytelist.ToArray());
                                bytelist.Clear();
                                var readSocketPackageTime = DateTime.Now - startTime;
                                if (readSocketPackageTime.TotalMilliseconds > 5)
                                {
                                    Console.WriteLine($"Time to read a package from socket: {readSocketPackageTime.TotalMilliseconds}");
                                }
                                startTime = DateTime.Now;
                                Thread.Sleep(2);
                            }
                        }
                        else
                        {
                            byte[] myReadBuffer = new byte[4000];
                            int numberOfBytesRead = 0;
                            do
                            {
                                numberOfBytesRead = _stream.Read(myReadBuffer, 0, myReadBuffer.Length);
                            }
                            while (_stream.DataAvailable);

                            byte[] package = new byte[numberOfBytesRead];
                            Array.Copy(myReadBuffer, package, numberOfBytesRead);
                            DecodeRtdePacage(package);
                        }
                    }
                    else
                    {
                        throw new SystemException("Sorry.  You cannot read from this NetworkStream.");
                    }
                }
            }
        }

        
        private void DecodeRtdePacage(byte[] recievedPackage)
        {
            DateTime startTime = DateTime.Now;
            byte[] sizeArray = new byte[2];
            UR_RTDE_Command type = (UR_RTDE_Command)recievedPackage[2];
            Array.Copy(recievedPackage, sizeArray, 2);
            sizeArray = RTDEDatePackageDecoder.CheckEndian(sizeArray);
            ushort size = BitConverter.ToUInt16(sizeArray, 0);
            if ((size > 3) && (size == recievedPackage.Length))
            {
                byte[] payloadArray = new byte[size - 3];
                Array.Copy(recievedPackage, 3, payloadArray, 0, size - 3);

                switch (type)
                {
                    case UR_RTDE_Command.RTDE_REQUEST_PROTOCOL_VERSION:
                        _robotModel.RTDEProtocolVersion = DecodeProtocolVersion(payloadArray);
                        break;
                    case UR_RTDE_Command.RTDE_GET_URCONTROL_VERSION:
                        _robotModel.URControlVersion = DecodeUniversalRobotsControllerVersion(payloadArray);
                        break;
                    case UR_RTDE_Command.RTDE_CONTROL_PACKAGE_SETUP_OUTPUTS:
                        DecodeRTDESetupPackage(payloadArray, _rtdeOutputConfiguration);
                        break;
                    case UR_RTDE_Command.RTDE_CONTROL_PACKAGE_SETUP_INPUTS:
                        DecodeRTDESetupPackage(payloadArray, _rtdeInputConfiguration);
                        break;
                    case UR_RTDE_Command.RTDE_DATA_PACKAGE:
                        if (!readFixedRTDEPackageSize)
                        {
                            readFixedRTDEPackageSize = true;
                        }
                        _rtdeDataPackageQueue.Enqueue(payloadArray);
                        var delta = DateTime.Now - lastRtdeDataPackTime;
                        if (delta.TotalMilliseconds > 100)
                        {
                            Console.WriteLine($"Real time since last RTDE Package decode: {delta.TotalMilliseconds} milliseconds");
                        }
                        lastRtdeDataPackTime = DateTime.Now;
                        break;
                    case UR_RTDE_Command.RTDE_CONTROL_PACKAGE_START:
                        _robotModel.RTDEConnectionState = DecodeRTDEControlPackageStart(payloadArray);
                        break;
                    case UR_RTDE_Command.RTDE_CONTROL_PACKAGE_PAUSE:
                        _robotModel.RTDEConnectionState = DecodeRTDEControlPacagePause(payloadArray);
                        break;
                    default:
                        log.Error("Package type not implemented " + type);
                        throw new NotImplementedException("Package type not implemented " + type);
                }
            }
            else
            {
                log.Error("Got a packet of unexpected size");
                readFixedRTDEPackageSize = false;
            }
            var decodeRtdePackageTime = DateTime.Now - startTime;
            if (decodeRtdePackageTime.TotalMilliseconds > 2)
            {
                Console.WriteLine($"Time to Decode a RTDE package: {decodeRtdePackageTime.TotalMilliseconds}");
            }
        }
        
        private ConnectionState DecodeRTDEControlPacagePause(byte[] payloadArray)
        {
            if (payloadArray[0] == 1)
            {
                readFixedRTDEPackageSize = false;
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
                readFixedRTDEPackageSize = true;
                log.Debug("RTDE has started");
                return ConnectionState.Started;
            }
            else
            {
                throw new NotImplementedException();
            }

        }

        private void DecodeRTDESetupPackage(byte[] payloadArray, List<KeyValuePair<string, string>> rtdeConfiguration)
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



        private URControlVersion DecodeUniversalRobotsControllerVersion(byte[] payload)
        {
            byte[] majorArray = new byte[4];
            Array.Copy(payload, 0, majorArray, 0, 4);
            majorArray = RTDEDatePackageDecoder.CheckEndian(majorArray);
            UInt32 major = BitConverter.ToUInt32(majorArray, 0);
            byte[] minorArray = new byte[4];
            Array.Copy(payload, 4, minorArray, 0, 4);
            minorArray = RTDEDatePackageDecoder.CheckEndian(minorArray);
            UInt32 minor = BitConverter.ToUInt32(minorArray, 0);
            byte[] bugfixArray = new byte[4];
            Array.Copy(payload, 8, bugfixArray, 0, 4);
            bugfixArray = RTDEDatePackageDecoder.CheckEndian(bugfixArray);
            UInt32 bugfix = BitConverter.ToUInt32(bugfixArray, 0);
            byte[] buildArray = new byte[4];
            Array.Copy(payload, 12, buildArray, 0, 4);
            buildArray = RTDEDatePackageDecoder.CheckEndian(buildArray);
            UInt32 build = BitConverter.ToUInt32(buildArray, 0);

            return new URControlVersion((int)major, (int)minor, (int)bugfix, (int)build);
        }

        private int DecodeProtocolVersion(byte[] payload)
        {
            return payload[0];
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
