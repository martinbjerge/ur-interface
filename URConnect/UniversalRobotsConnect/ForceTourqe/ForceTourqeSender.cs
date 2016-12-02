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
    class ForceTourqeSender
    {
        private static readonly ILog log = LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        private NetworkStream _stream;
        private Thread _thread;
        ConcurrentQueue<byte[]> _dataToSend = new ConcurrentQueue<byte[]>();

        public ForceTourqeSender(NetworkStream _stream)
        {
            this._stream = _stream;
            _thread = new Thread(Run);
            _thread.Start();
        }

        internal void SendData(byte[] data)
        {
            _dataToSend.Enqueue(data);
        }

        private void Run()
        {
            while (true)
            {
                if (_dataToSend.Count > 0)
                {
                    byte[] package;
                    bool success = _dataToSend.TryDequeue(out package);
                    if (success)
                    {
                        _stream.Write(package, 0, package.Length);
                    }
                }
                Thread.Sleep(10);
            }
        }
    }
}
