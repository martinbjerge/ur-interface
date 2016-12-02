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

        public async void Send(byte[] payload)
        {
            byte[] sendBytes = new byte[payload.Length+2];
            Array.Copy(payload, sendBytes, payload.Length);
            sendBytes[sendBytes.Length - 2] = (byte) 92;        //backslash
            sendBytes[sendBytes.Length - 1] = (byte) 'n';
            log.Debug($"Send to robot {Encoding.UTF8.GetString(sendBytes)}");
            _realtimeClientSender.SendData(payload);
            await Task.Delay(100);
        }

        public void Send(string payload)
        {
            Send(Encoding.UTF8.GetBytes(payload));
        }

        public void SendProgram(byte[] payload)
        {
            byte[] sendBytes = new byte[payload.Length + 2];
            Array.Copy(payload, sendBytes, payload.Length);
            sendBytes[sendBytes.Length - 2] = (byte)92;        //backslash
            sendBytes[sendBytes.Length - 1] = (byte)'n';
            //while (_robotModel.RuntimeState != RuntimeState.Idle)
            //{
            //    Console.WriteLine($"Waiting for idle robot");
            //    Thread.Sleep(2);
            //}
            log.Debug($"Send program to robot {Encoding.UTF8.GetString(sendBytes)}");
            _realtimeClientSender.SendData(payload);
            while (_robotModel.RuntimeState != RuntimeState.Running)
            {
                //Debug.WriteLine($"Waiting for program to start - Runtime state is {_robotModel.RuntimeState} - Robot Time {_robotModel.RobotTimestamp}");
                Thread.Sleep(1);
            }
            //Debug.WriteLine($"Finished waiting - program running - RobotTime {_robotModel.RobotTimestamp}");
            //ToDo - handle timeout for invalid RTC Data
            //Thread.Sleep(8);

            //await Task.Delay(500);
        }

        public void SendProgram(string payload)
        {
            SendProgram(Encoding.UTF8.GetBytes(payload));
        }
    }
}
