using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using log4net;

namespace UniversalRobotsConnect
{
    class RealTimeClientSender
    {
        //private static readonly ILog log = LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        //ConcurrentQueue<byte[]> _dataToSend = new ConcurrentQueue<byte[]>();
        private NetworkStream _stream;
        private Thread _thread;


        internal void SendData(byte[] data)
        {
            _stream.Write(data, 0, data.Length);
            _stream.Flush();
            Thread.Sleep(1);
            //_dataToSend.Enqueue(data);
        }

        internal RealTimeClientSender(NetworkStream stream)
        {
            _stream = stream;
            //_thread = new Thread(Run);
            //_thread.Start();
        }

        //private void Run()
        //{
        //    while (true)
        //    {
        //        if (_dataToSend.Count > 0)
        //        {
        //            byte[] package;
        //            bool success = _dataToSend.TryDequeue(out package);
        //            if (success)
        //            {
        //                _stream.Write(package, 0, package.Length);
        //            }
        //        }
        //        Thread.Sleep(50);
        //    }
        //}
    }
}
