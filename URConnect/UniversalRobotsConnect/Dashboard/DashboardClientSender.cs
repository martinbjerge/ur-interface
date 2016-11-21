using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using log4net;

namespace UniversalRobotsConnect
{
    public class DashboardClientSender
    {
        private static readonly ILog log = LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        private NetworkStream _stream;
        private Thread _thread;
        private List<byte[]> _dataToSend = new List<byte[]>();


        public DashboardClientSender(NetworkStream _stream)
        {
            this._stream = _stream;
            _thread = new Thread(Run);
            _thread.Start();
        }

        public void SendData(byte[] data)
        {
            _dataToSend.Add(data);
        }

        private void Run()
        {
            while (true)
            {
                if (_dataToSend.Count > 0)
                {
                    _stream.Write(_dataToSend[0], 0, _dataToSend[0].Length);
                    _dataToSend.RemoveAt(0);
                    Thread.Sleep(2000);  //Dashboard server is slow
                }
                Thread.Sleep(130);      //From experience we know the Universal Robotics robot doesnt like to recieve quicker than 125 ms
            }
        }
    }
}