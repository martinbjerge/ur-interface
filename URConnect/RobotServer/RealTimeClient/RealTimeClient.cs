using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace RobotServer
{
    class RealTimeClient
    {
        private TcpClient _client;
        private NetworkStream _stream;
        private RealTimeClientSender _sender;

        public RealTimeClient(IPAddress ipAddress)
        {
            
        }
    }

    sealed class RealTimeClientSender
    {
        private byte[] _dataToSend = new byte[0];
        private NetworkStream _stream;
        private Thread _thread;
        List<KeyValuePair<string, string>> _rtdeOutputConfiguration;

        internal void SendData(byte[] data)
        {
            _dataToSend = data;
        }

        internal RealTimeClientSender(NetworkStream stream, List<KeyValuePair<string, string>> rtdeOutputConfiguration)
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
                    Thread.Sleep(130);      //From experience we know the Universal Robotics robot doesnt like to recieve quicker than 125 ms
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
