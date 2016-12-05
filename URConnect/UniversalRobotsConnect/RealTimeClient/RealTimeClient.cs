using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using log4net;

namespace UniversalRobotsConnect
{
    public class RealTimeClient
    {
        private static readonly ILog log = LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        private const int port = 30003;
        private TcpClient _client;
        private NetworkStream _stream;
        private RealTimeClientSender _realtimeClientSender;
        private RealTimeClientReceiver _realTimeClientReceiver;
        private RobotModel _robotModel;

        public RealTimeClient(RobotModel robotModel)
        {
            _robotModel = robotModel;
            _client = new TcpClient(_robotModel.IpAddress.ToString(), port);
            _stream = _client.GetStream();
            log.Debug("Starting RealtimeClientReceiver");
            _realTimeClientReceiver = new RealTimeClientReceiver(_stream);
            log.Debug("Starting RealtimeClientSender");
            _realtimeClientSender = new RealTimeClientSender(_stream);
        }

        public void Send(byte[] payload)
        {
            log.Debug($"Send to robot {Encoding.UTF8.GetString(payload)}");
            _realtimeClientSender.SendData(payload);
            Thread.Sleep(10);
        }

        public void Send(string payload)
        {
            Send(Encoding.UTF8.GetBytes(payload));
        }

        public void SendProgram(byte[] payload)
        {
            while (_robotModel.RuntimeState == RuntimeState.Running)
            {
                Console.WriteLine("Robot was running");
                Thread.Sleep(10);
            }
            log.Debug($"Send program to robot {Encoding.UTF8.GetString(payload)}");
            _realtimeClientSender.SendData(payload);
            while (_robotModel.RuntimeState != RuntimeState.Running)
            {
                Thread.Sleep(1);
            }
            //ToDo - handle timeout for invalid RTC Data
        }

        public void SendProgram(string payload)
        {
            SendProgram(Encoding.UTF8.GetBytes(payload));
        }
    }
}
